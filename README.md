Demo: [https://text-file-translation-system-12.onrender.com/](https://text-file-translation-system-12.onrender.com/)
 File Translation Service

A simple web application that allows users to upload text files, translate them to a desired language, and download the translated files. The app also keeps a history of translations and allows users to download or delete previous translations.

 Features

- Upload a file: Users can upload text files for translation.
- Language selection: Choose a target language from a list of supported languages.
- Translate the content: The app uses the Google Translate API to translate the content of the uploaded file.
- Translation history: View, download, and delete previous translations.
- Download translated file: Once translated, users can download the translated content in a text file.

 Technologies Used

- FastAPI: A modern, fast web framework for building APIs with Python 3.7+.
- Google Translate API: For translating text.
- HTML/CSS/JavaScript: For the frontend, providing a user-friendly interface.
- File handling: Supports file uploads and downloads.

 Installation

1. Clone the repository:
   git clone https://github.com/Emon16A/Text-File-Translation-System.git
   

2. Install dependencies:
   Use a virtual environment to install dependencies.
   cd file-translation-service
   python -m venv venv
   source venv/bin/activate   On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   

3. Start the FastAPI server:
   uvicorn app.main:app --reload
   

   The server will be running on `http://localhost:8000`.

 Folder Structure

- app: Main application folder containing the FastAPI backend.
  - routes: Contains the different API route handlers (e.g., upload, download, history).
  - static: Folder for static files like images, CSS, and JavaScript.
  - templates: Folder for HTML templates.
- static/css: Contains styles for the frontend.
- static/js: Contains the JavaScript for the frontend.

 Endpoints

- `GET /`: Serves the main HTML page.
- `POST /api/upload/`: Upload a file and translate it to a chosen language.
- `GET /api/languages`: Get a list of supported languages for translation.
- `GET /api/upload/history`: Get the history of translations.
- `GET /api/upload/download/{history_id}`: Download a previous translation based on history ID.
- `DELETE /api/upload/delete/{history_id}`: Delete a translation history item.

 How to Use

 1. Upload a File
- Go to the main page and use the form to upload a text file.
- Select the target language you want to translate the file into from the dropdown list.
- Click Upload and Translate to send the file to the server.

 2. Translation Results
- After the translation is complete, the translated text will appear on the page.
- You can download the translated text as a `.txt` file.

 3. Translation History
- View the translation history below the main form.
- Each history entry displays the translated text's preview and buttons to download or delete the translation.
- You can click Download Translation to download a translated file or Delete to remove an entry from the history.

 Example Request for Translation

The `/api/upload/` endpoint accepts a POST request with a file and a language to translate to. Here's an example using `curl`:

bash
curl -X 'POST' \
  'http://localhost:8000/api/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.txt' \
  -F 'language=en'


 Example Response
json
{
  "original": "This is the original text.",
  "translated": "This is the translated text.",
  "language": "en",
  "id": 1
}


 Frontend

The frontend is a simple HTML, CSS, and JavaScript-based interface. 

 Key Files:

- `index.html`: The main template for rendering the page.
- `style.css`: Contains styles for the page layout and buttons.
- `app.js`: Handles frontend logic like submitting the form, fetching supported languages, showing translation results, and handling history.

 Styling

- The page uses light colors with a gradient background for a soft, modern look.
- Buttons are styled with gradients and hover effects for a more interactive experience.

 Contribution

1. Fork the repository.
2. Clone your fork:
   git clone https://github.com/Emon16A/Text-File-Translation-System.git
   
3. Create a new branch for your feature or fix:
   git checkout -b feature-name
   
4. Make changes and commit them:
   git commit -am 'Add new feature'
   
5. Push to your forked repository:
   git push origin feature-name
   
6. Create a Pull Request to the main repository.

 License

MIT License. See `LICENSE` for more information.

Happy translating! 🎉


 Explanation of the `README.md`:
1. Introduction and Features: Describes the functionality and technologies used in the app.
2. Installation: Provides the steps for cloning and setting up the project.
3. Folder Structure: Gives an overview of the project directory layout.
4. Endpoints: Lists the available API endpoints.
5. Usage Instructions: Describes how users can interact with the app through the UI.
6. Frontend Details: Briefly explains the structure of the frontend.
7. Contribution: Instructions for contributing to the project.
8. License: Mentions the project license.

Feel free to customize any part of the `README.md` as per your project’s specific needs or improvements!