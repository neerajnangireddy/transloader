import logging
import os
import time
from os import environ
from telegram.ext import *
from selenium import webdriver
import scrapper
import pyshorteners
import dynoInfo

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

API_KEY = environ["API_KEY"]
HOST_URL = environ["HOST_URL"]

# set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.info("Starting bot.......")


def start_command(update, context):
    update.message.reply_text("Waking up Bot\n")


def help_command(update, context):
    update.message.reply_text("This Bot uses {0} to transload"
                              "\n->mega Links are not supported by the site\n"
                              "if bot doesn't work contact @babysheldon ".format(HOST_URL))


# def custom_command(update, context):
#     update.message.reply_text("custom Bot")


# def cancel_command(update, context):
#     update.message.reply_text("Quitting...")
#     handle_message.driver.quit()


def stats(update, context):
    stats_info = scrapper.stats()
    update.message.reply_text(stats_info)


def dyno_stats(update, context):
    usageInfo = dynoInfo.dynoStats()
    update.message.reply_text(usageInfo)


def get_links(update, context):
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-gpu")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    op.page_load_strategy = 'eager'
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)

    try:
        driver.get(HOST_URL)
        print("accessing leech")
        driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table[1]/tbody/tr/td[3]').click()
        list_table = driver.find_element_by_id("table_filelist")
        link_list = list_table.find_elements_by_css_selector("tbody td tr a")
        print("getting links")
        for link in link_list:
            final_link = link.get_attribute("href")
            update.message.reply_text("{}\n".format(final_link))
    except Exception as ex:
        print(ex)
    finally:
        print("closing browser")
        driver.quit()


"""
def load_driver():
    options = webdriver.FirefoxOptions()

    # enable trace level for debugging
    options.log.level = "trace"

    options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    firefox_driver = webdriver.Firefox(
        firefox_binary=binary,
        executable_path=os.environ.get('GECKODRIVER_PATH'),
        options=options)

    return firefox_driver
"""


def handle_message(update, context):
    msg_id = update.message.message_id
    chat_id = update.message.chat_id
    url = update.message.text
    context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, text="transloading")

    # driver = load_driver() # use this for firefox
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-gpu")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    op.page_load_strategy = 'eager'
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)

    try:
        driver.get(HOST_URL)
        time.sleep(3)
        print("accessing leech13040")
        input_field = driver.find_element_by_id("link")
        input_field.clear()
        input_field.send_keys(url)
        input_field.submit()
        time.sleep(5)
        try:
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
        except:
            html_error = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[2]/span').text
            html_error = html_error.replace("/", " or ")
            context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, text=html_error)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, text="Couldn't transload \n"
                                                                                   "Error: {0}".format(e))
        print(e)
    finally:
        driver.save_screenshot("screenshots/error.png")
        context.bot.send_photo(chat_id=chat_id, reply_to_message_id=msg_id, photo=open("screenshots/error.png", "rb"))
        print("Closing browser")
        driver.quit()


def short(url):
    return pyshorteners.Shortener().tinyurl.short(url)


def error(update, context):
    # logs errors
    logging.error(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("getlinks", get_links))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("usage", dyno_stats))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    # Log Handler
    dp.add_error_handler(error)

    # Run Bot
    updater.start_polling()
    updater.idle()
