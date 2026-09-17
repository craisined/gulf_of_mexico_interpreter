from flask import Flask, render_template, request
from openrouter import OpenRouter
import os

API_HOST = os.getenv("API_HOST", default="https://ai.hackclub.com/proxy/v1")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL", default="~openai/gpt-luna-latest")
if API_KEY is None:
    raise ValueError("API Key not found!")

app = Flask(__name__)
ai_client = OpenRouter(
    api_key=API_KEY,
    server_url=API_HOST
)

with open("prompt.md") as prompt_file:
    system_prompt = prompt_file.read()
user_prompt = "What would you expect this program to log to the console? Only output the console logs."

def compiler(code):
    response = ai_client.chat.send(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}\n```{code}```"}
        ],
        temperature=0
    )
    return response.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=['POST'])
def api():
    code = request.form.get('code')
    output = compiler(code)
    return output

if __name__=="__main__":
    app.run()