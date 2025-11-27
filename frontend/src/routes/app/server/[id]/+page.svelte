<script>
    import { onDestroy, onMount } from "svelte";
    import { profile, socket } from "../../stores.js";
    import { page } from "$app/stores";
	import Chat from "$lib/Chat.svelte";

    let channels = $state([]);
    let messages = $state([]);
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
        
        if(data.channels) channels = data.channels;
        if(data.messages) messages = data.messages;

        if(data.type === "new_message")  messages.push(data);
        else if(data.type === "add_channel") channels.push(data);
        else if(data.type === "remove_message") messages = messages.filter(message => message.message_id !== data.message_id);
        else if(data.type === "remove_channel") channels = channels.filter(channel => channel.channel_id !== data.channel_id);
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

    onMount(async () => {
        let token = localStorage.getItem('token');
        if (token === undefined) window.location.href = '/login';

        let connected = false;
        let tries = 0;
        while(!connected) {
            if($socket?.readyState === WebSocket.OPEN)connected = true;
            tries += 1;
            if(tries > 3) {
                window.location.pathname = "/login"
                return;
            };
            console.warn("Not connected to the web socket. Retrying in 1 second...");

            await sleep(1000)
        }

        $socket.addEventListener('message', message);

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));

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

<div class="server-container">
    <div class="channels-container">
        <button class="server-options" onclick={ServerOptions}>Server Options</button>

        {#each channels as channel}
            <div class="channel-wrapper">
                <button class="channel" onclick={() => SwitchChannel(channel.channel_id)}>{channel.channel_name}</button>
                <!-- enable editing when user has permission -->
                
                <!-- {$if $profile.id === channel.owner_id} --> 
                    <button 
                        class="edit-channel" 
                        onclick={ () => {
                            editing_channel.state = !editing_channel.state;
                            editing_channel.id = channel.channel_id;
                            editing_channel.name = channel.channel_name;
                        }}
                    >
                        ...
                    </button>
                <!-- {/if}  -->

            </div>
        {/each}
    
        <button class="create-channel" onclick={() => open = !open}>Create Channel</button>
    </div>
    
    <Chat bind:messages={messages}></Chat>
</div>

{#if open}
    <div class="modal">
        <h2>Create Channel</h2>
        <input type="text" placeholder="Channel Name" id="channel-name"/>
        <button onclick={() => HandleCreatingChannel()}>Create</button>
        <button onclick={() => open = false}>Cancel</button>
    </div>
{/if}

{#if editing_channel.state}
    <div class="modal">
        <h2>Edit Channel</h2>
        <input type="text" placeholder="Channel Name" id="channel-name" bind:value={editing_channel.name}/>
        <button onclick={() => EditChannel()}>Edit</button>
        <button onclick={() => DeleteChannel()}>Delete</button>
        <button onclick={() => editing_channel.state = false}>Cancel</button>
    </div>
{/if}

<style>
    .channel-wrapper {
        display: flex;
        background-color: #bbb;
    }
    
    .edit-channel {
        height: 40px;
        aspect-ratio: 1/1;
    }

    .server-container {
        display: flex;
    }

    .channels-container {
        width: 200px;
        height: 100svh;
        background-color: #ccc;

        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .channel, .create-channel, .server-options {
        width: 100%;
        height: 40px;

    }

    .modal {
        width: 200px;
        height: 200px;

        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        background-color: #fff;

        padding: 20px;

        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

        border-radius: 8px;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-evenly;
    }

    #channel-name {
        width: 80%;
        text-align: center;
    }
</style>