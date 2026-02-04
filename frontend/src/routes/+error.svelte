<script>
    import { page } from '$app/stores';
    import cat404 from '$lib/assets/404 cat.png';
    import home_icon from '$lib/assets/home_icon.svg';
</script>

<div class="min-h-screen flex items-center justify-center p-4" style="border: 0 solid #E5E7EB; background: linear-gradient(45deg, #F8E7FF 50%, #E7F3FF 85.36%, #FFF0F8 120.71%);">
<div class="max-w-2xl w-full text-center">
        <div class="flex justify-center mb-8">
            <div class="bg-pink-200/40 rounded-3xl p-8 inline-block">
                <img src={cat404} alt="404 Cat" class="w-80 h-auto" />
            </div>
        </div>

        <h1 class="text-9xl font-normal mb-4" style="color: #F472B6; font-family: Nunito;">
            404
        </h1>

        <h2 class="text-3xl font-semibold mb-4" style="color: #1F2937; font-family: Nunito;">
            Ups! Zgubiłeś się...
        </h2>

        <p class="text-lg mb-8" style="color: #4B5563; font-family: Nunito;">
            Wygląda na to, że ta strona nie istnieje lub została przeniesiona.
        </p>

        <a href="/" class="inline-flex items-center gap-2 px-8 py-4 text-white font-semibold transition" 
           style="border-radius: 9999px; border: 0 solid #E5E7EB; background: linear-gradient(90deg, #F472B6 0%, #C084FC 50%, #60A5FA 100%); box-shadow: 0 25px 50px 0 rgba(0, 0, 0, 0.25); text-decoration: none; font-family: Nunito;">
            <img src={home_icon} alt="home"/>
            Wróć na stronę główną
        </a>
    </div>
</div>
