from telegram import ForceReply, Update
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import asyncio
import os
openai.api_key = os.getenv('OPENAI_API_KEY')
botToken = os.getenv('TELEGRAM_BOT_TOKEN')
msg = []
def send_message(m):
    global msg
    c = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-0301',
        messages = m
    )
    cost = c.usage.total_tokens/1000*0.002
    reply = c.choices[0].message.content
    msg.append({'role':'assistant', 'content': reply})
    print(f"${'{:.5f}'.format(cost)} - {reply}")
    return reply

# Initialize the Telegram API with your bot token
bot = telegram.Bot(token=botToken)

# Define the function to handle user inputs
async def handle_user_input(update, context):
    global msg
    # Get user input as text
    inp = update.message.text
    if inp in ['Reset','reset','\\r','R','r']:
        msg = []
        await update.message.reply_text("Chat has been reset")
    else: 
        msg.append({'role': 'user', 'content': inp})
        response = send_message(msg)
        # Send the response back to the user in Telegram
        await update.message.reply_text(response,parse_mode='Markdown')

# Configure the Telegram bot using the python-telegram-bot library
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(botToken).build()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()