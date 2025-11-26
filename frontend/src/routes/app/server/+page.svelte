<script>
    import { onDestroy, onMount } from "svelte";
    import { socket } from "../stores.js";
    import { page } from "$app/stores";
	import Chat from "$lib/Chat.svelte";
    // import { derived } from 'svelte/runes';

    let channels = $state([]);
    let messages = $state([]);
    let open = $state(false);
    let server_id = null;

    const page_unsubscribe = page.subscribe(p => {
        server_id = p.url.search.split('=')[1];
        
        if($socket?.readyState !== WebSocket.OPEN)return;

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));
    });

    function message(event){
        const message = JSON.parse(JSON.parse(event.data));
        
        if(message.channels) channels = message.channels;
        if(message.messages) messages = message.messages;

        if(message.message_id !== null && message.message_id !== undefined) messages.push(message);
    }

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    onMount(async () => {
/*         let token = localStorage.getItem('token');
        if (token === undefined) window.location.href = '/login';

        let connected = false;
        let tries = 0;
        while(!connected) {
            if($socket?.readyState === WebSocket.OPEN)break;
            tries += 1;
            if(tries > 3) {
                window.location.pathname = "/login"
                return;
            };
            console.warn("Not connected to the web socket. Retrying in 1 second...");

            await sleep(1000)
        }

        server_id = window.location.search.split('=')[1];

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));

        $socket.addEventListener('message', message); */
    });

    onDestroy(() => {
        $socket?.removeEventListener('message', message);
        page_unsubscribe();
    });

    async function CreateChannel(token, channel_name) {
        if(server_id === null)return;

        try {
            const res = await fetch("http://localhost:8000/add_channel", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    server_id: server_id,
                    channel_name: channel_name
                }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function SwitchChannel(channel_id) {
        if($socket?.readyState !== WebSocket.OPEN || (channel_id === null && channel_id === undefined))return;

        $socket.send(JSON.stringify({
            type: "channel",
            content: channel_id
        }));
    }

    async function HandleCreatingChannel() {
        if($socket?.readyState !== WebSocket.OPEN)return;

        const token = localStorage.getItem('token');
        const input = document.getElementById('channel-name');
        const channel_name = input.value;
        const id = await CreateChannel(token, channel_name);

        channels.push(id);
        open = false;

        $socket.send(JSON.stringify({
            type: "channel",
            content: id
        }));
    }
</script>

<div class="flex" style="width: calc(100vw - 72px); height: 100vh; max-width: calc(100vw - 72px); overflow: hidden;">
    <div class="w-60 bg-[#f7f3f9] border-r border-pink-200/50 flex flex-col flex-shrink-0">
        <div class="h-14 px-4 flex items-center justify-between border-b border-pink-200/50">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
                <span class="font-semibold text-gray-800">server-name</span>
                <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto px-2 py-3">
            <div class="flex items-center justify-between px-2 py-1">
                <button class="flex items-center gap-1 text-xs text-gray-600 hover:text-gray-800 font-semibold uppercase tracking-wide">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                    Text Channels
                </button>
                <button 
                    onclick={() => open = !open}
                    aria-label="Create Channel"
                    class="p-1 hover:bg-pink-100/60 rounded text-gray-600 hover:text-gray-800"
                >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
                    </svg>
                </button>
            </div>

            <div class="mt-1 space-y-0.5">
                {#each channels as channel}
                    <button 
                        onclick={() => SwitchChannel(channel[0])} 
                        class="w-full flex items-center gap-2 px-2 py-1.5 rounded text-gray-700 hover:bg-pink-100/60 hover:text-gray-900 group"
                    >
                        <span class="text-purple-500 group-hover:text-purple-600">#</span>
                        <span class="text-sm font-medium">{channel[1]}</span>
                    </button>
                {/each}
            </div>
        </div>

        <div class="h-14 px-2 bg-transparent border-t border-[#E5E7EB]/0 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full border-0 border-[#E5E7EB] bg-black"></div>
                <div class="flex flex-col">
                    <span class="text-xs font-semibold text-gray-800">user-name</span>
                    <div class="flex items-center gap-1">
                        <div class="w-2 h-2 rounded-full bg-green-500"></div>
                        <span class="text-xs text-green-600">Online</span>
                    </div>
                </div>
            </div>
            <div class="flex items-center gap-1">
                <button aria-label="Microphone" class="p-1.5 hover:bg-pink-100/60 rounded">
                    <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z"/>
                    </svg>
                </button>
                <button aria-label="Headphones" class="p-1.5 hover:bg-pink-100/60 rounded">
                    <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
                    </svg>
                </button>
                <button aria-label="Settings" class="p-1.5 hover:bg-pink-100/60 rounded">
                    <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <Chat bind:messages={messages}></Chat>

    <div class="w-60 bg-[#f7f3f9] border-l border-pink-200/50 flex flex-col flex-shrink-0">
        <div class="p-4">
            <h3 class="text-sm font-semibold text-gray-700">Members</h3>
        </div>
    </div>
</div>

{#if open}
<div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 w-96 shadow-2xl border border-pink-200/50">
        <h2 class="text-2xl font-semibold text-purple-900 mb-6">Create Channel</h2>
        <input 
            type="text" 
            placeholder="Channel Name" 
            id="channel-name"
            class="w-full px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
        />
        <div class="flex gap-3">
            <button 
                onclick={() => open = false}
                class="flex-1 px-4 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-colors"
            >Cancel</button>
            <button 
                onclick={async () => {
                    const token = localStorage.getItem('token');
                    const input = document.getElementById('channel-name');
                    const channel_name = input.value;
                    const id = await CreateChannel(token, channel_name);
                    channels.push(id);
                    open = false;

                    $socket.send(JSON.stringify({
                        type: "channel",
                        content: id
                    }));
                }}
                class="flex-1 px-4 py-2.5 rounded-xl text-white font-medium transition-colors shadow-lg"
                style="background: linear-gradient(135deg, #E9D5FF 0%, #BFDBFE 70.71%);"
            >
                <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent font-semibold">Create</span>
            </button>
        </div>
    </div>
</div>
{/if}