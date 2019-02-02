from tkinter import *
import tkinter
import socket
from threading import Thread
import sys


def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except:
            print("There is an error while receiving a message")
            break


def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))

    if msg == "#quit":
        s.send(bytes(msg, "utf8"))
        s.close()
        window.quit()
        print('[+] Quitting...')
        exit()
        quit()
        os._exit(1)


def on_closing():
    my_msg.set("#quit")
    send()


window = Tk()
window.title("Chat Room")
window.configure(bg="black")
messages_frame = Frame(window, height=100, width=100, bg="black")
my_msg = StringVar()
my_msg.set("")
scroll_bar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame, height=15, width=100, bg="white", yscrollcommand=scroll_bar.set)

scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack()
messages_frame.pack()
button_label = Label(window, text="Enter Your Message", fg="black", font="Aerial", bg="white")
button_label.pack()
entry_field = Entry(window, textvariable=my_msg, fg="black", width=50)
entry_field.pack()
send_button = Button(window, text="Send", bg="light green", font="Aerial", fg="black", command=send)
send_button.pack()

quit_button = Button(window, text="Quit", bg="light green", font="Aerial", fg="black", command=on_closing)
quit_button.pack()
window.protocol("WM_DELETE_WINDOW", on_closing)

Host = '127.0.0.1'
Port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))

receive_thread = Thread(target=receive)
receive_thread.start()
mainloop()

