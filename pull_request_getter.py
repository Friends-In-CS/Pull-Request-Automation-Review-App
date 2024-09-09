import requests



def get_pull_request(pull_url:str, access_token:str, ):
    """
    This function is used to query the github pull request api to get the content of the code and 
    difference in code and comment on the pull request using the Chatgpt llm. 
    """
    # Set up authentication
    headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
    # Get the pull request details

    response = requests.get(pull_url, headers=headers)
    pull_request_data = response.json()

    # Get the URL for the pull request differnce
    diff_url = pull_request_data['diff_url']
    print(f'Difference url {diff_url}')

    # Retrieve the diff
    response = requests.get(diff_url, headers=headers)
    diff_text = response.text
    print(f'Difference text: {diff_text}')

    # Process the diff and identify the changes
    #Possibly use `difflib` to parse the diff and extract the changes?
    # Example:
    # import difflib
    # diff = difflib.unified_diff(...)

    # Leave comments on the pull request
    comments_url = pull_request_data['comments_url']

    # Example comment data
    comment_data = {
        'body': 'This is a comment on the pull request. This code needs review!',
        'path': 'app\page.js',
        'position': 10  # Line number to comment on
    }

    # Send a POST request to create the comment
    response = requests.post(comments_url, headers=headers, json=comment_data)

    # Check the response status code
    if response.status_code == 201:
        return 'Comment created successfully!'
    else:
        return 'Failed to create comment:', response.text