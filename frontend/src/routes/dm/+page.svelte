<script>
  import { dmUser, dmMessages } from "./store.js";
  import { get } from "svelte/store";

  let msg = "";

  function send() {
    const user = get(dmUser);
    if (!user) return;

    dmMessages.update(m => [...m, { from: "me", text: msg }]);
    msg = "";
  }
</script>

{#if $dmUser}
  <h2>Rozmowa z {$dmUser.name}</h2>

  <div class="chat">
    {#each $dmMessages as m}
      <div class="msg">{m.text}</div>
    {/each}
  </div>

  <input bind:value={msg} placeholder="Napisz wiadomość..." />
  <button on:click={send}>Wyślij</button>

{:else}
  <h2>Wybierz użytkownika, aby rozpocząć DM</h2>
{/if}
