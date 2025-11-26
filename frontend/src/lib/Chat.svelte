<script>
	import { onMount } from "svelte";
    import { socket } from "../routes/app/stores";

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
</script>

<div class="messages-container">
    <div class="messages-wrapper">
        {#each messages as message}
            <div class="message-wrapper">
                <div class="avatar">{message.author_id}</div>
                <div class="message">
                    {message.date} <br>
                    {message.content}
                </div>
            </div>
        {/each}
    </div>
    <form class="input-wrapper" name="message-form">
        <input type="text" placeholder="Message" class="text-input"/>
        <input type="submit" value="->" class="submit-input"/>
    </form>
</div>

<style>
    .message-wrapper {
        height: 50px;
        width: 100%;

        background-color: #ccc;

        display: flex;
    }

    .avatar {
        height: 50px;
        aspect-ratio: 1/1;
    }
    .message {
        width: 100%;
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