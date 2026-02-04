<script>
    import one_svg from '$lib/assets/message_box/1.svg';
    import two_svg from '$lib/assets/message_box/2.svg';
    import three_svg from '$lib/assets/message_box/3.svg';
	import { json } from '@sveltejs/kit';
    import { profile } from "../stores";
    let friends = $state([]);
    let friend_req = $state([]);
import { onMount } from 'svelte';
	import { messages } from './dm/store';
onMount(() => {
    const token = localStorage.getItem("token");
    fetch('http://localhost:8000/get_friends', {
        method: "POST",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({token: token})
    })
    .then(response => response.json())
    .then(data => {
        friends = data;
    })
    .catch(error => console.error(error));
    fetch('http://localhost:8000/get_friend_reqs', {
        method: "POST",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({token: token})
    })
    .then(response => response.json())
    .then(data => {
        friend_req = data;
    })
    .catch(error => console.error(error))
});

function add_friend(friend_tag){
    const token = localStorage.getItem("token");
    if(friend_tag == profile.name){
        alert("Oh hell nah");
        return;
    };
    fetch('http://localhost:8000/send_friend_req', {
        method: "POST",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({token:token, name:friend_tag})
    })
    .then(response => {
        isopen = !isopen
    })
}

function reject_friend_request(friend_tag){
    const token = localStorage.getItem("token");
    fetch('http://localhost:8000/reject_friend_req', {
        method: "PATCH",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({token:token, name:friend_tag})
    })
    .then(response => {

    })
}

function accept_friend_request(friend_tag){
    const token = localStorage.getItem("token");
    fetch('http://localhost:8000/accept_friend_req', {
        method: "PUT",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({token:token, name:friend_tag})
    })
    .then(response => {

    })
}
let isopen = $state(false);
let friend_tag = $state("");
</script>

<div class="flex w-screen h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <div class="flex flex-col w-[242px] bg-white/30 p-4 gap-4">
        <div class="font-semibold text-lg mb-2">Znajomi</div>
        <div class="flex flex-col gap-2">
            <!-- {#each privateMessages as msg}
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-black"></div>
                    <span class="text-sm">{msg.name}</span>
                </div>
            {/each} -->
        </div>
    </div>

    <main class="flex-1 flex flex-col px-8 py-6 gap-4">
        <div class="flex items-center gap-4 mb-4">
            <div class="font-semibold text-lg">Znajomi</div>
            <button class="px-4 py-1 rounded-xl bg-white/60 text-gray-700 font-semibold shadow">Wszystkie</button>
            <button class="px-4 py-1 rounded-xl bg-white/60 text-gray-700 font-semibold shadow">Online</button>
            <button onclick={() => isopen = !isopen} type="toggle" class="px-4 py-1 rounded-xl bg-blue-100 text-blue-700 font-semibold shadow">Dodaj znajomego</button>
            {#if isopen}
            <div class="flex items-center gap-2 bg-white/70">
                <input
                    type="text"
                    bind:value={friend_tag}
                    placeholder=""
                    class="px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-200 bg-white/90 text-gray-700 text-sm w-48"
                >
                <button
                    onclick={() => add_friend(friend_tag)}
                    class="px-4 py-2 rounded-lg bg-blue-100 text-blue-700 font-semibold shadow hover:bg-blue-200 transition"
                >
                    Zatwierdź
                </button>
            </div>
            {/if}
        </div>
        <div>
        {#if friend_req.length > 0}
            <div>Zaproszenia</div>
        {/if}
        {#each friend_req as fr}
            <div class="flex items-center justify-between bg-pink-100/80 hover:bg-pink-200 rounded-xl px-4 py-2 gap-3">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-pink-300"></div>
                    <div class="text-sm font-medium text-pink-700">{fr.name}</div>
                </div>
                <div class="flex gap-2">
                    <button onclick={() => accept_friend_request(fr.name)} class="px-3 py-1 rounded-md bg-pink-500 text-white text-sm hover:bg-pink-600">Akceptuj</button>
                    <button onclick={() => reject_friend_request(fr.name)} class="px-3 py-1 rounded-md bg-white text-pink-600 border border-pink-200 hover:bg-pink-50 text-sm">Odrzuć</button>
                </div>
            </div>
        {/each}
        </div>
        <div class="text-xs text-gray-500 mb-2">Znajomi — {friends.length}</div>
        <div class="flex flex-col gap-4">
            {#if friends.length === 0}
                    <span class="">Kitty nie ma jeszcze żadnych przyjaciół</span>
                    {:else}
                    {#each friends as friend}
                <div class="flex items-center bg-white/70 rounded-xl px-6 py-4 shadow gap-4">
                    <div class="w-10 h-10 rounded-full bg-black relative">
                        <span class="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"></span>
                    </div>
                    <div class="flex-1">
                        <div class="font-semibold text-base">{friend}</div>
                        <!-- <div class="text-xs text-gray-500">{friend.status}</div> -->
                    </div>
                    <div class="flex gap-2">
                        <button aria-label="Message" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center shadow">
                            <img src={one_svg} alt="message" class="w-4 h-4"/>
                        </button>
                        <button aria-label="Call" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center shadow">
                            <img src={two_svg} alt="call" class="w-4 h-4"/>
                        </button>
                        <button aria-label="Options" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center shadow">
                            <img src={three_svg} alt="options" class="w-4 h-4"/>
                        </button>
                    </div>
                </div>                
            {/each}
            {/if}
        </div>
    </main>

    <aside class="w-64 bg-white/20 p-4 flex flex-col gap-4">
        <div class="font-semibold text-lg mb-2">Aktywne teraz</div>
        <div class="flex flex-col gap-2">
            <!-- {#each activities as act}
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-black"></div>
                    <div>
                        <div class="text-sm font-semibold">{act.name}</div>
                        <div class="text-xs text-green-500">{act.game}</div>
                    </div>
                    <div class="ml-auto text-xs text-gray-400">{act.time}</div>
                </div>
            {/each} -->
        </div>
    </aside>
</div>