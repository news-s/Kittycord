<script>
    import { profile } from "../routes/app/stores";
</script>

<div class="h-[95px] px-2 bg-[#f7f3f9] border-t border-pink-200/50 flex items-center justify-between absolute bottom-0 left-[72px] w-60 z-10">
    <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-full border-0 border-[#E5E7EB] bg-black"></div>
        <div class="flex flex-col">
            <span class="text-xs font-semibold text-gray-800">{$profile?.display_name}</span>
            <div class="flex items-center gap-1">
                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                <span class="text-xs text-green-600">Online</span>
            </div>
        </div>
    </div>
    <div class="flex items-center gap-1">
        <a href="/settings" aria-label="Settings" class="p-1.5 hover:bg-pink-100/60 rounded">
            <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
            </svg>
        </a>
    </div>
</div>