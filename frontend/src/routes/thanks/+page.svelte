<script>
    import thanksCat from '$lib/assets/thanks cat.png';
    
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
            <svg width="18" height="16" viewBox="0 0 18 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7.66055 2.59805L11.9777 6.91523C12.2309 7.16836 12.375 7.51641 12.375 7.875C12.375 8.23359 12.2309 8.58164 11.9777 8.83477L7.66055 13.152C7.43555 13.377 7.1332 13.5 6.8168 13.5C6.15937 13.5 5.625 12.9656 5.625 12.3082V10.125H1.125C0.502734 10.125 0 9.62227 0 9V6.75C0 6.12773 0.502734 5.625 1.125 5.625H5.625V3.4418C5.625 2.78437 6.15937 2.25 6.8168 2.25C7.1332 2.25 7.43555 2.37656 7.66055 2.59805ZM12.375 13.5H14.625C15.2473 13.5 15.75 12.9973 15.75 12.375V3.375C15.75 2.75273 15.2473 2.25 14.625 2.25H12.375C11.7527 2.25 11.25 1.74727 11.25 1.125C11.25 0.502734 11.7527 0 12.375 0H14.625C16.4883 0 18 1.51172 18 3.375V12.375C18 14.2383 16.4883 15.75 14.625 15.75H12.375C11.7527 15.75 11.25 15.2473 11.25 14.625C11.25 14.0027 11.7527 13.5 12.375 13.5Z" fill="white"/>
            </svg>
            Zaloguj się
        </button>

        <a href="/" class="inline-block mt-6 text-gray-600 text-sm hover:text-gray-800 transition-colors">
            Wróć na stronę główną
        </a>
    </div>
</div>