import time
import random
import datetime
import telepot
import telepot.namedtuple
import socket


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    m = telepot.namedtuple.Message(**msg)
    ok = False
    winking_face = u'\U0001F609'

    print '[%s:%s - %s:%s] --> %s' % (m.chat.id, m.chat.username, str(datetime.datetime.now().hour),
                                      str(datetime.datetime.now().minute), command)
    with open('Users.txt') as f:
        array = [line.rstrip() for line in f]
    f.close()
    if m.chat.username in array:
        ok = True
    if ok:
        if command == '/start':
            bot.sendMessage(chat_id, 'Tron Avviato...')
        elif command == '/ping':
            buff = 'Al tuo servizio ' + winking_face
            bot.sendMessage(chat_id, buff)
        elif command == '/casuale100':
            bot.sendMessage(chat_id, random.randint(1, 100))
        elif command == '/casuale20':
            bot.sendMessage(chat_id, random.randint(1, 20))
        elif command == '/casuale6':
            bot.sendMessage(chat_id, random.randint(1, 6))
        elif command == '/data':
            buff = '%s/%s/%s' % (str(datetime.datetime.now().day), str(datetime.datetime.now().month),
                                 str(datetime.datetime.now().year))
            bot.sendMessage(chat_id, buff)
        elif command == '/localip':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com", 80))
            bot.sendMessage(chat_id, s.getsockname()[0])
            s.close()
        elif command == '/listautenti':
            with open('Admin.txt') as f1:
                array1 = [line.rstrip() for line in f1]
            f1.close()
            if m.chat.username in array1:
                with open('Users.txt') as f:
                    array = [line.rstrip() for line in f]
                f.close()
                for user in array:
                    bot.sendMessage(chat_id, user)
            else:
                buff = 'Perdonami %s ma bisogna essere amministratore per esequire questo comando...' % m.chat.first_name
                bot.sendMessage(chat_id, buff)
        else:
            buff = 'Perdonami %s ma non conosco questo comando...' % m.chat.first_name
            bot.sendMessage(chat_id, buff)

    else:
        buff = 'Perdonami %s ma non hai i permessi per farmi eseguire comandi...' % m.chat.first_name
        bot.sendMessage(chat_id, buff)
        if m.chat.username == 'None':
            bot.sendMessage(chat_id, 'Sembra inoltre che tu non abbia uno Username, per crearne uno vai in impostazioni'
                                     '-->Username')


bot = telepot.Bot('324692150:AAENW7pqXh74gIn0ruxdbDeFUMytRqtlkaM')
bot.message_loop(handle)
print 'Tron Avviato ...'

while 1:
    time.sleep(0)
