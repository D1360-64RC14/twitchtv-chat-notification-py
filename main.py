from socket import socket as socket, error as socketError, timeout as socketTimeout

HOST = 'irc.twitch.tv'
PORT = 6667
TWITCH = 'D1360_64RC14'
PASS = open('./.oauthToken', 'r').read() # OAuth Token (por padrão, lê do arquivo ".oauthToken")
CHANNEL = '#' + TWITCH.lower()

class Send(object):
    def oauth(self, PASS):
        connect.send((bytes(f'PASS {PASS}\r\n', 'UTF-8')))
    def nickname(self, NICK):
        connect.send((bytes(f'NICK {TWITCH}\r\n', 'UTF-8')))
    def channel(self, CHANNEL):
        connect.send((bytes(f'JOIN {CHANNEL}\r\n', 'UTF-8')))

connect = socket()
connect.connect((HOST, PORT))

Send.oauth(Send(), PASS)
Send.nickname(Send(), TWITCH)
Send.channel(Send(), CHANNEL)

ignore = True

while True:
    try:
        if ignore:
            ignore = False
        else:
            data = connect.recv(2048).decode()

            # print(f'"{data}"') # Debug
            if 'JOIN' in data[:data.find(CHANNEL)]:
                print(f'Connected on {TWITCH}!')
            elif '366' in data[:data.find(CHANNEL)]:
                pass
            elif 'PRIVMSG' in data:
                channel = CHANNEL
                username = data[1:data.find('!')]
                message = data[data.find(CHANNEL):][len(CHANNEL)+2:-2]
                print(f'[{channel}] {username}: {message}')

            # else:
            #     print(f'"{data}"')

    except socketError:
        print('Socket Error')
        break
    except socketTimeout:
        print('Socket Timeout')
        break