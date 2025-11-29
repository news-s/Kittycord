<script>
    import { FetchData } from "$lib/Fetch";
    let { users, user_permissions, user_id, server_id } = $props();

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
        showing_profile.roles = await FetchData(
            `all_user_roles/${user_id}/${server_id}`, 
            "GET"
        );
        showing_profile.state = true;

        roles = await FetchData(`roles_in_server/${server_id}/`, "GET");
    }

    async function AddRole(user_id) {
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

        const role = await GetRoleById(role_id);
        showing_profile.roles.push(role)
    }

    async function RemoveRole(user_id, role_id) {
        const result = FetchData(
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
</script>

<div class="w-60 bg-[#f7f3f9] border-l border-pink-200/50 flex flex-col flex-shrink-0">
        <div class="p-4">
            <h3 class="text-sm font-semibold text-gray-700">Members</h3>

            {#each users as user}
                <div class="user-container">
                    <button onclick={() => ShowProfile(user.user_id)}>{user.name}</button>
                </div>
            {/each}
            
            {#if showing_profile.state}
                <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50" onclick={() => showing_profile.state = false} onkeydown={(e) => {e.key === 'Escape'; showing_profile.state = false}} role="button" tabindex="0">
                    <div class="profile bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 shadow-2xl border border-pink-200/50 flex flex-col items-center" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="dialog" tabindex="-1" style="width: 440px;">
                        <h1>{showing_profile.display_name}</h1>
                        <h5>{showing_profile.name}</h5>
                        
                        <p>{showing_profile.note}</p>

                        <div class="roles">
                            {#if user_permissions?.["Manage roles"] || user_permissions?.["Admin"]}
                                <select class="w-20" id="role">
                                    {#each roles as role}
                                        {#if !showing_profile.roles.some(obj => obj.id === role.id)}
                                            <option value={role.id} style={`color: ${role.color}`}>{role.role_name}</option>
                                        {/if}
                                    {/each}
                                </select>
                                <button onclick={() => AddRole(showing_profile.user_id)}>Add Role</button>
                            {/if}
                            {#each showing_profile.roles as role}
                                <br>
                                {#if user_permissions?.["Manage roles"] || user_permissions?.["Admin"]}
                                    <button onclick={() => RemoveRole(showing_profile.user_id, role.id)}>{role.role_name}</button>
                                {:else}
                                    <div>{role.role_name}</div>
                                {/if}
                            {/each}
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>