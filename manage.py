# Import the necessary libraries
import socket
import select
import time

#sel = selectors.DefaultSelector()
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("0.0.0.0", 3000))
#serv.bind(("192.168.1.13", 62222))
serv.listen()
#serv.setblocking(False)
Income = {}
Outcome = []
#client, address = serv.accept()
#print(address)
#flag = True
print('Ready to receive')
client, adr = serv.accept()
print('client {} connected from {}'.format('1', adr))
Income[1] = client
client.sendall('1'.encode('utf8'))

client, adr = serv.accept()
print('client {} connected from {}'.format('2', adr))
Income[2] = client
client.sendall('2'.encode('utf8'))


class Game:
    def __init__(self):
        self.board = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
        self.count = 0
        self.cont = True
        self.starter = 1
        self.start(self.starter)

    def put(self, x, y, player):
        if self.board[y][x] == 0:
            self.board[y][x] = player
            self.count += 1
            print(self.board)
            if self.count >= 5:
                self.check()
            #if self.count == 9:
            #    self.tie()
            turn = str(x)+str(y)
            #if self.cont:
            if player == 1:
                print(turn, 'SENT to 2')
                Income[2].sendall(turn.encode('utf8'))
            else:
                print(turn, 'SENT to 1')
                Income[1].sendall(turn.encode('utf8'))
            #else:
            if not self.cont:
                print('questioning started')
                restart = {}
                answer = ''
                rdble = []
                while True:
                    r, w, e = select.select(Income.values(), [], [])
                    print('recieve- ', r)
                    for rdble in r:
                        answer = rdble.recv(1024).decode('utf8')
                    if answer:
                        print('+answer')
                        restart[rdble] = answer
                    if answer == 'no':
                        return True
                    if len(restart.values()) == 2:
                        self.renew()
                        return True

    def renew(self):
        self.board = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
        self.count = 0
        self.cont = True
        Income[1].sendall('again'.encode('utf8'))
        Income[2].sendall('again'.encode('utf8'))
        if self.starter == 1:
            self.starter = 2
        else:
            self.starter = 1
        self.start(self.starter)

    def check(self):
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != 0:  # across the top
            winner = str(self.board[0][0])
            self.finish(winner)
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] != 0:  # across the top
            winner = str(self.board[1][0])
            self.finish(winner)
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] != 0:  # across the top
            winner = str(self.board[2][0])
            self.finish(winner)
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] != 0:  # across the top
            winner = str(self.board[0][0])
            self.finish(winner)
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] != 0:  # across the top
            winner = str(self.board[0][1])
            self.finish(winner)
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] != 0:  # across the top
            winner = str(self.board[0][2])
            self.finish(winner)
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:  # across the top
            winner = str(self.board[0][0])
            self.finish(winner)
        elif self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:  # across the top
            winner = str(self.board[2][0])
            self.finish(winner)
        elif self.count == 9:
            self.finish(str(3))

    def finish(self, pl):
        print("\nGame Over.\n")
        print(" Player " + pl + " won. ****")
        self.cont = False
        Income[1].sendall(pl.encode('utf8'))
        Income[2].sendall(pl.encode('utf8'))

    def start(self, starter):
        if starter == 1:
            Income[1].sendall('yes'.encode('utf8'))
            while True:
                # data = []
                # while not data:
                data = Income[1].recv(1024).decode('utf8')
                self.put(int(data[0]), int(data[1]), 1)
                data = Income[2].recv(1024).decode('utf8')
                self.put(int(data[0]), int(data[1]), 2)
        else:
            Income[2].sendall('yes'.encode('utf8'))
            while True:
                # data = []
                # while not data:
                data = Income[2].recv(1024).decode('utf8')
                if self.put(int(data[0]), int(data[1]), 2):
                    break
                data = Income[1].recv(1024).decode('utf8')
                if self.put(int(data[0]), int(data[1]), 1):
                    break


game = Game()


#    #data = []
#    #while not data:
#    data = Income[1].recv(1024).decode('utf8')
#    game.put(int(data[0]), int(data[1]), 1)
#    data = Income[2].recv(1024).decode('utf8')
#    game.put(int(data[0]), int(data[1]), 2)

"""
    toread, towrite, toexcept = select.select(Income, Outcome, Income)
    for mess in toread:

        else:
            data = mess.recv(1024)
            if data:
                for out in Outcome:
                    if out != mess:
                        data = str(Income[mess] + ": " + data.decode('utf8'))
                        out.sendall(data.encode('utf8'))
                print(Income[mess], ': ', data)
                data = ""
"""















