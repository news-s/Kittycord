<script>
    import { page } from "$app/stores";
	import { isValidationError } from "@sveltejs/kit";
	import { onMount, onDestroy } from "svelte";
    import { profile } from "../../../../stores";
    import { FetchData } from "$lib/Fetch";

    const server_id = $page.params.id;

    let editing = $state({state: false, id: null});
    let roles = $state([]);

    const permission_keys = [
        "Admin",
        "Manage server",
        "Manage roles",
        "Manage channels",
        "Ban members",
        "Kick members",
        "Mute members"
    ]

    function IsValidFullHex(color) {
        return /^#[0-9A-Fa-f]{6}$/.test(color);
    }

    async function CreateRole() {
        const token = localStorage.getItem("token");

        const name_input = document.getElementById("create-role-name");
        const name = name_input.value;        

        const color_input = document.getElementById("create-role-color");
        const color = color_input.value.trim();

        if(!IsValidFullHex(color))return;

        const response = await FetchData(
            "add_role",
            "POST",
            {
                token: token,
                server_id: server_id,
                role_name: name,
                role_color: color
            }
        );

        if( typeof response != "number")return;

        roles.push({role_name: name, color: color, id: response, permissions: {}});
    }

    async function RemoveRole(role_id) {
        const token = localStorage.getItem("token");
        
        if(token === undefined || role_id === undefined) return;

        const response = await FetchData(
            "remove_role",
            "PATCH",
            {
                token: token,
                role_id: role_id
            }
        );

        if(response !== "success")return;

        roles = roles.filter(role => role.id !== role_id);
    }

    function EnableEditingRole(role) {
        editing.id = role.id;
        editing.name = role.role_name;
        editing.color = role.color;
        editing.state = true;
    }

    async function EditName() {
        const token = localStorage.getItem("token");

        const name_input = document.getElementById("edit-role-name");
        const name = name_input.value.trim();

        if(!name || name === editing.name)return;

        const name_result = await FetchData(
            "edit_role/name",
            "PUT",
            {
                token: token,
                role_id: role_id,
                new_val: name
            }
        );
        
        if( name_result !== "success") return;

        for(const role of roles) {
            if(role.id !== role_id)continue;

            role.role_name = name;
            break;
        }
    }

    async function EditColor() {
        const token = localStorage.getItem("token");

        const color_input = document.getElementById("edit-role-color");
        const color = color_input.value.trim();

        if(!IsValidFullHex(color) || color == editing.color)return;

        const color_result = await FetchData(
            "edit_role/color",
            "PUT",
            {
                token: token,
                role_id: role_id,
                new_val: color
            }
        );

        if( color_result !== "success") return;

        for(const role of roles) {
            if(role.id !== role_id)continue;

            role.color = color;
            break;
        }
    }

    async function EditPermissions() {
        let new_permissions = {};

        for(const key of permission_keys) {
            const input = document.getElementsByName(key)[0];
            const value = input.checked;

            new_permissions[key] = value;   
        }

        const permissions_result = await FetchData(
            "edit_role/permissions",
            "PUT",
            {
                token: token,
                role_id: role_id,
                new_permissions: new_permissions
            }
        );

        if( permissions_result !== "success") return;

        for(const role of roles) {
            if(role.id !== role_id)continue;

            role.permissions = new_permissions;
            break;
        }
    }

    async function HandleEditing(role_id) {
        EditName();
        EditColor();
        EditPermissions();
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

        const user_permissions = await FetchData(`permissions/${$profile.user_id}/${server_id}/`, "GET");
        if( !user_permissions["Manage roles"] || user_permissions["Admin"] )window.location.href(`/app/server/${server_id}`);
    });

    onDestroy(unsubscribe);

    onMount(async () => {
        roles = await FetchData(`roles_in_server/${server_id}/`, "GET");
    });
</script>

<div class="w-full h-screen flex flex-row">
  <aside class="w-64 h-full overflow-y-auto flex flex-col gap-2 ml-12">
    {#each roles as role}
      <div class="flex items-center justify-between bg-white/70 rounded-xl px-4 py-2 shadow m-2">
        <button onclick={() => EnableEditingRole(role)} class="text-purple-700 font-semibold hover:underline">{role.role_name}</button>
        <button onclick={() => HandleRemovingRole(role.id)} class="text-red-600 font-semibold hover:underline">Usuń</button>
      </div>
    {/each}
  </aside>
  <main class="flex-1 flex flex-col items-center w-full overflow-y-auto">
    <div class="w-full flex flex-col items-center pt-[8vh]" style="margin-right: 18rem;">
      <form class="flex flex-col gap-6 w-full max-w-md bg-white/80 rounded-2xl shadow-lg p-8 border border-pink-100 mx-auto">
        <input type="text" placeholder="Nazwa roli" id="create-role-name" class="px-4 py-2 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 transition" />
        <input type="text" placeholder="Kolor (np. #ff00ff)" id="create-role-color" class="px-4 py-2 rounded-xl border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-300 transition"/>
        <button type="button" onclick={CreateRole} class="bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold px-6 py-2 rounded-xl shadow hover:scale-105 hover:from-pink-400 hover:to-purple-400 transition-all">Dodaj rolę</button>
      </form>
      {#if editing.state}
        <div class="mt-8 w-full max-w-md mx-auto bg-white/90 rounded-xl shadow p-6 flex flex-col gap-4">
          <input type="text" placeholder="Nazwa" id="edit-role-name" value={editing.name} class="px-4 py-2 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 transition"/>
          <input type="text" placeholder="Kolor" id="edit-role-color" value={editing.color} class="px-4 py-2 rounded-xl border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-300 transition"/>
          <form name="editing-form" class="flex flex-col gap-2">
            {#each permission_keys as key}
              <label for={key} class="flex items-center gap-2">
                <input type="checkbox" checked={roles.find(r => r.id === editing.id)?.permissions[key]} name={key} class="accent-pink-500"/>
                <span>{key}</span>
              </label>
            {/each}
          </form>
          <button onclick={() => HandleEditing(editing.id)} class="bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold px-6 py-2 rounded-xl shadow hover:scale-105 hover:from-pink-400 hover:to-purple-400 transition-all">Zapisz</button>
        </div>
      {/if}
    </div>
  </main>
</div>