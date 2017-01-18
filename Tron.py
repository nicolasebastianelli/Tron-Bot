import time
import random
import datetime
import telepot
import telepot.namedtuple
import socket

ruserlist = list()
auserlist = list()

def rimuoviUtente(m,command):
	global ruserlist
	ok=-1
	ruserlist.remove(m.chat.first_name)
	f= open("Users.txt","r")
	lines= f.readlines()
	f.close()
	f= open("Users.txt","w")
	for line in lines:
		if line!= command+"\n":
			f.write(line)
		else:
			ok=1
	f.close()
	if ok==1:
		bot.sendMessage(m.chat.id, 'Utente %s rimosso con successo' % command)
	else:
		bot.sendMessage(m.chat.id, 'Utente %s non presente nella lista utenti' % command)

def aggiungiUtente(m,command):
	global auserlist
	ok=1
	auserlist.remove(m.chat.first_name)
	f= open("Users.txt","r")
	lines= f.readlines()
	f.close()
	f= open("Users.txt","w")
	for line in lines:
		if line == command+"\n":
			f.write(line)
			ok=-1
		else:
			f.write(line)
	if ok==1:
		f.write(command+"\n")
		bot.sendMessage(m.chat.id, 'Utente %s aggiunto con successo' % command)
	else:
		bot.sendMessage(m.chat.id, 'Utente %s gia presente nella lista utenti' % command)
	f.close()
	

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
	with open('Admin.txt') as f:
		array = [line.rstrip() for line in f]
	f.close()
	if m.chat.username in array:
		ok = True
	if ok:
		if command == '/start':
			bot.sendMessage(chat_id, 'Tron Avviato...\nDimmi cosa fare e faro del mio meglio per aiutarti '+winking_face)
		elif command == '/ping':
			buff = 'Al tuo servizio ' + winking_face
			bot.sendMessage(chat_id, buff)
		elif  m.chat.first_name in ruserlist:
			rimuoviUtente(m,command)
		elif m.chat.first_name in auserlist:
			aggiungiUtente(m, command)
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
		elif command == '/rimuoviutente':
			global ruserlist
			with open('Admin.txt') as f1:
				array1 = [line.rstrip() for line in f1]
			f1.close()
			if m.chat.username in array1:
				ruserlist.extend([m.chat.first_name])
				buff= 'Ok %s inviami il nome utente da rimuvere' %  m.chat.first_name
				bot.sendMessage(chat_id, buff)
			else:
				buff = 'Perdonami %s ma bisogna essere amministratore per esequire questo comando...' % m.chat.first_name
				bot.sendMessage(chat_id, buff)
		elif command == '/aggiungiutente':
			global auserlist
			with open('Admin.txt') as f1:
				array1 = [line.rstrip() for line in f1]
			f1.close()
			if m.chat.username in array1:
				auserlist.extend([m.chat.first_name])
				buff = 'Ok %s inviami il nome utente da aggiungere' % m.chat.first_name
				bot.sendMessage(chat_id, buff)
			else:
				buff = 'Perdonami %s ma bisogna essere amministratore per esequire questo comando...' % m.chat.first_name
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
				with open('Users.txt') as f2:
					array2 = [line.rstrip() for line in f2]
				f2.close()
				for user in array2:
					bot.sendMessage(chat_id, user)
			else:
				buff = 'Perdonami %s ma bisogna essere amministratore per esequire questo comando...' % m.chat.first_name
				bot.sendMessage(chat_id, buff)
		elif command == '/sam':
			i=random.randint(1, 6)
			in_file = open("sam/"+str(i)+".jpeg", "r")
			bot.sendPhoto(chat_id, in_file)
			in_file.close()
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
