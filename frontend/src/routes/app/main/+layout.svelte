<script>
    import { profile } from "../stores";
    let { children } = $props();

</script>

<div class="friends-container">
    <div class="friend-container">
        {#each profile?.friends as friend}
            <button class="friend" onclick={() => SwitchChannel(friend.id)}>{friend.name}</button>
        {/each}
    </div>

    {@render children()}
</div>

<style>
    .friends-container {
        display: flex;
    }

    .friend-container {
        width: 200px;
        height: 100svh;
        background-color: #ccc;

        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .friend {
        width: 100%;
        height: 40px;

        background-color: #bbb;
    }
</style>