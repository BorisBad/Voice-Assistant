import os
import sys
import speech_recognition as sr
import pyaudio
import threading
import datetime
import time
import db_handler as dbh
import subprocess

def mycallback(recognizer, audio):
    text = recognizer.recognize_google(audio, language="ru-RU")
    print(text)
    #print()
#recognize_google(self, audio_data, key=None, language="en-US", pfilter=0, show_all=False, with_confidence=False):

def main():
# #region WTF?
    db_name = 'test.db'
    db = dbh.create_or_connect_to_db(db_name)
    c = dbh.create_cursor(db)

    dbh.create_table(db,c,'Commands',[[],[],[],[],[],[]],[('id', 1),('awaited_request', 3),('module',3),('command',3),('last_modified', 4)])
    print(dbh.read_from(db,c,'Commands'))
    print('----------------')
    #request, module, command, last_mod
    dbh.insert_into(db,c,'Commands',["Скажи привет","cmd","echo Здарова",datetime.datetime.now()])
    print(dbh.read_from(db,c,'Commands'))
    print('----------------')
    #SET ? = ? WHERE id = ? 
    dbh.update_in(db,c,'Commands', ["command", "echo Привет", 1])
    print(dbh.read_from(db,c,'Commands'))


    items = dbh.read_from(db,c,'Commands')
    # print(items)
    # print(items[0])
    # print(items[0][3])
    # print("Print 'stop' to end")
    # while input() != "stop":
    #     print("Print 'stop' to end")
    #rez = subprocess.run(["cd"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(rez.stdout.decode())
    




    
#     print('----------------')
#     dbh.delete_from(db,c,'Commands',[1])
#     print(dbh.read_from(db,c,'Commands'))
#     print('----------------')

#     print("Print 'stop' to end")
#     while input() != "stop":
#         print("Print 'stop' to end")

#     dbh.delete_table(db,c,'Commands')
#     dbh.delete_cursor(c)
#     dbh.close_connection(db)

# #endregion
    
  print(dbh.check_table_name(input()))  
    
    
    # mic = sr.Microphone()
    # recognizer = sr.Recognizer()
    # is_stop = True

    # while is_stop:
    #     # with mic as source:
    #     #     recognizer.adjust_for_ambient_noise(source)
    #     text = recognizer.listen(mic)
    #     #stopper = recognizer.listen_in_background(mic, mycallback)
    #     time.sleep(3)
    #     #stopper()
    #     is_stop = False
    #     print(text)
            
#if __name__ == '__main__':
main()