import socket
from threading import Thread

clients = {}
addresses = {}

host = '127.0.0.1'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))


def accept_client_connections():
    while True:
        client_con, client_address = s.accept()
        print(client_address, " Has connected")
        client_con.send("Welcome to the chat room! Please Type your Name to continue".encode("utf8"))
        addresses[client_con] = client_address
        Thread(target=handle_client, args=(client_con, client_address)).start()


def broadcast(msg, prefix=""):
    for x in clients:
        x.send(bytes(prefix, "utf8") + msg)


def handle_client(conn, addr):
    name = conn.recv(1024).decode("utf8")
    welcome = "Welcome " + name + ", to the chat room"
    conn.send(bytes(welcome, "utf8"))

    msg = name + " has recently joined the chat room"
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(1024)

        if msg != bytes("#quit", "utf8"):
            broadcast(msg, name + ": ")

        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(name + " has left the chat room."))


if __name__ == "__main__":
    s.listen(2)
    print("The server has been started and is now listening to clients requests")
    t1 = Thread(target=accept_client_connections)
    t1.start()
    t1.join()

