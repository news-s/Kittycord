<script>
	import { onDestroy } from "svelte";
    import { load_server_bar } from "../../../stores";

    const { children } = $props();

    load_server_bar.set(false);

    onDestroy(() => {
        load_server_bar.set(true);
    });
</script>

{@render children()}