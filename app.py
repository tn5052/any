from flask import Flask, request, jsonify
from textblob import TextBlob
import re
import time
from groq import Groq

app = Flask(__name__)


# Replace with your actual Groq API key
client = Groq(
    api_key="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",
)

def use_llama_api(prompt, max_tokens=1000):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during text processing: {e}")
        return prompt

def regenerate_text(text):
    return use_llama_api(f"Regenerate the following text without adding any extra information and ensure don't add any extra text, gimme only folowing generated text and ensure very simple and easy to understandable wording:\n{text}")

def simplify_text(text):
    return use_llama_api(f"Simplify the following text in very easy and simple wording and ensure don't add any extra text, gimme only folowing generated text:\n{text}")

def shorten_text(text):
    return use_llama_api(f"Shorten the following text in very easy and simple wording and ensure don't add any extra text, gimme only folowing generated text:\n{text}")

def extend_text(text):
    return use_llama_api(f"Extend the following text in very simple and easy to understandable wording:\n{text}")

def humanize_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return use_llama_api(f"Humanize the following text in very simple and easy to understand wording:\n{text}")






@app.route('/api/simplify', methods=['POST'])
def simplify():
    data = request.get_json() 
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    simplified_text = simplify_text(text)
    humanized_result = humanize_text(simplified_text)
    return jsonify({'result': humanized_result})

@app.route('/api/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    shortened_text = shorten_text(text)
    humanized_result = humanize_text(shortened_text)
    return jsonify({'result': humanized_result})

@app.route('/api/extend', methods=['POST'])
def extend():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    extended_text = extend_text(text)
    humanized_result = humanize_text(extended_text)
    return jsonify({'result': humanized_result})

@app.route('/api/regenerate', methods=['POST'])
def regenerate():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    regenerated_text = regenerate_text(text)
    humanized_result = humanize_text(regenerated_text)
    return jsonify({'result': humanized_result})

if __name__ == '__main__':
    app.run(debug=True, port=5001)