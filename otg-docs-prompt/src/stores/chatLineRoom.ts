import { defineStore } from 'pinia'

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
        messages: Array<{ role: string; content: string }>
        userId: string
      }
    >,
  }),
  actions: {
    async fetchChatLineRooms() {
      try {
        const response = await fetch('http://localhost:5500/room_line_option')
        const data = await response.json()
        data.forEach(
          (element: {
            _id: { 
              $oid: string 
            }
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
            this.chatLineRoom[element._id.$oid] = {
              id: element._id.$oid,
              sender: element.sender,
              chatOption: element.chatOption,
              messages: element.message,
              userId: element.userId
            }
          },
        )
      } catch (error) {
        console.error('Failed to fetch ChatLineRooms:', error)
      }
    },
    async fetchTempChatLineRooms() {
      try {
        const response = await fetch('http://localhost:5500/short_polling_message')
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
        const response = await fetch('http://localhost:5500/room_line_option', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(config),
        })
      } catch (error) {
        console.error('Failed to create ChatLineRoom:', error)
      }
    },
    async deleteChatLineRooms(id: string) {
      try {
        await fetch('http://localhost:5500/room_line_option/' + id, {
          method: 'DELETE',
        })
        delete this.chatLineRoom[id]
      } catch (error) {
        console.error('Failed to create ChatLineRooms:', error)
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
          role: 'assistant',
          content: message.message,
        })
        const response = await fetch('http://localhost:5500/sending_line_assistant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(message),
        })
      } catch (error) {
        console.error('Failed to create ChatLineRooms:', error)
      }
    },
  },
})
