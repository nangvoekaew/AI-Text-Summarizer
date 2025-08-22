# AI-Text-Summarizer
An AI-powered tool to summarize text. This application has a backend made with Python and a Flask server that uses a Hugging Face Transformers model for summarization. The frontend is a user-friendly website made with HTML, CSS, and JavaScript.

# Feature
Summarize text using a pre-trained AI model.

Control the length of the summary by setting minimum and maximum token counts.

See the number of characters and words in both your input and the final summary.

The application checks your input text and settings on both the website and the server to prevent errors.

Copy the summary to your clipboard with one click.

The design is modern with a dark theme.

Shows a loading animation and status messages while it works.

# How to use
Set up the server: You'll need Python, Flask, flask_cors, and transformers. Install these using pip, for example, pip install Flask flask_cors transformers torch. Then run the server from your command line with python AI_Test.py.

Open the website: Open the AI_TextSummarizer.html file in your web browser.

Summarize: Type or paste your text into the box. You can change the summary length by typing in new numbers for "Min Length" and "Max Length". Click the "Summarize Text" button to get the result.

# Files
AI_Test.py: This is the Python file for the server. It handles the summarization process and checks for bad input.

AI_TextSummarizer.html: This is the main website file. It has all the buttons and text boxes you see. The JavaScript code inside this file talks to the server to get the summary.

AI_TextSummarizer.css: This file makes the website look good with its colors and layout.

# Thanks
Hugging Face: For the tools that make the AI part possible.

Juny & Leon (STIU Students): The people who made this project.
