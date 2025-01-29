from flask import Flask, request, jsonify, Response
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, utility, DataType
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import os
import datetime
import numpy as np
import logging
from db import Connection
from bson.json_util import dumps
import openai
import json

MILVUS_HOST = os.environ.get('MILVUS_HOST', 'milvus')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')
VLLM_HOST = os.environ.get('VLLM_HOST', '172.17.0.1:8000')
SYSTEM_PROMPT = os.environ.get('SYSTEM_PROMPT', 'คุณคือ OpenThaiGPT พัฒนาโดยสมาคมผู้ประกอบการปัญญาประดิษฐ์ประเทศไทย (AIEAT)')
# connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
openai.api_base = f"https://{VLLM_HOST}/v1"
openai.api_key = "dummy"  # vLLM doesn't require a real API key
print(f"OpenAI API base: {openai.api_base}")
print(f"OpenAI API key: {openai.api_key}")

logger = logging.getLogger(__name__)

# Function to initialize Milvus collection
def initialize_milvus_collection():
    # Check if collection exists
    if not utility.has_collection("document_embeddings"):
        # Create collection if it doesn't exist
        # You may need to adjust the schema based on your specific requirements

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),  # Adjust dim if needed
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, "Document embeddings for Information database")
        collection = Collection("document_embeddings", schema)
        
        # Create an IVF_FLAT index for the embedding field
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index("embedding", index_params)
    else:
        collection = Collection("document_embeddings")
    
    return collection

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collection = initialize_milvus_collection()
logger.info("Successfully connected with MILVUS database.")

logger.info("Loading... BAAI/bge-m3 embedding model")
# Load BAAI/bge-m3 model and tokenizer
bge_model = AutoModel.from_pretrained("BAAI/bge-m3")
logger.info("Loading... BAAI/bge-m3 tokenizer model")
bge_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
logger.info("Successfully Load BAAI/bge-m3 embedding and tokenizer.")
logger.info("Now it is ready to serve.")

# Function to generate embeddings
def generate_embedding(text):
    inputs = bge_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = bge_model(**inputs).pooler_output
    return embeddings

# Rerank documents based on cosine similarity
def rerank_documents(query_embedding, document_embeddings):
    # Ensure query_embedding is a 2D array
    if isinstance(query_embedding, list):
        query_embedding = np.array(query_embedding).reshape(1, -1)
    elif isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.reshape(1, -1)
    
    # Ensure document_embeddings is a 2D array
    if isinstance(document_embeddings, list):
        document_embeddings = np.array(document_embeddings)
    if len(document_embeddings.shape) == 1:
        document_embeddings = document_embeddings.reshape(1, -1)
    
    # Check if document_embeddings is empty
    if document_embeddings.size == 0:
        logging.warning("Document embeddings array is empty")
        return []
    
    logger.debug(f"Query embedding shape: {query_embedding.shape}, Document embeddings shape: {document_embeddings.shape}")
    logger.debug(f"Query embedding: {query_embedding}, Document embeddings: {document_embeddings}")
    
    similarities = cosine_similarity(query_embedding, document_embeddings)
    ranked_documents = sorted(enumerate(similarities.flatten()), key=lambda x: x[1], reverse=True)
    return ranked_documents

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get current temperature at a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": 'The location to get the temperature for, in the format "City, State, Country".',
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": 'The unit to return the temperature in. Defaults to "celsius".',
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_temperature_date",
            "description": "Get temperature at a location and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": 'The location to get the temperature for, in the format "City, State, Country".',
                    },
                    "date": {
                        "type": "string",
                        "description": 'The date to get the temperature for, in the format "Year-Month-Day".',
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": 'The unit to return the temperature in. Defaults to "celsius".',
                    },
                },
                "required": ["location", "date"],
            },
        },
    },
]

def compute_model(query,arr_history, system_prompt, temperature):
    # Step 1: Generate query embedding
    query_embedding = generate_embedding(query).numpy().flatten().tolist()
    
    # Prepare search parameters
    search_param = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    if not collection.is_empty:
        collection.load()
        
    # Step 2: Retrieve top-10 documents from Milvus
    search_results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_param,
        limit=10,
        output_fields=["id", "text", "embedding"],
        expr=None
    )
    
    # Extract document texts and embeddings
    retrieved_documents = []
    document_embeddings = []
    for hits in search_results:
        for hit in hits:

            retrieved_documents.append(hit.entity)
            embedding = hit.entity.get('embedding')

            if embedding is not None:
                document_embeddings.append(embedding)

    ranked_indices = rerank_documents(query_embedding, document_embeddings)
    top_documents = [retrieved_documents[i] for i, _ in ranked_indices[:3]]

    # system_prompt = os.environ.get('SYSTEM_PROMPT', 'คุณคือ OpenThaiGPT พัฒนาโดยสมาคมผู้ประกอบการปัญญาประดิษฐ์ประเทศไทย (AIEAT)')

    # <|im_start|>system\nคุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์<|im_end|>

    prompt = f"จากเอกสารต่อไปนี้\n\n"
    prompt += "\n\n".join([doc.get('text') for doc in top_documents])

    prompt_chatml = []

    for dat in arr_history:
        prompt_chatml.append(dat)
    prompt_chatml.append({
        'role': 'user',
        'content': query
    })

    # chatOptions = {"selectedModel": ".", "systemPrompt": 'คุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์ และเชื่อในข้อมูลจาก เอกสารเหล่านี้เท่านั้น \n\n'+system_prompt+'\n\n'+prompt, "temperature": float(temperature) if temperature != '' else 0.5 }
    historyPrompt = ""
    promptBody = "<|im_start|>system\nคุณคือผู้ช่วยตอบคำถามที่ฉลาดและซื่อสัตย์ และเชื่อในข้อมูลจาก เอกสารเหล่านี้เท่านั้น"+system_prompt+"\n\n"+prompt+"<|im_end|>\n"
    # "<|im_start|>user\n"+query+"<|im_end|>\n<|im_start|>assistant\n"
    for dat in arr_history:
        historyPrompt += "<|im_start|>"+dat['role']+"\n"+dat['content']+"<|im_end|>"
    
    promptBody = historyPrompt + promptBody
    promptBody += "<|im_start|>user\n"+query+"<|im_end|>\n<|im_start|>assistant\n"
    print("prompt_chatml :",promptBody)
    # print("chatOptions :",chatOptions)
    
    response = requests.post(
        'https://api.aieat.or.th/v1/completions',
        headers={
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
        },
        json={
            "model": ".",
            "max_tokens": 512,
            "temperature": float(temperature) if temperature != '' else 0.5,
            "top_p": 0.8,
            "top_k": 40,
            # "messages": prompt_chatml,
            # "chatOptions": chatOptions,
            "prompt": promptBody,
            "stop": ["<|im_end|>"]
        }
    )
    # response = requests.post(
    #     'https://demo72b.aieat.or.th/api/chat',
    #     headers={
    #         'accept': '*/*',
    #         'accept-language': 'en-US,en;q=0.9',
    #         'content-type': 'application/json',
    #         'dnt': '1',
    #         'origin': 'https://demo72b.aieat.or.th',
    #         'priority': 'u=1, i',
    #         'referer': 'https://demo72b.aieat.or.th/',
    #         'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"macOS"',
    #         'sec-fetch-dest': 'empty',
    #         'sec-fetch-mode': 'cors',
    #         'sec-fetch-site': 'same-origin',
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    #     },
    #     json={
    #         "messages": prompt_chatml,
    #         "chatOptions": chatOptions
    #     }
    # )

    print("response :",response.text)
    print("response :",response.text)
    return json.loads(response.text)

def convertTextFromRes(res):
    result = []
    lines = res.splitlines()
    for line in lines:
        if ':' in line:
            _, data = line.split(':', 1)  # Split on the first occurrence of ':'
            result.append(data.strip().replace('"', ''))
    return "".join(result)