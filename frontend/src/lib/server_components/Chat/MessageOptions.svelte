<script>
    import { tick } from "svelte";
    import { FetchData } from "$lib/Fetch"
    let { message, editing } = $props(); 

    async function EnableEditingMessage(event) {
        editing.state = !editing.state;
        editing.id = message.message_id;
        editing.content = message.content

        await tick();    

        editing.input.focus(); 
    }

    async function DeleteMessage(message_id) {
        const token = localStorage.getItem("token")

        FetchData(
            "remove_message", 
            "PATCH", 
            {
                token: token,
                message_id: message_id
            }
        );
    }
</script>

<div class="absolute top-0 right-2 -translate-y-1/2 opacity-0 group-hover/message:opacity-100 flex items-center gap-1 bg-white border border-purple-200/50 rounded-lg shadow-lg transition-opacity">
    <button 
        onclick={(event) => EnableEditingMessage(event)}
        class="p-2 hover:bg-purple-50 rounded-lg transition-colors"
        aria-label="Edit message"
    >
        <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
        </svg>
    </button>
    <button 
        onclick={() => DeleteMessage(message.message_id)}
        class="p-2 hover:bg-red-50 rounded-lg transition-colors"
        aria-label="Delete message"
    >
        <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
    </button>
</div>