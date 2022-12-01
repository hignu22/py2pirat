import socket
import threading
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = False

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("Новое подключение: ", clientAddress)

    def run(self):
        print("Подключение с клиента : ", clientAddress)

        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()
            print(msg)

            if msg == '':
                print("Отключение")
                break

            elif msg == '979879789':
                self.csocket.send(bytes('Что найти?', 'UTF-8'))

            elif msg == 'Поиск по названию':
                f = open("text.txt", "w")
                f.write("название")
                f.close()
                self.csocket.send(bytes('Введите название:', 'UTF-8'))

            elif msg == 'Поиск по описанию':
                f = open("text.txt", "w")
                f.write("описание")
                f.close()
                self.csocket.send(bytes('Введите описание:', 'UTF-8'))

            elif msg == 'Случайный':
                f = open("text.txt", "w")
                f.write("cлучайный")
                f.close()
                self.csocket.send(bytes('Обрабатываю запрос...', 'UTF-8'))

                db = sqlite3.connect('KINO3.db')
                cur = db.cursor()

                for rand in cur.execute('SELECT * FROM KINO3 WHERE ID IN (SELECT ID FROM KINO3 ORDER BY RANDOM() LIMIT 1)'):

                    print(rand)
                    name = rand[2]
                    god = rand[3]
                    opisanie = rand[4]
                    link1 = rand[5]

                    driver = webdriver.Firefox(options=options)

                    try:
                        driver.get(link1)
                        time.sleep(2)

                        driver.switch_to.frame(
                            driver.find_element_by_tag_name("iframe"))
                        element2 = driver.find_element(
                            By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                        print(element2.get_attribute('src'))

                        itog = str(element2.get_attribute('src'))

                        a1 = itog.split('/240.mp4')
                        a2 = str(a1[0]) + "/720.mp4"
                        print(a2)

                        link2 = a2

                    except:
                        print("Ошибка")

                        link2 = "Ошибка"

                    driver.quit()

                    q = open("text.txt", "w")
                    q.write(str(name))
                    q.write('\n')
                    q.write(str(god))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(opisanie))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(link1))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(link2))
                    q.close()

                    msgH = open("text.txt", "r")
                    msgR = msgH.read()
                    qqq = str(msgR)
                    print(qqq)
                    self.csocket.send(bytes(qqq, 'UTF-8'))

            else:
                self.csocket.send(bytes('Обрабатываю запрос...', 'UTF-8'))

                db = sqlite3.connect('KINO3.db')
                cur = db.cursor()

                word = msg
                r = open("text.txt", "r")
                readR = r.read()

                if readR == "название":
                    driver = webdriver.Firefox(options=options)

                    name_list = []
                    opisanie_list = []
                    god_list = []
                    Link1_list = []
                    Link2_list = []

                    for name in cur.execute('SELECT NAME FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                        name_list.append(name[0])

                    for opisanie in cur.execute('SELECT OPISANIE FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                        opisanie_list.append(opisanie[0])

                    for god in cur.execute('SELECT GOD FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                        god_list.append(god[0])

                    for Link1 in cur.execute('SELECT LINK_STR FROM KINO3 WHERE NAME LIKE ?', ('%'+word+'%',)):
                        Link1_list.append(Link1[0])

                    for film in Link1_list:
                        try:
                            driver.get(film)
                            time.sleep(2)
                            driver.switch_to.frame(
                                driver.find_element_by_tag_name("iframe"))
                            element2 = driver.find_element(
                                By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                            itog = str(element2.get_attribute('src'))
                            a1 = itog.split('/240.mp4')
                            a2 = str(a1[0]) + "/720.mp4"
                            print(a2)

                            Link2_list.append(a2)

                        except:
                            print("Ошибка")

                            Link2_list.append("Ошибка")

                    driver.quit()

                    i = 0
                    while i < len(name_list):

                        q = open("text.txt", "w")
                        q.write(str(name_list[i]))
                        q.write('\n')
                        q.write(str(god_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(opisanie_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(Link1_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(Link2_list[i]))
                        q.close()

                        msgH = open("text.txt", "r")
                        msgR = msgH.read()

                        self.csocket.send(bytes(msgR, 'UTF-8'))
                        time.sleep(1)
                        i = i + 1

                elif readR == "описание":

                    driver = webdriver.Firefox(options=options)
                    z = open('text.txt', 'w')
                    z.seek(0)
                    z.close()
                    name_list = []
                    opisanie_list = []
                    god_list = []
                    Link1_list = []
                    Link2_list = []
                    for name in cur.execute('SELECT NAME FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                        print(name)
                        name_list.append(name[0])

                    for opisanie in cur.execute('SELECT OPISANIE FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                        print(opisanie)
                        opisanie_list.append(opisanie[0])

                    for god in cur.execute('SELECT GOD FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                        print(god)
                        god_list.append(god[0])

                    for Link1 in cur.execute('SELECT LINK_STR FROM KINO3 WHERE OPISANIE LIKE ?', ('%'+word+'%',)):
                        print(Link1)
                        Link1_list.append(Link1[0])

                    for film in Link1_list:

                        try:
                            driver.get(film)
                            time.sleep(2)

                            driver.switch_to.frame(
                                driver.find_element_by_tag_name("iframe"))
                            element2 = driver.find_element(
                                By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                            print(element2.get_attribute('src'))

                            itog = str(element2.get_attribute('src'))

                            a1 = itog.split('/240.mp4')
                            a2 = str(a1[0]) + "/720.mp4"
                            print(a2)

                            Link2_list.append(a2)

                        except:

                            print("Ошибка")

                            Link2_list.append("Ошибка")

                    driver.quit()

                    i = 0
                    while i < len(name_list):

                        q = open("text.txt", "w")
                        q.write(str(name_list[i]))
                        q.write('\n')
                        q.write(str(god_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(opisanie_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(Link1_list[i]))
                        q.write('\n')
                        q.write('\n')
                        q.write(str(Link2_list[i]))
                        q.close()

                        msgH = open("text.txt", "r")
                        msgR = msgH.read()

                        self.csocket.send(bytes(msgR, 'UTF-8'))
                        time.sleep(1)
                        i = i + 1

            print("Запрос " + str(msg) + " обработан")

        print("Клиент ", clientAddress, " покинул нас...")


LOCALHOST = "127.0.0.1"#"10.8.0.6"
PORT = 1488

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((LOCALHOST, PORT))
print("Сервер запущен!")


while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
