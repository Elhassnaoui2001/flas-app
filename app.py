from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/omidroshani/imdb-sentiment-analysis"
HEADERS = {"Authorization": "Bearer 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"}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['text']
        payload = {"inputs": user_input}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        result = response.json()

        # Debugging: Print the full API response
        print("API Response:", result)

        try:
            # Access the result and find the label with the highest score
            highest_score_label = max(result[0], key=lambda x: x['score'])['label']
            # Map 'LABEL_1' to 'POSITIVE' and 'LABEL_0' to 'NEGATIVE'
            sentiment = "POSITIVE" if highest_score_label == "LABEL_1" else "NEGATIVE"
        except Exception as e:
            print("Error processing the response:", e)
            sentiment = "Error in processing API response"

        return render_template('index.html', sentiment=sentiment, user_input=user_input)
    return render_template('index.html', sentiment=None, user_input=None)

if __name__ == '__main__':
    app.run(debug=True)
