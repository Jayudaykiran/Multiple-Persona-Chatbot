from flask import Flask, request, jsonify, render_template
import cohere
import os

app = Flask(__name__)

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "dRrV13nDT200p0mV7g3hKyBfmgIAf2YWxspzO4cl")
co = cohere.Client(COHERE_API_KEY)

# Persona prompts
personas = {
    "Doctor": "You are a compassionate doctor helping patients with health advice.",
    "Travel Agent": "You are a cheerful travel agent helping users plan vacations.",
    "Teacher": "You are a patient teacher explaining academic concepts.",
    "Tech Support": "You are a friendly tech support assistant helping solve computer problems."
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data['message']
        persona = data['persona']
        system_prompt = personas.get(persona, "You are a helpful assistant.")

        response = co.chat(
            message=user_msg,
            preamble=system_prompt,
            model="command-r-plus",  # or use "command-r" / "command-light" if needed
            temperature=0.7,
        )

        reply = response.text
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
