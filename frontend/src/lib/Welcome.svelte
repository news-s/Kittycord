<script>
    import Arrow from '../assets/ArrowRight.png';
    import People from '../assets/People.png';
    import Star from '../assets/Star.png';
    import Cats from '../assets/Cats.png';
</script>

<div id="welcome">
    <div class="wrapper">
        <div class="wrapper">
            <div class="subtitle">Lekki, szybki i przyjazny komunikator</div>
            <div class="title">Witaj w Kittycord</div>
            <div class="description">
                Odkryj nowy sposób komunikacji. Rozmawiaj z przyjaciółmi, <br>
                twórz społeczności i baw się dobrze w przestrzeni <br>
                stworzonej z myślą o Tobie. <br>
            </div>
            <div class="button">
                Otwórz discord
                <img src={Arrow} alt="Arrow Right"/>
            </div> 
            <div class="info">
                <img src={People} alt="People"/>
                100k+ użytkowników

                &nbsp;&nbsp;&nbsp;&nbsp;

                <img src={Star} alt="Star"/>
                4.9/5 ocena
            </div>
        </div>
        <div class="image-container">
            <img src={Cats} alt="Cats on computers" />
        </div>
    </div>
</div>

<style>
    *{
        text-decoration: none;
        font-family: 'Inter';
    }

    #welcome {
        width: 100%;
        height: 703px;

        display: flex;
        justify-content: center;

        background: linear-gradient(30deg, #FAF5FF 0%, #FDF2F8 50%, #EFF6FF 100%);
    }

    #welcome > .wrapper {
        max-width: 1232px;
        width: 100%;
        height: 100%;

        padding-left: 104px;
        padding-right: 104px;

        display: flex;
        flex-direction: row;

        align-items: center;
    }

    .wrapper > .wrapper {
        width: fit-content;
        height: calc(100% - 135px);

        padding-top: 135px;

        gap: 0px;

        display: flex;
        flex-direction: column;
    }

    .subtitle {
        height: 36px;
        width: 285px;

        font-weight: 600;
        font-size: 14px;

        text-align: center;
        align-content: center;

        border-radius: 100svh;

        color: #7E22CE;
        background-color: #F3E8FF;
    }

    .title {
        margin-top: 36px;

        font-size: 60px;
        font-weight: 700;
        line-height: 75px;

        color: #9333EA;
    }

    .description {
        width: 584px;

        margin-top: 28px;

        font-size: 20px;
        font-weight: 400;
        line-height: 35px;

        color: #4B5563;
    }

    .button {
        height: 68px;
        width: 258px;

        margin-top: 31px;

        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;

        font-size: 18px;
        line-height: 28px;
        font-weight: 700;

        border-radius: 16px;

        color: #FFFFFF;
        background: linear-gradient(to right, #9333EA 0%, #DB2777 100%);
    }

    .info {
        margin-top: 47px;

        display: flex;
        align-items: center;
        gap: 8px;

        font-size: 14px;
        line-height: 20px;
        font-weight: 400;

        color: #4B5563;
    }

    .image-container {
        width: fit-content;
        height: fit-content;

        margin-left: auto;
        padding: 33px;

        border-radius: 24px;

        box-shadow: 0 30px 30px rgba(0, 0, 0, 0.25);

        background: linear-gradient(135deg, rgba(192, 132, 252, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
    }
</style>