<script>
	import { onMount } from "svelte";
    import { socket } from "../routes/app/stores";

    let { messages } = $props();

    async function SendMessage(event) {
        event.preventDefault();

        if($socket?.readyState !== WebSocket.OPEN)return;

        const input = document.querySelector('.text-input');
        const message = input.value.trim();
        input.value = ""; 

        if(!message) return;

        $socket.send(JSON.stringify({
            type: "message",
            content: message
        }));
    }
</script>

<div class="flex-1 flex flex-col" style="background: linear-gradient(180deg, #FDF4FF 0%, #EDE9FE 100%);">
    <div class="h-14 px-4 flex items-center justify-between border-b border-purple-200/50">
        <div class="flex items-center gap-2">
            <span class="text-purple-500 font-semibold">#</span>
            <span class="font-semibold text-gray-800">chanel-name</span>
        </div>
        <div class="flex items-center gap-2">
            <button aria-label="Notifications" class="p-2 hover:bg-white/50 rounded">
                <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
                </svg>
            </button>
            <button aria-label="Search" class="p-2 hover:bg-white/50 rounded">
                <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                </svg>
            </button>
        </div>
    </div>

    <div class="flex-1 overflow-y-auto px-6 py-4">
        {#each messages as message}
            <div class="flex gap-4 mb-6 hover:bg-white/30 px-3 py-2 rounded">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex-shrink-0"></div>
                <div class="flex-1">
                    <div class="flex items-baseline gap-2 mb-1">
                        <span class="font-semibold text-gray-800 text-base">User {message.author_id}</span>
                        <span class="text-xs text-gray-500">{message.date}</span>
                    </div>
                    <p class="text-gray-700 text-base leading-relaxed">{message.content}</p>
                </div>
            </div>
        {/each}
    </div>

    <div class="flex justify-center items-center w-full px-6 py-6 border-t border-pink-300/50 bg-white/50">
        <form onsubmit={SendMessage} class="relative w-full">
            <input 
                type="text" 
                placeholder="Message #cute-cats" 
                class="w-full px-5 py-4 pr-36 rounded-3xl bg-white/80 border border-purple-200/50 text-gray-800 text-base placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent text-input"
            />
            <div class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                <button type="button" aria-label="Add emoji" class="p-2.5 rounded-full border-0 border-[#E5E7EB]" style="background: linear-gradient(90deg, #FBCFE8 0%, #E9D5FF 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M7 14C8.85652 14 10.637 13.2625 11.9497 11.9497C13.2625 10.637 14 8.85652 14 7C14 5.14348 13.2625 3.36301 11.9497 2.05025C10.637 0.737498 8.85652 0 7 0C5.14348 0 3.36301 0.737498 2.05025 2.05025C0.737498 3.36301 0 5.14348 0 7C0 8.85652 0.737498 10.637 2.05025 11.9497C3.36301 13.2625 5.14348 14 7 14ZM4.48711 8.90039C4.97656 9.46641 5.81328 10.0625 7 10.0625C8.18672 10.0625 9.02344 9.46641 9.51289 8.90039C9.67148 8.71719 9.94766 8.69805 10.1309 8.85664C10.3141 9.01523 10.3332 9.29141 10.1746 9.47461C9.56484 10.1746 8.50664 10.9375 7 10.9375C5.49336 10.9375 4.43516 10.1746 3.82539 9.47461C3.6668 9.29141 3.68594 9.01523 3.86914 8.85664C4.05234 8.69805 4.32852 8.71719 4.48711 8.90039ZM3.94844 5.6875C3.94844 5.45544 4.04062 5.23288 4.20472 5.06878C4.36881 4.90469 4.59137 4.8125 4.82344 4.8125C5.0555 4.8125 5.27806 4.90469 5.44216 5.06878C5.60625 5.23288 5.69844 5.45544 5.69844 5.6875C5.69844 5.91956 5.60625 6.14212 5.44216 6.30622C5.27806 6.47031 5.0555 6.5625 4.82344 6.5625C4.59137 6.5625 4.36881 6.47031 4.20472 6.30622C4.04062 6.14212 3.94844 5.91956 3.94844 5.6875ZM9.19844 4.8125C9.4305 4.8125 9.65306 4.90469 9.81716 5.06878C9.98125 5.23288 10.0734 5.45544 10.0734 5.6875C10.0734 5.91956 9.98125 6.14212 9.81716 6.30622C9.65306 6.47031 9.4305 6.5625 9.19844 6.5625C8.96637 6.5625 8.74381 6.47031 8.57972 6.30622C8.41562 6.14212 8.32344 5.91956 8.32344 5.6875C8.32344 5.45544 8.41562 5.23288 8.57972 5.06878C8.74381 4.90469 8.96637 4.8125 9.19844 4.8125Z" fill="#9333EA"/>
                    </svg>
                </button>
                <button type="button" aria-label="Attach file" class="p-2.5 rounded-full border-0 border-[#E5E7EB]" style="background: linear-gradient(90deg, #FBCFE8 0%, #E9D5FF 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="14" viewBox="0 0 13 14" fill="none">
                        <path d="M9.84375 2.03232C9.17656 1.36514 8.09375 1.36514 7.42656 2.03232L2.39531 7.06357C1.24414 8.21475 1.24414 10.0796 2.39531 11.2308C3.54648 12.3819 5.41133 12.3819 6.5625 11.2308L10.7188 7.07451C11.0168 6.77646 11.5035 6.77646 11.8016 7.07451C12.0996 7.37256 12.0996 7.85928 11.8016 8.15732L7.64531 12.3136C5.89531 14.0636 3.0625 14.0636 1.3125 12.3136C-0.4375 10.5636 -0.4375 7.73076 1.3125 5.98076L6.34375 0.949512C7.60977 -0.316504 9.66055 -0.316504 10.9266 0.949512C12.1926 2.21553 12.1926 4.26631 10.9266 5.53232L6.11406 10.3448C5.33203 11.1269 4.06328 11.1269 3.28125 10.3448C2.49922 9.56279 2.49922 8.29404 3.28125 7.51201L7.21875 3.57451C7.5168 3.27646 8.00352 3.27646 8.30156 3.57451C8.59961 3.87256 8.59961 4.35928 8.30156 4.65732L4.36406 8.59482C4.18086 8.77803 4.18086 9.07881 4.36406 9.26201C4.54727 9.44522 4.84805 9.44522 5.03125 9.26201L9.84375 4.44951C10.5109 3.78232 10.5109 2.69951 9.84375 2.03232Z" fill="#2563EB"/>
                    </svg>
                </button>
                <button type="submit" aria-label="Send message" class="p-2.5 rounded-full border-0 border-[#E5E7EB]" style="background: linear-gradient(90deg, #FBCFE8 0%, #E9D5FF 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M13.6197 0.15323C13.8959 0.344636 14.0408 0.675495 13.9889 1.00635L12.2389 12.3814C12.1978 12.6466 12.0365 12.879 11.8014 13.0103C11.5662 13.1415 11.2846 13.1579 11.0357 13.054L7.76542 11.695L5.89237 13.7212C5.64902 13.9864 5.2662 14.0739 4.92987 13.9427C4.59355 13.8114 4.3748 13.486 4.3748 13.1251V10.8392C4.3748 10.7298 4.41581 10.6259 4.48964 10.5466L9.07245 5.54542C9.23105 5.37315 9.22558 5.10792 9.06151 4.94385C8.89745 4.77979 8.63222 4.76886 8.45995 4.92471L2.89823 9.86573L0.483781 8.65714C0.193937 8.51221 0.00799964 8.22237 -0.000203481 7.89971C-0.00840661 7.57706 0.161125 7.27628 0.440031 7.11495L12.69 0.114948C12.9826 -0.0518486 13.3435 -0.0354423 13.6197 0.15323Z" fill="#9333EA"/>
                    </svg>
                </button>
            </div>
        </form>
    </div>
</div>