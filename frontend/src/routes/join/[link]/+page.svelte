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

    let status = $state(null);

    async function HandleJoiningServer() {
        const result = await JoinServer();

        status = result;
    }

    onMount(() => {
        HandleJoiningServer();
    });
</script>


{#if status == "success"}
    <div class="fixed inset-0 flex flex-col items-center justify-center bg-gradient-to-br from-pink-50 to-purple-50 z-10">
        <h1 class="text-2xl font-bold text-purple-800 mb-4">Dziękujemy za dołączenie!</h1>
        <a href="/app/main" class="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold shadow hover:scale-105 transition-all">Otwórz Kittycord</a>
    </div>
{:else if status == "404"}
    <div class="fixed inset-0 flex flex-col items-center justify-center bg-gradient-to-br from-red-50 to-pink-100 z-10">
        <h1 class="text-2xl font-bold text-red-700 mb-4">Nie znaleziono serwera</h1>
        <a href="/app/main" class="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold shadow hover:scale-105 transition-all">Otwórz Kittycord</a>
    </div>
{:else if status == "500"}
    <div class="fixed inset-0 flex flex-col items-center justify-center bg-gradient-to-br from-yellow-50 to-pink-100 z-10">
        <h1 class="text-2xl font-bold text-yellow-700 mb-4">Już jesteś na tym serwerze</h1>
        <a href="/app/main" class="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-300 to-purple-300 text-purple-900 font-semibold shadow hover:scale-105 transition-all">Otwórz Kittycord</a>
    </div>
{/if}