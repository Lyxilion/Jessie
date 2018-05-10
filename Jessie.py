import twitter
import re
from gtts import gTTS
import os
import time
import keyboard
import pyglet
import json

player = pyglet.media.Player()
Twitter = False
TwitterConnected = False
Stop = False
PushToTalk = True

def TwitterInt() :
    """
    Initialisation de l'api Twitter
    :return: 0
    """
    global api                                                                   #Lancement API
    global LastMentionId
    global LastDMId
    global TwitterConnected
    print('Verifying credentials...')
    if os.path.exists("Data/credentials.txt"):                                                  #Récuperation infos. connexion
        fichier = open("Data/credentials.txt", "r")
        credentials = fichier.read()
        fichier.close()
        print("-Credentials ok!")
    else :
        print("-No credentials found, please lunch config.py...")

    credentials = re.split("""\n""",credentials)

    api = twitter.Api(consumer_key=credentials[0],                                              #Connexion
                      consumer_secret=credentials[1],
                      access_token_key=credentials[2],
                      access_token_secret=credentials[3])
    if api.VerifyCredentials() :
        print("-Connected to Twitter API !")
    else :
        print("Connection failed, please check your credentials !")

    print("Verifying data...")
    if not os.path.exists("Data/data.txt"):                                                     #au premier lancement, creation des data
        LastMention = api.GetMentions(count=1)
        LastMentionId = re.match("""^.*ID=(.*)\, S.*$""", str(LastMention)).group(1)
        LastDM = api.GetDirectMessages(count=1)
        LastDMId = re.match("""^.*ID=(.*)\, S.*$""", str(LastDM)).group(1)

        fichier = open("Data/data.txt", "w")
        fichier.write(LastMentionId + "\n" + LastDMId)
        fichier.close()
        print("-No data found, creating data.")
    else :
        print("-Data ok!")

    fichier = open("Data/data.txt", "r")                                                       #récuperations des data dernier co
    buffer = fichier.read()
    buffer = re.split("""\n""",buffer)
    LastMentionId = buffer[0]
    LastDMId = buffer[1]
    fichier.close()
    TwitterConnected = True
    return 0

def ReadMentions():
    """
    Fonction qui lit les dernière mentions
    :return: LastMentionId
    """
    if len(mentions) > 0 :
        for e in mentions:
            tweet = json.loads(str(e))
            speech ="De " + tweet["user"]['name'] + " : " + tweet["text"]
            print(speech)
            Talk(speech)
        LastMentionId = tweet["id"]
        fichier = open("Data/data.txt", "w")
        fichier.write(str(LastMentionId)+ "\n" + str(LastDMId))
        fichier.close()
        return LastMentionId
    else :
        print("Vous n'avez pas de nouvelles mentions !")

def ReadDM() :
    """
    Fonction qui lit les derniers DM
    :return: LastDMId
    """
    if len(DM) > 0 :
        for e in reversed(DM):
            tweet = json.loads(str(e))
            speech ="De " + tweet["sender_screen_name"] + " : " + tweet["text"]
            print(speech)
            Talk(speech)
        LastDMId = tweet["id"]
        fichier = open("Data/data.txt", "w")
        fichier.write(str(LastMentionId) + "\n" + str(LastDMId))
        fichier.close()
        return LastDMId
    else :
        print("Vous n'avez pas de nouveau méssage!")

def TwitterCheck():
    """
    check si ya de nouveau dm ou mentions
    :return: 0
    """
    global mentions
    global DM
    mentions = api.GetMentions(since_id=LastMentionId)  # since_id=LastMentionId)
    DM = api.GetDirectMessages(since_id=LastDMId)
    if len(mentions) >0 or len(DM) > 0 :
        speech = "Vous avez "+ str(len(mentions))+ " mentions et "+ str(len(DM))+ " D M à lire!"
        print(speech)
        Talk(speech)

def Talk(sentence : str):
    tts = gTTS(sentence, lang='fr')
    tts.save("Sound/voice.mp3")
    song = pyglet.media.load('Sound/voice.mp3')
    player.queue(song)
    player.play()

speech = "Bonjour, je suis Jessie."
print(speech)
Talk(speech)
while not Stop :
    if PushToTalk :
        Talk("Que puis-je faire pour vous ?")
        answer = input("Que puis-je faire pour vous ?")

        PushToTalk = False

    if answer == "twitter":
        Twitter = True
    if answer == "stop" :
        Stop = True
        break
    if answer == "musique" :
        print("soon")

    if Twitter:
        if not TwitterConnected :
            TwitterInt()
        TwitterCheck()

        if len(mentions) >0 or len(DM) > 0 :
            Talk("Que voulez vous Lire ?")
            choice = input("Que voulez vous Lire ?")
            buff = re.split(""" """, choice)
            if re.match("""[Ll]ire""", buff[0]):
                if len(buff) > 1:
                    if re.match("[Dd][Mm]", buff[1]):
                        LastDMId = ReadDM()
                    elif re.match("[Mm]entions?", buff[1]):
                        LastMentionId = ReadMentions()
                    else:
                        print('ERROR : no such subcommande')
                else :
                    print("ERROR : No argurments")
            else:
                print("ERROR : cette commande n'existe pas")

    i = 0
    while i < 600:
        time.sleep(0.5)
        if keyboard.is_pressed("pause"):
            PushToTalk = True
            break
        i += 1
Talk("A bientôt !")
print("A bientôt !")
time.sleep(2)