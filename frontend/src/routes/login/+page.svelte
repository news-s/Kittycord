<script>
    import { FetchData } from "$lib/Fetch";

    import login_icon from '$lib/assets/login_icon.svg';
    import register from '$lib/assets/icons/add_user.svg';

    let username = $state("");
    let password = $state("");
    let rememberMe = $state(false);

    let error_message = $state("");

    async function onsubmit(event) {
        event.preventDefault();

        error_message = "";
        
        let data = await FetchData(
            "login",
            "POST",
            {
                username: username,
                hashed_password: password
            }
        )

        if(data === 401) {
            error_message = "Zły username albo hasło.";
            return;
        }
        
        localStorage.setItem('token', data.token);
        window.location.href = '/app/main';
    } 
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-200 via-purple-100 to-blue-200">
    <div class="w-full max-w-md">
        <div class="text-center mb-8" style="display: flex; flex-direction: column; align-items: center;">
            <h1 style="font-family: Inter; font-size: 48px; font-style: normal; font-weight: 700; line-height: 48px; color: #1F2937; text-align: center; white-space: nowrap;">
                Zaloguj się do <span style="color: #9333EA;">Kittycord</span>
            </h1>
            <p class="mt-2" style="color: #4B5563; font-family: Inter; font-size: 18px; font-style: normal; font-weight: 400; line-height: 30px; text-align: center; display: flex; justify-content: center; align-items: center; white-space: nowrap;">
                Dołącz do rozmowy i bądź w kontakcie z przyjaciółmi.
            </p>
        </div>

        <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8">
            <p class="text-red-600">{error_message}</p>
            <form {onsubmit} class="space-y-5">
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                        Username
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        bind:value={username} 
                        placeholder="Username"
                        class="w-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                        style="border-radius: 16px; border: 1px solid #E5E7EB; background: rgba(255, 255, 255, 0.70);"
                        required 
                    />
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                        Hasło
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        bind:value={password} 
                        placeholder="••••••••"
                        class="w-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                        style="border-radius: 16px; border: 1px solid #E5E7EB; background: rgba(255, 255, 255, 0.70);"
                        required 
                    />
                </div>
                <div class="flex items-center justify-between text-sm">
                    <label class="flex items-center cursor-pointer">
                        <input 
                            type="checkbox" 
                            bind:checked={rememberMe}
                            class="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                        />
                        <span class="ml-2 text-gray-700">Zapamiętaj mnie</span>
                    </label>
                    <a href="https://x.com" class="text-purple-600 hover:text-purple-700 font-medium">
                        Nie pamiętam hasła
                    </a>
                </div>
                <button 
                    type="submit"
                    class="w-full text-white font-semibold py-3.5 px-4 transition flex items-center justify-center gap-2"
                    style="border-radius: 16px; border: 0 solid #E5E7EB; background: linear-gradient(45deg, #A855F7 50%, #EC4899 120.71%); box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.10), 0 10px 15px 0 rgba(0, 0, 0, 0.10);"
                >
                <img src={login_icon} alt="login"/>
                    Zaloguj się
                </button>
            </form>
            <div class="mt-5 text-center">
                <button 
                    onclick={() => window.location.href = '/register'}
                    class="w-full text-gray-800 font-medium py-3 px-4 transition flex items-center justify-center gap-2"
                    style="border-radius: 16px; border: 1px solid #E5E7EB; background: rgba(255, 255, 255, 0.70); box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.10), 0 4px 6px 0 rgba(0, 0, 0, 0.10);"
                >
                <img src={register} alt="register"/>
                    Utwórz nowe konto
                </button>
            </div>
        </div>
    </div>
</div>