# -*- coding: utf-8 -*-
import time
import json
import os
import random
import datetime
import telepot
import telepot.namedtuple
import socket
import urllib
import urllib2
import thread
from bs4 import BeautifulSoup
from slugify import slugify
from gtts import gTTS
from tempfile import NamedTemporaryFile

ruserlist = list()
auserlist = list()
muserlist = list()
duserlist = list()
playing = 0

def say(word,args):
        global playing
        if(playing==0):
                tts= gTTS(text=word,lang='it')
                f=NamedTemporaryFile()
                tts.write_to_fp(f)
                cmd="mpg321 -q "+f.name
                os.system("pkill -SIGHUP mpg321")
                os.system(cmd)
                f.close()

def play(m,arg):
        global playing
        if(playing==1):
                bot.sendMessage(m.chat.id, "Le canzoni sono gia in play")
        else:
                bot.sendMessage(m.chat.id, "Avvio riproduzione canzoni")
                say("Ok "+m.chat.first_name+", avvio riproduzione canzoni",1)
                playing = 1
                os.system("mpg321 -q -z -l 0 Music/*")

def stop(m):
        global playing
        if(playing==0):
                bot.sendMessage(m.chat.id, "Nessuna canzone in play al momento")
                say("Nessuna canzone in play al momento "+m.chat.first_name,1)
        else:
                playing = 0
                os.system("pkill -SIGHUP mpg321")
                bot.sendMessage(m.chat.id, "Stop riproduzione canzoni")

def next(m):
        global playing
        if(playing==0):
                bot.sendMessage(m.chat.id, "Nessuna canzone in play al momento")
                say("Nessuna canzone in play al momento "+m.chat.first_name,1)
        else:
                os.system("pkill -SIGINT mpg321")
                bot.sendMessage(m.chat.id, "Cambio canzone")
                
        
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
		buff="Utente %s rimosso con successo" % command
	else:
		buff="Utente %s non presente nella lista utenti" % command	
        thread.start_new_thread(say,(buff,1))
	bot.sendMessage(m.chat.id,buff)

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
		buff= "Utente %s aggiunto con successo" % command
	else:
		buff = "Utente %s gia presente nella lista utenti" % command
	thread.start_new_thread(say,(buff,1))
	bot.sendMessage(m.chat.id, buff)
	f.close()

def downloadCanzone(m,command):
        global muserlist
        global duserlist
        base_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='
	muserlist.remove(m.chat.first_name)
	song_name = command
	buff='Bene '+m.chat.first_name+', la canzone \"'+song_name+'\" e in preparazione...'
	bot.sendMessage(m.chat.id,buff)
	say(buff,1)
	query = urllib.quote(song_name+ "song")
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read(), "html.parser")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                video_url = 'https://www.youtube.com' + vid['href']
                print ('Video url: ' + video_url)
                json_url = base_url + video_url
                print ('Json url: ' + json_url)
                response = urllib.urlopen(json_url)
                try:
                        data = json.loads(response.read())
                        if 'length' not in data:
                                raise ValueError("No length present.")
                                break
                        if 'link' not in data:
                                raise ValueError("No link present.")
                                break
                        if 'title' not in data:
                                raise ValueError("No title present.")
                                break
                        length = data['length']
                        downLoad_url = data['link']
                        title = data['title']
                        print ('length: ' + str(length))
                        print ('download url: ' + downLoad_url)
                        print ('title: ' + title)
                        upload_file = path + slugify(title).lower() + '.mp3'
                        print ('upload_file name : ' + upload_file)
                        if not (os.path.exists(upload_file)) :
                                if(int(length)>601):
                                        buff="La lunghezza della canzone supera i 10 minuti, download annullato. Riprova con un titolo diverso"
                                        bot.sendMessage(m.chat.id, buff)
                                        say(buff,1)
                                        print ('Lunghezza canzone superiore a 10 minuti, download annullato.')
                                else:
                                        buff=m.chat.first_name+" il download della tua canzone e iniziato..."
                                        bot.sendMessage(m.chat.id, buff)
                                        say(buff,1)
                                        print ('Download della canzone nella collezione del bot.')
                                        downloadSong(downLoad_url, upload_file)
                                        buff="Download completato. La canzone e stata aggiunta alla collezione"
                                        bot.sendMessage(m.chat.id, buff)
                                        say(buff,1)
                                        print ('Download completato.')
                                duserlist.remove(m.chat.first_name)
                        else:
                                buff=m.chat.first_name+" la canzone "+song_name+" e gia presente nella collezione"
                                bot.sendMessage(m.chat.id, buff)
                                say(buff,1)
                                print ('Canzone gia presente nella collezione.')
                                duserlist.remove(m.chat.first_name)
                except ValueError as e:
                        print 'Nessuna canzone trovata'
                        duserlist.remove(m.chat.first_name)
                        buff="Non e stata trovata nessuna canzone con quel titolo "+m.chat.first_name+", per favore, riprova con un titolo diverso"
                        bot.sendMessage(m.chat.id, buff)
                        say(buff,1)
                except Exception as e:
                        print 'Errore inaspettato' , e
                        duserlist.remove(m.chat.first_name)
                        buff= "Errore nel download inaspettato, per favore riprova piu tardi"+m.chat.first_name
                        bot.sendMessage(m.chat.id, buff)
                        say(buff,1)
                break

def downloadSong(url, fileLoc):
    f = open(fileLoc, 'wb')
    usock = urllib2.urlopen(url)
    try :
      file_size = int(usock.info().getheaders("Content-Length")[0])
      print ('Scaricando: %s Bytes: %s' % (fileLoc, file_size))
    except IndexError:
      print ('Dimensione file sconosciuta: index error')
    block_size = 8192
    while True:
        buff = usock.read(block_size)
        if not buff:
            break
        f.write(buff)
    f.close()
	

def handle(msg):
        global duserlist
        global muserlist
        global auserlist
        global ruserlist
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
                        buff="Tron Avviato...\nDimmi cosa fare e faro del mio meglio per aiutarti "+winking_face
			bot.sendMessage(chat_id, buff)
			thread.start_new_thread(say,(buff,1))
		elif command == '/ping':
			buff = 'Al tuo servizio ' + winking_face
			thread.start_new_thread(say,(buff,1))
			bot.sendMessage(chat_id, buff)
		elif  m.chat.first_name in ruserlist:
			rimuoviUtente(m,command)
		elif m.chat.first_name in auserlist:
			aggiungiUtente(m, command)
		elif m.chat.first_name in muserlist:
                        duserlist.extend([m.chat.first_name])
                        thread.start_new_thread(downloadCanzone,(m, command))
                elif command == '/play':
                        thread.start_new_thread(play,(m,1))
                elif command == '/stop':
                        stop(m)
                elif command == '/next':
                        next(m)
		elif command == '/casuale100':
			bot.sendMessage(chat_id, random.randint(1, 100))
		elif command == '/casuale20':
			bot.sendMessage(chat_id, random.randint(1, 20))
		elif command == '/casuale6':
			bot.sendMessage(chat_id, random.randint(1, 6))
		elif command == '/data':
                        nday=datetime.datetime.today().weekday()
                        if(nday==0):
                                day="Lunedì"
                        elif(nday==1):
                                day="Martedì"
                        elif(nday==2):
                                day="Mercoledì"
                        elif(nday==3):
                                day="Giovedì"
                        elif(nday==4):
                                day="Venerdì"
                        elif(nday==5):
                                day="Sabato"
                        elif(nday==6):
                                day="Domenica"
			buff = 'Oggi è %s %s/%s/%s' % (day, str(datetime.datetime.now().day), str(datetime.datetime.now().month),
								 str(datetime.datetime.now().year))
			thread.start_new_thread(say,(buff,1))
			bot.sendMessage(chat_id, buff)
		elif command == '/downloadsong':
			if  m.chat.first_name in duserlist:
                            buff="Download di una canzone già in corso, attendi per favore"
                        else:
                            muserlist.extend([m.chat.first_name])
                            buff= 'Ok %s inviami il titolo e/o l autore della canzone' %  m.chat.first_name
                        thread.start_new_thread(say,(buff,1))
                        bot.sendMessage(chat_id, buff)
		elif command == '/aggiungiutente':
			with open('Admin.txt') as f1:
				array1 = [line.rstrip() for line in f1]
			f1.close()
			if m.chat.username in array1:
				auserlist.extend([m.chat.first_name])
				buff = 'Ok %s inviami il nome utente da aggiungere' % m.chat.first_name
			else:
				buff = 'Perdonami %s ma bisogna essere amministratore per eseguire questo comando...' % m.chat.first_name
			thread.start_new_thread(say,(buff,1))
			bot.sendMessage(chat_id, buff)
		elif command == '/rimuoviutente':
			with open('Admin.txt') as f1:
				array1 = [line.rstrip() for line in f1]
			f1.close()
			if m.chat.username in array1:
				ruserlist.extend([m.chat.first_name])
				buff= 'Ok %s inviami il nome utente da rimuovere' %  m.chat.first_name
				thread.start_new_thread(say,(buff,1))
				bot.sendMessage(chat_id, buff)
			else:
				buff = 'Perdonami %s ma bisogna essere amministratore per eseguire questo comando...' % m.chat.first_name
				thread.start_new_thread(say,(buff,1))
				bot.sendMessage(chat_id, buff)
		elif command == '/localip':
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("gmail.com", 80))
			buff=s.getsockname()[0]
			bot.sendMessage(chat_id, buff)
			thread.start_new_thread(say,("IP locale: "+buff,1))
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
				buff = 'Perdonami %s ma bisogna essere amministratore per eseguire questo comando...' % m.chat.first_name
				thread.start_new_thread(say,(buff,1))
				bot.sendMessage(chat_id, buff)
		elif command == '/sam':
			i=random.randint(1, 6)
			in_file = open("sam/"+str(i)+".jpeg", "r")
			bot.sendPhoto(chat_id, in_file)
			in_file.close()
		else:
			buff = 'Perdonami %s ma non conosco questo comando...' % m.chat.first_name
			thread.start_new_thread(say,(buff,1))
			bot.sendMessage(chat_id, buff)

	else:
		buff = 'Perdonami %s ma non hai i permessi per farmi eseguire comandi...' % m.chat.first_name
		thread.start_new_thread(say,(buff,1))
		bot.sendMessage(chat_id, buff)
		if m.chat.username == 'None':
			bot.sendMessage(chat_id, 'Sembra inoltre che tu non abbia uno Username, per crearne uno vai in impostazioni'
									 '-->Username')

path = '/home/pi/Desktop/Tron/Music/'
bot = telepot.Bot('324692150:AAENW7pqXh74gIn0ruxdbDeFUMytRqtlkaM')
bot.message_loop(handle)
print 'Tron Avviato ...'

while 1:
	time.sleep(0)
