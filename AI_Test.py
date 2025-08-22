from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app) # Enable CORS for all routes


try:
    # summarizer = pipeline("summarization", model="t5-small")
     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    #summarizer = pipeline("summarization", model="google/pegasus-large")
   
except Exception as e:
    print(f"Error loading summarizer model: {e}")
    print("Please ensure your summarization model is correctly installed and accessible.")
    print("If you are using Keras 3 with TensorFlow, ensure 'pip install tf-keras' is run.")
    summarizer = None # Set summarizer to None if loading fails

@app.route('/summarize', methods=['POST'])
def summarize_text():
    # Check if the summarizer model was loaded successfully
    if summarizer is None:
        return jsonify({"error": "Summarization model not loaded. Please check server logs and ensure all dependencies are met."}), 500

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request. Please send JSON with a 'text' field."}), 400

    article = data['text']

    # Server-side validation for input text length
    if not isinstance(article, str):
        return jsonify({"error": "Input text must be a string."}), 400
    if len(article) == 0:
        return jsonify({"error": "Input text cannot be empty."}), 400
    if len(article) < 50: # Minimum recommended length for effective summarization
        return jsonify({"error": "Input text too short. Please provide at least 50 characters for summarization."}), 400
    if len(article) > 15000: # Max input text length to prevent excessively large requests
        return jsonify({"error": "Input text too long. Please provide text up to 15,000 characters."}), 400

    # Safely get max_length and min_length from the request, with default values
    # and robust error handling for non-integer inputs.
    try:
        # Default to common values if not provided or invalid
        max_length = int(data.get('max_length', 130))
        min_length = int(data.get('min_length', 30))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid 'max_length' or 'min_length' provided. Must be integers."}), 400

    # Server-side validation for length parameters
    if not (10 <= min_length <= 1000): # Reasonable bounds for min_length
        return jsonify({"error": "Minimum length must be between 10 and 400 tokens."}), 400
    if not (50 <= max_length <= 1000): # Reasonable bounds for max_length
        return jsonify({"error": "Maximum length must be between 50 and 500 tokens."}), 400
    if min_length >= max_length:
        return jsonify({"error": "Minimum length must be less than maximum length."}), 400


    try:
        # Perform summarization using the loaded pipeline
        # do_sample=False is typical for summarization for more deterministic and coherent output
        summary = summarizer(article, max_length=max_length, min_length=min_length, do_sample=False)

        # Check if the summary is empty or malformed after processing
        if not summary or not summary[0].get('summary_text'):
            return jsonify({"error": "Summarization model failed to produce a valid output. Try different text or parameters, or a different model."}), 500

        return jsonify({"summary": summary[0]['summary_text']})

    except Exception as e:
        # Catch any unexpected errors during summarization
        print(f"An error occurred during summarization: {e}", exc_info=True) # Log full traceback
        return jsonify({"error": f"An unexpected error occurred during summarization: {str(e)}. Please try again."}), 500

if __name__ == '__main__':
    # When running locally for development, debug=True provides useful error messages
    app.run(debug=True, port=5000)