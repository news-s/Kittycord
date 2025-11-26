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

<div class="container">
  <div class="menu">
    <ul>
			<button>img menu</button>
      {#each channels as channel}
        <li 
          on:mouseenter={() => hoveredId = channel.id}
          on:mouseleave={() => hoveredId = null}
        >
          <button>img channel n{channel.id}</button>
          {#if hoveredId === channel.id}
            <span class="tooltip">{channel.name}</span>
          {/if}
        </li>
      {/each}
			<button>create channel</button>
    </ul>
  </div>
</div>


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

.container {
  display: flex;
  gap: 10px;
}

.menu {
  border: lightblue 2px solid;
  width: 17%;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  position: relative;
  margin: 5px 0;
  padding: 5px;
  cursor: pointer;
}

.tooltip {
  position: absolute;
  left: 100%;
  top: 0;
  margin-left: 10px;
  background: #333;
  color: white;
  padding: 3px 6px;
  border-radius: 4px;
  white-space: nowrap;
  font-size: 0.9em;
}

.frame {
  border: green 2px solid;
}

button {
  cursor: pointer;
}

.modal {
  position: relative;
  background: black;
  padding: 20px;
  border: 2px solid #123;
  border-radius: 8px;
  box-shadow: 0 5px 15px #12a;
  color: white;
  min-width: 250px;
	top: 1%;
}

.modal .close {
  position: absolute;
  top: 5px;
  right: 5px;
  background: transparent;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
}

</style>