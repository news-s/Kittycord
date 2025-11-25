<script>
    import Arrow from './assets/ArrowRight.png';
    import People from './assets/People.png';
    import Star from './assets/Star.png';
    import Cats from './assets/Cats.png';
</script>

<div class="w-full h-[703px] flex justify-center bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50 font-['Inter']">
    <div class="max-w-[1232px] w-full h-full px-[104px] flex flex-row items-center">
        <div class="w-fit h-[calc(100%-135px)] pt-[135px] flex flex-col">
            <div class="h-9 w-[285px] font-semibold text-sm text-center content-center rounded-full text-purple-700 bg-purple-200">
                Lekki, szybki i przyjazny komunikator
            </div>
            <div class="mt-9 text-[60px] font-bold leading-[75px] text-purple-600">
                Witaj w Kittycord
            </div>
            <div class="w-[584px] mt-7 text-xl font-normal leading-[35px] text-gray-600">
                Odkryj nowy sposób komunikacji. Rozmawiaj z przyjaciółmi, <br>
                twórz społeczności i baw się dobrze w przestrzeni <br>
                stworzonej z myślą o Tobie. <br>
            </div>
            <a href="/login" class="h-[68px] w-[258px] mt-[31px] flex justify-center items-center gap-2 text-lg leading-7 font-bold rounded-2xl text-white bg-gradient-to-r from-purple-600 to-pink-600 no-underline cursor-pointer">
                Otwórz Kittycord
                <img src={Arrow} alt="Arrow Right"/>
            </a> 
            <div class="mt-[47px] flex items-center gap-2 text-sm leading-5 font-normal text-gray-600">
                <img src={People} alt="People"/>
                100k+ użytkowników

                &nbsp;&nbsp;&nbsp;&nbsp;

                <img src={Star} alt="Star"/>
                4.9/5 ocena
            </div>
        </div>
        <div class="w-fit h-fit ml-auto p-[33px] rounded-3xl shadow-[0_25px_50px_rgba(0,0,0,0.25)] bg-gradient-to-br from-purple-300/20 to-pink-300/20">
            <img src={Cats} alt="Cats on computers" />
        </div>
    </div>
</div>