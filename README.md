# AI Blog App
---

**Creator:** Halleluyah Oludele
**Contact:** [here](mailto:halleuyaholudele@gmail.com)
**Try it out at:** [AI Blog App](https://ai-blog-app-aye3.onrender.com)

## Overview
---

AI Blog App is a Django-based web application that allows users to generate high-quality blog articles, LinkedIn posts, and tweets from YouTube video links using AI technologies. The app extracts the transcript from the provided YouTube link and uses Generative AI to create content based on the transcript.

## Features
---

- **User Authentication:** Secure user registration, login, and logout functionality.
- **YouTube Video Transcription:** Extracts transcripts from YouTube videos.
- **Content Generation:** Converts transcripts into blog articles, LinkedIn posts, or tweets using Generative AI.
- **Blog Management:** Allows users to view, create, and delete generated content.
- **Responsive Design:** User-friendly interface with responsive design using Tailwind CSS.

## Technologies Used
---

- **Backend:** Django
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** PostgreSQL
- **APIs and Libraries:** 
  - pytube for YouTube video extraction
  - YouTube Transcript API for transcript extraction
  - AssemblyAI for audio transcription
  - Google Generative AI for content generation
- **Environment Management:** `python-dotenv`

## Installation and Setup
---

### Prerequisites

- Python 3.11.5
- PostgreSQL
- Tailwind CDN  for the tailwind css

### Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```env
SECRET_KEY=<your-django-secret-key>
GOOGLE_API_KEY=<your-google-api-key>
ASSEMBLY_AI_API_KEY=<your-assembly-ai-api-key>
DATABASE_NAME=<your-database-name>
DATABASE_USER=<your-database-user>
DATABASE_PASSWORD=<your-database-password>
DATABASE_HOST=<your-database-host>
DATABASE_PORT=<your-database-port>
```

### Steps to Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ai-blog-app
   ```

2. **Create and activate a virtual environment:**

   ```bash
   pipenv shell
   ```

3. **Install the dependencies:**

   ```bash
   pipenv install requirements.txt
   ```

4. **Setup the database:**

   Ensure your PostgreSQL server is running and then run:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage
---
### User Authentication

- **Sign Up:** Create a new account.
- **Login:** Access your account.
- **Logout:** Securely log out of your account.

### Generate Content

1. **Enter YouTube Link:** Provide a link to the YouTube video you want to generate content from.
2. **Select Content Type:** Choose the type of content you want to generate (Blog Article, LinkedIn Post, or Tweet).
3. **Generate:** Click on the 'Generate' button to create the content.

### View and Manage Blogs

- **Blog List:** View a list of all generated blog articles.
- **Blog Details:** View the details of a specific blog article.
- **Delete Blog:** Remove unwanted blog articles.

## Code Overview
---

### Models

- **BlogPost:** Represents a blog post with fields for user, YouTube title, URL, content type, generated content, and creation timestamp.

### Views

- **index:** Renders the homepage.
- **user_login:** Handles user login.
- **generate_blog:** Processes the YouTube link, extracts the transcript, generates content, and saves it to the database.
- **blog_list:** Displays a list of all blogs created by the user.
- **blog_article_by_id:** Displays details of a specific blog article.
- **delete_blog:** Deletes a specified blog article.
- **user_signup:** Handles user registration.
- **user_logout:** Handles user logout.

### Frontend

- **index.html:** Main template for the homepage.
- **details.html:** Template for displaying blog details.
- **blogs.html:** Template for displaying the list of blogs.

### API Keys and Environment Variables

Ensure you keep your API keys secure and do not expose them publicly. Use the `.env` file to manage your environment variables securely.

## Contributing
---

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License
---

This project is licensed under the MIT License.

---