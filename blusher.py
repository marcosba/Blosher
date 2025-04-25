from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import markdown
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

app = Flask(__name__)
CORS(app)

# Replace with your own CLIENT_SECRETS_FILE
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/blogger']

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/publish', methods=['POST'])
def publish():
    """
    Publish a post to Blogger.
    ---
    Request Body:
    {
        "content": "# Title\nBody of the post in Markdown"
    }
    Response:
    - Success: {"success": "Post published successfully!", "url": "https://blog-url"}
    - Error: {"error": "Error message"}
    """
    data = request.get_json()
    app.logger.info(f"Datos recibidos: {data}")

    content = data.get('content')
    if not content:
        return jsonify({"error": "Content is required"}), 400

    # Extract title from the first line
    lines = content.splitlines()
    title = None
    if lines and lines[0].startswith('# '):
        title = lines[0][2:].strip()
        content = '\n'.join(lines[1:])
    if not title:
        return jsonify({"error": "Title is required (H1 in Markdown)"}), 400

    # Convert Markdown to HTML
    html_content = markdown.markdown(content)

    # Handle credentials
    credentials_file = 'credentials.json'
    credentials = None
    if os.path.exists(credentials_file):
        credentials = Credentials.from_authorized_user_file(credentials_file, SCOPES)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open(credentials_file, 'w') as token:
            token.write(credentials.to_json())

    blogger = googleapiclient.discovery.build('blogger', 'v3', credentials=credentials)

    # Replace with your own blog ID
    blog_id = 'YOUR-BLOG-ID'
    request_body = {
        'kind': 'blogger#post',
        'title': title,
        'content': html_content
    }

    try:
        response = blogger.posts().insert(blogId=blog_id, body=request_body).execute()
        post_url = response.get('url')
        return jsonify({"success": "Post published successfully!", "url": post_url})
    except googleapiclient.errors.HttpError as error:
        return jsonify({"error": f"An error occurred: {error}"}), 500

@app.route('/status', methods=['GET'])
def status():
    """
    Check the status of the server.
    ---
    Response:
    {"status": "Server is running"}
    """
    return jsonify({"status": "Server is running"})

@app.route('/blogs', methods=['GET'])
def list_blogs():
    """
    List all blogs associated with the authenticated account.
    ---
    Response:
    - Success: {"blogs": [{"id": "123", "name": "My Blog", "url": "https://blog-url"}]}
    - Error: {"error": "Error message"}
    """
    credentials_file = 'credentials.json'
    if not os.path.exists(credentials_file):
        return jsonify({"error": "Authentication required"}), 401

    credentials = Credentials.from_authorized_user_file(credentials_file, SCOPES)
    blogger = googleapiclient.discovery.build('blogger', 'v3', credentials=credentials)

    try:
        response = blogger.blogs().listByUser(userId='self').execute()
        blogs = [{"id": blog['id'], "name": blog['name'], "url": blog['url']} for blog in response.get('items', [])]
        return jsonify({"blogs": blogs})
    except googleapiclient.errors.HttpError as error:
        return jsonify({"error": f"An error occurred: {error}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
