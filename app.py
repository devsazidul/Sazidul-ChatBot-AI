from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer , ChatterBotCorpusTrainer
# from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests

def duckduckgo_search(query):
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,
        'format': 'json',
        'no_redirect': '1',
        'skip_disambig': '1'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    print("DuckDuckGo API response:", data)  # For debugging
    
    answer = data.get("AbstractText")
    if answer:
        return answer
    related = data.get("RelatedTopics")
    if related and len(related) > 0:
        first = related[0]
        if 'Text' in first:
            return first['Text']
    return None
def google_search(query):
    url='https://www.googleapies.com/customsearch/v1'
    params={
        'q':query,
        'key':'AIzaSyC_oqPVvun0QF6GAZ7vhF-jC6W7U-hCFzo',
        'cx':'0043beecbb9ef4d05'
    }
    resp=requests.get(url,params=params)
    results=resp.json()
    if 'items' in results:
        first =results['items'][0]
        snippet=first.get('snippet')
        link=first.get('link')
        return f"{snippet}\n Link: {link}"
    return None


# model_name="EleutherAI/gpt-neo-2.7B"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# def genarete_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     inputs = {k: v.to(model.device) for k, v in inputs.items()}
#     outputs = model.generate(**inputs, max_new_tokens=150, do_sample=True, temperature=0.9)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     print("Model raw response:", response)
#     return response.strip()



app = Flask(__name__)
CORS(app)  # frontend theke cross-origin request allow korar jonno

bot = ChatBot('ChatBot', read_only=False, logic_adapters=[{"import_path":'chatterbot.logic.BestMatch',"defult_response":"Sorry, I dont' have an answer","maximum_similarity_threshold":0.9,},
                                                          "chatterbot.logic.MathematicalEvaluation","chatterbot.logic.UnitConversion"],)

list_to_train = [
    "hi", "Hello",
    "how are you?", "i am fine, thank you!",
    "what is your name?", "my name is Sazidul",
    "how old are you?", "i am 22 years old",
    "what is your favorite color?", "my favorite color is green",
    "what is your favorite food?", "my favorite food is pizza",
    "what is your hobby?", "my hobby is playing cricket",
    "what is your favorite sport?", "my favorite sport is football",
    "what is your favorite movie?", "my favorite movie is Avengers",
    "jan","bolo jan"
    "sazidul","munmun"
]

list_to_train2 =[
    "hi","hi there",
    "how are you?","i am good and you?","i am good too","ok, can i help you?","yes, i need your help",
    "what is your name?","my name is Sazidul chatbot",
    "are you machine?", "yes, i am machine",
    "what is your favorite color?","my favorite color is red",
    "what is your gf name?","my gf name is munmun",
    "what is your job?","i'm an assistant Chatbot"
    ,"i love you","i love you too",    
]

business_list=[
    'hi','yes',
    'what courses do you have?','we have python, java, c, c++, javascript, html, css , please visit this link for more details https://docs.google.com/spreadsheets/d/1R7A_Rso-UDl6s4JUQEL8qsbZW1wwLOjGQG3pQVd9USw/edit?gid=0#gid=0',
]
banglish_convos = [
    "kemon aso?",
    "ami bhalo asi, tumi kemon aso?",
    "tumi kothai?",
    "ami computer er moddhe asi.",
    "bhalo lagse tomake dekhe.",
    "thank you!"
]

list_trainer = ListTrainer(bot)
trainer= ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")
# trainer.train("data.corpus.bangla")
# trainer.train("data.corpus.banglish")
list_trainer.train(list_to_train)
list_trainer.train(list_to_train2)
list_trainer.train(business_list)
list_trainer.train(banglish_convos)


@app.route("/")
def index():
    return send_from_directory('.','index.html')


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]
        bot_response = bot.get_response(user_message)
        if bot_response.confidence <0.5:
        # 0 case
            # llm_answer=genarete_response(user_message)
            # if llm_answer:
            #     return jsonify({"response":llm_answer})
        # 1 case
            serch_answer=duckduckgo_search(user_message)
            if serch_answer:
                return jsonify({"response":serch_answer})
        # 2 case
            serch_answer =google_search(user_message)
            if serch_answer:
                return jsonify({"response":serch_answer})
            else:
                query = user_message.replace(' ', '+')
                serch_URL=f"https://www.google.com/search?q={query}"
                fallback_message=f"Sorry, i' dont't know the answer. Maybe you can find it on Google: {serch_URL}"
            return jsonify({"response":fallback_message})
        return jsonify({"response": str(bot_response)})
    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Sorry, something went wrong."})


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=5001)
