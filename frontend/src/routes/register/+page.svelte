<script>
    import bcrypt from 'bcryptjs';

    let username = $state("");
    let password = $state("");
    let repassword = $state("");

    async function register() {
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);
        console.log(hash)

        const res = await fetch('http://localhost:8000/add_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: username,
                hashed_password: password
            })
        });

        return await res.json();
    }

    async function onsubmit(event) {
      event.preventDefault();

      if(password !== repassword) {
        console.warn("Hasła nie są identyczne");
        return;
      }
        
      await register();
      console.log('Zarejestrowano pomyślnie');

    //    window.location.href = '/thanks';
    } 
</script>

<div>Zarejestruj Się</div>
<div>
    <form {onsubmit}>
        <label for="username">Username:</label> <br>
        <input type="text" id="username" name="username" bind:value={username} required /> <br>

        <label for="password">Hasło:</label> <br>
        <input type="password" id="password" name="password" bind:value={password} required /> <br>
    
        <label for="repassword">Powtórz hasło:</label> <br>
        <input type="password" id="repassword" name="repassword" bind:value={repassword} required /> <br>
    
        <button type="submit">Zarejestruj się</button>
    </form>
    <button onclick={() => window.location.href = '/login'}>Zaloguj się</button>
</div>