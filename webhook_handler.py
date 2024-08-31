import os
import datetime
import requests
import jwt
from flask import Flask, request, jsonify
from pull_request_getter import get_pull_request
from pathlib import Path
APP_ID = 984766
PRIV_KEY_PATH = Path("privatekey.pem")
#INSTALLATION_ID = os.environ.get('GITHUB_INSTALLATION_ID')

app = Flask(__name__)

# Read the private key
with open(PRIV_KEY_PATH, 'r') as file:
    private_key = file.read()

def generate_jwt_token():
    payload = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        'iss': APP_ID
    }
    jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
    return jwt_token
def get_installation_id():
    jwt_token = generate_jwt_token()
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = 'https://api.github.com/app/installations'
    response = requests.get(url, headers=headers)
    installations = response.json()
    if installations:
        installation_id = installations[0]['id']
        return installation_id
    else:
        return None

def get_installation_access_token(installation_id):
    jwt_token = generate_jwt_token()
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    response = requests.post(url, headers=headers)
    access_token = response.json()['token']
    return access_token

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        data = request.json
        
        # Validate that JSON data is present
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON payload found'}), 400
        
        # Safely access 'action' and other keys
        action = data.get('action', None)
     

        if action == 'opened' and 'pull_request' in data:
             installation_id = get_installation_id()
             if installation_id:
                access_token = get_installation_access_token(installation_id)
                # Handle pull request opened event
                repository_name = data['repository']['name']
                pull_request_number = data['pull_request']['number']
                pull_request_title = data['pull_request']['title']
                pull_request_body = data['pull_request']['body']
                pull_request_url = data['pull_request']['url']
                # Extract the repository name
                #print(f"Pull request opened for repository: {repository_name}")
                # Extract the repository number
                #print(f"Pull request number: {pull_request_number}")
                # Extract the repository title
                #print(f"Pull request title: {pull_request_title}")
                # Extract the pull request body
                print(f"Pull request body:")
                print(pull_request_body)
                # Extract the pull request url
                #print(f"Pull request URL: {pull_request_url}")
                
                # Extract the changed files
                changed_files = data['pull_request']['changed_files']
                print(f"Number of changed files: {changed_files}")
                # Extract the commits
                commits_url = data['pull_request']['commits_url']
                # Additional API request to retrieve the commits data
                # using the `commits_url` if needed
                print(commits_url)
                result = get_pull_request(pull_request_url, access_token)
                print(result)
             else:
                print('No installations found for the app.')
             return jsonify({'status': 'success'}), 200       
        
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported action or missing data'}), 400

        '''elif action == 'closed' and 'pull_request' in data:
            # Handle pull request closed event
            repository_name = data.get('repository', {}).get('name', 'Unknown')
            pull_request_number = data['pull_request'].get('number', 'Unknown')
            print(f"Pull request closed for repository: {repository_name}")
            print(f"Pull request number: {pull_request_number}")
            # Add your custom logic here
            return jsonify({'status': 'success', 'message': 'Pull request closed handled'}), 200'''

        

    return jsonify({'status': 'error', 'message': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(port=3000)


## COMMANDS TO RUN IN TERMINAL
## flask --app webhook_handler  run -p 3000