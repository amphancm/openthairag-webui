import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useChatLineRoomStore = defineStore('ChatLineRoomStore', {
  state: () => ({
    chatLineRoom: {} as Record<
      string,
      {
        id: string
        sender: {
          displayName: string;
          language: string;
          pictureUrl: string;
          userId: string;
        }
        chatOption: {
          temperature: string;
          greeting: string;
          systemPrompt: string; 
          botToggle: boolean;
        }
        messages: Array<{ type: string; role: string; content: string }>
        userId: string
      }
    >,
  }),
  actions: {
    async fetchChatLineRooms() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_line_option`, {
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        const data = await response.json()
        data.data.forEach(
          (element: {
            _id:  string
            sender: {
              displayName: string;
              language: string;
              pictureUrl: string;
              userId: string;
            }
            chatOption: { 
              temperature: string; 
              greeting: string; 
              systemPrompt: string; 
              botToggle: boolean; 
            }
            message: Array<{ 
              role: string; 
              user: string; 
              content: string 
              timestamp: string; 
            }>
            userId: string
          }) => {

            const message_split: Array<{ type: string; role: string; content: string }> = []
            element.message.forEach((ele) => {
              const parts = processText(ele.content)
              for (const part of parts) {
                if(isValidImageUrl(part)) {
                  message_split.push({
                    type: 'image',
                    role: ele.role,
                    content: part,
                  })
                } else if(part != '-' && part != ',' && part != '' && part.length > 1) {
                  message_split.push({
                    type: 'text',
                    role: ele.role,
                    content: part,
                  })
                }
              }
            })

            this.chatLineRoom[element._id] = {
              id: element._id,
              sender: element.sender,
              chatOption: element.chatOption,
              messages: message_split,
              userId: element.userId
            }
          },
        )
        console.log('this.chatLineRoom :',this.chatLineRoom)
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to fetch ChatLineRooms:', error)
      }
    },
    async fetchTempChatLineRooms() {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/short_polling_message`,{
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
        const data = await response.json()
      } catch (error) {
        console.error('Failed to fetch ChatLineRooms:', error)
      }
    },
    async saveChatLineRooms(config: {
      id: string
      chatOption: { temperature: string; systemPrompt: string; botToggle: boolean; }
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_line_option`, {
          method: 'PATCH',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(config),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create ChatLineRoom:', error)
      }
    },
    async deleteChatLineRooms(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_line_option/` + id, {
          method: 'DELETE',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
        })
        delete this.chatLineRoom[id]
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create ChatLineRooms:', error)
      }
    },async deleteTempLineRooms(send_id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/reset_line_tempMessage`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify({
            send_id: send_id
          }),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create ChatFBRooms:', error)
      }
    },
    async submitMessage(message: {
      id: string
      line_ids: string
      message: string
    }) {
      try {
        console.log('message :',message)
        this.chatLineRoom[message.id].messages.push({
          type: 'text',
          role: 'assistant',
          content: message.message,
        })
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/sending_line_assistant`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer '+token
          },
          body: JSON.stringify(message),
        })
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push({ path: "/login" }).catch((err) => console.error(err));
          return;
        }
      } catch (error) {
        console.error('Failed to create ChatLineRooms:', error)
      }
    },
  },
})


function processText(input: string) {
  const regex = /!?\[.*?\]\((.*?)\)/g;
  const parts: string[] = [];

  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(input)) !== null) {
    if (lastIndex !== match.index) {
      parts.push(input.slice(lastIndex, match.index).trim());
    }
    if (match[0].startsWith('!')) {
      parts.push(match[1]);
    } else {
      parts.push(match[0].trim());
    }
    
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < input.length) {
    parts.push(input.slice(lastIndex).trim());
  }

  if (parts.length === 1) {
    const splitResult = input.split(/(https?:\/\/.*\.(?:png|jpg|jpeg|gif))/gi); // Regex to split text and URL
    return splitResult.map((item) => item.trim()).filter((item) => item !== "");
  }

  return parts;
}

function isValidImageUrl(url: string): boolean {
  const regex = /^http.*\.(jpg|png)$/;
  return regex.test(url);
}
