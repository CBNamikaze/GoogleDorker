import telebot
import ast
import time
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from telebot import types

API_KEY = "<api_key>"
bot = telebot.TeleBot(API_KEY)
txt=''

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def makeKeyboard(message):
    global txt
    stringList = scrape_google(txt)
    markup = types.InlineKeyboardMarkup()
    if stringList!=[]:
        for key in stringList:
            markup.add(types.InlineKeyboardButton(text=key,url=key))
    else:
        markup.add(types.InlineKeyboardButton("None",callback_data="None"))

    return markup

def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return False
    else:
        return True

def valuexist():
    pass

@bot.message_handler(commands=['start'])
def initiate(message):
    bot.send_message(message.chat.id,"Welcome to Google Dorker,\n\nA Google dork query, sometimes just referred to as a dork, is a search string or custom query that uses advanced search operators to find information not readily available on a website")
    bot.send_message(message.chat.id,"Use '/dork' to start dorking")
@bot.message_handler(commands=['dork'])
def query(message):
    bot.reply_to(message,text="Hi, Use options below to use a dorking operators\nUse 'nil' for values not applicable")
    bot.send_message(text="Enter text to be present in url:",chat_id=message.chat.id)
    print(message.text)
    global txt
    txt=''
    bot.register_next_step_handler(message,query2)
def query2(message):
    bot.send_message(text="Enter the file type expected:",chat_id=message.chat.id)
    print(message.text)
    global txt
    if (message.text).lower()!="nil":
        txt+="inurl:" + message.text
    bot.register_next_step_handler(message,query4)
def query4(message):
    bot.send_message(text="Enter the text to check on website:",chat_id=message.chat.id)
    print(message.text)
    global txt
    if (message.text).lower()!="nil":
        txt+=" filetype:" + message.text
    bot.register_next_step_handler(message,queryfinal)
def queryfinal(message):
    print(message.text)
    global txt
    if (message.text).lower()!="nil":
        txt+=" intext:" + message.text
    print (txt)
    bot.send_message(text="The results are:",
                 chat_id=message.chat.id,
                 reply_markup=makeKeyboard(message),
                 parse_mode='HTML')    
bot.polling()
