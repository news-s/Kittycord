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

<div>
    <nav>
        <a href="general">General</a>
        <a href="roles">Roles</a>
        <a href="/app/server/{server_id}">Exit</a>
    </nav>
    {@render children()}
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;

        width: 100%;
    }

    nav {
        width: 20%;

        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
</style>