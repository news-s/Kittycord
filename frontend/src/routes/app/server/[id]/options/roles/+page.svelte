<script>
    import { page } from "$app/stores";
	import { isValidationError } from "@sveltejs/kit";
	import { onMount, onDestroy } from "svelte";
    import { profile } from "../../../../stores";

    const server_id = $page.params.id;

    async function GetRoles() {
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
            
            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    let editing = $state({state: false, id: null});
    let roles = $state([]);
    
    async function CreateRole(token, name, color) {
        try {
            const res = await fetch(`http://localhost:8000/add_role`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id,
                    role_name: name,
                    role_color: color
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

    function IsValidFullHex(color) {
        return /^#[0-9A-Fa-f]{6}$/.test(color);
    }

    async function HandleCreatingRole() {
        const token = localStorage.getItem("token");
        const name_input = document.getElementById("create-role-name");
        const name = name_input.value.trim();        

        const color_input = document.getElementById("create-role-color");
        const color = color_input.value.trim();

        if(!color || !IsValidFullHex(color) || !name || token === undefined)return;

        const response = await CreateRole(token, name, color);

        roles.push({role_name: name, color: color, id: response, permissions: {}});
    }

    async function RemoveRole(role_id, token) {
        try {
            const res = await fetch(`http://localhost:8000/remove_role`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id
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


    async function HandleRemovingRole(role_id) {
        const token = localStorage.getItem("token");
        
        if(token === undefined || role_id === undefined) return;

        const response = await RemoveRole(role_id, token);

        if(response !== "success")return;

        roles = roles.filter(role => role.id !== role_id);
    }

    function EnableEditingRole(role) {
        editing.id = role.id;
        editing.name = role.role_name;
        editing.color = role.color;
        editing.state = true;
    }

    let user_permissions = $state(null);

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

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
    //getting profile;
    const unsubscribe = profile.subscribe(async () => {
        let tries = 0;
        if($profile === null){
            while(tries < 3){
                await sleep(1000);
                
                if($profile !== null) break;
    
                tries += 1;
            }

            if(tries >= 3)return;
        };

        user_permissions = await GetUserPermissions($profile.user_id);
    });

    onDestroy(unsubscribe);

    onMount(async () => {
        let tries = 0;
        while(tries < 3){
            await sleep(1000);
            
            if(user_permissions !== null) break;

            tries += 1;
        }
        if(tries >= 3)return;

        if(!user_permissions?.["Manage roles"])window.location.href(`/app/server/${server_id}`)

        roles = await GetRoles();
        console.log($state.snapshot(roles));
    });

    let permission_keys = [
        "Admin",
        "Manage server",
        "Manage roles",
        "Manage channels",
        "Ban members",
        "Kick members",
        "Mute members"
    ]

    async function EditPermissions(token, role_id, new_permissions) {
        try {
            const res = await fetch(`http://localhost:8000/edit_role/permissions`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id,
                    new_permissions: new_permissions
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

    async function EditName(token, role_id, new_val) {
        try {
            const res = await fetch(`http://localhost:8000/edit_role/name`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id,
                    new_val: new_val
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

    async function EditColor(token, role_id, new_val) {
        try {
            const res = await fetch(`http://localhost:8000/edit_role/color`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    role_id: role_id,
                    new_val: new_val
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

    async function HandleEditing(role_id) {
        const token = localStorage.getItem("token");
        if(token === undefined)return;

        const name_input = document.getElementById("edit-role-name");
        const name = name_input.value.trim();
        if(name && name !== editing.name) {
            const name_result = await EditName(token, role_id, name);
            
            console.log(name_result);
            if( name_result !== "success") return;

            for(const role of roles) {
                if(role.id !== role_id)continue;

                role.role_name = name;
                break;
            }
        }

        const color_input = document.getElementById("edit-role-color");
        const color = color_input.value.trim();

        if(color && IsValidFullHex(color) && color !== editing.color) {
            const color_result = await EditColor(token, role_id, color);

            console.log(color_result);
            if( color_result !== "success") return;

            for(const role of roles) {
                if(role.id !== role_id)continue;

                role.color = color;
                break;
            }
        }

        let new_permissions = {};

        for(const key of permission_keys) {
            const input = document.getElementsByName(key)[0];
            const value = input.checked;

            new_permissions[key] = value;   
        }

        const permissions_result = await EditPermissions(token, role_id, new_permissions);
        if( permissions_result !== "success") return;

        for(const role of roles) {
            if(role.id !== role_id)continue;

            role.permissions = new_permissions;
            break;
        }
    }
</script>

<div class="options-container">
	<div class="roles-container">
		<form>
			<input type="text" placeholder="Name" id="create-role-name" />
			<input type="text" placeholder="Color" id="create-role-color" />
			<input type="submit" value="Add Role" onclick={HandleCreatingRole} />
		</form>

		{#each roles as role}
			<div>
				<button onclick={() => EnableEditingRole(role)}>
					{role.role_name}
				</button>
				<button onclick={() => HandleRemovingRole(role.id)}>remove</button>
			</div>
		{/each}
	</div>

	{#if editing.state}
		<div class="editing-container">
            <input type="text" placeholder="Name" id="edit-role-name" value={editing.name}/>
			<input type="text" placeholder="Color" id="edit-role-color" value={editing.color}/>
			{#each roles as role}
				{#if role.id === editing.id}
					<form name="editing-form">
						{#each permission_keys as key}
							<label for={key}>{key}:</label>
							<input type="checkbox" checked={role.permissions[key]} name={key}/>
						{/each}
					</form>
				{/if}
			{/each}

            <button onclick={() => HandleEditing(editing.id)}>Save</button>
		</div>
	{/if}
</div>

<style>
	form {
		height: fit-content;

		display: flex;
		flex-direction: column;

		border: 1px solid #999;
	}

	input {
		border: 1px solid #999;
	}

	button {
		border: 1px solid #999;
	}

	.options-container {
		display: flex;
		flex-direction: row;
	}

	.roles-container {
		display: flex;
		flex-direction: column;
	}

	.editing-container {
		width: 500px;

		display: flex;
		flex-direction: column;
	}
</style>
