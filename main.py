import socket

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'D1360_64RC14'
PASS = open('./.oauth', 'r').read() # Pega o token de autenticação de um arquivo ".oauth"
CHANNEL = '#' + NICK.lower()

class Send(object):
    def oauth(self, PASS):
        connect.send((bytes(f'PASS {PASS}\r\n', 'UTF-8')))
    def nickname(self, NICK):
        connect.send((bytes(f'NICK {NICK}\r\n', 'UTF-8')))
    def channel(self, CHANNEL):
        connect.send((bytes(f'JOIN {CHANNEL}\r\n', 'UTF-8')))

connect = socket.socket()
connect.connect((HOST, PORT))

Send.oauth(Send(), PASS)
Send.nickname(Send(), NICK)
Send.channel(Send(), CHANNEL)

while True:
    try:
        
        data = connect.recv(1024)
        print(data.decode())
        # Retorna um bytes com os output do chat, porém ao adicionar
        # caractere especial (ex: á, ã, ç) dá UnicodeEncodeError

        # UnicodeEncodeError: 'ascii' codec can't encode character '\xe1' in position 77: ordinal not in range(128)
    
    except socket.error:
        print('Socket Error')
    except socket.timeout:
        print('Socket Timeout')