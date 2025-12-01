<script>
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
                            <svg width="14" height="13" viewBox="0 0 14 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M14.0001 5.6875C14.0001 8.8293 10.8665 11.375 7.00008 11.375C5.98563 11.375 5.02313 11.2 4.15359 10.8855C3.8282 11.1234 3.29773 11.4488 2.66883 11.7223C2.01258 12.0066 1.22234 12.25 0.437578 12.25C0.259844 12.25 0.10125 12.1434 0.032891 11.9793C-0.0354684 11.8152 0.00281283 11.6293 0.12586 11.5035L0.134063 11.4953C0.142266 11.4871 0.153203 11.4762 0.16961 11.457C0.199688 11.4242 0.246172 11.3723 0.303594 11.3012C0.415703 11.1645 0.566094 10.9621 0.719219 10.7105C0.992657 10.2566 1.25242 9.66055 1.30438 8.99062C0.484063 8.06094 7.84598e-05 6.9207 7.84598e-05 5.6875C7.84598e-05 2.5457 3.13367 0 7.00008 0C10.8665 0 14.0001 2.5457 14.0001 5.6875Z" fill="#8B5A7D"/>
                            </svg>
                        </button>
                        <button aria-label="Call" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center shadow">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M4.50898 0.67254C4.29844 0.163947 3.74336 -0.106757 3.21289 0.0381654L0.806641 0.694415C0.330859 0.825665 0 1.2577 0 1.74988C0 8.51473 5.48516 13.9999 12.25 13.9999C12.7422 13.9999 13.1742 13.669 13.3055 13.1932L13.9617 10.787C14.1066 10.2565 13.8359 9.70145 13.3273 9.4909L10.7023 8.39715C10.2566 8.21121 9.73984 8.33973 9.43633 8.71434L8.33164 10.0624C6.40664 9.15184 4.84805 7.59324 3.9375 5.66824L5.28555 4.56629C5.66016 4.26004 5.78867 3.74598 5.60273 3.30027L4.50898 0.675275V0.67254Z" fill="#8B5A7D"/>
                            </svg>
                        </button>
                        <button aria-label="Options" class="w-8 h-8 rounded-full bg-white/80 flex items-center justify-center shadow">
                            <svg width="4" height="12" viewBox="0 0 4 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M1.53125 8.75C1.12514 8.75 0.735658 8.91133 0.448493 9.19849C0.161328 9.48566 0 9.87514 0 10.2812C0 10.6874 0.161328 11.0768 0.448493 11.364C0.735658 11.6512 1.12514 11.8125 1.53125 11.8125C1.93736 11.8125 2.32684 11.6512 2.61401 11.364C2.90117 11.0768 3.0625 10.6874 3.0625 10.2812C3.0625 9.87514 2.90117 9.48566 2.61401 9.19849C2.32684 8.91133 1.93736 8.75 1.53125 8.75ZM1.53125 4.375C1.12514 4.375 0.735658 4.53633 0.448493 4.82349C0.161328 5.11066 0 5.50014 0 5.90625C0 6.31236 0.161328 6.70184 0.448493 6.98901C0.735658 7.27617 1.12514 7.4375 1.53125 7.4375C1.93736 7.4375 2.32684 7.27617 2.61401 6.98901C2.90117 6.70184 3.0625 6.31236 3.0625 5.90625C3.0625 5.50014 2.90117 5.11066 2.61401 4.82349C2.32684 4.53633 1.93736 4.375 1.53125 4.375ZM3.0625 1.53125C3.0625 1.12514 2.90117 0.735658 2.61401 0.448493C2.32684 0.161328 1.93736 0 1.53125 0C1.12514 0 0.735658 0.161328 0.448493 0.448493C0.161328 0.735658 0 1.12514 0 1.53125C0 1.93736 0.161328 2.32684 0.448493 2.61401C0.735658 2.90117 1.12514 3.0625 1.53125 3.0625C1.93736 3.0625 2.32684 2.90117 2.61401 2.61401C2.90117 2.32684 3.0625 1.93736 3.0625 1.53125Z" fill="#8B5A7D"/>
                            </svg>
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