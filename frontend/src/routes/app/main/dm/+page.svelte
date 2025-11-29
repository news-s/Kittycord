<script>
    import { onMount, onDestroy } from "svelte";
    import { get } from "svelte/store";
    import { socket, connectedUserId, wsReady } from "$lib/stores/socket.js";
    import { friends, messages, activeDM } from "./store.js";

    let inputText = "";
    let loadingFriends = true;
    let ws = null;
    let unsubscribeSocket = null;
    let unsubscribeReady = null;

    // Wczytaj listę znajomych
    async function loadFriends() {
        const userId = get(connectedUserId);
        if (!userId) return;

        try {
            const res = await fetch(`/friends/list/${userId}`);
            if (!res.ok) throw new Error(res.statusText);
            const json = await res.json();
            friends.set(json);
        } catch (e) {
            console.error("Failed to load friends:", e);
            friends.set([]);
        } finally {
            loadingFriends = false;
        }
    }

    // Otwórz DM z wybranym znajomym
    function openDM(friendId) {
        const s = get(socket);
        if (!s || s.readyState !== WebSocket.OPEN) return;

        activeDM.set(friendId);
        messages.set([]); // wyczyść poprzednie wiadomości
        s.send(JSON.stringify({ type: "load_dms", content: friendId }));
    }

    // Wyślij wiadomość
    function sendDM() {
        const s = get(socket);
        const target = get(activeDM);
        if (!s || s.readyState !== WebSocket.OPEN) return;
        if (!target || !inputText.trim()) return;

        s.send(JSON.stringify({
            type: "dm",
            content: inputText,
            target_id: target
        }));

        inputText = "";
    }

    // Obsługa wiadomości z serwera
    function handleServerRaw(ev) {
        let data;
        try { data = JSON.parse(ev.data); } 
        catch { return console.warn("Non-JSON WS message"); }

        if (data.status && data.status >= 400) {
            console.warn("Server error:", data.detail ?? data);
            return;
        }

        if (data.type === "load_dms" && Array.isArray(data.messages)) {
            messages.set(data.messages);
        }

        if (data.type === "new_dm") {
            const target = get(activeDM);
            const userId = get(connectedUserId);

            if (target === data.reciever_id || target === data.author_id) {
                messages.update(arr => [...arr, data]);
            }
        }
    }

    // Inicjalizacja
    onMount(() => {
        unsubscribeSocket = socket.subscribe(s => {
            if (ws && ws !== s) ws.removeEventListener("message", handleServerRaw);
            ws = s;
            if (ws) ws.addEventListener("message", handleServerRaw);
        });

        unsubscribeReady = wsReady.subscribe(async ready => {
            if (ready) await loadFriends();
        });
    });

    onDestroy(() => {
        if (ws) ws.removeEventListener("message", handleServerRaw);
        unsubscribeSocket?.();
        unsubscribeReady?.();
    });

    function getFriendName(id) {
        const arr = get(friends);
        const found = arr.find(x => x.id === id);
        return found ? found.username : `#${id}`;
    }
//ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    async function addFriend(friendId) {
    const token = localStorage.getItem("token"); // albo gdzie trzymasz token
    if (!token) return alert("Not logged in");

    try {
        const res = await fetch("/friends/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token, friend_id: friendId })
        });

        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();

        // odśwież listę znajomych
        await loadFriends();

        alert("Friend added!");
    } catch (err) {
        console.error(err);
        alert("Failed to add friend");
    }
}

let newFriendId = "";

//ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

</script>

<!-- Dodawanie znajomego (tymczasowe UI) -->
<div style="margin-bottom:12px;">
    <input bind:value={newFriendId} placeholder="Friend ID" style="width:120px; padding:4px;" />
    <button on:click={() => addFriend(Number(newFriendId))} style="padding:4px 8px;">Add Friend</button>
</div>
<!-- Dodawanie znajomego (tymczasowe UI) -->



<div class="dm-layout" style="display:flex; height:100vh;">
    <aside style="width:220px; background:#f3f3f3; padding:10px; box-sizing:border-box;">
        <h3>Friends</h3>
        {#if loadingFriends}
            <div>Loading...</div>
        {:else}
            {#each $friends as f}
                <button
                    on:click={() => openDM(f.id)}
                    class:selected={f.id === $activeDM}
                    style="display:block; width:100%; text-align:left; padding:8px; margin-bottom:6px;"
                >
                    {f.username}
                </button>
            {/each}
            {#if $friends.length === 0}
                <div>No friends</div>
            {/if}
        {/if}
    </aside>

    <main style="flex:1; display:flex; flex-direction:column;">
        {#if $activeDM === null}
            <div style="padding:20px;">Wybierz znajomego, żeby rozpocząć DM.</div>
        {:else}
            <div style="padding:12px; border-bottom:1px solid #ddd;">
                <strong>Chat z: </strong>{getFriendName($activeDM)}
            </div>

            <div class="messages" style="flex:1; overflow:auto; padding:12px;">
                {#each $messages as m}
                    <div style="margin-bottom:10px;">
                        <small style="color:#666">{m.date}</small><br/>
                        <strong>{m.author_id === $connectedUserId ? "You" : getFriendName(m.author_id)}</strong>: {m.content}
                    </div>
                {/each}
            </div>

            <div style="padding:12px; border-top:1px solid #ddd; display:flex; gap:8px;">
                <input
                    bind:value={inputText}
                    on:keydown={(e) => e.key === "Enter" && sendDM()}
                    placeholder="Napisz wiadomość..."
                    style="flex:1; padding:8px;"
                />
                <button on:click={sendDM} style="padding:8px 12px;">Send</button>
            </div>
        {/if}
    </main>
</div>

<style>
    button.selected {
        background:#cfcfcf;
    }
</style>
