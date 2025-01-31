from flask import Flask, render_template, request, jsonify
import spacy
import json

app = Flask(__name__)

# Load the SpaCy model for processing the user's questions
nlp = spacy.load("en_core_web_sm")

# Load the FAQ data (replace with your domain-specific data)
def load_faqs():
    with open('data/faq_data.json') as f:
        faqs = json.load(f)
    return faqs['faqs']

# Function to find the most relevant FAQ based on user input using SpaCy
def find_relevant_faq(user_question):
    # Process the user's question using SpaCy
    doc = nlp(user_question)

    # Extract the most relevant keywords (e.g., nouns, proper nouns, etc.)
    keywords = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    # Load FAQs
    faqs = load_faqs()

    # Search for the most relevant FAQ answer
    for faq in faqs:
        faq_keywords = [token.text.lower() for token in nlp(faq["question"]).doc if token.pos_ in ['NOUN', 'PROPN']]

        # Check if any of the extracted keywords match the FAQ question's keywords
        if any(keyword in faq_keywords for keyword in keywords):
            return faq["answer"]

    # If no relevant answer is found, return a default response
    return "Sorry, I don't have an answer to that question."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_faq', methods=['POST'])
def get_faq():
    user_question = request.form['user_question']

    # Use SpaCy to process and find a relevant FAQ answer
    answer = find_relevant_faq(user_question)

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
