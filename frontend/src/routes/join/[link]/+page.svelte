<script>
	import { onMount } from "svelte";
    import { page } from "$app/stores";
	import { error } from "@sveltejs/kit";
	import Error from "../../+error.svelte";
    
    const link = $page.params.link;

    async function JoinServer() {
        const token = localStorage.getItem("token");
        if(token === undefined)return;

        try {
            const res = await fetch(`http://localhost:8000/join`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    link: link
                })
            });

            if (!res.ok) {
                return res.status;
            }

            return await res.json();
        }catch(err) {
            console.error("Fetch error:", err);
        }
    }

    let status = $state(null)

    async function HandleJoiningServer() {
        const result = await JoinServer();

        status = result;
    }

    onMount(() => {
        HandleJoiningServer();
    });
</script>

{#if status == "success"}
    <div>
        <h1>Thanks for joining</h1>
        <a href="/app/main">Open Kittycord</a>
    </div>
{:else if status == "404"}
    <div>
        <h1>Server not found</h1>
        <a href="/app/main">Open Kittycord</a>
    </div>
{:else if status == "500"}
    <div>
        <h1>You already are on the server</h1>
        <a href="/app/main">Open Kittycord</a>
    </div>
{/if}