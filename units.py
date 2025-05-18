from chatterbot import ChatBot

# how many minutes in a year
# 60 minutes in an hour * 24 hours in a day * 365 days in a year


bot= ChatBot("units",logic_adapters=["chatterbot.logic.UnitConversion"])


while True:
    user_text = input("Ask a question:")
    chatbot_response= str(bot.get_response(user_text))
    print(chatbot_response)