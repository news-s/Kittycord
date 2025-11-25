<script>
    import bcrypt from 'bcryptjs';

    let username = $state("");
    let password = $state("");
    let rememberMe = $state(false);

    async function login() {
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);

        const res = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                hashed_password: password
            })
        });

        return await res.json();
    }

    async function onsubmit(event) {
        event.preventDefault();
        let data = await login();
        
        console.log('Zalogowano pomyślnie');
        console.log(data.token);
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
                    <a href="x.com" class="text-purple-600 hover:text-purple-700 font-medium">
                        Nie pamiętam hasła
                    </a>
                </div>
                <button 
                    type="submit"
                    class="w-full text-white font-semibold py-3.5 px-4 transition flex items-center justify-center gap-2"
                    style="border-radius: 16px; border: 0 solid #E5E7EB; background: linear-gradient(45deg, #A855F7 50%, #EC4899 120.71%); box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.10), 0 10px 15px 0 rgba(0, 0, 0, 0.10);"
                >
                <svg width="16" height="14" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.80937 2.30938L10.6469 6.14687C10.8719 6.37187 11 6.68125 11 7C11 7.31875 10.8719 7.62812 10.6469 7.85312L6.80937 11.6906C6.60938 11.8906 6.34062 12 6.05937 12C5.475 12 5 11.525 5 10.9406V9H1C0.446875 9 0 8.55313 0 8V6C0 5.44688 0.446875 5 1 5H5V3.05937C5 2.475 5.475 2 6.05937 2C6.34062 2 6.60938 2.1125 6.80937 2.30938ZM11 12H13C13.5531 12 14 11.5531 14 11V3C14 2.44688 13.5531 2 13 2H11C10.4469 2 10 1.55313 10 1C10 0.446875 10.4469 0 11 0H13C14.6562 0 16 1.34375 16 3V11C16 12.6562 14.6562 14 13 14H11C10.4469 14 10 13.5531 10 13C10 12.4469 10.4469 12 11 12Z" fill="white"/>
                </svg>
                    Zaloguj się
                </button>
            </form>
            <div class="mt-5 text-center">
                <button 
                    onclick={() => window.location.href = '/register'}
                    class="w-full text-gray-800 font-medium py-3 px-4 transition flex items-center justify-center gap-2"
                    style="border-radius: 16px; border: 1px solid #E5E7EB; background: rgba(255, 255, 255, 0.70); box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.10), 0 4px 6px 0 rgba(0, 0, 0, 0.10);"
                >
                <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 4C3 2.93913 3.42143 1.92172 4.17157 1.17157C4.92172 0.421427 5.93913 0 7 0C8.06087 0 9.07828 0.421427 9.82843 1.17157C10.5786 1.92172 11 2.93913 11 4C11 5.06087 10.5786 6.07828 9.82843 6.82843C9.07828 7.57857 8.06087 8 7 8C5.93913 8 4.92172 7.57857 4.17157 6.82843C3.42143 6.07828 3 5.06087 3 4ZM0 15.0719C0 11.9937 2.49375 9.5 5.57188 9.5H8.42813C11.5063 9.5 14 11.9937 14 15.0719C14 15.5844 13.5844 16 13.0719 16H0.928125C0.415625 16 0 15.5844 0 15.0719ZM15.75 9.75V7.75H13.75C13.3344 7.75 13 7.41563 13 7C13 6.58437 13.3344 6.25 13.75 6.25H15.75V4.25C15.75 3.83437 16.0844 3.5 16.5 3.5C16.9156 3.5 17.25 3.83437 17.25 4.25V6.25H19.25C19.6656 6.25 20 6.58437 20 7C20 7.41563 19.6656 7.75 19.25 7.75H17.25V9.75C17.25 10.1656 16.9156 10.5 16.5 10.5C16.0844 10.5 15.75 10.1656 15.75 9.75Z" fill="black"/>
                </svg>
                    Utwórz nowe konto
                </button>
            </div>
        </div>
    </div>
</div>