<script>
    import Microphone from './assets/Microphone.png';
    import Messages from './assets/Messages.png';
    import Paint from './assets/Paint.png';

    class functionItem {
        constructor(title, description, icon, background) {
            this.title = title;
            this.description = description;
            this.icon = icon;
            this.background = background;
        }
    }

    let functions = [
        new functionItem(
            "Czat tekstowy",
            "Wysyłaj wiadomości błyskawicznie. Twórz kanały tematyczne i organizuj rozmowy według własnych preferencji.",
            Messages,
            "linear-gradient(-45deg, #C084FC 0%, #9333EA 100%)"
        ),
        new functionItem(
            "Kanały głosowe",
            "Rozmawiaj z przyjaciółmi w krystalicznie czystej jakości. Niskie opóźnienia i stabilne połączenie gwarantowane.",
            Microphone,
            "linear-gradient(-45deg, #F472B6 0%, #DB2777 100%)"
        ),
        new functionItem(
            "Personalizacja",
            "Dostosuj swój profil, wybierz motywy kolorystyczne i stwórz przestrzeń idealną dla siebie.",
            Paint,
            "linear-gradient(-45deg, #60A5FA 0%, #2563EB 100%)"
        )
    ];
</script>

<div class="w-full h-[703px] flex justify-center bg-white">
    <div class="max-w-[1232px] w-full h-full px-[55px] flex flex-col items-center">
        <div class="w-fit h-fit mt-[94px] flex flex-col items-center">
            <div class="font-bold text-5xl leading-[48px] text-purple-600">Funkcje Kittycord</div>
            <div class="mt-[15px] font-normal text-xl leading-7 text-center text-gray-600">Wszystko czego potrzebujesz do doskonałej komunikacji w jednym <br> miejscu</div>
        </div>
        <div class="w-full h-fit mt-[87px] flex flex-row justify-between gap-10">
            {#each functions as func}
                <div class="w-[325px] h-[300px] p-8 shadow-lg border border-purple-100 rounded-3xl flex flex-col">
                    <div class="w-16 aspect-square rounded-2xl flex justify-center items-center" style="background: {func.background};">
                        <img src={func.icon} alt={func.title} />
                    </div>
                    <div class="mt-6 font-bold text-2xl text-gray-800">{func.title}</div>
                    <div class="mt-[15px] font-normal text-base text-gray-600">{func.description}</div>
                </div>
            {/each}
        </div>
    </div>
</div>