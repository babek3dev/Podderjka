import telebot

TOKEN = '7369491468:AAGV8LC67zjiA_WnEN2l-s_J7LGC-kn3DQU'
GROUP_ID = -1002712764512  # замени на ID своей группы

bot = telebot.TeleBot(TOKEN)

# Словарь: ID пересланного сообщения в группе → ID пользователя
reply_map = {}

# Когда пользователь пишет боту
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def user_message(message):
    # Пересылаем сообщение в группу
    fwd = bot.forward_message(GROUP_ID, message.chat.id, message.message_id)
    
    # Сохраняем, кто это был
    reply_map[fwd.message_id] = message.chat.id

# Когда кто-то из группы отвечает на пересланное сообщение
@bot.message_handler(func=lambda message: message.chat.id == GROUP_ID and message.reply_to_message)
def group_reply(message):
    original_msg_id = message.reply_to_message.message_id

    if original_msg_id in reply_map:
        user_id = reply_map[original_msg_id]
        try:
            bot.send_message(user_id, message.text)
        except Exception as e:
            bot.send_message(GROUP_ID, f"❌ Ошибка при отправке: {e}")
    else:
        bot.send_message(GROUP_ID, "⚠️ Неизвестный получатель.")
bot.polling(none_stop=True)