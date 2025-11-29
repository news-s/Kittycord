<script>
    import { FetchData } from "$lib/Fetch";

    let { open, server_id } = $props();

    async function CreateChannel() {
        const input = document.getElementById('channel-name');
        const channel_name = input.value;

        const token = localStorage.getItem("token");

        console.log({
                token: token, 
                server_id: server_id, 
                channel_name: channel_name
            })
        await FetchData(
            "add_channel", 
            "POST", 
            {
                token: token, 
                server_id: server_id, 
                channel_name: channel_name
            }
        );

        open = false;
    }
</script>

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
                onclick={CreateChannel}
                class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                style="width: 376px;"
            >Create</button>
        </div>
    </div>
{/if}