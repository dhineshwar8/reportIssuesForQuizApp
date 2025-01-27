import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AIRTABLE_PAT = os.getenv('AIRTABLE_PAT')          # Load from environment variable
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')  # Load from environment variable
AIRTABLE_TABLE_NAME = 'issues'

@app.route('/report-issue', methods=['POST'])
def report_issue():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    issue = data.get('issue')

    # Send data to Airtable
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_PAT}',
        'Content-Type': 'application/json'
    }
    payload = {
        'fields': {
            'Username': username,
            'Email': email,
            'Issue': issue
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return jsonify({'message': 'Issue reported successfully!'}), 200
    else:
        return jsonify({'message': 'Failed to report issue'}), 500

if __name__ == '__main__':
    app.run(debug=True)
