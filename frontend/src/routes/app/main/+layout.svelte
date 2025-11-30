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