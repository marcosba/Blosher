# Blosher - Blogger Publisher

This project is a simple Blogger application built using Flask. It allows users to publish content to their Blogger account using the Google Blogger API. The application takes Markdown-formatted text, converts it to HTML, and publishes it as a blog post.

## Project Overview

The application provides a user-friendly interface where users can:
- Input Markdown content directly in a textarea or upload a `.md` file.
- Automatically extract the title from the first line of the Markdown content (formatted as an H1 header).
- Publish the content to a specified Blogger account.

## Requirements

To ensure the application works without issues, the following are required:

### Software Requirements
- **Python 3.x**: Ensure Python is installed and added to your system's PATH.
- **Flask**: A lightweight web framework for Python.
- **Flask-CORS**: To handle cross-origin requests.
- **Markdown**: For converting Markdown content to HTML.
- **Google API libraries**: For authenticating and interacting with the Blogger API.

### Setup Requirements
1. **Google API Credentials**:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Blogger API for your project.
   - Create OAuth 2.0 credentials and download the JSON file.
   - Place the JSON file in the project directory and name it `client_secrets.json`.

2. **Blogger Account**:
   - Ensure you have a Blogger account and a blog where the posts will be published.
   - Note down your blog's ID, which is required for publishing posts.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/marcosba/Blosher.git
   cd Blosher
   ```

2. **Install dependencies:**
   Make sure you have `pip` installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Google Authentication:**
   - Place the `client_secrets.json` file in the project directory.
   - Ensure the file contains valid credentials for accessing the Blogger API.

4. **Run the Flask server:**
   Start the application by running:
   ```bash
   python blosher.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000` to access the Blogger application.

## Text Format Requirements

To ensure the application processes your content correctly, follow these guidelines for the Markdown text:

1. **Title**:
   - The first line of the content must be an H1 header (e.g., `# My Blog Post Title`).
   - This line will be used as the title of the blog post.
   - Example:
     ```markdown
     # My Blog Post Title
     ```

2. **Content**:
   - The rest of the text will be treated as the body of the blog post.
   - Use standard Markdown syntax for formatting (e.g., paragraphs, lists, images, etc.).
   - Example:
     ```markdown
     # My Blog Post Title

     This is the body of the blog post. You can use **bold text**, *italic text*, and other Markdown features.

     - Item 1
     - Item 2
     ```

3. **File Format**:
   - If uploading a file, ensure it is a valid `.md` file with UTF-8 encoding.

## API Usage

The application provides a RESTful API to interact with the Blogger functionality. Below are the available endpoints and how to use them:

### 1. **Check Server Status**
- **Endpoint**: `GET /status`
- **Description**: Verifies if the server is running.
- **Response**:
  ```json
  {
    "status": "Server is running"
  }
  ```
- **How to Test**:
  - Open your browser and go to `http://127.0.0.1:5000/status`.

---

### 2. **Publish a Post**
- **Endpoint**: `POST /publish`
- **Description**: Publishes a post to Blogger.
- **Request Body**:
  ```json
  {
    "content": "# My Blog Post Title\nThis is the body of the blog post."
  }
  ```
- **Response**:
  - **Success**:
    ```json
    {
      "success": "Post published successfully!",
      "url": "https://your-blog-url"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Error message"
    }
    ```
- **How to Test**:
  - Use a tool like Postman or `curl` to send a `POST` request:
    ```bash
    curl -X POST http://127.0.0.1:5000/publish \
    -H "Content-Type: application/json" \
    -d '{"content": "# My Blog Post Title\nThis is the body of the blog post."}'
    ```

---

### 3. **List Blogs**
- **Endpoint**: `GET /blogs`
- **Description**: Lists all blogs associated with the authenticated account.
- **Response**:
  - **Success**:
    ```json
    {
      "blogs": [
        {
          "id": "123456789",
          "name": "My Blog",
          "url": "https://my-blog-url"
        }
      ]
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Authentication required"
    }
    ```
- **How to Test**:
  - Open your browser and go to `http://127.0.0.1:5000/blogs`.

---

## Troubleshooting

- If the application fails to publish, ensure:
  - The `client_secrets.json` file is correctly configured.
  - The content includes a valid H1 header for the title.
  - The Blogger API is enabled in your Google Cloud project.

## License

This project is licensed under the MIT License.
