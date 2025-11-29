<script>    
    import { profile } from "../../../../stores";
    import { page } from "$app/stores";
	import { onDestroy } from "svelte";

    const server_id = $page.params.id;

    let server_name = "";
    let updated_server_name = $state(server_name);

    let server_link = "";
    let updated_server_link = $state(server_link);

    let user_permissions = $state(null);

    async function EditServerName() {
        updated_server_name = updated_server_name.trim();
        if(server_name === updated_server_name || !updated_server_name)return;

        const token = localStorage.getItem("token");
        server_name = updated_server_name

        try {
            const res = await fetch("http://localhost:8000/edit_server/name", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id,
                    new_val: server_name
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function EditServerLink() {
        updated_server_link = updated_server_link.trim();
        if(server_link === updated_server_link || !updated_server_link)return;
        
        const token = localStorage.getItem("token");
        server_link = updated_server_link;

        try {
            const res = await fetch("http://localhost:8000/edit_server/link", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id,
                    new_link: server_link
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    function UpdateServer() {
        EditServerName();
        EditServerLink();
    }

    async function DeleteServer() {
        const token = localStorage.getItem("token");

        try {
            const res = await fetch("http://localhost:8000/remove_server", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

        } catch (err) {
            console.error("Fetch error:", err);
        }

        window.location.href = "/app/main";
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
</script>
<div class="options-wrapper">
    <form>
        <input type="text" bind:value={updated_server_name} placeholder="Name" />
        <input type="text" bind:value={updated_server_link} placeholder="Link"/>
        {#if user_permissions?.["Manage server"]}
            <input type="submit" onclick={UpdateServer} value="Update"/>
        {/if}
    </form>

    {#if user_permissions?.["Manage server"]}
        <button onclick={DeleteServer}>Delete</button>
    {/if}
</div>

<style>
    .options-wrapper {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        gap: 50px;
        
        align-items: center;

        overflow-y: scroll; 
    }

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
</style>