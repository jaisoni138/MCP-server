# webui.py
from quart import Quart, render_template_string, request
from client_ollama import query_ollama
import asyncio

app = Quart(__name__)

HTML = """
<!doctype html>
<html>
<head>
<title>Minimal Ollama UI</title>
</head>
<body>
<h1>Minimal Ollama UI</h1>
<form id="form">
<textarea id="prompt" style="width:100%;height:100px;"></textarea><br>
<button type="submit">Send</button>
</form>
<pre id="output"></pre>
<script>
const form = document.getElementById("form");
const output = document.getElementById("output");
form.addEventListener("submit", async e => {
    e.preventDefault();
    const prompt = document.getElementById("prompt").value;
    output.textContent = "⏳ Waiting for response...";
    const res = await fetch("/ask?prompt=" + encodeURIComponent(prompt));
    const text = await res.text();
    output.textContent = text;
});
</script>
</body>
</html>
"""

@app.route("/")
async def index():
    return await render_template_string(HTML)

@app.route("/ask")
async def ask():
    prompt = request.args.get("prompt","")
    if not prompt:
        return "⚠️ No prompt provided"
    try:
        response = await query_ollama(prompt)
        return response
    except Exception as e:
        return f"❌ Error: {e}"
