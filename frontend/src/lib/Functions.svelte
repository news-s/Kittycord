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

<div id="functions">
    <div class="wrapper">
        <div class="text-wrapper">
            <div class="title">Funkcje Kittycord</div>
            <div class="subtitle">Wszystko czego potrzebujesz do doskonałej komunikacji w jednym <br> miejscu</div>
        </div>
        <div class="functions-wrapper">
            {#each functions as func}
                <div class="function-item">
                    <div class="icon" style="background: {func.background};">
                        <img src={func.icon} alt={func.title} />
                    </div>
                    <div class="title">{func.title}</div>
                    <div class="description">{func.description}</div>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    *{
        text-decoration: none;
        font-family: 'Inter';
    }

    #functions {
        width: 100%;
        height: 703px;

        display: flex;
        justify-content: center;

        background-color: #FFFFFF;
    }

    #functions > .wrapper {
        max-width: 1232px;
        width: 100%;
        height: 100%;

        padding-left: 104px;
        padding-right: 104px;

        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .text-wrapper {
        width: fit-content;
        height: fit-content;

        margin-top: 94px;

        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .text-wrapper > .title {
        font-weight: 700;
        font-size: 48px;
        line-height: 48px;

        color: #9333EA;
    }

    .text-wrapper > .subtitle {
        margin-top: 15px;

        font-weight: 400;
        font-size: 20px;
        line-height: 28px;

        text-align: center;

        color: #4B5563;
    }

    .functions-wrapper {
        width: 100%;
        height: fit-content;

        margin-top: 67px;

        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    .function-item {
        width: 325px;
        height: 216px;

        padding: 32px;

        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
        border: 1px solid #F3E8FF;
        border-radius: 24px;

        display: flex;
        flex-direction: column;
    }

    .function-item > .icon {
        width: 64px;
        aspect-ratio: 1/1;

        border-radius: 16px;

        display: flex;
        justify-content: center;
        align-items: center;
    }

    .function-item > .title {
        margin-top: 24px;

        font-weight: 700;
        font-size: 24px;

        color: #1F2937;
    }

    .function-item > .description {
        margin-top: 15px;

        font-weight: 400;
        font-size: 16px;

        color: #4B5563;
    }
    
</style>