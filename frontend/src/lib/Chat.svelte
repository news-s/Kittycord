<script>
	import { onMount, tick } from "svelte";
    import { socket, profile } from "../routes/app/stores";

    let { messages } = $props();   

    async function SendMessage(event) {
        event.preventDefault();

        if($socket?.readyState !== WebSocket.OPEN)return;

        const input = document.querySelector('.text-input');
        const message = input.value.trim();

        if(!message) return;

        $socket.send(JSON.stringify({
            type: "message",
            content: message
        }));

        event.target.reset()
    }

    onMount(() => {
        const form = document.forms["message-form"];
        form.addEventListener("submit", SendMessage);
    });

    let editing = $state({state: false, id: null, input: null});

    async function EnableEditingMessage(event, message_id) {
        editing.state = !editing.state;
        editing.id = message_id;

        await tick();          
        editing.input.focus(); 
    }

    async function DeleteMessage(message_id) {
        const token = localStorage.getItem("token")

        try {
            const res = await fetch("http://localhost:8000/remove_message", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    message_id: message_id,
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

    async function EditMessage() {
        editing.state = !editing.state;

        if(editing.input === null || editing.id === null)return;

        const token = localStorage.getItem('token');
        const new_content = editing.input.value.trim();

        if(!new_content){
            DeleteMessage(editing.id);
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/edit_message", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    message_id: editing.id,
                    new_content: new_content
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
</script>

<div class="messages-container">
    <div class="messages-wrapper">
        {#each messages as message}
            <div class="message-wrapper">
                <div class="avatar">{message.author_id}</div>
                <div class="message">
                    {message.date} <br>
                    {#if editing.state && editing.id === message.message_id}
                        <input 
                            type="text"
                            bind:value={message.content}
                            bind:this={editing.input}
                            onblur={() => editing.state = false}
                            onkeydown={(event) => event.key === "Enter" && EditMessage()}
                        >
                    {:else}
                        {message.content}
                    {/if}
                </div>
                <!-- enable after getting profile will provide id -->

                <!-- {#if message.author_id === $profile.id}
                {/if} -->

                {#if !editing.state}
                    <div class="options-container">
                        <button class="edit" onclick={(event) => EnableEditingMessage(event, message.message_id)}>edit</button>
                        <button class="delete" onclick={(event) => DeleteMessage(message.message_id)}>delete</button>
                    </div>
                {/if}
            </div>
        {/each}
    </div>
    <form class="input-wrapper" name="message-form">
        <input type="text" placeholder="Message" class="text-input"/>
        <input type="submit" value="->" class="submit-input"/>
    </form>
</div>

<style>
    :root {
        --edit-display: none;
    }

    .message-wrapper {
        height: 50px;
        width: 100%;

        background-color: #ccc;

        display: flex;
    }

    .message-wrapper:hover {
        --edit-display: flex;
    }

    .avatar {
        height: 50px;
        aspect-ratio: 1/1;
    }

    .options-container {
        height: 50px;
        aspect-ratio: 1/1;

        background-color: #666;

        display: var(--edit-display);
    }

    .message {
        width: 100%; 
        
        overflow: hidden;
    }

    .messages-container {
        width: calc(100svw - 272px);
        height: 100svh;
        background-color: #aaa;

        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .messages-wrapper {
        height: calc(100svh - 60px);
        width: 100%;

        display: flex;
        flex-direction: column;

        overflow-y: scroll;
    }

    .input-wrapper {
        height: 60px;
        width: 100%;

        display: flex;
        flex-direction: row;
    }

    .text-input {
        background-color: #999;
        color: #000;

        width: 100%;
    }

    .submit-input {
        width: 60px;
        height: 60px;

        background-color: #888;
    }   
</style>