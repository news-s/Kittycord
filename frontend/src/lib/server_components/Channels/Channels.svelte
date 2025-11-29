<script>
    import { FetchData } from "$lib/Fetch";
	import AddChannel from "./AddChannel.svelte";
	import EditChannel from "./EditChannel.svelte";
    let { socket, server_id, channels, user_permissions } = $props();

    let open = $state(false);
    let editing_channel = $state({
        state: false, 
        id: null, 
        name: null, 
        color: null, 
        role: null,

        name_error: null,
        color_error: null,
        role_error: null
    });

    async function SwitchChannel(channel_id) {
        if($socket?.readyState !== WebSocket.OPEN || !channel_id)return;

        $socket.send(JSON.stringify({
            type: "channel",
            content: channel_id
        }));
    }
</script>

<div class="flex-1 overflow-y-auto px-2 py-3">
    <div class="flex items-center justify-between px-2 py-1">
        <button class="flex items-center gap-1 text-xs text-gray-600 hover:text-gray-800 font-semibold uppercase tracking-wide">
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
            Text Channels
        </button>
        {#if user_permissions?.["Manage channels"] || user_permissions?.["Admin"]}
            <button 
                onclick={() => open = !open}
                aria-label="Create Channel"
                class="p-1 hover:bg-pink-100/60 rounded text-gray-600 hover:text-gray-800"
            >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
            </button>
        {/if}
    </div>
    <div class="mt-1 space-y-0.5">
        {#each channels as channel}
            <div class="flex items-center gap-1 w-full group/item">
                <button 
                    onclick={() => SwitchChannel(channel.channel_id)} 
                    class="flex-1 flex items-center gap-2 px-2 py-1.5 rounded text-gray-700 hover:bg-pink-100/60 hover:text-gray-900"
                >
                    <span style="color: {channel.color || '#a855f7'}" class="group-hover/item:brightness-110">#</span>
                    <span class="text-sm font-medium">{channel.channel_name}</span>
                </button>
                {#if user_permissions?.["Manage channels"] || user_permissions?.["Admin"]}
                    <button 
                        onclick={ () => {
                            editing_channel.state = !editing_channel.state;
                            editing_channel.id = channel.channel_id;
                            editing_channel.name = channel.channel_name;
                            editing_channel.color = channel.color;
                            editing_channel.role = channel.channel_role;
                        }}
                        class="p-1.5 opacity-0 group-hover/item:opacity-100 hover:bg-pink-100/60 rounded transition-opacity"
                        aria-label="Edit channel"
                    >
                        <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                        </svg>
                    </button>
                {/if}
            </div>
        {/each}
    </div>
</div>

<AddChannel {open} {server_id}/>
<EditChannel {editing_channel}/>