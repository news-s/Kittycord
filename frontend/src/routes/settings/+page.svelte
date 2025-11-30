<script>
  import { profile } from "../app/stores";
    let username = "";
    let note = "";
    const token = localStorage.getItem("token");

    function save(){
      if(!username.length < 3 && username.length > 20){
        alert("Nazwa użytkownika musi mieć od 3 do 20 znaków!");
        return;
      }
      if(!note.length < 0 && note.length > 100){
        alert("Notatka może mieć maksymalnie 100 znaków!");
        return;
      }
      if (username !== ""){
        fetch('http://localhost:8000/edit_profile/name', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({token: token, new_val: username})
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        }
        )
        .then(() => {
          username = "";
          profile.update(p => ({...p, display_name: p.display_name = username}));
      })
    }
      if (note !== ""){
      fetch('http://localhost:8000/edit_profile/note', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({token: token, new_val: note})
      })
    .then(() => {
        note = "";
        profile.update(p => ({...p, note: p.note = note}));
      })
      }
    }
    function logout(){
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
</script>

<div>
  <a href="/app/main">Powrót</a>
  <input bind:value={username} id="setting-username" type="text" placeholder={$profile.name}/>
  <input bind:value={note} id="setting-username" type="text" placeholder={$profile.note}/>
  <button on:click={logout}>Wyloguj</button>

  {#if username !== "" || note !== ""}
    <p>Masz nie zapisane zmiany! <button on:click={save}>Zapisz</button></p>
  {/if}
</div>