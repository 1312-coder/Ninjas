import time
import random
import webbrowser
import requests

def read_file():
    response = requests.get("https://www.youtube.com/watch?v=vnMLCe54C8Q&list=RDvnMLCe54C8Q&start_radio=1")
    urls = response.content.decode().split("\n")
    return urls

def set_clock(clock):
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == clock:
            break
        time.sleep(1)

def set_url(urls):
    webbrowser.open(random.choice(urls))

def main():
    urls = read_file
    clock = input ("24 hors format (HH:MM)")
    set_clock(clock)
    set_url(urls)
    

main()