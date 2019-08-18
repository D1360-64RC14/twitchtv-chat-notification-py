import socket
import re

HOST = 'irc.twitch.tv'
PORT = 6667
TWITCH = 'D1360_64RC14'
PASS = open('./.oauth', 'r').read() # Pega o token de autenticação de um arquivo ".oauth"
CHANNEL = '#' + TWITCH.lower()

class Send(object):
    def oauth(self, PASS):
        connect.send((bytes(f'PASS {PASS}\r\n', 'UTF-8')))
    def nickname(self, NICK):
        connect.send((bytes(f'NICK {TWITCH}\r\n', 'UTF-8')))
    def channel(self, CHANNEL):
        connect.send((bytes(f'JOIN {CHANNEL}\r\n', 'UTF-8')))

connect = socket.socket()
connect.connect((HOST, PORT))

Send.oauth(Send(), PASS)
Send.nickname(Send(), TWITCH)
Send.channel(Send(), CHANNEL)

while True:
    try:
        data = connect.recv(2048).decode()
        
        if f':tmi.twitch.tv 001 d1360_64rc14 :Welcome, GLHF!' in data:
            print(f'Connected on {TWITCH}!')
        elif f':{TWITCH.lower()}.tmi.twitch.tv 366 {TWITCH.lower()} #{TWITCH.lower()} :End of /NAMES list' in data or f'JOIN #{TWITCH.lower()}' in data:
            pass
        elif 'PRIVMSG' in data:
            channel = re.search('#\w*', data)[0]
            username = re.search(':\w*!', data)[0][1:-1]
            message = re.search('#\w*.*', data)[0][len(CHANNEL)+2:]
            print(f'{channel} | {username}: {message}')
        # else:
        #     print(data)
        
    except socket.error:
        print('Socket Error')
    except socket.timeout:
        print('Socket Timeout')