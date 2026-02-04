<script>
    import pcCat from '$lib/assets/pc cat.png';
    import { FetchData } from '$lib/Fetch';

    //svg
    import one_svg from '$lib/assets/register/1.svg';
    import two_svg from '$lib/assets/register/2.svg';
    import login from '$lib/assets/login_icon.svg';
    import three_svg from '$lib/assets/register/3.svg';

    let username = $state("");
    let email = $state("");
    let password = $state("");
    let repassword = $state("");
    let acceptRegulations = $state(false);

    let error_message = $state("");

    async function onsubmit(event) {
        event.preventDefault();

        error_message = "";

        if(password !== repassword) {
            error_message = "Hasla nie sa identyczne";
            return;
        }
        
        const result = await FetchData(
            "add_user",
            "POST",
            {
                name: username,
                hashed_password: password
            }
        );

        if(result === 409) {
            error_message = "Username jest zajety";
            return;
        }
        
        if(result != "success")return;

        window.location.href = '/thanks';
    } 
</script>

<div class="min-h-screen flex items-center justify-center p-4" style="border: 0 solid #E5E7EB; background: linear-gradient(45deg, #F8E7FF 50%, #E7F3FF 85.36%, #FFF0F8 120.71%);">
    <div class="w-full max-w-6xl flex gap-16 items-center justify-center">
        <div class="w-full max-w-md">
            <div class="text-center mb-8" style="display: flex; flex-direction: column; align-items: center;">
                <h1 style="font-family: Inter; font-size: 48px; font-style: normal; font-weight: 700; line-height: 48px; color: #1F2937; text-align: center; white-space: nowrap;">
                    Utwórz konto do <span style="color: #9333EA;">Kittycord</span>
                </h1>
                <p class="mt-2" style="color: #4B5563; font-family: Inter; font-size: 18px; font-style: normal; font-weight: 400; line-height: 30px; text-align: center; white-space: nowrap;">
                    Dołącz do rozmowy i bądź w kontakcie z przyjaciółmi.
                </p>
            </div>

            <div style="border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.30); background: #FFFFFFB2; box-shadow: 0 25px 50px 0 rgba(0, 0, 0, 0.25);" class="backdrop-blur-sm p-8">
                <p class="text-red-600">{error_message}</p>
                <form {onsubmit} class="space-y-5">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700 mb-2 ml-3">
                            Nazwa użytkownika
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <img src={two_svg} alt="user"/>
                            </div>
                            <input 
                                type="text" 
                                id="username" 
                                name="username" 
                                bind:value={username} 
                                placeholder="Nazwa użytkownika"
                                class="w-full pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                                style="border-radius: 16px; border: 0 solid #E5E7EB; background: #FFF;"
                                required 
                            />
                        </div>
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700 mb-2 ml-3">
                            Hasło
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <img src={one_svg} alt="password"/>
                            </div>
                            <input 
                                type="password" 
                                id="password" 
                                name="password" 
                                bind:value={password} 
                                placeholder="••••••••"
                                class="w-full pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                                style="border-radius: 16px; border: 0 solid #E5E7EB; background: #FFF;"
                                required 
                            />
                        </div>
                    </div>
                    <div>
                        <label for="repassword" class="block text-sm font-medium text-gray-700 mb-2 ml-3">
                            Powtórz hasło
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <img src={one_svg} alt="password"/>
                            </div>
                            <input 
                                type="password" 
                                id="repassword" 
                                name="repassword" 
                                bind:value={repassword} 
                                placeholder="••••••••"
                                class="w-full pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                                style="border-radius: 16px; border: 0 solid #E5E7EB; background: #FFF;"
                                required 
                            />
                        </div>
                    </div>
                    <div class="flex items-center text-sm">
                        <label class="flex items-center cursor-pointer">
                            <input 
                                type="checkbox" 
                                bind:checked={acceptRegulations}
                                class="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                                required
                            />
                            <span class="ml-2 text-gray-700">Akceptuję regulamin</span>
                        </label>
                    </div>
                    <button 
                        type="submit"
                        class="w-full text-white font-semibold py-3.5 px-4 transition flex items-center justify-center gap-2"
                        style="border-radius: 16px; border: 0 solid #E5E7EB; background: linear-gradient(45deg, #A855F7 50%, #EC4899 120.71%); box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.10), 0 10px 15px 0 rgba(0, 0, 0, 0.10);"
                    >
                    <img src={login} alt="register"/>
                        Zarejestruj się
                    </button>
                </form>
                <div class="mt-6 text-center">
                    <p class="text-sm text-gray-600">
                        Masz już konto? 
                        <a href="/login" class="text-purple-600 hover:text-purple-700 font-medium">Zaloguj się</a>
                    </p>
                </div>
            </div>
        </div>

        <div class="hidden lg:block w-full max-w-md ml-32 mt-28">
            <div class="bg-pink-300/60 backdrop-blur-sm rounded-3xl p-8 shadow-2xl relative">
                <img src={pcCat} alt="Cat with laptop" class="w-full h-auto" />
                <button aria-label="Łapka kota" class="absolute bottom-6 right-6 w-14 h-14 bg-pink-400 rounded-full flex items-center justify-center shadow-lg hover:bg-pink-500 transition">
                    <img src={three_svg} alt="cat paw" class="w-8 h-8"/>
                </button>
            </div>
        </div>
    </div>
</div>