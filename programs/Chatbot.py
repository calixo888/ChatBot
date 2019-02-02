from tkinter import *
import tkinter
import socket
from threading import Thread
import pyautogui
import sys
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np
import random
import string

questions = ()
answers = {}


class Bot:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        f = open('chatbot.txt', 'r', errors='ignore')
        raw = f.read()
        raw = raw.lower()
        self.sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        word_tokens = nltk.word_tokenize(raw)
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        self.start()

    def textSend(self, result):
        print('[-] Unanswerable Question: ' + result)
        message = "Alert! Unrecognized response: " + result
        SMTPserver = [SMTPSERVER HERE]
        sender = [YOUR EMAIL HERE]
        destination = [YOUR EMAIL HERE]

        USERNAME = [USERNAME]
        PASSWORD = [PASSWORD]

        # typical values for text_subtype are plain, html, xml
        text_subtype = 'plain'

        content = """\
        Test message
        """

        subject = "Sent from Python"

        import sys
        import os
        import re

        from smtplib import SMTP_SSL as SMTP  # this invokes the secure SMTP protocol (port 465, uses SSL)
        # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

        # old version
        # from email.MIMEText import MIMEText
        from email.mime.text import MIMEText

        try:
            msg = MIMEText(content, text_subtype)
            msg['Subject'] = 'Alert'
            msg['From'] = sender  # some SMTP servers will do this automatically, not all

            conn = SMTP(SMTPserver)
            conn.set_debuglevel(False)
            conn.login(USERNAME, PASSWORD)
            try:
                conn.sendmail(sender, destination, msg.as_string())
            finally:
                conn.quit()

        except:
            sys.exit("mail failed; %s" % "CUSTOM_ERROR")  # give an error message
        self.unAnswerables(result)

    def howareyou(self, sentence):
        INPUTS = ("how are you", 'how are you?', 'how are you doing?', 'how have you been doing?', 'hey, how are you?',
                  'hi, how are you?', 'hello, how are you?')
        RESPONSES = ["I'm good! How are you?", "I'm doing fine, how about you?"]
        if sentence in INPUTS:
            return random.choice(RESPONSES)

    def response(self, user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf == 0):
            self.textSend(user_response)
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            self.automation(robo_response)

    def greeting(self, sentence):
        GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
        GREETING_RESPONSES = ["Hi!", "Hey!", "Hi there!", "Hello!", "I am glad! You are talking to me"]
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def watchadoin(self, sentence):
        INPUTS = ("what are you doing?", 'what are you doin?', 'watcha doin?', 'what are you doing right now?')
        RESPONSES = ["Nothing much, how about you?", "Not much, you?"]
        if sentence in INPUTS:
            return random.choice(RESPONSES)

    def randoms(self, sentence):
        INPUTS = ("what is your favorite color?", "what's your favorite color?", "what's your favorite food?")
        RESPONSES = ["I don't really have an opinion on that.", "I don't have an opinion on that."]
        if sentence in INPUTS:
            return random.choice(RESPONSES)

    def answered(self, sentence):
        global questions
        global answers
        if sentence in questions:
            return answers[sentence]

    def unAnswerables(self, sentence):
        global questions
        global answers
        result = input(sentence + ": ")
        questions = questions + (sentence,)
        answers[sentence] = result
        self.automation(result)

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def automation(self, message):
        pyautogui.moveTo(457, 340, duration=1)  # Click and type in entry box
        pyautogui.click()
        pyautogui.typewrite(message)
        pyautogui.moveTo(464, 369, duration=1)  # Click send
        pyautogui.click()

    def other(self, user_response):
        if 'Bot: ' in user_response:
            pass
        else:
            if user_response == 'Welcome to the chat room! Please Type your Name to continue' or 'to the chat room' in user_response or 'has recently joined the chat room' in user_response:
                self.automation('Bot')
            else:
                user_response = user_response.lower()
                user_response = user_response.split(": ")[1]
                print(user_response)
                if (user_response != 'bye'):
                    if ('thanks' in user_response or 'thank you' in user_response):
                        user_response = "You're welcome"
                        self.automation(user_response)
                    else:
                        if (self.randoms(user_response) != None):
                            new_response = self.randoms(user_response)
                            self.automation(new_response)

                        elif (self.hobbies(user_response) != None):
                            new_response = self.hobbies(user_response)
                            self.automation(new_response)

                        elif (self.watchadoin(user_response) != None):
                            new_response = self.watchadoin(user_response)
                            self.automation(new_response)

                        elif (self.howareyou(user_response) != None):
                            new_response = self.howareyou(user_response)
                            self.automation(new_response)

                        elif (self.greeting(user_response) != None):
                            new_response = self.greeting(user_response)
                            self.automation(new_response)

                        elif (self.answered(user_response) != None):
                            new_response = self.answered(user_response)
                            self.automation(new_response)

                        else:
                            new_response = self.response(user_response)
                            self.sent_tokens.remove(user_response)

                else:
                    new_response = "Goodbye!"
                    self.automation(new_response)

    def receive(self):
        while True:
            msg = self.s.recv(1024).decode("utf8")
            self.msg_list.insert(tkinter.END, msg)
            self.other(msg)

    def send(self):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.s.send(bytes(msg, "utf8"))

        if msg == "#quit":
            self.s.send(bytes(msg, "utf8"))
            self.s.close()
            self.window.quit()
            print('[+] Quitting...')
            os._exit(1)

    def on_closing(self):
        self.my_msg.set("#quit")
        self.send()

    def hobbies(self, sentence):
        INPUTS = (
        "what do you like to do?", "what do you do?", "what do you like to do for fun?", "do you have any hobbies?")
        RESPONSES = ["I don't do much, but I'm here talking with you!", "I enjoy talking to others"]
        if sentence in INPUTS:
            return random.choice(RESPONSES)

    def start(self):
        self.window = Tk()
        self.window.title("Chat Room")
        self.window.configure(bg="black")
        messages_frame = Frame(self.window, height=100, width=100, bg="black")
        self.my_msg = StringVar()
        self.my_msg.set("")
        scroll_bar = Scrollbar(messages_frame)
        self.msg_list = Listbox(messages_frame, height=15, width=100, bg="white", yscrollcommand=scroll_bar.set)

        scroll_bar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack()
        messages_frame.pack()
        button_label = Label(self.window, text="Enter Your Message", fg="black", font="Aerial", bg="white")
        button_label.pack()
        entry_field = Entry(self.window, textvariable=self.my_msg, fg="black", width=50)
        entry_field.pack()
        send_button = Button(self.window, text="Send", bg="light green", font="Aerial", fg="black", command=self.send)
        send_button.pack()

        quit_button = Button(self.window, text="Quit", bg="light green", font="Aerial", fg="black",
                             command=self.on_closing)
        quit_button.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        mainloop()


bot = Bot('127.0.0.1', 8080)