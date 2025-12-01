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

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100">
  <div class="max-w-xl w-full p-12 bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-purple-100">
    <h2 class="text-3xl font-bold text-purple-600 mb-6 text-center">Ustawienia profilu</h2>
    <div class="flex flex-col gap-4">
      <div>
        <label for="setting-username" class="block text-sm font-medium text-gray-700 mb-1">Nazwa użytkownika</label>
        <input 
          bind:value={username}
          id="setting-username"
          type="text"
          placeholder={$profile.name}
          class="w-full px-4 py-2 rounded-xl bg-white border border-purple-200 focus:ring-2 focus:ring-purple-300 focus:outline-none shadow-sm transition"
        />
      </div>
      <div>
        <label for="setting-note" class="block text-sm font-medium text-gray-700 mb-1">Notatka</label>
        <input 
          bind:value={note}
          id="setting-note"
          type="text"
          placeholder={$profile.note}
          class="w-full px-4 py-2 rounded-xl bg-white border border-purple-200 focus:ring-2 focus:ring-purple-300 focus:outline-none shadow-sm transition"
        />
      </div>
      <button 
        on:click={logout}
        class="mt-2 w-full py-2 rounded-xl text-white font-semibold shadow-lg hover:shadow-xl transition"
        style="background: linear-gradient(45deg, #A855F7 50%, #EC4899 120.71%);"
      >
        Wyloguj
      </button>
      {#if username !== "" || note !== ""}
        <div class="mt-2 p-4 bg-yellow-50 border border-yellow-200 rounded-xl text-yellow-800 text-sm flex items-center justify-between">
          <span>Masz niezapisane zmiany!</span>
          <button 
            on:click={save}
            class="px-4 py-1 bg-purple-500 text-white rounded-lg shadow hover:bg-purple-600 transition"
          >
            Zapisz
          </button>
        </div>
      {/if}
      <a 
        href="/app/main" 
        class="block text-center mt-4 text-purple-600 hover:text-purple-800 font-medium"
      >
        Powrót
      </a>
    </div>
  </div>
</div>