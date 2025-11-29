<script>
	import { onDestroy } from "svelte";
    import { load_server_bar } from "../../../stores";
    import { page } from "$app/stores";

    const server_id = $page.params.id;
    const { children } = $props();

    load_server_bar.set(false);

    onDestroy(() => {
        load_server_bar.set(true);
    });
</script>

<div class="fixed inset-0 w-full h-full bg-gradient-to-br from-pink-50 to-purple-50 -z-10"></div>
<div class="flex flex-col items-center w-full relative">
  <nav class="flex justify-center gap-6 my-8 bg-gradient-to-br from-pink-50 to-purple-50 rounded-3xl shadow-2xl border border-pink-200/50 px-10 py-6 backdrop-blur-sm">
    <a href="./general" class="flex items-center gap-3 px-6 py-3 rounded-2xl text-purple-800 font-semibold hover:bg-gradient-to-r hover:from-pink-200 hover:to-purple-200 hover:text-purple-900 transition-all duration-300 transform hover:scale-105">
      General
    </a>
    <a href="./roles" class="flex items-center gap-3 px-6 py-3 rounded-2xl text-purple-800 font-semibold hover:bg-gradient-to-r hover:from-pink-200 hover:to-purple-200 hover:text-purple-900 transition-all duration-300 transform hover:scale-105">
      Roles
    </a>
    <a use:goto href={`/app/server/${server_id}`} class="flex items-center gap-3 px-6 py-3 rounded-2xl text-red-600 font-semibold hover:bg-gradient-to-r hover:from-red-200 hover:to-red-300 hover:text-red-800 transition-all duration-300 transform hover:scale-105">
      Exit
    </a>
  </nav>
  <div class="w-full flex justify-center">
    {@render children()}
  </div>
</div>