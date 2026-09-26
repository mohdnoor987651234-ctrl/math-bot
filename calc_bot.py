import telebot
import sympy as sp
import math
import re
import time
import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

API_TOKEN = "8847681782:AAEv7mZxdaTeZhJ0R-wbPthBeXURB3X7JIs"
ADMIN_USERNAME = "NOORXMODS"

bot = telebot.TeleBot(API_TOKEN)
bot_active = True

def to_fancy_font(text):
    normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    fancy_chars  = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"
    trans_table = str.maketrans(normal_chars, fancy_chars)
    return text.translate(trans_table)

@bot.message_handler(commands=['off'])
def turn_off(message):
    global bot_active
    if message.from_user.username == ADMIN_USERNAME:
        bot_active = False
        bot.reply_to(message, "🔴 <b>𝕊𝕐𝕊𝕋𝔼𝕄 𝔻𝕀𝕊𝔸𝔹𝕃𝔼𝔻</b>\n<i>Bot turned OFF by Admin.</i>", parse_mode="HTML")
    else:
        bot.reply_to(message, "⚠️ <i>Access Denied! Only @NOORXMODS can use this.</i>", parse_mode="HTML")

@bot.message_handler(commands=['on'])
def turn_on(message):
    global bot_active
    if message.from_user.username == ADMIN_USERNAME:
        bot_active = True
        bot.reply_to(message, "🟢 <b>𝕊𝕐𝕊𝕋𝔼𝕄 𝕆ℕ𝕃𝕀ℕ𝔼</b>\n<i>Bot is now active and ready!</i>", parse_mode="HTML")
    else:
        bot.reply_to(message, "⚠️ <i>Access Denied! Only @NOORXMODS can use this.</i>", parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    if not bot_active:
        return
    user_name = message.from_user.first_name or "User"
    styled_name = to_fancy_font(user_name)
    
    msg = (
        f"✨ 𝔐𝔄𝔗ℌ 𝔖𝔒𝔏𝔍𝔈ℜ 𝔛 𝔅𝔒𝔗 ✨\n"
        f"═════════════════════\n"
        f"👋 Welcome <b>{styled_name}</b>!\n\n"
        f"💎 <i>Send any mathematical problem to get instant solution!</i>\n\n"
        f"📝 <b>E𝔵𝔞𝔪𝔭𝔩𝔢𝔰:</b>\n"
        f"🔹 <code>6-6+1²-3(7)⁴+1</code>\n"
        f"🔹 <code>sqrt(144) + sin(pi/2)</code>\n"
        f"🔹 <code>2^10 + log(100)</code>\n\n"
        f"👑 <b>D𝔢𝔳𝔢𝔩𝔬𝔭𝔢𝔯:</b> @NOORXMODS"
    )
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1.5)
        bot.reply_to(message, msg, parse_mode="HTML")
    except Exception as e:
        print(f"Error: {e}")

def solve_math(expr):
    text = expr.strip()
    text = re.sub(r'=\s*\??$', '', text)
    
    superscript_map = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
    fixed_chars = [("^" + c.translate(superscript_map)) if c in "⁰¹²³⁴⁵⁶⁷⁸⁹" else c for c in text]
    text = "".join(fixed_chars)

    text = re.sub(r'([a-zA-Z])2\^', r'\1^', text)
    text = text.replace('^', '**')
    text = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', text)

    try:
        res = sp.simplify(text)
        return str(res).replace('**', '^')
    except Exception:
        pass

    try:
        clean_eval = text.replace('^', '**')
        allowed_names = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "pi": math.pi, "log": math.log}
        res = eval(clean_eval, {"__builtins__": None}, allowed_names)
        return str(res)
    except Exception:
        pass

    return None

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not bot_active:
        return

    text = message.text.strip()
    if text.startswith('/'):
        return

    try:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1.5)
    except Exception:
        pass

    ans = solve_math(text)
    
    try:
        if ans is not None:
            reply_msg = (
                f"⚡ <b>𝔐𝔄𝔗ℌ ℜ𝔈𝔖𝔘𝔏𝔗</b> ⚡\n"
                f"═════════════════════\n"
                f"📥 <b>I𝔫𝔭𝔲𝔱:</b> <code>{text}</code>\n"
                f"📤 <b>O𝔲𝔱𝔭𝔲𝔱:</b> <code>{ans}</code>\n"
                f"═════════════════════\n"
                f"✨ <i>Powered by @NOORXMODS</i>"
            )
            bot.reply_to(message, reply_msg, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ <b>𝕊𝕐ℕ𝕋𝔸𝕏 𝔼ℝℝ𝕆ℝ!</b> Sahi math expression bhejo.", parse_mode="HTML")
    except Exception as e:
        print(f"Reply Error: {e}")

if __name__ == '__main__':
    Thread(target=run_web).start()
    print("🚀 Calculator Bot Online!")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(3)
