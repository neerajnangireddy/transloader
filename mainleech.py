import logging
import os
import time
from os import environ

from selenium import webdriver
from telegram.ext import *

API_KEY = environ["API_KEY"]

# set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.info("Starting bot.......")


def start_command(update, context):
    update.message.reply_text("Waking up Bot")


def help_command(update, context):
    update.message.reply_text("Send link to transload")


# def custom_command(update, context):
#     update.message.reply_text("custom Bot")


# def cancel_command(update, context):
#     update.message.reply_text("Quitting...")
#     handle_message.driver.quit()


def handle_message(update, context):
    msg_id = update.message.message_id
    chat_id = update.message.chat_id
    url = update.message.text
    context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, text="transloading")

    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    op.page_load_strategy = 'eager'
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)

    try:

        driver.get("https://aws.rapidleech.gq")
        print(driver.title)
        input_field = driver.find_element_by_id("link")
        input_field.clear()
        input_field.send_keys(url)
        input_field.submit()

        file_name = driver.find_element_by_xpath("/html/body/div/b[1]").text
        file_size = driver.find_element_by_xpath("/html/body/div/b[2]").text
        average_speed = driver.find_element_by_xpath("/html/body/div[1]/b[6]").text
        download_link = driver.find_element_by_css_selector("div a").get_attribute("href")

        result = "File Name: {0}\n" \
                 "File Size: {1}\n" \
                 "Average Speed: {2}\n" \
                 "Download Link: {3}".format(file_name, file_size, average_speed, download_link)

        context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id,
                                 text=result)

    except Exception as e:
        context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, text="Couldn't transload \n"
                                                                                   "Error: {0}".format(e))
        print(e)
    finally:
        time.sleep(3)
        driver.quit()


def error(update, context):
    # logs errors
    logging.error(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("cancel", cancel_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log Handler
    dp.add_error_handler(error)

    # Run Bot
    updater.start_polling()
    updater.idle()
