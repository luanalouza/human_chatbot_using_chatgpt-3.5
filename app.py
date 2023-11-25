from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key securely
openai.api_key = 'your_API_Key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    try:
        user_message = request.form['message']
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        # Use the OpenAI API to generate a response
        if user_message.lower() == 'hi':
            # Include the system message for the first message
            prompt = "You are a helpful assistant for an internet company. Offer plans and ask if the user needs help. Stay within the script."
        elif user_message.lower() == 'tell me about your internet plans':
            # If the user inquires about internet plans, guide the conversation accordingly
            prompt = "Tell me about your internet plans."
        else:
            # For other messages, omit the system message
            prompt = f"English: {user_message}"

        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,  # You can adjust temperature to control randomness
            stop=None  # You can add stop words to limit the response length
        )

        # Extract the generated response content
        ai_response = completion['choices'][0]['text']
        print(f"Generated response: {ai_response}")

        return jsonify({'message': ai_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
