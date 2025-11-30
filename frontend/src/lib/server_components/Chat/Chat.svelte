<script>
	import { tick } from "svelte";
    import { FetchData } from "$lib/Fetch";
    import { socket } from "../../../routes/app/stores";
	import MessageInput from "./MessageInput.svelte";
	import MessageOptions from "./MessageOptions.svelte";
	import ChatName from "./ChatName.svelte";

    let { messages, user_id, server_id, channel_name, user_permissions } = $props();   
    
    let editing = $state({state: false, id: null, input: null});
    let user_cache = $state({});
    let error_message = $state("");
    

    async function DeleteMessage(message_id) {
        const token = localStorage.getItem("token")

        const result = await FetchData(
            "remove_message", 
            "PATCH", 
            {
                token: token,
                message_id: message_id
            }
        );

        if(result.status && result.status != 200) {
            error_message = await result.json();
            error_message = error_message.detail;

            setTimeout(() => error_message = "", 3000);
            return;
        }
        if(result == "invalid input") {
            error_message = result;

            setTimeout(() => error_message = "", 3000);
            return;
        }
    }

    async function EditMessage(message_id) {
        editing.state = !editing.state;

        if(editing.input === null || editing.id === null)return;

        const token = localStorage.getItem('token');
        const new_content = editing.input.value.trim();

        if(!new_content){
            DeleteMessage(editing.id);
            return;
        }

        const result = await FetchData(
            "edit_message", 
            "PUT", 
            {
                token: token,
                message_id: editing.id,
                new_content: new_content
            }
        );

        if(result.status && result.status != 200) {
            error_message = await result.json();
            error_message = error_message.detail;

            setTimeout(() => error_message = "", 3000);
            return;
        }
        if(result == "invalid input") {
            error_message = result;
            setTimeout(() => error_message = "", 3000);
            return;
        }

        const message = document.getElementById(message_id);
        message.innerHTML = new_content
    }

    async function GetUser(user_id) {
        if(user_cache[user_id])return user_cache[user_id];
        
        const user = await FetchData(`profile/${user_id}/`, "GET");
        user_cache[user_id] = user;
        return user;
    }

</script>

<div class="flex-1 flex flex-col" style="background: linear-gradient(180deg, #FDF4FF 0%, #EDE9FE 100%);">
    <ChatName chat_name={channel_name} />

    <div class="flex-1 overflow-y-auto px-6 py-4">
        {#each messages as message}
            <div class="flex gap-4 mb-6 hover:bg-white/30 px-3 py-2 rounded group/message relative">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex-shrink-0"></div>
                <div class="flex-1">
                    <div class="flex items-baseline gap-2 mb-1">
                        <span class="font-semibold text-gray-800 text-base">{user_cache[message.author_id]?.display_name || GetUser(message.author_id)}</span>
                        <span class="text-xs text-gray-500">{message.date}</span>
                    </div>
                    {#if editing.state && editing.id === message.message_id}
                    <input 
                    type="text"
                    bind:value={editing.content}
                    bind:this={editing.input}
                    onblur={() => editing.state = false}
                    onkeydown={(event) => event.key === "Enter" && EditMessage(message.message_id)}
                    class="w-full px-3 py-2 rounded-lg bg-white/80 border border-purple-200 text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
                    >
                    {:else}
                    <p class="text-gray-700 text-base leading-relaxed break-words whitespace-pre-line overflow-x-auto max-w-full" id={message.message_id}>{message.content}</p>
                    {/if}
                </div>
                {#if message.author_id === user_id || user_permissions?.["Manage channels"] || user_permissions?.["Admin"]}
                {#if !editing.state}
                <MessageOptions {message} bind:editing={editing}/>
                {/if}
                {/if}
            </div>
            {/each}
        </div>
        <p class="text-red-600">{error_message}</p>
    <MessageInput {socket} bind:messages={messages} {user_id}/>
</div>