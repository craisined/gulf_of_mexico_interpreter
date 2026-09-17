""" <- evil triple quotes so the Python functions. this file functions as markdown, html, and python, although github tends to be less happy with the markdown. made because i felt the need to make something cursed
<html>
<body>
<hgroup>
<h1>gulf of mexico compiler</h1>
<p>up to spec with the <a href="https://github.com/TodePond/GulfOfMexico">original gulf of mexico specification</a> as of 9/16/26. made by <a href="https://craisin.tech">@craisin</a></p>
</hgroup>
<h2>usage</h2>
<p>head to <a href="https://gulfofmexico.craisin.tech">here</a> to see this abomination in action! this uses my hackclub ai api, so note that this might break depending on the uptime of that</p>
<h3>deployment</h3>
<p>create a .env file specifiying API_KEY, and optionally specifiying API_HOST (openrouter endpoint) and MODEL</p>
<code>pip install Flask openrouter python-dotenv<br>
python3 README.md</code>
<h2>code</h2>
<form>
<textarea name="code"></textarea><br>
<button type="submit">run code</button>
</form>
<h2>output</h2>
<div class="output"></div>
</body>
<head>
<script>
document.querySelector("form").addEventListener("submit", async function (event) {
event.preventDefault();
const formData = new FormData(event.target);
const response = await fetch("/api", {
method: 'POST',
body: formData
});
if (response.ok) {
const output = await response.text();
document.querySelector(".output").textContent = output;
}
})
</script>
<title>gulf of mexico compiler</title>
</head>
</html>
<!-- """
from contextlib import suppress
from dotenv import load_dotenv
from flask import Flask, render_template, request
from openrouter import OpenRouter
import os
load_dotenv()
API_HOST = os.getenv("API_HOST", default="https://ai.hackclub.com/proxy/v1")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL", default="~openai/gpt-luna-latest")
if API_KEY is None: raise ValueError("API Key not found!")
app = Flask(__name__)
ai_client = OpenRouter(api_key=API_KEY, server_url=API_HOST)
with open("README.md") as website_file: website_html = website_file.read()
with open("prompt.md") as prompt_file: system_prompt = prompt_file.read()
user_prompt = "What would you expect this program to log to the console? Only output the console logs."
compiler = lambda code: ai_client.chat.send(model=MODEL, messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"{user_prompt}\n```{code}```"}], temperature=0).choices[0].message.content
index = lambda: website_html
api = lambda: compiler(request.form.get('code'))
index.__name__, api.__name__ = "index", "api"
app.route("/")(index)
app.route("/api", methods=['POST'])(api)
if __name__=="__main__": app.run(host="0.0.0.0")
# --->