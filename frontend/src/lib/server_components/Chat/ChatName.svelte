<script>
    let { chat_name } = $props(); 
</script>

<div class="h-14 px-4 flex items-center justify-between border-b border-purple-200/50">
    <div class="flex items-center gap-2">
        <span class="text-purple-500 font-semibold">#</span>
        <span class="font-semibold text-gray-800">{chat_name}</span>
    </div>
    <div class="flex items-center gap-2">
        <button aria-label="Notifications" class="p-2 hover:bg-white/50 rounded">
            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
            </svg>
        </button>
        <button aria-label="Search" class="p-2 hover:bg-white/50 rounded">
            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
            </svg>
        </button>
    </div>
</div>