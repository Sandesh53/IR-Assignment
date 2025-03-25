from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

model = joblib.load("news_classification_model.pkl")

app = Flask(__name__)
CORS(app)
@app.route("/predictions", methods=["GET", "POST"])
def predictions():
    if request.method == "GET":
        return jsonify({"message": "Send a POST request with input features to get a prediction"})

    elif request.method == "POST":
        try:
            data = request.get_json()

            if isinstance(data["text"], str):
                text = [data["text"]]
            elif isinstance(data["text"], list):
                text = data["text"]
            else:
                return jsonify({"error": "Invalid input format. Provide a string or a list of strings."})

            prediction = model.predict(text)

            return jsonify({"prediction": prediction.tolist()})

        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
