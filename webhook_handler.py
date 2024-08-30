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

        if action == 'created':
            # Handle repository creation event
            repository_name = data.get('repository', {}).get('name', 'Unknown')
            print(f"New repository created: {repository_name}")
            # Add your custom logic here
            return jsonify({'status': 'success', 'message': 'Repository creation handled'}), 200

        elif action == 'push':
            # Handle push event
            repository_name = data.get('repository', {}).get('name', 'Unknown')
            branch = data.get('ref', '').split('/')[-1]
            print(f"Push event received for repository: {repository_name}, branch: {branch}")
            # Add your custom logic here
            return jsonify({'status': 'success', 'message': 'Push event handled'}), 200

        elif action == 'opened' and 'pull_request' in data:
            # Handle pull request opened event
            repository_name = data.get('repository', {}).get('name', 'Unknown')
            pull_request_number = data['pull_request'].get('number', 'Unknown')
            pull_request_title = data['pull_request'].get('title', 'Unknown')
            print(f"Pull request opened for repository: {repository_name}")
            print(f"Pull request number: {pull_request_number}")
            print(f"Pull request title: {pull_request_title}")
            # Add your custom logic here
            return jsonify({'status': 'success', 'message': 'Pull request opened handled'}), 200

        elif action == 'closed' and 'pull_request' in data:
            # Handle pull request closed event
            repository_name = data.get('repository', {}).get('name', 'Unknown')
            pull_request_number = data['pull_request'].get('number', 'Unknown')
            print(f"Pull request closed for repository: {repository_name}")
            print(f"Pull request number: {pull_request_number}")
            # Add your custom logic here
            return jsonify({'status': 'success', 'message': 'Pull request closed handled'}), 200

        else:
            return jsonify({'status': 'error', 'message': 'Unsupported action or missing data'}), 400

    return jsonify({'status': 'error', 'message': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(port=3000)


## COMMANDS TO RUN IN TERMINAL
## flask --app /Users/cise7/Desktop/Pull-Request-Bot/Pull-Request-Automation-Review-App/webhook_handler.py run -p 3000