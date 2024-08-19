import time
import json
import telebot
import random

# TOKEN DETAILS
TOKEN = "POINTS"

BOT_TOKEN = "7534264405:AAFX53dTF3UAhAivBYLClwHpCLTBZEkxUq4"
PAYMENT_CHANNEL = "@PremiumVpn02"
OWNER_ID = 7483776980
CHANNELS = ["@PremiumVpn02"]
Daily_bonus = 0
Mini_Withdraw = 10  # Minimum points to redeem the smallest reward
Per_Refer = 1

# Predefined accounts
netflix_accounts = ["netflix_account1", "netflix_account2", "netflix_account3"]
crunchyroll_accounts = ["crunchyroll_account1", "crunchyroll_account2", "crunchyroll_account3"]
trial_accounts = ["trial_account1", "trial_account2", "trial_account3"]

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Redeem Points')
    keyboard.row('📊Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        user = str(user)
        data = json.load(open('users.json', 'r'))

        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = user
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total'] + 1
        json.dump(data, open('users.json', 'w'))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
        msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
        for i in CHANNELS:
            msg_start += f"\n➡️ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "This command has an error. Please wait for the admin to fix the glitch.")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\nError on command: {message.text}\n{str(e)}")
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)

                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                    json.dump(data, open('users.json', 'w'))

                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)

                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0

                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1

                        # Notify referral owner
                        bot.send_message(ref_id, f"*🏧 New Referral! You got: +{Per_Refer} {TOKEN}*",
                                         parse_mode="Markdown")
                        bot.send_message(ref_id, f"YOUR REFERRAL WAS SUCCESSFUL @USER_ID", parse_mode="Markdown")

                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)

            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ You have not joined.')
                bot.delete_message(call.message.chat.id, call.message.message_id)

                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='❌ Invalid action.')
    except Exception as e:
        bot.send_message(call.message.chat.id, "This command has an error. Please wait for the admin to fix the glitch.")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\nError on command: {call.data}\n{str(e)}")
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        data = json.load(open('users.json', 'r'))

        if message.text == '🆔 Account':
            accmsg = '*👮 User : {}\n\n💸 Balance : *{}* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            msg = accmsg.format(message.from_user.first_name, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        if message.text == '🙌🏻 Referrals':
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Referral System\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referral Link ⬇️\n{}*"
            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = f'https://telegram.me/{bot_name}?start={user_id}'
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        if message.text == "🎁 Bonus":
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int(time.time())

            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60 * 60 * 24):
                data['balance'][user] += Daily_bonus
                bot.send_message(user_id, f"Congrats, you just received {Daily_bonus} {TOKEN}!")
                bonus[user_id] = cur_time
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(message.chat.id, "❌*You can only take bonus once every 24 hours!*",
                                 parse_mode="markdown")

        if message.text == "📊Statistics":
            user_id = message.chat.id
            msg = "*📊 Total members : {} Users\n\n🥊 Total successful Withdrawals : {} {}*"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="Markdown")

        if message.text == "💸 Redeem Points":
            user_id = message.chat.id
            user = str(user_id)
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Netflix - 20 points', 'Crunchyroll - 10 points', 'Trial - 10 points')
            keyboard.row('🚫 Cancel')
            bot.send_message(user_id, "_Choose your redeem option_", parse_mode="Markdown", reply_markup=keyboard)
            bot.register_next_step_handler(message, process_redeem)

    except Exception as e:
        bot.send_message(message.chat.id, "This command has an error. Please wait for the admin to fix the glitch.")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\nError on command: {message.text}\n{str(e)}")
        return

def process_redeem(message):
    try:
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))

        if message.text == "Netflix - 20 points":
            if data['balance'][user] >= 20:
                account = random.choice(netflix_accounts)
                bot.send_message(user_id, f"_Here's your Netflix account:_\n\n{account}", parse_mode="Markdown")
                data['balance'][user] -= 20
                data['totalwith'] += 1
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(user_id, "❌*You don't have enough points to redeem this!*", parse_mode="markdown")

        elif message.text == "Crunchyroll - 10 points":
            if data['balance'][user] >= 10:
                account = random.choice(crunchyroll_accounts)
                bot.send_message(user_id, f"_Here's your Crunchyroll account:_\n\n{account}", parse_mode="Markdown")
                data['balance'][user] -= 10
                data['totalwith'] += 1
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(user_id, "❌*You don't have enough points to redeem this!*", parse_mode="markdown")

        elif message.text == "Trial - 10 points":
            if data['balance'][user] >= 10:
                account = random.choice(trial_accounts)
                bot.send_message(user_id, f"_Here's your trial account:_\n\n{account}", parse_mode="Markdown")
                data['balance'][user] -= 10
                data['totalwith'] += 1
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(user_id, "❌*You don't have enough points to redeem this!*", parse_mode="markdown")

        elif message.text == "🚫 Cancel":
            menu(user_id)
        else:
            bot.send_message(user_id, "❌ Invalid option selected.")
            menu(user_id)
    except Exception as e:
        bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        bot.send_message(OWNER_ID, f"Error in process_redeem: {str(e)}")

# Start the bot
bot.polling(none_stop=True)
