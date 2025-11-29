// src/lib/stores/socket.js
import { browser } from "$app/environment";
import { writable, get } from "svelte/store";

export const socket = writable(null);           
export const connectedUserId = writable(null);  
export const wsReady = writable(false);         

if (browser) {
    const token = localStorage.getItem("token");
    if (!token) {
        console.warn("No token found in localStorage — websocket will not connect");
    } else {
        const host = location.hostname || "localhost";
        const wsUrl = `ws://${host}:8000/ws?token=${token}`;

        const ws = new WebSocket(wsUrl);

        ws.addEventListener("open", () => {
            socket.set(ws);
            wsReady.set(true);
            console.log("WS open", wsUrl);
        });

        ws.addEventListener("message", (ev) => {
            try {
                const data = JSON.parse(ev.data);
                if (data?.user_id) {
                    connectedUserId.set(Number(data.user_id));
                }
            } catch (e) {
            }
        });

        ws.addEventListener("close", () => {
            socket.set(null);
            wsReady.set(false);
            connectedUserId.set(null);
            console.warn("WS closed");
        });

        ws.addEventListener("error", (err) => {
            console.error("WS error", err);
        });

        socket.set(ws);
    }
}
