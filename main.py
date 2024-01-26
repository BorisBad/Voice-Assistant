# import os
# import speech_recognition as sr
# import pyaudio
# import datetime
import db_handler as dbh
import server.back.server as server
import tts_stt as text_speech
import multiprocessing
import time
import threading
import asyncio
import subprocess
# import pyttsx3
# import json
# from fuzzywuzzy import fuzz
# from vosk import Model, KaldiRecognizer
# import platform

def start_voice_assistant():
#start tts engine, creade test db
        tns = text_speech.init_text_speech()
        
        #start recognising
        text_speech.start_recognising(tns[0],tns[1])

        #stop
        text_speech.end_text_speech(tns[0])

def kill_them_all(procs):
    for p in procs:
        p.terminate()

def main():
    if __name__ == '__main__':
        processes = {}
        manager = multiprocessing.Manager()
        return_code = manager.dict()
        run = manager.Event()
        run.set()  # We should keep running.
        # for i in range(5):
        #     process = multiprocessing.Process(
        #         target=find, args=(f"computer_{i}", i, return_code, run)
        #     )
        #     processes.append(process)
        #     process.start()

        # for process in processes:
        #     process.join()

        # print(return_code.values())


        va_proc = multiprocessing.Process(target=start_voice_assistant)
        sercer_proc = multiprocessing.Process(target=server.start_server)
        processes[0] = va_proc
        processes[1] = sercer_proc
        sercer_proc.start()
        va_proc.start()

        while True:
            if va_proc.exitcode == None:
                 pass
            elif va_proc.exitcode > 0:
                 pass
            elif va_proc.exitcode == 0:
                #terminate all other sub processes
                sercer_proc.terminate()
                #exit!
                exit(0)
                # va_proc.join()
                # break
                # pass
            pass
    
    
main()