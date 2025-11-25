<script>
    import { onDestroy, onMount } from "svelte";
    import { socket } from "../stores.js";
    import { page } from "$app/stores";
    // import { derived } from 'svelte/runes';

    let channels = $state([]);
    let messages = $state([]);
    let open = $state(false);
    let server_id = null;

    console.log(page)

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
        
        channels = message.channels;
    }

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    onMount(async () => {
        let token = localStorage.getItem('token');
        if (token === undefined) window.location.href = '/login';

        let connected = false;
        let tries = 0;
        while(!connected) {
            if($socket?.readyState === WebSocket.OPEN)break;
            if(tries > 3) window.location.pathname = "/login"
            console.warn("Not connected to the web socket. Retrying in 1 second...");

            await sleep(1000)
        }

        server_id = window.location.search.split('=')[1];

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));

        $socket.addEventListener('message', message);
    });

    onDestroy(() => {
        $socket?.removeEventListener('message', message);
        page_unsubscribe();
    });

    async function CreateChannel(token, channel_name) {
        if(server_id === null)return;

        try {
            const res = await fetch(`http://localhost:8000/add_channel`, {
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
        
    }
</script>

<div class="channels-container">
    {#each channels as channel}
        <div class="channel"></div>
    {/each}

    <button class="create-channel" onclick={() => open = !open}>Create Channel</button>
</div>

{#if open}
<div class="modal">
    <h2>Create Channel</h2>
    <input type="text" placeholder="Channel Name" id="channel-name"/>
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
        }
    }>Create</button>
    <button onclick={() => open = false}>Cancel</button>
</div>
{/if}

<style>
    .channels-container {
        width: 200px;
        height: 100svh;
        background-color: #ccc;

        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .channel, .create-channel {
        width: 100%;
        height: 40px;

        background-color: #bbb;
    }

    .create-channel {
        margin-top: auto;
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