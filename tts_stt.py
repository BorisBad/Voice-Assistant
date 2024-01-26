import os
import speech_recognition as sr
import pyaudio
import datetime
import db_handler as dbh
import pyttsx3
import json
from fuzzywuzzy import fuzz
from vosk import Model, KaldiRecognizer
import platform

vosk_path = r"C:\Users\XE\Desktop\Pet projects\Voice asssiatant\vosk-model-small-ru-0.22\vosk-model-small-ru-0.22"

#robot voice
def play_voice(text: str, ttsEngine: pyttsx3.Engine, voice_name: str):
    voices = ttsEngine.getProperty("voices")
    for voice in voices:
        if voice.name == voice_name:
            ttsEngine.setProperty('voice', voice.id)    
    ttsEngine.say(str(text))
    ttsEngine.runAndWait()

#creation of test db useless in a long run
def create_test_db(name: str):
    db_name = name
    db = dbh.create_or_connect_to_db(db_name)
    c = dbh.create_cursor(db)
    dbh.delete_table(db,c,'Commands')
    dbh.create_table(db,c,'Commands',[1,2])
    print(dbh.read_from(db,c,'Commands'))
    print('----------------')
    dbh.insert_into(db,c,'Commands',["Скажи привет","cmd","echo Привет",datetime.datetime.now()])
    dbh.insert_into(db,c,'Commands',["Поздоровайся","cmd","echo Здравствуйте",datetime.datetime.now()])
    dbh.insert_into(db,c,'Commands',["Покажи все файлы в текущей папке","cmd","dir",datetime.datetime.now()])
    print(dbh.read_from(db,c,'Commands'))
    print('----------------')
    return (db, c)

#delete test db, useless later    
def del_test_db(db, c):
    dbh.delete_table(db,c,'Commands')
    dbh.delete_cursor(c)
    dbh.close_connection(db)

#offline recognition of a command
def offline_recognition(path:str) -> str:
    model = Model(path) # полный путь к модели
    rec = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=16000, 
    input=True, 
    frames_per_buffer=8192
    )
    stream.start_stream()
    print('Listening...')
    while True:
        data = stream.read(4096) 
        if rec.AcceptWaveform(data):
            text = rec.Result()
            #print(text)
            json_text = json.loads(text) # string to json
            print(json_text['text'])
            if len(json_text['text']) != 0:
                return json_text['text']

#region execute cmd on os
def execute_command_linux(command:str):
    os.system(command)

def execute_command_macos(command:str):
    os.system(command)

def execute_command_win10(command:str, ttsEngine):
    if 'echo' in command:
        play_voice(command.strip('echo'), ttsEngine, 'Irina')
    else:
        os.system(command)
#endregion

def choose_platform_and_execute(command, ttsEngine):
    plfm = platform.system()
    if plfm == 'Windows':
        execute_command_win10(command,ttsEngine)
    elif plfm == 'Linux':
        execute_command_linux(command,ttsEngine)
    elif plfm == 'Darwin':
        execute_command_macos(command,ttsEngine)

#is there code phrase in given command?
def activate(text:str):
    #if fuzz.ratio('Компьютер',text) > 90: 
    if 'Компьютер'.lower() in text.lower():
        return True
    else:
        return False

def shut_off(text:str):
    if 'выключись'.lower() in text.lower():
        return True
    else:
        return False      

def start_recognising(db_data, ttsEngine):
    while True:
        given_command = offline_recognition(vosk_path)
        if activate(given_command):
            given_command = given_command[9:]
            if shut_off(given_command):
                break
        else:
            continue

    #given_command = offline_recognition()
        items = dbh.read_from(db_data[0],db_data[1],'Commands')
                
        accuracy = 0
        for item in items:
            if given_command == item[1].lower():
                selected_command = item[3]
                break
            if fuzz.partial_ratio(item[1].lower(), given_command) >= accuracy:
                selected_command = item[3]
                accuracy = fuzz.partial_ratio(item[1], given_command)
            

        choose_platform_and_execute(selected_command, ttsEngine)

def init_text_speech():

    db_data = create_test_db('test.db')
    ttsEngine = pyttsx3.init()
    return [db_data, ttsEngine]
    #startserver

    # while True:
    #     given_command = offline_recognition(vosk_path)
    #     if activate(given_command):
    #         given_command = given_command[9:]
    #         if shut_off(given_command):
    #             break
    #     else:
    #         continue

    # #given_command = offline_recognition()
    #     items = dbh.read_from(db_data[0],db_data[1],'Commands')
                
    #     accuracy = 0
    #     for item in items:
    #         if given_command == item[1].lower():
    #             selected_command = item[3]
    #             break
    #         if fuzz.partial_ratio(item[1].lower(), given_command) >= accuracy:
    #             selected_command = item[3]
    #             accuracy = fuzz.partial_ratio(item[1], given_command)
            

    #     choose_platform_and_execute(selected_command, ttsEngine)
    
    # del_test_db(db_data[0], db_data[1])

def end_text_speech(db_data:tuple):
    del_test_db(db_data[0], db_data[1])

#main()

