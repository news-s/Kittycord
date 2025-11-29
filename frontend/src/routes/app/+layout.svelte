<script>
    import { onMount } from "svelte";
    import { socket, profile, load_layout } from "./stores.js";
    import ServersNavbar from "$lib/ServersNavbar.svelte";
	import Profile from "$lib/Profile.svelte";

    let {children} = $props();

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

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    // onMount(() => {
    //     let token = localStorage.getItem('token');
    //     if (token === undefined) window.location.href = '/login';

    //     console.log('Token:', token);

    //     let ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    //     socket.set(ws);

    //     ws.addEventListener("error", (err) => {
    //         if (ws.readyState === WebSocket.CLOSED) {
    //             console.error("Failed to connect to WebSocket server.");
    //             window.location.href = '/login';
    //         } else {
    //             console.error("WebSocket error:", err);
    //         }
    //     });

    //     ws.addEventListener('message', async (event) => {
    //         const data = JSON.parse(event.data);
    //         console.log('Message from server:', data);

    //         if(data.user_id === undefined || data.user_id === null) return;

    //         const profile_data = await GetProfile(data.user_id);
    //         profile.set(profile_data);
    //     });
    // });
</script>

<div class="flex w-screen max-w-screen h-screen overflow-hidden relative">
    {#if $load_layout}
        <ServersNavbar />
        <Profile />
    {/if}
    {@render children()}
</div>