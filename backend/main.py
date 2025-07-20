from flask import Flask,request, jsonify
from flask_cors import CORS
from query import qa_chain

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "App is running"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message","")

    if not user_input:
        return jsonify({"response": f"You said: {user_input}"})
    
    
    try:
        response= qa_chain(user_input)
        answer = response["result"]
    except Exception as e:
        return jsonify({"response":f"Error:{str(e)}"})

    return jsonify({"response":answer})





if __name__ == "__main__":
    app.run(debug=True)

