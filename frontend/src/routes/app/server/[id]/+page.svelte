<script>
    import { onDestroy, onMount } from "svelte";
    import { profile, socket, load_server_bar } from "../../stores.js";
    import { page } from "$app/stores";
	import Chat from "$lib/Chat.svelte";
	import { json } from "@sveltejs/kit";

    let users_cache = {};
    let users = $state(null);
    let channels = $state(null);
    let messages = $state(null);
    let open = $state(false);
    let server_id = null;
    let user_permissions = $state([]);

    const page_unsubscribe = page.subscribe(p => {
        server_id = p.params.id
        
        if($socket?.readyState !== WebSocket.OPEN)return;

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));
    });

    function message(event){
        const data = JSON.parse(event.data);
        
        if(data.type === "load_server") {
            channels = data.channels;
            messages = data.messages;
        }
        else if(data.type === "load_channel") {
            messages = data.messages;
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

    async function CreateChannel(token, channel_name) {
        if(server_id === null)return;

        try {
            const res = await fetch("http://localhost:8000/add_channel", {
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
        if($socket?.readyState !== WebSocket.OPEN || (channel_id === null && channel_id === undefined))return;

        $socket.send(JSON.stringify({
            type: "channel",
            content: channel_id
        }));
    }

    async function HandleCreatingChannel() {
        if($socket?.readyState !== WebSocket.OPEN)return;

        const token = localStorage.getItem('token');
        const input = document.getElementById('channel-name');
        const channel_name = input.value;
        const id = await CreateChannel(token, channel_name);

        open = false;
    }

    let editing_channel = $state({state: false, id: null, name: null, color: null, role: null});

    async function EditChannelName() {
        editing_channel.state = false;
        const new_name = editing_channel.name.trim();
        editing_channel.name = "";
        
        if(editing_channel.id === null || !new_name)return;
        
        const token = localStorage.getItem("token");

        try {
            const res = await fetch("http://localhost:8000/edit_channel/name", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
                    new_val: new_name
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

    function IsValidFullHex(color) {
        return /^#[0-9A-Fa-f]{6}$/.test(color);
    }

    async function EditChannelColor() {
        editing_channel.state = false;
        const new_color = editing_channel.color.trim();
        editing_channel.color = "";
        
        if(editing_channel.id === null || !new_color || !IsValidFullHex(new_color))return;
        
        const token = localStorage.getItem("token");

        try {
            const res = await fetch("http://localhost:8000/edit_channel/color", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
                    new_val: new_color
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

    async function EditChannelRole() {
        editing_channel.state = false;
        const new_role = editing_channel?.new_role.trim();
        editing_channel.role = "";
        
        if(editing_channel.id === null || !new_role)return;
        
        const token = localStorage.getItem("token");

        try {
            const res = await fetch("http://localhost:8000/edit_channel/role_needed", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
                    new_val: new_role
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

    function HandleEditingChannel() {
        EditChannelName();
        EditChannelColor();
        EditChannelRole();
    }

    async function DeleteChannel() {
        console.log("editing")
        editing_channel.state = false;
        
        if(editing_channel.id === null || editing_channel.id === undefined)return;
        
        const token = localStorage.getItem("token");
        try {
            const res = await fetch("http://localhost:8000/remove_channel", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    channel_id: editing_channel.id,
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

    function ServerOptions() {
        window.location.href = `/app/server/${server_id}/options`;
    }

    async function GetAllUsers() {
        try {
            const res = await fetch(`http://localhost:8000/get_members/${server_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();

        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function GetProfile(user_id) {
        try {
            const res = await fetch(`http://localhost:8000/profile/${user_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function GetUserRoles(user_id) {
        try {
            const res = await fetch(`http://localhost:8000/all_user_roles/${user_id}/${server_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    let showing_profile = $state({state: false, name: null, username: null, note: null, user_id: null, roles: []});
    let roles = $state([]);

    async function ShowProfile(user_id) {
        const profile = await GetProfile(user_id);

        showing_profile.display_name = profile.display_name;
        showing_profile.name = profile.name;
        showing_profile.note = profile.note;
        showing_profile.user_id = profile.user_id;
        showing_profile.roles = await GetUserRoles(user_id);
        showing_profile.state = true;

        roles = await GetAllRoles();
    }

    async function GetAllRoles() {
        try {
            const res = await fetch(`http://localhost:8000/roles_in_server/${server_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function AddRole(token, role_id, user_id) {
        try {
            const res = await fetch("http://localhost:8000/add_role", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id,
                    user_id: user_id
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function RemoveRole(token, role_id, user_id) {
        try {
            const res = await fetch("http://localhost:8000/remove_role", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id,
                    user_id: user_id
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function HandleRemovingRoles(user_id, role_id) {
        const token = localStorage.getItem("token");

        if(token === undefined || user_id === undefined || role_id === undefined)return;

        const result = await RemoveRole(token, role_id, user_id)

        if(result !== "success")return;

        showing_profile.roles = showing_profile.roles.filter(role => role.id !== role_id);
    }

    async function GetRoleById(role_id) {
        try {
            const res = await fetch(`http://localhost:8000/get_role_by_id/${role_id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function HandleAddingRoles(user_id) {
        const token = localStorage.getItem("token");

        const select = document.getElementById("role");
        const role_id = select.value;

        if( !role_id || role_id === undefined || user_id === undefined || token === undefined) return;

        const result = await AddRole(token, role_id, user_id);

        if(result !== "success")return;

        // const role = await GetRoleById(role_id);
        // showing_profile.roles.push(role)
    }   

    async function GetUserPermissions(user_id) {
        try {
            const res = await fetch(`http://localhost:8000/permissions/${user_id}/${server_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    onMount(async () => {
        let token = localStorage.getItem('token');
        if (token === undefined) window.location.href = '/login';

        load_server_bar.set(true);

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

            await sleep(1000)
        }

        $socket.addEventListener('message', message);

        $socket.send(JSON.stringify({
            type: "server",
            content: server_id
        }));

        users = await GetAllUsers();
        roles = await GetAllRoles();
        user_permissions = await GetUserPermissions($profile.user_id);
    });

    onDestroy(() => {
        $socket?.removeEventListener('message', message);
        page_unsubscribe();
    });

</script>

<div class="flex" style="width: calc(100vw - 72px); height: 100vh; max-width: calc(100vw - 72px); overflow: hidden;">
    <div class="w-60 bg-[#f7f3f9] border-r border-pink-200/50 flex flex-col flex-shrink-0">
        <div class="h-14 px-4 flex items-center justify-between border-b border-pink-200/50">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
                <span class="font-semibold text-gray-800">server-name</span>
                <svg 
                    class="w-4 h-4 text-gray-600 cursor-pointer" 
                    fill="currentColor" 
                    viewBox="0 0 20 20" 
                    role="button" 
                    tabindex="0" 
                    aria-label="Opcje serwera"
                    onclick={ServerOptions}
                    onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && ServerOptions()}
                >
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto px-2 py-3">
            <div class="flex items-center justify-between px-2 py-1">
                <button class="flex items-center gap-1 text-xs text-gray-600 hover:text-gray-800 font-semibold uppercase tracking-wide">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                    Text Channels
                </button>
                {#if user_permissions?.["Manage channels"]}
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
                        {#if user_permissions?.["Manage channels"]}
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
    </div>

    <Chat bind:messages={messages}></Chat>

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
                            <select class="w-20" id="role">
                                {#each roles as role}
                                    {#if !showing_profile.roles.some(obj => obj.id === role.id)}
                                        <option value={role.id} style={`color: ${role.color}`}>{role.role_name}</option>
                                    {/if}
                                {/each}
                            </select>
                            <button onclick={() => HandleAddingRoles(showing_profile.user_id)}>Add Role</button>
                            {#each showing_profile.roles as role}
                                <br>
                                <button onclick={() => HandleRemovingRoles(showing_profile.user_id, role.id)}>{role.role_name}</button>
                            {/each}
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>

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
                onclick={HandleCreatingChannel}
                class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                style="width: 376px;"
            >Create</button>
        </div>
    </div>
{/if}

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
            <input 
                type="text" 
                placeholder="Channel Role" 
                bind:value={editing_channel.role}
                class="px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300" 
                style="width: 376px;"
            />
            <div class="flex gap-3" style="width: 376px;">
                <button 
                    onclick={() => HandleEditingChannel()}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold"
                >Save</button>
                <button 
                    onclick={() => DeleteChannel()}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold"
                >Delete</button>
            </div>
        </div>
    </div>
{/if}

<style>
    .profile {
        height: 400px;
        width: 200px;

        position: absolute;
        top: 50%;
        left: 50%;
        
        background-color: #999;

        display: flex;
        flex-direction: column;
        align-items: center;

        transform: translate(-50%, -50%);
    }
</style>