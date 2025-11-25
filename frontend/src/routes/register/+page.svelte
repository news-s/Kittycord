<script>
    import bcrypt from 'bcryptjs';
    import pcCat from '$lib/assets/pc cat.png';

    let username = $state("");
    let email = $state("");
    let password = $state("");
    let repassword = $state("");
    let acceptRegulations = $state(false);

    async function register() {
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);
        console.log(hash)

        const res = await fetch('http://localhost:8000/add_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: username,
                hashed_password: password
            })
        });

        return await res.json();
    }

    async function onsubmit(event) {
        event.preventDefault();

        if(password !== repassword) {
        console.warn("Hasła nie są identyczne");
        return;
        }
        
        await register();
        console.log('Zarejestrowano pomyślnie');

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
                <form {onsubmit} class="space-y-5">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700 mb-2 ml-3">
                            Nazwa użytkownika
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                                </svg>
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
                        <label for="email" class="block text-sm font-medium text-gray-700 mb-2 ml-3">
                            Email
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                                </svg>
                            </div>
                            <input 
                                type="email" 
                                id="email" 
                                name="email" 
                                bind:value={email} 
                                placeholder="example@mail.com"
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
                                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                                </svg>
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
                                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                                </svg>
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
                    <svg width="16" height="14" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6.80937 2.30938L10.6469 6.14687C10.8719 6.37187 11 6.68125 11 7C11 7.31875 10.8719 7.62812 10.6469 7.85312L6.80937 11.6906C6.60938 11.8906 6.34062 12 6.05937 12C5.475 12 5 11.525 5 10.9406V9H1C0.446875 9 0 8.55313 0 8V6C0 5.44688 0.446875 5 1 5H5V3.05937C5 2.475 5.475 2 6.05937 2C6.34062 2 6.60938 2.1125 6.80937 2.30938ZM11 12H13C13.5531 12 14 11.5531 14 11V3C14 2.44688 13.5531 2 13 2H11C10.4469 2 10 1.55313 10 1C10 0.446875 10.4469 0 11 0H13C14.6562 0 16 1.34375 16 3V11C16 12.6562 14.6562 14 13 14H11C10.4469 14 10 13.5531 10 13C10 12.4469 10.4469 12 11 12Z" fill="white"/>
                    </svg>
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
                    <svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8.84535 2.3771C9.40394 4.05288 8.83363 5.74429 7.57191 6.15835C6.31019 6.57242 4.83363 5.54898 4.27504 3.8732C3.71644 2.19742 4.28676 0.506009 5.54847 0.0919469C6.81019 -0.322116 8.28675 0.701322 8.84535 2.3771ZM3.91957 6.50601C4.65785 7.77163 4.47816 9.24429 3.52113 9.79117C2.5641 10.338 1.1891 9.75601 0.454723 8.49038C-0.279652 7.22476 -0.107777 5.7521 0.849254 5.20523C1.80629 4.65835 3.18129 5.24038 3.91566 6.50601H3.91957ZM2.70082 14.4201C4.74769 8.90054 8.38441 7.4982 9.99769 7.4982C11.611 7.4982 15.2477 8.90054 17.2946 14.4201C17.4352 14.799 17.4977 15.2052 17.4977 15.6115V15.674C17.4977 16.6818 16.6813 17.4982 15.6735 17.4982C15.2243 17.4982 14.7789 17.4435 14.3453 17.3341L10.9078 16.4748C10.3102 16.3263 9.68519 16.3263 9.08754 16.4748L5.65004 17.3341C5.21644 17.4435 4.77113 17.4982 4.32191 17.4982C3.3141 17.4982 2.49769 16.6818 2.49769 15.674V15.6115C2.49769 15.2052 2.56019 14.799 2.70082 14.4201ZM16.4743 9.79117C15.5172 9.24429 15.3375 7.77163 16.0758 6.50601C16.8141 5.24038 18.1852 4.65835 19.1422 5.20523C20.0993 5.7521 20.2789 7.22476 19.5407 8.49038C18.8024 9.75601 17.4313 10.338 16.4743 9.79117ZM12.111 6.15835C10.8493 5.74429 10.2789 4.05288 10.8375 2.3771C11.3961 0.701322 12.8727 -0.322116 14.1344 0.0919469C15.3961 0.506009 15.9664 2.19742 15.4078 3.8732C14.8493 5.54898 13.3727 6.57242 12.111 6.15835Z" fill="white"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>