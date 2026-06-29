exports.handler = async (event) => {
    const GROQ_KEY = "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";
    const TG_TOKEN = "8946598928:AAFg3Xvljjp0PBcbyrBzYeoPmlxya5tP3Jo";
    const TG_CHAT_ID = "8642564605";
    const MODEL = "llama-3.1-8b-instant";

    const body = JSON.parse(event.body);
    const path = event.path.replace("/.netlify/functions/api", "");

    // Groq API
    if (path === "/groq") {
        try {
            const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${GROQ_KEY}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            });
            const data = await resp.json();
            return {
                statusCode: resp.status,
                body: JSON.stringify(data),
                headers: { "Content-Type": "application/json" }
            };
        } catch(e) {
            return { statusCode: 500, body: JSON.stringify({ error: "API error" }) };
        }
    }

    // Telegram лог
    if (path === "/tg-log") {
        try {
            await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    chat_id: TG_CHAT_ID,
                    text: body.text.substring(0, 3500)
                })
            });
            return { statusCode: 200, body: "ok" };
        } catch(e) {
            return { statusCode: 200, body: "ok" };
        }
    }

    return { statusCode: 404, body: "not found" };
};
