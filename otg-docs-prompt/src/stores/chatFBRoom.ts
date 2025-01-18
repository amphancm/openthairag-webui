import { defineStore } from 'pinia'

export const useChatFBRoomStore = defineStore('ChatFBRoomStore', {
  state: () => ({
    chatFBRoom: {} as Record<
      string,
      {
        id: string
        sender: {
          displayName: string;
          pictureUrl: string;
          userId: string;
        }
        chatOption: {
          temperature: string;
          greeting: string;
          systemPrompt: string; 
          botToggle: boolean;
        }
        messages: Array<{ role: string; content: string }>
        userId: string
      }
    >,
  }),
  actions: {
    async fetchChatFBRooms() {
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/room_fb_option')
        const data = await response.json()
        data.forEach(
          (element: {
            _id: { 
              $oid: string 
            }
            sender: {
              displayName: string;
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
            this.chatFBRoom[element._id.$oid] = {
              id: element._id.$oid,
              sender: element.sender,
              chatOption: element.chatOption,
              messages: element.message,
              userId: element.userId
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch ChatFBRooms:', error)
      }
    },
    async fetchTempChatFBRooms() {
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/fb_short_polling_message')
        const data = await response.json()
      } catch (error) {
        console.error('Failed to fetch ChatFBRooms:', error)
      }
    },
    async saveChatFBRooms(config: {
      id: string
      chatOption: { temperature: string; systemPrompt: string; botToggle: boolean; }
    }) {
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/room_fb_option', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(config),
        })
      } catch (error) {
        console.error('Failed to create ChatFBRoom:', error)
      }
    },
    async deleteChatFBRooms(id: string) {
      try {
        await fetch('https://otg-server.odoo365cloud.com/room_fb_option/' + id, {
          method: 'DELETE',
        })
        delete this.chatFBRoom[id]
      } catch (error) {
        console.error('Failed to create ChatFBRooms:', error)
      }
    },
    async deleteTempChatFBRooms(send_id: string) {
      try {
        await fetch('https://otg-server.odoo365cloud.com/reset_fb_tempMessage/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(send_id),
        })
      } catch (error) {
        console.error('Failed to create ChatFBRooms:', error)
      }
    },
    async submitMessage(message: {
      id: string
      sending_id: string
      message: string
    }) {
      try {
        console.log('message :',message)
        this.chatFBRoom[message.id].messages.push({
          role: 'assistant',
          content: message.message,
        })
        const response = await fetch('https://otg-server.odoo365cloud.com/sending_fb_assistant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(message),
        })
      } catch (error) {
        console.error('Failed to create ChatFBRooms:', error)
      }
    },
  },
})
