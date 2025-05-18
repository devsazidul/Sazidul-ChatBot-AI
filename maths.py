# at first akhane math er logic likhci then app er modde jast logic_adapter add kore dici tatei mathd er kaj hosse.
from chatterbot import ChatBot

bot = ChatBot(
    "math",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation"
    ]
)

print("--------- Math ChatBot ---------")

while True:
    user_text = input("Type the math equation that you want to solve: ")
    print("ChatBot:", bot.get_response(user_text))
