#refarance by https://www.makeuseof.com/python-alarm-clock-simple-create/
import datetime
import time 
import random
import webbrowser

with open('C:\\Users\\samra\\OneDrive\\Desktop\\IT007\\prctice\\youtube.txt', 'r') as file:
    youtube_urls = file.readlines()

invalid = True
while(invalid):
    # Get a valid user input for the clock 
    print("set clock(HH:MM)")
    userinput = input(">> ")

    alarmTime = [int(n) 
                # convert 6:30 to an array of [6, 30].
                for n in userinput.split(":")]
    #enter valid time 
    if alarmTime[0] >= 24 or alarmTime[0] < 0:
        invalid=True
    elif alarmTime[1] >= 60 or alarmTime[1] < 0:
        invalid=True
    else:
        invalid= False

now = datetime.datetime.now()
# Create datetime object with today's date 
alarmDateTime = datetime.datetime(now.year, now.month, now.day, alarmTime[0], alarmTime[1])

# Waiting for alarm time 
while datetime.datetime.now() < alarmDateTime:
    time.sleep(1)

# open random YouTube URL
webbrowser.open(random.choice(youtube_urls))