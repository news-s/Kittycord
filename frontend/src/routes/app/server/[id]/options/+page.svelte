<script>    
    import { page } from "$app/stores";

    const server_id = $page.params.id;

    let server_name = "";
    let updated_server_name = $state(server_name);

    let server_link = "";
    let updated_server_link = $state(server_link);

    async function EditServerName() {
        updated_server_name = updated_server_name.trim();
        if(server_name === updated_server_name || !updated_server_name)return;

        const token = localStorage.getItem("token");
        server_name = updated_server_name

        try {
            const res = await fetch(`http://localhost:8000/edit_server/name`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id,
                    new_val: server_name
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    async function EditServerLink() {
        updated_server_link = updated_server_link.trim();
        if(server_link === updated_server_link || !updated_server_link)return;
        
        const token = localStorage.getItem("token");
        server_link = updated_server_link;

        try {
            const res = await fetch(`http://localhost:8000/edit_server/link`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id,
                    new_link: server_link
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

            return res.json();
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    function UpdateServer() {
        console.log("update");

        EditServerName();
        EditServerLink();
    }

    async function DeleteServer() {
        const token = localStorage.getItem("token");

        try {
            const res = await fetch(`http://localhost:8000/remove_server`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    server_id: server_id
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }

        } catch (err) {
            console.error("Fetch error:", err);
        }

        window.location.href = "/app/main";
    }

    async function () {
        
    }

</script>
<div class="options-wrapper">
    <form>
        <input type="text" bind:value={updated_server_name} />
        <input type="text" bind:value={updated_server_link} />
        <input type="submit" onclick={UpdateServer} value="Update"/>
    </form>
    
    <div>
        
    </div>

    <button onclick={DeleteServer}>Delete</button>
</div>

<style>
    .options-wrapper {
        width: 100%;
        height: 100%;

        display: flex;
        flex-direction: column;
        gap: 50px;
        
        align-items: center;

        overflow-y: scroll; 
    }

    form {
        height: fit-content;

        display: flex;
        flex-direction: column;

        border: 1px solid #999;
    }

    input {
        border: 1px solid #999;
    }

    button {
        border: 1px solid #999;
    }
</style>