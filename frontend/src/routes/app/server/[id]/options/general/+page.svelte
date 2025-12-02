<script>    
    import { profile } from "../../../../stores";
    import { page } from "$app/stores";
	import { onDestroy, onMount } from "svelte";
    import { FetchData } from "$lib/Fetch";

    const server_id = $page.params.id;

    let server_name = "";
    let updated_server_name = $state(server_name);

    let server_link = "";
    let updated_server_link = $state(server_link);

    let user_permissions = $state(null);

    let success_message = $state("");
    let error_message = $state("");

    async function EditServerName() {
        updated_server_name = updated_server_name.trim();
        if(server_name === updated_server_name)return;

        const token = localStorage.getItem("token");
        server_name = updated_server_name

        if(server_name.length > 30) {
            error_message = "Server name is too long! ";
            return;
        }

        const result = await FetchData(
            "edit_server/name", 
            "PUT",
            {
                token: token,
                server_id: server_id,
                new_val: server_name
            }
        );

        success_message += "Zaktualizowano Nazwe";
    }

    async function EditServerLink() {
        updated_server_link = updated_server_link.trim();
        if(server_link === updated_server_link || !updated_server_link)return;
        
        const token = localStorage.getItem("token");
        server_link = updated_server_link;

        if(server_link.length > 20) {
            error_message += "Server link is too long! ";
            return;
        }

        const result = await FetchData(
            "edit_server/link", 
            "PUT",
            {
                token: token,
                server_id: server_id,
                new_val: server_link
            }
        );

        if(result.status && result.status != 200) {
            error_message = await result.json();
            error_message = error_message.detail;
            return;
        }
        if(result == "invalid input") {
            error_message = result;
            return;
        }

        if(success_message === "") {
            success_message += "Zaktualzowano Link"; 
            return;
        }
        success_message = " i Link"
    }

    function UpdateServer() {
        success_message = "";
        error_message = "";

        EditServerName();
        EditServerLink();
    }

    async function DeleteServer() {
        const token = localStorage.getItem("token");

        const result = await FetchData(
            "remove_server", 
            "PATCH",
            {
                token: token,
                server_id: server_id,
            }
        );

        window.location.href = "/app/main";
    }

    
    async function LeaveServer() {
        const token = localStorage.getItem("token");
        
        const result = await FetchData(
            "leave",
            "PUT",
            {
                token: token,
                server_id: server_id
            }
        );
        
        window.location.href = "/app/main";
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
        
        user_permissions = await FetchData(`permissions/${$profile.user_id}/${server_id}/`, "GET");
    });
    onDestroy(unsubscribe);


    onMount(async () => {
        const data = await FetchData(`server_name/${server_id}/`, "GET");
        
        server_name = data.server_name
        updated_server_name = data.server_name
        
        server_link = data.server_link
        updated_server_link = data.server_link
    });
</script>

<div class="flex flex-col items-center justify-center min-h-[80vh] w-full">
    <p class="text-green-600">{success_message}</p>
    <p class="text-red-600">{error_message}</p>
    <form class="flex flex-col gap-6 w-full max-w-md bg-white/80 rounded-2xl shadow-lg p-8 border border-pink-100 mx-auto">
        <input disabled={!user_permissions?.["Manage server"] || !user_permissions?.["Admin"]} type="text" bind:value={updated_server_name} placeholder="Nazwa serwera" class="px-4 py-2 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 transition" />
        <input disabled={!user_permissions?.["Manage server"] || !user_permissions?.["Admin"]} type="text" bind:value={updated_server_link} placeholder="Link do serwera" class="px-4 py-2 rounded-xl border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-300 transition"/>
        {#if user_permissions?.["Manage server"] || user_permissions?.["Admin"]}
            <button type="button" onclick={UpdateServer} class="bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold px-6 py-2 rounded-xl shadow hover:scale-105 hover:from-pink-400 hover:to-purple-400 transition-all">Aktualizuj</button>
        {/if}
    </form>
    {#if user_permissions?.["Manage server"] || user_permissions?.["Admin"]}
        <button onclick={DeleteServer} class="mt-8 bg-gradient-to-r from-red-200 to-pink-200 text-red-700 font-semibold px-6 py-2 rounded-xl shadow hover:scale-105 hover:from-red-300 hover:to-pink-300 transition-all">Usuń serwer</button>
    {/if}

    <button onclick={LeaveServer} class="mt-8 bg-gradient-to-r from-red-200 to-pink-200 text-red-700 font-semibold px-6 py-2 rounded-xl shadow hover:scale-105 hover:from-red-300 hover:to-pink-300 transition-all">Opuść serwer</button>
</div>
