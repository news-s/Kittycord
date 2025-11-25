<script>
    const { servers } = $props();

    let open = $state(false);

    async function CreateServer(token, server_name) {
        try {
            const res = await fetch(`http://localhost:8000/add_server`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    token: token,
                    server_name: server_name,
                    invite_link: server_name
                }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    function OpenServer(id) {
        window.location.pathname = "/app/server"
        window.location.search = "?id=" + id
        // window.location.reload();
    }
</script>

<nav class="servers">
    <a href="/app/main" title="dms">
        <div class="dms"></div>
    </a>

    {#each servers as server, id}
        <a href={`server?id=${id}`} title={id}>
            <div class="server"></div>
        </a>
    {/each}

    <button class="create-server" onclick={() => open = !open}>+</button>
</nav>

{#if open}
    <div class="modal">
        <h2>Create Server</h2>
        <input type="text" placeholder="Server Name" id="server-name"/>
        <button 
            onclick={async () => {
                const token = localStorage.getItem('token');
                const input = document.getElementById('server-name');
                const server_name = input.value;
                const id = await CreateServer(token, server_name);
                servers.push(id);
                open = false;
            }
        }>Create</button>
        <button onclick={() => open = false}>Cancel</button>
    </div>
{/if}

<style>
    .servers {
        width: 72px;
        height: 100vh;

        background-color: #ddd;

        display: flex;
        flex-direction: column;
        align-items: center;

        padding: 10px 0;

    }
    .dms, .server, .create-server {
        width: 48px;
        height: 48px;

        background-color: #bbb;
        border-radius: 50%;

        margin-bottom: 10px;
    }

    .create-server {
        background-color: #fff;
        color: #999;
        margin-top: auto;
    }

    .modal {
        width: 200px;
        height: 200px;

        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        background-color: #fff;

        padding: 20px;

        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

        border-radius: 8px;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-evenly;
    }

    #server-name {
        width: 80%;
        text-align: center;
    }
</style>