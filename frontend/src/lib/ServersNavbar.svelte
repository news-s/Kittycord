<script>
	import { onDestroy } from "svelte";
	import { profile } from "../routes/app/stores";
    import { FetchData } from "./Fetch";

    let open = $state(false);
    let servers = $state([]);
    let error_message = $state("");

    async function CreateServer() {
        error_message = "";

        const token = localStorage.getItem('token');
        const name_input = document.getElementById('server-name');
        const server_name = name_input.value.trim();

        const link_input = document.getElementById('server-link');
        const server_link = link_input.value.trim();

        const result = await FetchData(
            "add_server",
            "POST",
            {
                token: token,
                server_name: server_name,
                invite_link: server_link
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
        
        open = false;

        if($profile === null)return;
        profile.update(object => ({...object, servers: [...object.servers, result.server_id]}));

    }
</script>

<nav class="flex flex-col items-center gap-2 py-3 h-screen w-[72px] bg-white/60 border-r border-[#fbcfe8]/50">
    <a href="/app/main" title="dms" class="flex items-center justify-center w-12 h-12 rounded-full border-0 border-[#E5E7EB] shadow-[0_4px_6px_0_rgba(0,0,0,0.10),0_10px_15px_0_rgba(0,0,0,0.10)] hover:rounded-xl transition-all duration-200" style="background: linear-gradient(45deg, #FCE7F3 50%, #F3E8FF 120.71%);">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M11.2481 7.5H11.9161C12.7793 8.99609 14.3965 10 16.2481 10C16.6778 10 17.0997 9.94531 17.4981 9.84375V10V11.25V18.75C17.4981 19.4414 16.9395 20 16.2481 20C15.5567 20 14.9981 19.4414 14.9981 18.75V13.25L9.68559 17.5H11.8731C12.5645 17.5 13.1231 18.0586 13.1231 18.75C13.1231 19.4414 12.5645 20 11.8731 20H6.24809C4.17778 20 2.49809 18.3203 2.49809 16.25V7.51953C2.49809 6.89062 2.02934 6.35547 1.40434 6.27734L1.09575 6.23828C0.412155 6.15234 -0.0761265 5.52734 0.009811 4.84375C0.0957485 4.16016 0.720749 3.67187 1.40434 3.75781L1.71294 3.79688C3.58794 4.03125 4.99809 5.625 4.99809 7.51953V10.8516C6.34184 8.83203 8.63872 7.5 11.2481 7.5ZM17.4981 8.53516C17.1075 8.67188 16.6856 8.75 16.2481 8.75C15.1387 8.75 14.1387 8.26562 13.4512 7.5C13.3067 7.33984 13.1778 7.16797 13.0645 6.98438C12.7051 6.40625 12.4981 5.72656 12.4981 5V1.25V0.46875V0.417969C12.4981 0.1875 12.6817 0.00390625 12.9122 0H12.92C13.0489 0 13.17 0.0625 13.2481 0.164062V0.167969L13.7481 0.832031L14.8106 2.25L14.9981 2.5H17.4981L17.6856 2.25L18.7481 0.832031L19.2481 0.167969V0.164062C19.3262 0.0625 19.4473 0 19.5762 0H19.584C19.8145 0.00390625 19.9981 0.1875 19.9981 0.417969V0.46875V1.25V5C19.9981 5.67578 19.8184 6.3125 19.5059 6.85938C19.0645 7.63281 18.3497 8.23438 17.4981 8.53516ZM15.6231 5C15.6231 4.83424 15.5572 4.67527 15.44 4.55806C15.3228 4.44085 15.1639 4.375 14.9981 4.375C14.8323 4.375 14.6734 4.44085 14.5562 4.55806C14.4389 4.67527 14.3731 4.83424 14.3731 5C14.3731 5.16576 14.4389 5.32473 14.5562 5.44194C14.6734 5.55915 14.8323 5.625 14.9981 5.625C15.1639 5.625 15.3228 5.55915 15.44 5.44194C15.5572 5.32473 15.6231 5.16576 15.6231 5ZM17.4981 5.625C17.6639 5.625 17.8228 5.55915 17.94 5.44194C18.0572 5.32473 18.1231 5.16576 18.1231 5C18.1231 4.83424 18.0572 4.67527 17.94 4.55806C17.8228 4.44085 17.6639 4.375 17.4981 4.375C17.3323 4.375 17.1734 4.44085 17.0562 4.55806C16.9389 4.67527 16.8731 4.83424 16.8731 5C16.8731 5.16576 16.9389 5.32473 17.0562 5.44194C17.1734 5.55915 17.3323 5.625 17.4981 5.625Z" fill="#9333EA"/>
        </svg>
    </a>
    <div class="w-8 h-[2px] bg-pink-300/50 rounded-full"></div>

    {#each $profile?.servers as id}
        <a href={"/app/server/" + id} title={id} class="flex items-center justify-center w-12 h-12 rounded-full hover:rounded-xl transition-all duration-200" style="background: linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%);">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
        </a>
    {/each}

    <button onclick={() => open = !open} aria-label="Create Server" class="flex items-center justify-center w-12 h-12 rounded-full border-2 border-dashed border-[#D8B4FE] shadow-[0_4px_6px_0_rgba(0,0,0,0.10),0_10px_15px_0_rgba(0,0,0,0.10)] hover:rounded-xl transition-all duration-200 text-purple-600 text-2xl font-light" style="background: linear-gradient(135deg, #E9D5FF 0%, #BFDBFE 70.71%);">
        <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8.4375 1.125C8.4375 0.502734 7.93477 0 7.3125 0C6.69023 0 6.1875 0.502734 6.1875 1.125V6.1875H1.125C0.502734 6.1875 0 6.69023 0 7.3125C0 7.93477 0.502734 8.4375 1.125 8.4375H6.1875V13.5C6.1875 14.1223 6.69023 14.625 7.3125 14.625C7.93477 14.625 8.4375 14.1223 8.4375 13.5V8.4375H13.5C14.1223 8.4375 14.625 7.93477 14.625 7.3125C14.625 6.69023 14.1223 6.1875 13.5 6.1875H8.4375V1.125Z" fill="#9333EA"/>
        </svg>
    </button>
</nav>

{#if open}
    <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-8 w-96 shadow-2xl border border-pink-200/50">
            <h2 class="text-2xl font-semibold text-purple-900 mb-6">Create Server</h2>
            <p class="text-red-600">{error_message}</p>
            <input 
                type="text" 
                placeholder="Server Name" 
                id="server-name"
                class="w-full px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            />
            <input 
                type="text" 
                placeholder="Server Link" 
                id="server-link"
                class="w-full px-4 py-3 rounded-xl bg-white/80 border border-pink-200 text-gray-800 placeholder-gray-400 mb-6 focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            />
            <div class="flex gap-3">
                <button 
                    onclick={() => open = false}
                    class="flex-1 px-4 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-colors"
                >Cancel</button>
                <button 
                    onclick={CreateServer}
                    class="flex-1 px-4 py-2.5 rounded-xl text-white font-medium transition-colors shadow-lg"
                    style="background: linear-gradient(135deg, #E9D5FF 0%, #BFDBFE 70.71%);"
                >
                    <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent font-semibold">Create</span>
                </button>
            </div>
        </div>
    </div>
{/if}