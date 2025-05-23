import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from flask import jsonify

# Import the functions to be tested
from openthairag.app.controllers.setting_controller import setting_post, setting_patch, setting_get

# Mock the Connection class and its 'setting' attribute
@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_post_with_model_fields(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection
    mock_setting_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())

    data = {
        'line_activate': True, 'fb_activate': True, 'product_activate': True,
        'feedback_activate': True, 'greeting_activate': True, 'line_key': 'key',
        'line_secret': 'secret', 'facebook_token': 'fb_token',
        'facebook_verify_password': 'fb_password', 'greeting_prompt': 'hello',
        'model_name': 'gpt-4', 'model_type': 'api', 'api_key': 'test_api_key'
    }
    
    response, status_code = setting_post(data)

    assert status_code == 201
    assert response.json['message'] == "Data inserted successfully"
    mock_setting_collection.insert_one.assert_called_once_with(data)


@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_post_without_model_fields(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection
    mock_setting_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())
    
    data = {
        'line_activate': False, 'fb_activate': False, 'product_activate': False,
        'feedback_activate': False, 'greeting_activate': False, 'line_key': '',
        'line_secret': '', 'facebook_token': '',
        'facebook_verify_password': '', 'greeting_prompt': ''
        # model_name, model_type, api_key are missing
    }
    
    expected_payload_to_db = {
        'line_activate': False, 'fb_activate': False, 'product_activate': False,
        'feedback_activate': False, 'greeting_activate': False, 'line_key': '',
        'line_secret': '', 'facebook_token': '',
        'facebook_verify_password': '', 'greeting_prompt': '',
        'model_name': '', 'model_type': 'local', 'api_key': '' # Defaults
    }

    response, status_code = setting_post(data)

    assert status_code == 201
    mock_setting_collection.insert_one.assert_called_once_with(expected_payload_to_db)


@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_patch_with_model_fields(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection
    
    object_id = ObjectId()
    data = {
        'id': str(object_id),
        'line_activate': True, 'fb_activate': True, 'product_activate': True,
        'feedback_activate': True, 'greeting_activate': True, 'line_key': 'key_new',
        'line_secret': 'secret_new', 'facebook_token': 'fb_token_new',
        'facebook_verify_password': 'fb_password_new', 'greeting_prompt': 'hello_new',
        'model_name': 'llama', 'model_type': 'local', 'api_key': ''
    }
    
    expected_set_operator = {
        "$set": {
            'line_activate': True, 'fb_activate': True, 'product_activate': True,
            'feedback_activate': True, 'greeting_activate': True, 'line_key': 'key_new',
            'line_secret': 'secret_new', 'facebook_token': 'fb_token_new',
            'facebook_verify_password': 'fb_password_new', 'greeting_prompt': 'hello_new',
            'model_name': 'llama', 'model_type': 'local', 'api_key': ''
        }
    }

    response, status_code = setting_patch(data)

    assert status_code == 201
    assert response.json['message'] == "Data updated successfully"
    mock_setting_collection.update_one.assert_called_once_with(
        {'_id': object_id},
        expected_set_operator
    )

@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_patch_partially_missing_model_fields(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection

    object_id = ObjectId()
    data = {
        'id': str(object_id),
        'line_activate': True, 'fb_activate': True, 'product_activate': True,
        'feedback_activate': True, 'greeting_activate': True, 'line_key': 'key_new',
        'line_secret': 'secret_new', 'facebook_token': 'fb_token_new',
        'facebook_verify_password': 'fb_password_new', 'greeting_prompt': 'hello_new',
        'model_name': 'claude' # model_type and api_key missing
    }
    
    expected_set_operator = {
        "$set": {
            'line_activate': True, 'fb_activate': True, 'product_activate': True,
            'feedback_activate': True, 'greeting_activate': True, 'line_key': 'key_new',
            'line_secret': 'secret_new', 'facebook_token': 'fb_token_new',
            'facebook_verify_password': 'fb_password_new', 'greeting_prompt': 'hello_new',
            'model_name': 'claude', 
            'model_type': 'local', # Default
            'api_key': '' # Default
        }
    }
    
    response, status_code = setting_patch(data)

    assert status_code == 201
    mock_setting_collection.update_one.assert_called_once_with(
        {'_id': object_id},
        expected_set_operator
    )

@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_get(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection
    
    object_id_1 = ObjectId()
    object_id_2 = ObjectId()

    # Note: BSON dumps will convert ObjectId to {'$oid': str(object_id)}
    mock_data_from_db = [
        {
            '_id': object_id_1, 'line_activate': True, 'fb_activate': False,
            'model_name': 'gpt-3.5-turbo', 'model_type': 'api', 'api_key': 'fake_key_1'
        },
        {
            '_id': object_id_2, 'line_activate': False, 'fb_activate': True,
            'model_name': 'titan', 'model_type': 'local', 'api_key': '' 
            # api_key might be empty string if saved with local type
        }
    ]
    mock_setting_collection.find.return_value = mock_data_from_db

    # Expected JSON string after dumps. Note ObjectId conversion.
    expected_json_output = f'[{{"_id": {{"$oid": "{str(object_id_1)}"}} , "line_activate": true, "fb_activate": false, "model_name": "gpt-3.5-turbo", "model_type": "api", "api_key": "fake_key_1"}}, {{"_id": {{"$oid": "{str(object_id_2)}"}} , "line_activate": false, "fb_activate": true, "model_name": "titan", "model_type": "local", "api_key": ""}}]'

    response_data, status_code = setting_get()
    
    assert status_code == 200
    assert response_data == expected_json_output
    mock_setting_collection.find.assert_called_once()

@patch('openthairag.app.controllers.setting_controller.Connection')
def test_setting_get_no_data(MockConnection):
    mock_db_instance = MockConnection.return_value
    mock_setting_collection = MagicMock()
    mock_db_instance.setting = mock_setting_collection
    mock_setting_collection.find.return_value = [] # No data

    response_data, status_code = setting_get()

    assert status_code == 200
    assert response_data == "[]" # Empty list in JSON
    mock_setting_collection.find.assert_called_once()

# It's good practice to ensure the module can be imported and basic setup works.
def test_module_import():
    assert True
