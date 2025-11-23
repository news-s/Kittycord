<script>
    let username = $state("");
    let password = $state("");

    async function login() {
        const res = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await res.json();
    }

    async function onsubmit(event) {
      event.preventDefault();
      let data = await login();
      
      console.log('Zalogowano pomyślnie');
      console.log(data.access_token);
    } 
</script>

<div>Zaloguj Sie</div>

<div>
    <form {onsubmit}>
        <label for="username">Username:</label> <br>
        <input type="text" id="username" name="username" bind:value={username} required /> <br>
    
        <label for="password">Hasło:</label> <br>
        <input type="password" id="password" name="password" bind:value={password} required /> <br>
    
        <button type="submit">Zaloguj się</button>
    </form>
    <!-- <button on:click={() => window.location.href = '/register'}>Zarejestruj się</button> -->
</div>