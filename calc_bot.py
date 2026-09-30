import os
import re
from telebot import TeleBot

# Render ke Environment Variable se Token lega (Safe Method)
BOT_TOKEN = "8847681782:AAEv7mZxdaTeZhJ0R-wbPthBeXURB3X7JIs"

# /start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Hi, I am calculator bot. No matter how difficult math question you ask, "
        "I will give you the answer in 2 seconds.\n\n"
        "Powered by @NOORXMODS"
    )
    bot.reply_to(message, welcome_text)

# /help Command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Hi, I am calculator bot. You can ask me any math problem you want!"
    bot.reply_to(message, help_text)

# Math Solver & Reply Logic
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip()
    
    # Check if input is only math numbers/symbols
    if re.match(r'^[0-9\+\-\*\/\^\%\(\)\.\s]+$', text):
        try:
            expression = text.replace('^', '**')
            result = eval(expression, {"__builtins__": None}, {})
            bot.reply_to(message, str(result))
        except Exception:
            bot.reply_to(message, "You cannot talk to me. I am a math bot, you can only ask me math questions.")
    else:
        bot.reply_to(message, "You cannot talk to me. I am a math bot, you can only ask me math questions.")

if __name__ == "__main__":
    bot.infinity_polling()
