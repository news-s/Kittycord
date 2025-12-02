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

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 p-4">
  <div class="max-w-md w-full bg-white rounded-3xl shadow-2xl overflow-hidden">
    <div class="bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-6">
      <h2 class="text-3xl font-bold text-white text-center">Ustawienia</h2>
      <p class="text-purple-100 text-center text-sm mt-1">Edytuj swój profil</p>
    </div>
    
    <div class="p-8 space-y-6">
      <div class="space-y-2">
        <label for="setting-username" class="block text-sm font-semibold text-gray-700">
          Nazwa użytkownika
        </label>
        <input 
          bind:value={username}
          id="setting-username"
          type="text"
          placeholder={$profile.name}
          class="w-full px-4 py-3 rounded-xl bg-gray-50 border-2 border-gray-200 focus:border-purple-500 focus:bg-white focus:ring-4 focus:ring-purple-100 focus:outline-none transition-all duration-200 text-gray-800 placeholder-gray-400"
        />
        <p class="text-xs text-gray-500">Od 3 do 20 znaków</p>
      </div>

      <div class="space-y-2">
        <label for="setting-note" class="block text-sm font-semibold text-gray-700">
          Notatka
        </label>
        <textarea
          bind:value={note}
          id="setting-note"
          rows="3"
          placeholder={$profile.note || "Dodaj notatkę..."}
          class="w-full px-4 py-3 rounded-xl bg-gray-50 border-2 border-gray-200 focus:border-purple-500 focus:bg-white focus:ring-4 focus:ring-purple-100 focus:outline-none transition-all duration-200 text-gray-800 placeholder-gray-400 resize-none"
        ></textarea>
        <p class="text-xs text-gray-500">Maksymalnie 40 znaków</p>
      </div>

      {#if username !== "" || note !== ""}
        <div class="bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-300 rounded-xl p-4 animate-pulse">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span class="text-sm font-medium text-amber-900">Niezapisane zmiany</span>
            </div>
            <button 
              on:click={save}
              class="px-5 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-semibold shadow-md hover:shadow-lg hover:scale-105 transition-all duration-200"
            >
              Zapisz
            </button>
          </div>
        </div>
      {/if}

      <button 
        on:click={logout}
        class="w-full py-3 rounded-xl text-white font-bold shadow-lg hover:shadow-xl transition-all duration-200 bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 transform hover:scale-[1.02]"
      >
        <div class="flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          Wyloguj się
        </div>
      </button>

      <a 
        href="/app/main" 
        class="flex items-center justify-center gap-2 text-purple-600 hover:text-purple-800 font-semibold transition-colors duration-200 group"
      >
        <svg class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Powrót do aplikacji
      </a>
    </div>
  </div>
</div>