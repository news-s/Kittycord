<script>
    import thanksCat from '$lib/assets/thanks cat.png';
    import login_icon from '$lib/assets/login_icon.svg';
    
    function onclick() {
        window.location.href = '/login';
    }
</script>

<div class="min-h-screen flex items-center justify-center relative overflow-hidden" style="border: 0 solid #E5E7EB; background: linear-gradient(45deg, #FCE7F3 0%, #E0E7FF 25%, #ECFDF5 50%, #FEF3C7 75%, #FCE7F3 100%); font-family: 'Nunito', sans-serif;">
    <div class="relative z-10 text-center px-6">
        <h1 class="text-4xl md:text-5xl font-normal text-gray-800 mb-3">
            Dziękujemy za dołączenie do
        </h1>
        <h2 class="text-4xl md:text-5xl font-normal text-pink-500 mb-12">
            Kittycord!
        </h2>

        <div class="mb-8 flex justify-center">
            <img 
                src={thanksCat} 
                alt="Cute cat" 
                class="w-64 h-auto rounded-3xl shadow-2xl"
            />
        </div>

        <p class="text-gray-700 text-lg mb-8 max-w-md mx-auto leading-relaxed">
            Twoje konto zostało pomyślnie utworzone. Możesz teraz
            zalogować się i rozpocząć rozmowę z przyjaciółmi.
        </p>

        <button 
            onclick={onclick}
            class="px-8 py-4 text-white text-lg transition-all duration-300 transform hover:scale-105 flex items-center gap-2 mx-auto"
            style="border-radius: 9999px; border: 0 solid #E5E7EB; background: linear-gradient(45deg, #EC4899 50%, #8B5CF6 120.71%); box-shadow: 0 8px 10px 0 rgba(0, 0, 0, 0.10), 0 20px 25px 0 rgba(0, 0, 0, 0.10);"
        >
            <img src={login_icon} alt="login"/>
            Zaloguj się
        </button>

        <a href="/" class="inline-block mt-6 text-gray-600 text-sm hover:text-gray-800 transition-colors">
            Wróć na stronę główną
        </a>
    </div>
</div>