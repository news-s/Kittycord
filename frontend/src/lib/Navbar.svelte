<script>
    import Logo from './assets/Logo.png';
</script>

<div class="w-full h-[77px] flex justify-center content-center bg-white">
    <nav class="w-[1232px] h-[77px] flex px-[104px]">
        <a class="text-purple-600 flex items-center gap-[13px] font-bold text-2xl no-underline" href="#welcome">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center overflow-hidden">
                <img src={Logo} alt="KittyCord Logo" class="w-full h-full object-cover" />
            </div>
            Kittycord
        </a>

        <div class="flex items-center ml-auto gap-8">
            <a class="text-gray-600 flex items-center gap-[13px] font-medium text-[17px] no-underline" href="#funkcje">Funkcje</a>
            <a class="text-gray-600 flex items-center gap-[13px] font-medium text-[17px] no-underline" href="#dlaczego-my">Dlaczego My</a>
            <a class="text-gray-600 flex items-center gap-[13px] font-medium text-[17px] no-underline" href="https://x.com">Kontakt</a>
            <a class="h-11 w-[132px] bg-gradient-to-r from-purple-500 to-pink-500 text-white content-center text-center font-medium rounded-xl no-underline" href="/login">Zaloguj się</a>
        </div>
    </nav>
</div>