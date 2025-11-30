<script>
    import { FetchData } from "$lib/Fetch";
    
    let { editing_channel, roles } = $props();

    async function EditChannelName() {
        const token = localStorage.getItem("token");

        const result = FetchData(
            "edit_channel/name", 
            "PUT", 
            {
                token: token, 
                channel_id: editing_channel.id, 
                new_val: editing_channel.name

            }
        );
        
        if(result === "success")return;
        
        editing_channel.name_error = result;
    }

    function IsValidFullHex(color) {
        return /^#[0-9A-Fa-f]{6}$/.test(color);
    }

    async function EditChannelColor() {
        const token = localStorage.getItem("token");

        if(!IsValidFullHex(editing_channel.color)) {
            editing_channel.color_error = "Invalid color";
            return;
        };

        const result = FetchData(
            "edit_channel/color", 
            "PUT", 
            {
                token: token, 
                channel_id: editing_channel.id,
                new_val: editing_channel.color
            }
        );

        if(result === "success")return;
        
        editing_channel.color_error = result;
    }

    async function EditChannelRole() {
        const token = localStorage.getItem("token");

        const result = FetchData(
            "edit_channel/role_needed", 
            "PUT", 
            {
                token: token, 
                channel_id: editing_channel.id,
                new_val: String(editing_channel.role)
            }
        );

        if(result === "success")return;
        
        editing_channel.role_error = result;
    }

    function HandleEditingChannel() {
        EditChannelName();
        EditChannelColor();
        EditChannelRole();
    }

    async function DelteChannel() {
        editing_channel.state = false;
        const token = localStorage.getItem("token");

        const result = await FetchData(
            "remove_channel", 
            "PATCH", 
            {
                token: token, 
                channel_id: editing_channel.id
            }
        )
    }
</script>

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
            <input 
                type="text" 
                placeholder="Channel Color" 
                bind:value={editing_channel.color}
                class="px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300" 
                style="width: 376px;"
            />
            <select 
                type="text" 
                placeholder="Channel Role" 
                bind:value={editing_channel.role}
                class="px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300" 
                style="width: 376px;"
            >
                {#each roles as role}
                    <option value={role.id}>{role.role_name}</option>
                {/each}
            </select>
            <div class="flex gap-3" style="width: 376px;">
                <button 
                    onclick={HandleEditingChannel}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                >Save</button>
                <button 
                    onclick={DelteChannel}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold"
                >Delete</button>
            </div>
        </div>
    </div>
{/if}