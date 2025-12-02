<script>
    import { FetchData } from "$lib/Fetch";
    let { users, user_permissions, server_id } = $props();

    let roles = $state([]);
    let showing_profile = $state({
        state: false, 
        name: null, 
        username: null, 
        note: null, 
        user_id: null, 
        roles: []
    });

    async function ShowProfile(user_id) {
        const profile = await FetchData(`profile/${user_id}/`, "GET");

        showing_profile.display_name = profile.display_name;
        showing_profile.name = profile.name;
        showing_profile.note = profile.note;
        showing_profile.user_id = profile.user_id;
        showing_profile.roles = await FetchData(`all_user_roles/${user_id}/${server_id}/`, "GET");
        console.log($state.snapshot(showing_profile.roles));

        showing_profile.state = true;

        roles = await FetchData(`roles_in_server/${server_id}/`, "GET");
    }

    async function AddRole(user_id) {
        const token = localStorage.getItem("token");
        const select = document.getElementById("role");
        const role_id = select.value;

        const result = await FetchData(
            "add_role", 
            "PUT", 
            {
                token: token, 
                role_id: role_id, 
                user_id: user_id
            }
        );

        if(result !== "success")return;

        const role = await FetchData(`role/${role_id}/`, "GET");
        showing_profile.roles.push(role)
    }

    async function RemoveRole(user_id, role_id) {
        const token = localStorage.getItem("token");

        const result = await FetchData(
            "remove_role", 
            "PUT", 
            {
                token: token, 
                role_id: role_id, 
                user_id: user_id
            }
        );

        if(result !== "success")return;

        showing_profile.roles = showing_profile.roles.filter(role => role.id !== role_id);
    }

    function IsLight(hex) {
        hex = hex.replace("#", "");

        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);

        const luminance = (0.299 * r + 0.587 * g + 0.114 * b);

        return luminance > 186;
    }
</script>

<div class="w-60 bg-[#f7f3f9] border-l border-pink-200/50 flex flex-col flex-shrink-0">
    <div class="p-4">
        <h3 class="text-sm font-semibold text-gray-700">Members</h3>

        <div class="space-y-2">
            {#each users as user}
                <button 
                    type="button"
                    class="flex items-center gap-3 p-2 rounded-lg hover:bg-pink-100 transition cursor-pointer w-full text-left"
                    onclick={() => ShowProfile(user.user_id)}
                    aria-label={`Show profile for ${user.name}`}
                >
                    <img src={user.avatar} alt="avatar" class="w-8 h-8 rounded-full border-2 border-pink-200" />
                    <div class="flex-1">
                        <div class="font-semibold text-gray-800">{user.name}</div>
                        <div class="text-xs text-gray-500">{user.status}</div>
                    </div>
                </button>
            {/each}
        </div>
        
        {#if showing_profile.state}
            <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50" onclick={() => showing_profile.state = false} onkeydown={(e) => {e.key === 'Escape'; showing_profile.state = false}} role="button" tabindex="0">
                <div class="profile bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 shadow-2xl border border-pink-200/50 flex flex-col items-center gap-4" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" tabindex="-1" style="width: 440px;">
                    <div class="w-24 h-24 rounded-full border-4 border-pink-200 shadow-lg mb-2 bg-black flex items-center justify-center">
                    </div>
                    <h1 class="text-2xl font-bold text-purple-800">{showing_profile.display_name}</h1>
                    <h5 class="text-lg text-gray-600">@{showing_profile.name}</h5>
                    <p class="max-w-md text-center text-gray-700 italic">{showing_profile.note}</p>
                    <div class="roles w-full flex flex-wrap justify-center gap-2 mt-4">
                        {#if user_permissions?.["Manage roles"] || user_permissions?.["Admin"]}
                            <select class="w-32 px-2 py-1 rounded-xl border border-pink-200 bg-white text-purple-800 font-semibold" id="role">
                                {#each roles as role}
                                    {#if !showing_profile.roles.some(obj => obj.id === role.id)}
                                        {console.log(IsLight(role.color))}
                                        {#if IsLight(role.color)}
                                            <option value={role.id} style={`color: ${role.color}; background-color: #333`}>{role.role_name}</option>
                                        {:else}
                                            <option value={role.id} style={`color: ${role.color}`}>{role.role_name}</option>
                                        {/if}
                                    {/if}
                                {/each}
                            </select>
                            <button onclick={() => AddRole(showing_profile.user_id)} class="ml-2 px-4 py-1 rounded-xl bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold shadow hover:scale-105 transition-all">Dodaj rolę</button>
                        {/if}
                        {#each showing_profile.roles as role}
                            {#if user_permissions?.["Manage roles"] || user_permissions?.["Admin"]}
                                <button onclick={() => RemoveRole(showing_profile.user_id, role.id)} class="px-3 py-1 rounded-xl bg-purple-100 text-purple-800 font-semibold shadow hover:bg-purple-200 transition-all">{role.role_name}</button>
                            {:else}
                                <div class="px-3 py-1 rounded-xl bg-purple-50 text-purple-700 font-semibold shadow">{role.role_name}</div>
                            {/if}
                        {/each}
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>