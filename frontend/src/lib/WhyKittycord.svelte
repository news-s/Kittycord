<script>
    import CatImage from './assets/apple enjoyer cat.png';
</script>

<div class="w-full h-[703px] flex justify-center bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50">
    <div class="max-w-[1232px] w-full h-full px-[104px] flex flex-row items-center gap-20">
        <div class="flex-1 flex flex-col">
            <div class="font-bold text-5xl leading-[60px] text-purple-600">
                Dlaczego Kittycord?
            </div>
            <div class="mt-6 font-normal text-lg leading-7 text-gray-600">
                Kittycord to więcej niż komunikator. To społeczność, która stawia na prostotę, bezpieczeństwo i radość z rozmowy.
            </div>
            
            <div class="mt-8 flex flex-col gap-4">
                <div class="flex items-start gap-3">
                    <div class="mt-1 w-6 h-6 flex-shrink-0 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-800">Całkowicie darmowy - bez ukrytych opłat</div>
                    </div>
                </div>
                
                <div class="flex items-start gap-3">
                    <div class="mt-1 w-6 h-6 flex-shrink-0 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-800">Szyfrowanie end-to-end dla Twojego bezpieczeństwa</div>
                    </div>
                </div>
                
                <div class="flex items-start gap-3">
                    <div class="mt-1 w-6 h-6 flex-shrink-0 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-800">Intuicyjny interfejs przyjazny dla każdego</div>
                    </div>
                </div>
                
                <div class="flex items-start gap-3">
                    <div class="mt-1 w-6 h-6 flex-shrink-0 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium text-gray-800">Dostępny na wszystkich urządzeniach</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="flex-shrink-0 w-[450px] h-[450px] bg-white rounded-3xl shadow-2xl p-8 flex items-center justify-center">
            <img src={CatImage} alt="Cat with laptop" class="w-full h-full object-contain rounded-2xl" />
        </div>
    </div>
</div>
