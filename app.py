from flask import Flask, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

app = Flask( __name__) 
CORS(app)
#@app.get("/")
#def index_get():
 #   return render_template("base.html")

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = "issues"
endpoint = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

headers = {
"Authorization": f"Bearer {AIRTABLE_API_KEY}",
"Content-Type": "application/json"
}
def save_rec(username, email, issue):
    data = {
  "records": [
          {
        "fields": {
            "Username": f"{username}",
            "Email": f"{email}",
            "Issue": f"{issue}"
        }
        },
    ]
    }

    r = requests.post(endpoint, json=data , headers=headers)
    r.json()


@app.post("/issue")
def predict():
    username = request.get_json().get("username")
    email = request.get_json().get("email")
    issue = request.get_json().get("issue")
    save_rec(username,email,issue)


if   __name__ == "__main__" : 
    app.run(debug=True)
