<script>
    import { onDestroy, onMount } from "svelte";
    import { profile, socket } from "../../stores.js";
    import { page } from "$app/stores";
	import Chat from "$lib/Chat.svelte";

        let channels = $state([
        // {
        //     channel_id: 1,
        //     channel_name: "general"
        // },
        // {
        //     channel_id: 2,
        //     channel_name: "random"
        // },
        // {
        //     channel_id: 3,
        //     channel_name: "memes"
        // }
    ]);
    let messages = $state([
        // {
        //     message_id: 1,
        //     author_id: 123,
        //     content: "Witaj! 😊",
        //     date: "12:34 PM"
        // }
    ]);
    let open = $state(false);
    let server_id = null;

    const page_unsubscribe = page.subscribe(p => {
        server_id = p.params.id
        
        if($socket?.readyState !== WebSocket.OPEN)return;

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));
    });

    function message(event){
        const data = JSON.parse(event.data);
        
        if(data.type === "load_server") {
            channels = data.channels;
            messages = data.messages;
        }
        else if(data.type === "load_channel") {
            messages = data.messages;
        }
        else if(data.type === "new_message")  messages.push(data);
        else if(data.type === "add_channel") channels.push(data);
        else if(data.type === "remove_message") messages = messages.filter(message => message.message_id !== data.message_id);
        else if(data.type === "remove_channel") {
            channels = channels.filter(channel => channel.channel_id !== data.channel_id);
            
            SwitchChannel(channels[0].channel_id);
        }
        else if(data.type === "edit_message") {
            for (const message of messages) {
                if(message.id !== data.message_id)continue;

                message.content = data.new_content;
                break;
            }
        }
        else if(data.type == "edit_channel_name") {
            for (const channel of channels) {
                if(channel.channel_id !== data.channel_id)continue;

                channel.channel_name = data.new_content;
                break;
            }
        }
    }

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms)); 

    // onMount(async () => {
    //     let token = localStorage.getItem('token');
    //     if (token === undefined) window.location.href = '/login';

    //     let connected = false;
    //     let tries = 0;
    //     while(!connected) {
    //         if($socket?.readyState === WebSocket.OPEN)connected = true;
    //         tries += 1;
    //         if(tries > 3) {
    //             window.location.pathname = "/login"
    //             return;
    //         };
    //         console.warn("Not connected to the web socket. Retrying in 1 second...");

    //         await sleep(1000)
    //     }

    //     $socket.addEventListener('message', message);

    //     $socket.send(JSON.stringify({
    //         type: "server",
    //         content: server_id
    //     }));

    // });

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

        open = false;
    }

    let editing_channel = $state({state: false, id: null, name: null});

    async function EditChannel() {
        editing_channel.state = false;
        const new_name = editing_channel.name.trim();
        editing_channel.name = "";
        
        if(editing_channel.id === null || !new_name)return;
        
        const token = localStorage.getItem("token");

        try {
            const res = await fetch("http://localhost:8000/edit_channel/name", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
                    new_name: new_name
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

    async function DeleteChannel() {
        console.log("editing")
        editing_channel.state = false;
        
        if(editing_channel.id === null || editing_channel.id === undefined)return;
        
        const token = localStorage.getItem("token");
        try {
            const res = await fetch("http://localhost:8000/remove_channel", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
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

    function ServerOptions() {
        window.location.href = `/app/server/${server_id}/options`;
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
                    <div class="flex items-center gap-1 w-full group/item">
                        <button 
                            onclick={() => SwitchChannel(channel.channel_id)} 
                            class="flex-1 flex items-center gap-2 px-2 py-1.5 rounded text-gray-700 hover:bg-pink-100/60 hover:text-gray-900"
                        >
                            <span class="text-purple-500 group-hover/item:text-purple-600">#</span>
                            <span class="text-sm font-medium">{channel.channel_name}</span>
                        </button>
                        <button 
                            onclick={ () => {
                                editing_channel.state = !editing_channel.state;
                                editing_channel.id = channel.channel_id;
                                editing_channel.name = channel.channel_name;
                            }}
                            class="p-1.5 opacity-0 group-hover/item:opacity-100 hover:bg-pink-100/60 rounded transition-opacity"
                            aria-label="Edit channel"
                        >
                            <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                            </svg>
                        </button>
                    </div>
                {/each}
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
    <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50" onclick={() => open = false} onkeydown={(e) => e.key === 'Escape' && (open = false)} role="button" tabindex="0">
        <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 shadow-2xl border border-pink-200/50 flex flex-col items-center" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" tabindex="-1" style="width: 440px;">
            <h2 class="text-2xl font-semibold text-purple-900 mb-6 text-center w-full">Create Channel</h2>
            <input 
                type="text" 
                placeholder="Channel Name" 
                id="channel-name"
                class="px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300" 
                style="width: 376px;"
            />
            <button 
                onclick={HandleCreatingChannel}
                class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                style="width: 376px;"
            >Create</button>
        </div>
    </div>
{/if}

{#if editing_channel.state}
    <div class="fixed top-0 left-0 w-screen h-screen bg-black/30 backdrop-blur-sm flex items-center justify-center z-50" onclick={() => editing_channel.state = false} onkeydown={(e) => e.key === 'Escape' && (editing_channel.state = false)} role="button" tabindex="0">
        <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 shadow-2xl border border-pink-200/50 flex flex-col items-center" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" tabindex="-1" style="width: 440px;">
            <h2 class="text-2xl font-semibold text-purple-900 mb-6 text-center w-full">Edit Channel</h2>
            <input 
                type="text" 
                placeholder="Channel Name" 
                bind:value={editing_channel.name}
                class="px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300" 
                style="width: 376px;"
            />
            <div class="flex gap-3" style="width: 376px;">
                <button 
                    onclick={() => EditChannel()}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                >Save</button>
                <button 
                    onclick={() => DeleteChannel()}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold"
                >Delete</button>
            </div>
        </div>
    </div>
{/if}