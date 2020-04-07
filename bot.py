"""Listens to twitch chat for dibs emotes and displays them one at a time"""
import socket
import queue
import threading
import datetime

OAUTH_TOKEN = "PUT TOKEN HERE"
USERNAME = "PUT BOT USERNAME HERE"
CHANNEL = "#dskoopa"


def process_message(dataobj):
    """Parse a received message"""
    messagething = dataobj.workqueue.get()
    message = messagething[1]
    user = messagething[0]
    if "dskoopadibs" in message:
        if user in dataobj.userdict:
            dataobj.userdict[user] += 1
        else:
            dataobj.userdict[user] = 1
        dibcount = dataobj.userdict[user]
        modmessage = message.replace("@dskoopa", "").replace("dskoopadibs", "DIBS").strip()
        with open(dataobj.csvname, "a") as writefile:
            writefile.write(f"{user}, {modmessage}\n")
        print(f"{dibcount} - {user} - \"{modmessage}\"", end='')
        input("")
    dataobj.workqueue.task_done()


def receive_messages(dataobj):
    """Receive messages from chat"""
    while True:
        message = dataobj.server.recv(2048).decode().strip()
        if ':' in message and len(message.split(':')) > 2:
            user = message.split(':')[1].split('!')[0]
            message = message.split(':', 2)[2].lower()
            # print(f"{user} - {message}")
            dataobj.workqueue.put((user, message))
        elif message == "PING :tmi.twitch.tv":
            # print(message)
            dataobj.server.send(bytes("PONG :tmi.twitch.tv\r\n", 'utf-8'))
            # print("PONGED")
        else:
            print(f"RAW MESSAGE - {message}")


class TwitchListener():
    """Setup and tell bot to do things"""
    def __init__(self):
        self.cmdlist = []
        self.solution = ""
        self.workqueue = queue.Queue()
        self.userdict = {}
        self.csvname = str(datetime.datetime.now()).replace(" ", "_") + '.csv'
        self.server = socket.socket()
        self.processthread = threading.Thread(target=receive_messages, args=(self,), daemon=True)

    def run(self):
        """Run the bot"""
        connection_data = ('irc.chat.twitch.tv', 6667)
        token = OAUTH_TOKEN
        user = USERNAME
        channel = CHANNEL

        self.server.connect(connection_data)
        self.server.send(bytes("PASS " + token + '\r\n', 'utf-8'))
        self.server.send(bytes("NICK " + user + '\r\n', 'utf-8'))
        self.server.send(bytes("JOIN " + channel + '\r\n', 'utf-8'))
        self.processthread.start()

        while True:
            process_message(self)


if __name__ == "__main__":
    LISTENER = TwitchListener()
    LISTENER.run()
