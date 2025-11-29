export async function FetchData(end_point, method, body) {
    //validacja inputu
    if( /undefined/.test(end_point) )return "invalid input";
    if( method !== "GET") {
        for(const key in body) {
            let value = body[key];

            if(typeof value === "string")value = value.trim();
            if(!value)return "invalid input";
        }
    }

    //fetchowanie
    try {
        const res = await fetch(`http://localhost:8000/${end_point}`, {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });
        
        if (!res.ok) {
            return res.status;
        }
        
        return res.json();
    } catch (err) {
        console.error(err);
    }
}