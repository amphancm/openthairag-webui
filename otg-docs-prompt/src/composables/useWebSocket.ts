import { ref, onUnmounted } from 'vue';

export function useWebSocket(url: string) {
    const socket = ref<WebSocket | null>(null);
    const messagesws = ref<string[]>([]);
    const isConnected = ref(false);

    const connect = () => {
        socket.value = new WebSocket(url);

        socket.value.onopen = () => {
            console.log('WebSocket connected');
            isConnected.value = true;
        };

        socket.value.onmessage = (event) => {
            console.log('Message received:', event.data);
            messagesws.value.push(event.data);
        };

        socket.value.onclose = () => {
            console.log('WebSocket disconnected');
            isConnected.value = false;
        };

        socket.value.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    };

    const sendMessage = (message: string) => {
        if (socket.value && isConnected.value) {
            socket.value.send(message);
        } else {
            console.error('WebSocket is not connected');
        }
    };

    const disconnect = () => {
        if (socket.value) {
            socket.value.close();
        }
    };

    onUnmounted(() => {
        disconnect();
    });

    return {
        messagesws,
        isConnected,
        connect,
        sendMessage,
        disconnect,
    };
}