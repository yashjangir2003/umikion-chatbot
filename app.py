import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_response(user_input):
    # 🔥 Excel har baar reload hoga (no cache issue)
    data = pd.read_excel("chatbot_data.xlsx").dropna()

    # normalize excel
    data['Question'] = data['Question'].astype(str).str.lower().str.strip()
    data['Answer'] = data['Answer'].astype(str)

    user_input = user_input.lower().strip()

    # ✅ STEP 1: exact match (hi, hello)
    for i in range(len(data)):
        if user_input == data['Question'][i]:
            return data['Answer'][i]

    # ✅ STEP 2: best keyword match
    best_score = 0
    best_answer = "Sorry, I didn't understand."

    for i in range(len(data)):
        question_words = data['Question'][i].split()

        score = 0
        for word in question_words:
            if word in user_input:
                score += 1

        if score > best_score:
            best_score = score
            best_answer = data['Answer'][i]

    # ✅ STEP 3: return best match
    if best_score > 0:
        return best_answer

    return "Sorry, I didn't understand."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    return jsonify({"response": get_response(user_input)})

if __name__ == "__main__":
    app.run(debug=True)