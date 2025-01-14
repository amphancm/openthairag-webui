// src/services/socket.ts
import { io, Socket } from "socket.io-client";

const URL = "http://localhost:3000"; // Replace with your server URL

const socket: Socket = io(URL, {
  autoConnect: false, // Connect manually
});

export default socket;