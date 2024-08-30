from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    
    if request.method == 'POST':
        data = request.json
        # Process the webhook payload
        print(data)

    if data['action'] == 'created':
            # Handle repository creation event
            repository_name = data['repository']['name']
            print(f"New repository created: {repository_name}")
            # Add your custom logic here

    elif data['action'] == 'push':
            # Handle push event
            repository_name = data['repository']['name']
            branch = data['ref'].split('/')[-1]
            print(f"Push event received for repository: {repository_name}, branch: {branch}")
            # Add your custom logic here

    elif data['action'] == 'opened' and 'pull_request' in data:
            # Handle pull request opened event
            repository_name = data['repository']['name']
            pull_request_number = data['pull_request']['number']
            pull_request_title = data['pull_request']['title']
            pull_request_body = data['pull_request']['body']
            pull_request_url = data['pull_request']['html_url']
            
            print(f"Pull request opened for repository: {repository_name}")
            print(f"Pull request number: {pull_request_number}")
            print(f"Pull request title: {pull_request_title}")
            print(f"Pull request body:")
            print(pull_request_body)
            print(f"Pull request URL: {pull_request_url}")
            
            # Extract the changed files
            changed_files = data['pull_request']['changed_files']
            print(f"Number of changed files: {changed_files}")
            
            # Extract the commits
            commits_url = data['pull_request']['commits_url']
            # Additional API request to retrieve the commits data
            # using the `commits_url` if needed
            print()
            print(commits_url)
            print()
            return jsonify({'status': 'success'}), 200        
    elif data['action'] == 'closed' and 'pull_request' in data:
            # Handle pull request closed event
            repository_name = data['repository']['name']
            pull_request_number = data['pull_request']['number']
            print(f"Pull request closed for repository: {repository_name}")
            print(f"Pull request number: {pull_request_number}")
            # Add your custom logic here

    
            return jsonify({'status': 'success'}), 200
    
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'}), 400

if __name__ == 'main':
     app.run(port=3000)