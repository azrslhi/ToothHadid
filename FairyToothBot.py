from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__, template_folder='templates')

openai.api_key = 'sk-proj-your-api-key-here' 
        
def predefined_responses(user_input):
    if "appointment" in user_input:
        return "Please fill out the form and we will contact you as soon as possible."
    elif "location" in user_input:
        return "Your Location"
    elif "time open" in user_input:
        return "Our Tooth Hadid dental clinic operating hours are from 9 AM to 9 PM everyday (10 AM to 7 PM for public holiday)"
    elif "operating hours" in user_input:
        return "Our Tooth Hadid dental clinic operating hours are from 9 AM to 9 PM everyday (10 AM to 7 PM for public holiday)"
    elif "service" in user_input:
        return "Services available at our Tooth Hadid dental clinic are such as Diagnosis & Examination, Scaling & Polishing, Whitening and Braces"
    else:
        return None

def chat_api(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'You are a dentist virtual assistant named Fairy Toothbot of Tooth Hadid Dental Clinic to give advice and respond only about dental and no others.'},
                {"role": "user", "content": user_input} 
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print("Error generating OpenAI Chat response:", e)
        return "I'm sorry, I didn't understand that. Could you please rephrase or ask something else?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    predefined_response = predefined_responses(user_message)
    if predefined_response:
        return jsonify({'message': predefined_response})
    
    bot_message = chat_api(user_message)
    return jsonify({'message': bot_message})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
