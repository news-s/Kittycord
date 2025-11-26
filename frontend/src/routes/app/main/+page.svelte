<script>
  import { dmUser, dmMessages } from "../dm/store.js";
  import { goto } from "$app/navigation";

	class Channel {
    constructor(id, name) {
      this.id = id;
      this.name = name;
    }
  }
  let channels = [
    new Channel(1, "General"),
    new Channel(2, "Random"),
    new Channel(3, "Music"), 
  ];

	let f = [
    { id: 1, name: 'franek'},
    { id: 2, name: 'franciszek'}, 
    { id: 3, name: 'franuszek'}, 
    { id: 4, name: 'franula'}, 
    { id: 5, name: 'franio'}
  ];

	let status = ['offline', 'offline', 'online', 'online', 'online']
  let search = "";
  let limit = 3
	
	// tu powyzej przyklad tylko, potem z bazy danych bedzie trzeba zajebać i podmienić za przykladowe zmienne

  let showSettings = false;
	let showProf = false;
	let showMic = true;
	let showHeadph = true;
  let hoveredId = null;
	let findFriendMenu = false;
	let showFriends = "online"
	$: total = f.length;
  $: online = status.filter(s => s === "online").length;
	
	function mic(){
		showMic = !showMic;
	}
	
	function headph(){
		showHeadph = !showHeadph;
	}
	
	function friendsEvery(){
		showFriends = "wszystkie";
	}
	
	function friendsOnline(){
		showFriends = "online";
	}

  function openDM(friend) {
    dmUser.set(friend);
    dmMessages.set([]); 
    goto("/app/dm");
  }
</script>

<button on:click={() => findFriendMenu = true}>find or start the conversation</button>

<div class="frame">
	<button on:click={() => showProf = true}>prof img + user name + status</button>
	<button on:click={mic}>mic img {showMic ? true : false}</button>
	<button on:click={headph}>headphones img {showHeadph ? true : false}</button>
	<button on:click={() => showSettings = true}>settings img</button>
</div>



{#if showProf}
  <div class="modal">
    <button on:click={() => showProf = false}>×</button>
    <div>tak</div>
  </div>
{/if}


{#if showSettings}
  <div class="modal">
    <button class="close" on:click={() => showSettings = false}>×</button>
    <div>tak</div>
  </div>
{/if}


{#if findFriendMenu}
  <div class="modal">
    <button class="close" on:click={() => findFriendMenu = false}>×</button>
    <input type="text" placeholder="Szukaj..." bind:value={search} /><br>

    {#each f
      .filter(friend => friend.name.toLowerCase().includes(search.toLowerCase()))
      .slice(0, limit) as friend}

      <button on:click={() => openDM(friend)}>
        {friend.name}
      </button><br>

    {/each}
  </div>
{/if}




<h2>img Znajomi</h2>
{#each f as friend, index}
	<button class="listFriend" on:click={() => openDM(friend)}>img prof {index+1} + status + {friend.name}</button><br>
{/each}


<button on:click={friendsEvery}>Wszystkie</button>
<button on:click={friendsOnline}>Online</button>
<h6>{showFriends} – {#if showFriends=="online"}{online}{/if}{#if showFriends=="wszystkie"}{total}{/if}</h6>
{#each f as friend, index}
	{#if status[index] == 'online'}
		<button class="listFriend" on:click={() => openDM(friend)}>img prof {index+1} + status + {friend.name}</button><br>
	{/if}
	{#if status[index] == 'offline' && showFriends == "wszystkie"}
		<button class="listFriend" on:click={() => openDM(friend)}>img prof {index+1} + status + {friend.name}</button><br>
	{/if}
{/each}

<style>

</style>