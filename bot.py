from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from quiz import questions, answers

user_answers = {}


def hello(update: Update, context: CallbackContext) -> None:
    username = update.effective_user.first_name

    user_answers[username] = []
    update.message.reply_text(questions[0])


def quiz(update: Update, context: CallbackContext) -> None:
    username = update.effective_user.first_name

    if username in user_answers:
        current_answer = 1 if update.message.text.lower() == 'да' else 0

        user_answers[username].append(current_answer)

        if len(user_answers[username]) == len(questions):
            total = sum(user_answers[username])
            result = 0 if total < 4 else 1
            del user_answers[username]

            update.message.reply_text(answers[result])
        else:
            update.message.reply_text(questions[len(user_answers[username])])
    else:
        update.message.reply_text("Тест еще не запущен, напиши мне /hello")


updater = Updater('1849724610:AAGjNrI_RzwrhiA7SNDpPAh3WbsjinTDZyc')

updater.dispatcher.add_handler(CommandHandler('hello', hello))  # /hello
updater.dispatcher.add_handler(MessageHandler(filters=Filters.update, callback=quiz))  # /quiz

updater.start_polling()
updater.idle()
