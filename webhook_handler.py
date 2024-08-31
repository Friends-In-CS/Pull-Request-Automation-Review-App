from flask import Flask, request, jsonify

app = Flask(__name__)

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
            # Handle pull request opened event
            repository_name = data['repository']['name']
            pull_request_number = data['pull_request']['number']
            pull_request_title = data['pull_request']['title']
            pull_request_body = data['pull_request']['body']
            pull_request_url = data['pull_request']['html_url']
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