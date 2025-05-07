from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
account_sid = "your_account_sid"
auth_token = "your_auth_token"
twilio_whatsapp_number = "whatsapp:+14155238886"  # Replace with Twilio's WhatsApp number
client = Client(account_sid, auth_token)

tokenizer = AutoTokenizer.from_pretrained("Felladrin/Pythia-31M-Chat-v1")
model = AutoModelForCausalLM.from_pretrained("Felladrin/Pythia-31M-Chat-v1")


RISK_KEYWORDS = ["hurt", "suicidal", "end my life", "self-harm", "depressed", "hopeless"]

def contains_risk_keywords(response):
    return any(keyword in response.lower() for keyword in RISK_KEYWORDS)

def escalate_message():
    return jsonify({'response': "I'm here for you. It sounds like you may be going through a difficult time. "
        "Please consider reaching out to a mental health professional or someone you trust. "
        "Remember, you're not alone, and help is available."})

def generate_safe_response():
    system_message = "Hello! I'm here to assist you with any mental health questions."
    data = request.get_json()
    user_message = data.get('message', '') 
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if contains_risk_keywords(user_message):
        return escalate_message()
    else:
        response = generate_structured_response(system_message, user_message)
        return response

def generate_structured_response(system_message, user_message, max_token_length=200):
    prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=max_token_length,   # Limit the length of the output
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,                    # Lower temperature for more controlled output
        top_k=50,                           # Top-K sampling to restrict the pool of candidate tokens
        top_p=0.9,                          # Nucleus sampling to restrict to top-probable tokens
        no_repeat_ngram_size=2,             # Avoid repeating n-grams
        do_sample=True,                     # Enable sampling to allow for more diverse outputs
    )
    assistant_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    assistant_response_start = assistant_response.find("<|im_start|>assistant") + len("<|im_start|>assistant\n")
    
    assistant_message = assistant_response[assistant_response_start:]
    return assistant_message

# Twilio WhatsApp webhook endpoint
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body")  # User's message
    from_number = request.form.get("From")  # User's WhatsApp number
    
    response_message = generate_safe_response(incoming_msg)
    
    response = MessagingResponse()
    response.message(response_message)
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
