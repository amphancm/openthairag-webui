import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SettingView from '@/views/SettingView.vue'
import { useSettingStore } from '@/stores/setting'

// Mock the store
vi.mock('@/stores/setting', () => ({
  useSettingStore: vi.fn()
}))

// Mock global alert
global.alert = vi.fn()

describe('SettingView.vue', () => {
  let wrapper: any
  let mockSettingStore: any

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks()

    mockSettingStore = {
      Settings: {
        id: 'test-id', // Simulating existing settings for save operations
        line_activate: false,
        fb_activate: false,
        product_activate: false,
        feedback_activate: false,
        greeting_activate: false,
        line_key: '',
        line_secret: '',
        facebook_token: '',
        facebook_verify_password: '',
        greeting_prompt: '',
        model_name: '',
        model_type: 'local',
        api_key: ''
      },
      fetchSettings: vi.fn().mockResolvedValue({}),
      createSetting: vi.fn().mockResolvedValue({}),
      saveSetting: vi.fn().mockResolvedValue({})
    }
    ;(useSettingStore as any).mockReturnValue(mockSettingStore)

    wrapper = mount(SettingView, {
      global: {
        stubs: {
          // Stub out child components or directives if necessary, e.g. router-link
        }
      }
    })
  })

  describe('handleSave validation', () => {
    it('API - Model Name Missing: shows alert and does not save', async () => {
      await wrapper.vm.modelType.value === 'api' // Directly set reactive property
      await wrapper.vm.modelName.value === ''
      await wrapper.vm.apiKey.value === 'valid-key'
      
      // Manually set the refs for the test since direct assignment above might not trigger reactivity as expected in tests
      wrapper.vm.modelType = 'api';
      wrapper.vm.modelName = '';
      wrapper.vm.apiKey = 'valid-key';
      await wrapper.vm.$nextTick(); // Wait for DOM updates if any


      await wrapper.vm.handleSave()

      expect(global.alert).toHaveBeenCalledWith('Model Name is required for API type.')
      expect(mockSettingStore.createSetting).not.toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).not.toHaveBeenCalled()
    })

    it('API - API Key Missing: shows alert and does not save', async () => {
      wrapper.vm.modelType = 'api'
      wrapper.vm.modelName = 'valid-model'
      wrapper.vm.apiKey = ''
      await wrapper.vm.$nextTick();

      await wrapper.vm.handleSave()

      expect(global.alert).toHaveBeenCalledWith('API Key is required for API type.')
      expect(mockSettingStore.createSetting).not.toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).not.toHaveBeenCalled()
    })

    it('API - Valid: calls saveSetting with correct payload', async () => {
      wrapper.vm.modelType = 'api'
      wrapper.vm.modelName = 'gpt-4'
      wrapper.vm.apiKey = 'secret-api-key'
      await wrapper.vm.$nextTick();

      await wrapper.vm.handleSave()

      expect(global.alert).not.toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 'test-id',
          model_name: 'gpt-4',
          model_type: 'api',
          api_key: 'secret-api-key'
        })
      )
      expect(mockSettingStore.createSetting).not.toHaveBeenCalled()
    })
    
    it('API - Valid (Create New): calls createSetting with correct payload if no ID', async () => {
      mockSettingStore.Settings.id = null; // Simulate no existing settings
       ;(useSettingStore as any).mockReturnValue(mockSettingStore) // Re-apply mock with new settings

      const newWrapper = mount(SettingView, { // Remount with new store state
        global: {
          stubs: {}
        }
      })
      newWrapper.vm.modelType = 'api'
      newWrapper.vm.modelName = 'gpt-4-new'
      newWrapper.vm.apiKey = 'secret-api-key-new'
      await newWrapper.vm.$nextTick();

      await newWrapper.vm.handleSave()

      expect(global.alert).not.toHaveBeenCalled()
      expect(mockSettingStore.createSetting).toHaveBeenCalled()
      expect(mockSettingStore.createSetting).toHaveBeenCalledWith(
        expect.objectContaining({
          model_name: 'gpt-4-new',
          model_type: 'api',
          api_key: 'secret-api-key-new'
        })
      )
      expect(mockSettingStore.saveSetting).not.toHaveBeenCalled()
    })

    it('Local - Model Name Missing: shows alert and does not save', async () => {
      wrapper.vm.modelType = 'local'
      wrapper.vm.modelName = ''
      await wrapper.vm.$nextTick();

      await wrapper.vm.handleSave()

      expect(global.alert).toHaveBeenCalledWith('Model Name is required for Local type.')
      expect(mockSettingStore.createSetting).not.toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).not.toHaveBeenCalled()
    })

    it('Local - Valid: calls saveSetting with correct payload', async () => {
      wrapper.vm.modelType = 'local'
      wrapper.vm.modelName = 'llama2'
      wrapper.vm.apiKey = '' // Should be ignored for local
      await wrapper.vm.$nextTick();

      await wrapper.vm.handleSave()

      expect(global.alert).not.toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).toHaveBeenCalled()
      expect(mockSettingStore.saveSetting).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 'test-id',
          model_name: 'llama2',
          model_type: 'local',
          api_key: '' // API key is still part of the payload but should be empty
        })
      )
      expect(mockSettingStore.createSetting).not.toHaveBeenCalled()
    })

    it('Local - Valid (Create New): calls createSetting with correct payload if no ID', async () => {
       mockSettingStore.Settings.id = null; // Simulate no existing settings
        ;(useSettingStore as any).mockReturnValue(mockSettingStore) // Re-apply mock

      const newWrapper = mount(SettingView, { // Remount with new store state
        global: {
          stubs: {}
        }
      })
      newWrapper.vm.modelType = 'local'
      newWrapper.vm.modelName = 'llama2-new'
      await newWrapper.vm.$nextTick();
      
      await newWrapper.vm.handleSave()

      expect(global.alert).not.toHaveBeenCalled()
      expect(mockSettingStore.createSetting).toHaveBeenCalled()
      expect(mockSettingStore.createSetting).toHaveBeenCalledWith(
        expect.objectContaining({
          model_name: 'llama2-new',
          model_type: 'local'
        })
      )
      expect(mockSettingStore.saveSetting).not.toHaveBeenCalled()
    })
  })
})

// Helper to wait for next tick
const nextTick = () => new Promise(resolve => setTimeout(resolve, 0));
