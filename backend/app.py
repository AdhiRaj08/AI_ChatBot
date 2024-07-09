from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
app = Flask(__name__)

dummy_responses = {
    "hello": "Hello! How can I assist you today?",
    "how are you": "I'm just a program, but thanks for asking!",
    "bye": "Goodbye! Have a great day!",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "what's the weather like today?": "I'm not sure about the weather, but I'm here to chat!",
    "who is your creator?": "I was created by OpenAI, but I'm here to assist you!",
    "how does AI work?": "AI, or artificial intelligence, works by using algorithms and machine learning models to analyze data, recognize patterns, and make decisions or predictions without explicit human intervention. In summary, AI works by processing and analyzing large amounts of data using algorithms and machine learning models to perform tasks, make decisions, or provide insights in a way that mimics human intelligence.",
    "what is the meaning of life?": "The question `What is the meaning of life?` has been a philosophical and existential inquiry debated by thinkers, philosophers, and religious scholars for centuries. There is no single definitive answer, as interpretations of life's meaning can vary greatly depending on individual beliefs, cultural backgrounds, and philosophical perspectives. Some people find meaning in personal relationships, others in pursuing passions or goals, while some find meaning in spiritual or religious beliefs. Existentialists might argue that life has no inherent meaning, and it's up to each individual to create their own meaning through their choices and actions. Ultimately, the search for the meaning of life is a deeply personal and subjective journey that each person must navigate and define for themselves.",
    "what's the latest news?": "I'm not up-to-date with current news, but I can provide general information.",
    "recommend a book": "Certainly! Here's a recommendation: `The Alchemist` by Paulo Coelho. The Alchemist is a philosophical book that tells the story of Santiago, an Andalusian shepherd boy who dreams of finding a hidden treasure in Egypt. Along his journey, Santiago encounters various characters and experiences that teach him important life lessons about following one's dreams, embracing the present moment, and understanding the language of the universe. This beautifully written novel is both inspiring and thought-provoking, exploring themes of destiny, personal legend, and the power of believing in oneself. It encourages readers to pursue their dreams with passion and to appreciate the transformative journey of self-discovery. Whether you're seeking wisdom, inspiration, or simply a captivating story, The Alchemist is a timeless book that resonates with readers of all ages and backgrounds.",
    "do you dream?": "No, I do not dream as I am a machine learning model and do not have consciousness or the ability to experience dreams.",
    "tell me a story": "Once upon a time in a small village nestled between rolling hills and dense forests, lived a young girl named Clara. Clara was known throughout the village for her kind heart and insatiable curiosity. She loved to explore the woods, discovering new plants and animals, and listening to the tales told by the elders.One day, while wandering deeper into the forest than she had ever gone before, Clara stumbled upon an ancient, overgrown path. Intrigued, she followed the path until she came upon a hidden glen bathed in dappled sunlight. In the center of the glen stood a majestic oak tree with a hollow trunk. Drawn to the tree, Clara peered inside the hollow and discovered a tiny, intricately carved wooden box. With trembling hands, she carefully opened the box and found a shimmering crystal nestled within its depths. As she touched the crystal, a rush of energy coursed through her, filling her with a sense of wonder and excitement. Over the next few days, Clara noticed that she had developed an extraordinary ability – she could communicate with animals! Birds would sing melodies just for her, squirrels would chatter tales of the forest, and even the wise old owl shared ancient wisdom that had been passed down through generations.Word of Clara's newfound gift spread throughout the village, and soon people from far and wide came to seek her advice and hear her stories. Clara used her gift to heal wounded animals, settle disputes among the villagers, and teach others to respect and cherish the natural world. As the years passed, Clara's reputation as a wise and compassionate soul grew, and she became a beloved figure in the village. The once-hidden glen became a sanctuary where people and animals alike gathered to listen to Clara's stories, learn from her wisdom, and celebrate the beauty and magic of the world around them. And so, in a small village nestled between rolling hills and dense forests, a young girl named Clara taught everyone the importance of kindness, curiosity, and the interconnectedness of all living things.",
    "who won the last world cup?": "As of my last update in January 2022, the most recent FIFA World Cup was held in 2018, and the winner was France. Please note that my information might be outdated, so I recommend checking the latest sources for the most current information on World Cup winners.",
    "what's your favorite movie?": "I don't have personal preferences, but I can recommend some popular movies!",
    "what is machine learning?": "Machine learning is a subset of artificial intelligence (AI) that involves developing algorithms and statistical models that enable computers to learn from and make predictions or decisions based on data without being explicitly programmed."
}

# Enable CORS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.route('/generate-response', methods=['POST'])
def generate_response():
    
    data = request.json
    message = data.get('message', '').lower()
    
    # Call OpenAI API to generate a response
    
    try:
         response = dummy_responses.get(message, "I'm sorry, I don't understand that.")
    
         return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
