LearnSphere: Your AI Study Partner 🎓

LearnSphere is an interactive, AI-powered web application built with Streamlit and Google's Gemini API. It's designed to be a personal study assistant, helping users learn new topics, test their knowledge, and summarize complex information, all in one place.

✨ Features
 * 📚 Learn: Get dynamic explanations on any topic, tailored to your chosen difficulty level.
 * 🧩 Quiz: Instantly generate 5-question multiple-choice quizzes to test your knowledge on any subject.
 * 📝 Summarize: Paste long articles, notes, or text and receive a concise, AI-generated summary.
 * 📈 History: Your learning sessions, quiz results, and summaries are saved for the duration of your session, allowing you to review your progress.
 * ⚙️ Adjustable Difficulty: A unique slider allows you to switch between Beginner, Intermediate, and Advanced modes, changing the depth and complexity of the AI's responses.

🛠️ Tech Stack
 * Frontend: Streamlit - For creating the interactive web application interface.
 * Backend Logic: Python
 * AI Model: Google Gemini API (google-generativeai)
 * Environment Management: python-dotenv - For managing API keys securely.

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.
Prerequisites
 * Python 3.9 or higher
 * A Google Gemini API Key. You can obtain one from Google AI Studio.
Installation
 * Clone the repository:
   git clone https://github.com/theprathameshkanade/learnsphere.git
   cd learnsphere

 * Create and activate a virtual environment (recommended):
   * On macOS/Linux:
     python3 -m venv venv
     source venv/bin/activate

   * On Windows:
     python -m venv venv
     .\venv\Scripts\activate

 * Install the required dependencies:
   Create a file named requirements.txt in the project's root directory and paste the following lines into it:
   streamlit
   google-generativeai
   python-dotenv

   Then, run the following command to install them:
   pip install -r requirements.txt

Configuration
 * Create a .env file in the root directory of the project.
 * Add your API key to the .env file in the following format:
   GEMINI_API_KEY="YOUR_API_KEY_HERE"

   Replace "YOUR_API_KEY_HERE" with your actual Google Gemini API key.
🏃‍♂️ Usage
Once the installation and configuration are complete, you can run the application with a single command:
streamlit run app.py

This will start the Streamlit server and the application should automatically open in your web browser.

🔮 Future Improvements
 * [ ] User accounts to save history across different sessions.
 * [ ] Database integration (e.g., SQLite, Firebase) for persistent storage.
 * [ ] More quiz types (e.g., fill-in-the-blanks, true/false).
 * [ ] Ability to summarize content directly from a URL.
 * [ ] "Flashcard" generation from learned topics.
