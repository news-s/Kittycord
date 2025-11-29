<script>
	import { onDestroy } from "svelte";
    import { load_server_bar, profile } from "../../../stores";
    import { page } from "$app/stores";

    const server_id = $page.params.id;
    const { children } = $props();

    load_server_bar.set(false);

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

<div>
    <nav>
        <a href="general">General</a>
        {#if user_permissions?.["Manage roles"]}
            <a href="roles">Roles</a>
        {/if}
        <a href="/app/server/{server_id}">Exit</a>
    </nav>
    {@render children()}
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;

        width: 100%;
    }

    nav {
        width: 20%;

        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
</style>