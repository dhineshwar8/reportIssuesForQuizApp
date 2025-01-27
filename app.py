import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Enable CORS for all routes (replace "*" with your frontend domain in production)
CORS(app, origins=["*"])

# Load environment variables
AIRTABLE_PAT = os.getenv('AIRTABLE_PAT')          # Personal Access Token
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')  # Airtable Base ID
AIRTABLE_TABLE_NAME = 'issues'                    # Airtable Table Name

@app.route('/report-issue', methods=['POST'])
def report_issue():
    try:
        # Get JSON data from the request
        data = request.json
        username = data.get('username')
        email = data.get('email')
        issue = data.get('issue')

        # Validate required fields
        if not username or not email or not issue:
            return jsonify({'message': 'Missing required fields'}), 400

        # Prepare payload for Airtable
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

        # Send data to Airtable
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        return jsonify({'message': 'Issue reported successfully!'}), 200

    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Airtable: {e}")
        return jsonify({'message': 'Failed to communicate with Airtable'}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'message': 'An unexpected error occurred'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
