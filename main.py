from socket import socket as socket, error as socketError, timeout as socketTimeout
from os import sys

if 'win' in sys.platform:
    from win10toast import ToastNotifier
    def notifier(message, username):
        ToastNotifier._show_toast(ToastNotifier(), username, message, None, 4)

elif 'linux' in sys.platform:
    import notify2
    notify2.init('Twitch.tv Chat')
    def notifier(message, username):
        notify2.Notification(username, message)

else:
    print(f'Sistema operacional não compatível :( ({sys.platform})')
    exit(1)

HOST = 'irc.twitch.tv'
PORT = 6667
TWITCH = 'D1360_64RC14' # Twitch.tv channel
PASS = open('./.oauthToken', 'r').read() # OAuth Token (por padrão, lê do arquivo ".oauthToken")
CHANNEL = '#' + TWITCH.lower()

connect = socket()
connect.connect((HOST, PORT))

connect.send((bytes(f'PASS {PASS}\r\n', 'UTF-8')))
connect.send((bytes(f'NICK {TWITCH}\r\n', 'UTF-8')))
connect.send((bytes(f'JOIN {CHANNEL}\r\n', 'UTF-8')))

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
                notifier('TwitchTv Notify', 'Connected on ' + TWITCH)
            elif '366' in data[:data.find(CHANNEL)]:
                pass
            elif 'PRIVMSG' in data:
                channel = CHANNEL
                username = data[1:data.find('!')]
                message = data[data.find(CHANNEL):][len(CHANNEL)+2:-2]
                print(f'[{channel}] {username}: {message}')
                message = message if len(message) < 136 else message[:126] + ' (More...)'
                notifier(message, username)

            # else:
            #     print(f'"{data}"')

    except socketError:
        print('Socket Error')
        break
    except socketTimeout:
        print('Socket Timeout')
        break
