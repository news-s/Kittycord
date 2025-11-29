<script>
    import { onDestroy, onMount } from "svelte";

    import { profile, socket, load_layout } from "../../stores.js";
    import { page } from "$app/stores";

    import { FetchData } from "$lib/Fetch.js";
	import Chat from "$lib/server_components/Chat/Chat.svelte";
	import Members from "$lib/server_components/Members.svelte";
	import Channels from "$lib/server_components/Channels/Channels.svelte";

    let token = null;

    let users = $state(null);
    let channels = $state(null);
    let messages = $state(null);
    let server_id = $state(null);
    let user_permissions = $state([]);
    let server_name = $state("Server Name");
    let channel_name = $state("Channel Name");    
    
    const page_subscription = page.subscribe(p => {
        server_id = p.params.id
        
        if($socket?.readyState !== WebSocket.OPEN)return;

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));
    });
    
    load_layout.set(true);

    function message(event){
        const data = JSON.parse(event.data);
        
        if(data.type === "load_server") {
            server_name = data.server_name
            channel_name = data.channels[0]?.channel_name

            channels = data.channels;
            messages = data.messages;
        }
        else if(data.type === "load_channel") {
            messages = data.messages;
            channel_name = data.channel_name
        }
        else if(data.type === "new_message")  messages.push(data);
        else if(data.type === "add_channel") channels.push(data);
        else if(data.type === "remove_message") messages = messages.filter(message => message.message_id !== data.message_id);
        else if(data.type === "remove_channel") {
            channels = channels.filter(channel => channel.channel_id !== data.channel_id);
            
            if(channels.length > 0) {
                SwitchChannel(channels[0].channel_id);
                return;
            }
            
            channels = [];
            messages = [];
        }
        else if(data.type === "edit_message") {
            for (const message of messages) {
                if(message.id !== data.message_id)continue;

                message.content = data.new_content;
                break;
            }
        }
        else {
            for (const channel of channels) {
                if(channel.channel_id !== data.channel_id)continue;

                if(data.type === "edit_channel_name") channel.channel_name = data.new_content;
                else if(data.type === "edit_channel_color")channel.color = data.new_content;
                else if(data.type === "edit_channel_role_needed")channel.role = data.new_content;

                break;
            }
        }
    }

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms)); 

    onMount(async () => {
        token = localStorage.getItem("token");
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

            await sleep(1000);
        }

        $socket.addEventListener('message', message);

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));

        users = await FetchData(`get_members/${server_id}/`, "GET");
        user_permissions = await FetchData(`permissions/${$profile.user_id}/${server_id}/`, "GET");

        const data = await FetchData(`server_name/${server_id}/`, "GET");
        server_name = data.server_name;
    });

    onDestroy(() => {
        $socket?.removeEventListener('message', message);
        page_subscription();
    });
</script> 

<div class="flex" style="width: calc(100vw - 72px); height: 100vh; max-width: calc(100vw - 72px); overflow: hidden;">
    <div class="w-60 bg-[#f7f3f9] border-r border-pink-200/50 flex flex-col flex-shrink-0">
        <div class="h-14 px-4 flex items-center justify-between border-b border-pink-200/50">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
                <span class="font-semibold text-gray-800">{server_name}</span>
                <a href={`/app/server/${server_id}/options`} title="Options">
                    <svg 
                        class="w-4 h-4 text-gray-600 cursor-pointer" 
                        fill="currentColor" 
                        viewBox="0 0 20 20" 
                        role="button" 
                        tabindex="0" 
                        aria-label="Opcje serwera"
                    >
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                </a>
            </div>
        </div>
        
        <Channels {socket} {server_id} {channels} {user_permissions}/>
    </div>

    <Chat {messages} user_id={$profile?.user_id} {server_id} {channel_name} {user_permissions}/>
    <Members {users} {user_permissions} user_id={$profile?.user_id} {server_id}/>
</div>