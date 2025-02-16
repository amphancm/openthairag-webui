import { defineStore } from 'pinia'
import { CONFIG } from '@/config'
import router from '@/router';
const token = localStorage.getItem("token");

export const useChatRoomStore = defineStore('ChatRoomStore', {
  state: () => ({
    chatRoom: {} as Record<
      string,
      {
        id: string
        chatOption: { name: string; temperature: string; systemPrompt: string }
        messages: Array<{ type: string; role: string; content: string }>
      }
    >,
  }),
  actions: {
    async fetchChatRooms(profile: { username: string; token: string }) {
      const username = profile.username
      try {
        console.log('token :',token)
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_option?account_owner=`+username, {
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
        data.forEach(
          (element: {
            _id: { $oid: string }
            chatOption: { name: string; temperature: string; systemPrompt: string }
            messages: Array<{ type: string; role: string; content: string }>
          }) => {

            const message_split: Array<{ type: string; role: string; content: string }> = []
            element.messages.forEach((ele) => {
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

            this.chatRoom[element._id.$oid] = {
              id: element._id.$oid,
              chatOption: element.chatOption,
              messages: message_split,
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch ChatRooms:', error)
      }
    },
    async saveChatRooms(config: {
      id: string
      chatOption: { name: string; temperature: string; systemPrompt: string }
    }) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_option`, {
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
        this.chatRoom[config.id].chatOption = config.chatOption
      } catch (error) {
        console.error('Failed to create ChatRoom:', error)
      }
    },
    async createChatRooms(config: {
      account_owner: string;
      chatOption: { name: string; temperature: string; systemPrompt: string }
      messages: Array<{ type: string; role: string; content: string }>
    }) {
      console.log('config :',config)
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_option`, {
          method: 'POST',
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
        const data = await response.json()
        this.chatRoom[data.id] = {
          id: data.id,
          chatOption: config.chatOption,
          messages: config.messages,
        }
      } catch (error) {
        console.error('Failed to create ChatRooms:', error)
      }
    },
    async deleteChatRooms(id: string) {
      try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/room_option/` + id, {
          method: 'DELETE',
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
        delete this.chatRoom[id]
      } catch (error) {
        console.error('Failed to create ChatRooms:', error)
      }
    },
    async submitMessage(message: {
      id: string
      systemPrompt: string
      temperature: string
      message: string
    }) {
      try {
        this.chatRoom[message.id].messages.push({
          type: 'text',
          role: 'user',
          content: message.message,
        })
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/chat_history`, {
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
        const data = await response.json()
        this.chatRoom[message.id].chatOption.name = data.title_name
        const parts = processText(data.message.content)
        for (const part of parts) {
          if(isValidImageUrl(part)) {
            this.chatRoom[message.id].messages.push({
              type: 'image',
              role: 'assistant',
              content: part,
            })
          } else if(part != '-' && part != ',' && part != '' && part.length > 1) {
            this.chatRoom[message.id].messages.push({
              type: 'text',
              role: 'assistant',
              content: part,
            })
          }
        }
        // this.chatRoom[message.id].messages.push({
        //   role: 'assistant',
        //   content: data.message.content,
        // })
      } catch (error) {
        console.error('Failed to create ChatRooms:', error)
      }
    },
    resetChatRooms() {
      this.chatRoom = {}
    }
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

  return parts
}

function isValidImageUrl(url: string): boolean {
  const regex = /^http.*\.(jpg|png)$/;
  return regex.test(url);
}

