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
        <div class="flex items-center gap-2 font-semibold text-lg mb-2">
            <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 4C3 2.93913 3.42143 1.92172 4.17157 1.17157C4.92172 0.421427 5.93913 0 7 0C8.06087 0 9.07828 0.421427 9.82843 1.17157C10.5786 1.92172 11 2.93913 11 4C11 5.06087 10.5786 6.07828 9.82843 6.82843C9.07828 7.57857 8.06087 8 7 8C5.93913 8 4.92172 7.57857 4.17157 6.82843C3.42143 6.07828 3 5.06087 3 4ZM0 15.0719C0 11.9937 2.49375 9.5 5.57188 9.5H8.42813C11.5063 9.5 14 11.9937 14 15.0719C14 15.5844 13.5844 16 13.0719 16H0.928125C0.415625 16 0 15.5844 0 15.0719ZM19.0406 16H14.7312C14.9 15.7063 15 15.3656 15 15V14.75C15 12.8531 14.1531 11.15 12.8188 10.0063C12.8938 10.0031 12.9656 10 13.0406 10H14.9594C17.7437 10 20 12.2562 20 15.0406C20 15.5719 19.5688 16 19.0406 16ZM13.5 8C12.5312 8 11.6562 7.60625 11.0219 6.97188C11.6375 6.14062 12 5.1125 12 4C12 3.1625 11.7938 2.37188 11.4281 1.67813C12.0094 1.25312 12.725 1 13.5 1C15.4344 1 17 2.56562 17 4.5C17 6.43437 15.4344 8 13.5 8Z" fill="#8B5A7D"/>
            </svg>
            Znajomi
        </div>
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
            <div class="flex items-center gap-2 font-semibold text-lg">
                <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 4C3 2.93913 3.42143 1.92172 4.17157 1.17157C4.92172 0.421427 5.93913 0 7 0C8.06087 0 9.07828 0.421427 9.82843 1.17157C10.5786 1.92172 11 2.93913 11 4C11 5.06087 10.5786 6.07828 9.82843 6.82843C9.07828 7.57857 8.06087 8 7 8C5.93913 8 4.92172 7.57857 4.17157 6.82843C3.42143 6.07828 3 5.06087 3 4ZM0 15.0719C0 11.9937 2.49375 9.5 5.57188 9.5H8.42813C11.5063 9.5 14 11.9937 14 15.0719C14 15.5844 13.5844 16 13.0719 16H0.928125C0.415625 16 0 15.5844 0 15.0719ZM19.0406 16H14.7312C14.9 15.7063 15 15.3656 15 15V14.75C15 12.8531 14.1531 11.15 12.8188 10.0063C12.8938 10.0031 12.9656 10 13.0406 10H14.9594C17.7437 10 20 12.2562 20 15.0406C20 15.5719 19.5688 16 19.0406 16ZM13.5 8C12.5312 8 11.6562 7.60625 11.0219 6.97188C11.6375 6.14062 12 5.1125 12 4C12 3.1625 11.7938 2.37188 11.4281 1.67813C12.0094 1.25312 12.725 1 13.5 1C15.4344 1 17 2.56562 17 4.5C17 6.43437 15.4344 8 13.5 8Z" fill="#8B5A7D"/>
                </svg>
                Znajomi
            </div>
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
            <div class="text-xs font-semibold text-gray-600 mb-2 uppercase tracking-wide">Oczekujące — {friend_req.length}</div>
        {/if}
        <div class="flex flex-col gap-1">
        {#each friend_req as fr}
            <div class="flex items-center justify-between bg-white hover:bg-gray-50 rounded-lg px-4 py-3 transition-colors duration-150 border-b border-gray-100">
                <div class="flex items-center gap-3 flex-1">
                    <div class="relative">
                        <div class="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center">
                        </div>
                        <span class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 rounded-full border-2 border-white"></span>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-900 text-sm">{fr.name}</div>
                    </div>
                </div>
                <div class="flex gap-2 items-center">
                    <button 
                        onclick={() => accept_friend_request(fr.name)} 
                        class="w-9 h-9 rounded-full bg-gray-100 hover:bg-green-500 flex items-center justify-center transition-all duration-200 group"
                        aria-label="Akceptuj"
                    >
                        <svg class="w-5 h-5 text-gray-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                        </svg>
                    </button>
                    <button 
                        onclick={() => reject_friend_request(fr.name)} 
                        class="w-9 h-9 rounded-full bg-gray-100 hover:bg-red-500 flex items-center justify-center transition-all duration-200 group"
                        aria-label="Odrzuć"
                    >
                        <svg class="w-5 h-5 text-gray-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>
        {/each}
        </div>
        </div>
        <div class="text-xs text-gray-500 mb-2">Znajomi — {friends.length}</div>
        <div class="flex flex-col gap-4 flex-1">
            {#if friends.length === 0}
                <div class="flex flex-col items-center justify-center h-full py-16 px-8 text-center">
                    <div class="mb-4">
                        <svg class="w-24 h-24 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-700 mb-2">Kitty nie ma jeszcze żadnych przyjaciół</h3>
                    <p class="text-sm text-gray-500 max-w-md">
                        Wygląda na to, że lista znajomych jest pusta. Dodaj kogoś, aby rozpocząć rozmowy!
                    </p>
                </div>
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