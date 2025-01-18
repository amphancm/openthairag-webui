import { defineStore } from 'pinia'

export const useChatRoomStore = defineStore('ChatRoomStore', {
  state: () => ({
    chatRoom: {} as Record<
      string,
      {
        id: string
        chatOption: { name: string; temperature: string; systemPrompt: string }
        messages: Array<{ role: string; content: string }>
      }
    >,
  }),
  actions: {
    async fetchChatRooms(profile: { username: string; token: string }) {
      const username = profile.username
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/room_option?account_owner='+username)
        const data = await response.json()
        data.forEach(
          (element: {
            _id: { $oid: string }
            chatOption: { name: string; temperature: string; systemPrompt: string }
            messages: Array<{ role: string; content: string }>
          }) => {
            this.chatRoom[element._id.$oid] = {
              id: element._id.$oid,
              chatOption: element.chatOption,
              messages: element.messages,
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
        const response = await fetch('https://otg-server.odoo365cloud.com/room_option', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(config),
        })
        this.chatRoom[config.id].chatOption = config.chatOption
      } catch (error) {
        console.error('Failed to create ChatRoom:', error)
      }
    },
    async createChatRooms(config: {
      account_owner: string;
      chatOption: { name: string; temperature: string; systemPrompt: string }
      messages: Array<{ role: string; content: string }>
    }) {
      console.log('account_owner :',config.account_owner)
      try {
        const response = await fetch('https://otg-server.odoo365cloud.com/room_option', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(config),
        })
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
        await fetch('https://otg-server.odoo365cloud.com/room_option/' + id, {
          method: 'DELETE',
        })
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
          role: 'user',
          content: message.message,
        })
        const response = await fetch('https://otg-server.odoo365cloud.com/chat_history', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(message),
        })
        const data = await response.json()
        this.chatRoom[message.id].messages.push({
          role: 'assistant',
          content: data.content,
        })
      } catch (error) {
        console.error('Failed to create ChatRooms:', error)
      }
    },
    resetChatRooms() {
      this.chatRoom = {}
    }
  },
})
