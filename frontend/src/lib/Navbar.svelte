
<script>
    import Logo from '../assets/Logo.png';
</script>

<nav class="navbar">
    <a class="button" href="/">
        <img src={Logo} alt="KittyCord Logo" class="logo" />
        Kittycord
    </a>

    <div class="right-links">
        <a class="button" href="#functions">Funkcje</a>
        <a class="button" href="#us">Dlaczego My</a>
        <a class="button" href="#contact">Kontakt</a>
        <a class="login" href="/login">Zaloguj się</a>
    </div>
</nav>

<style>
    * {
        text-decoration: none;

        font-family: 'Inter';
    }

    .navbar {
        width: 100%;
        height: 77px;

        display: flex;
        align-items: center;
        justify-content: center;

        background-color: #FFFFFF;
    }
    
    .right-links {
        display: flex;
        align-items: center;

        margin-left: 626px;
        gap: 32px;
    }

    .logo {
        height: 20px;
        aspect-ratio: 1/1;

        padding: 10px;

        border-radius: 12px;

        background: linear-gradient(-45deg, #C084FC, #F472B6);
    }

    .button {
        color: #9333ea;

        display: flex;
        align-items: center;
        gap: 13px;

        font-weight: 700;
        font-size: 24px;
    }

    .right-links > .button {
        color: #4B5563;

        font-weight: 500;
        font-size: 17px;
    }

    .login {
        height: 44px;
        width: 132px;

        background: linear-gradient(to right, #A855F7, #EC4899);
        color: #ffffff;

        align-content: center;

        text-align: center;
        font-weight: 500;

        border-radius: 12px;
    }
</style>