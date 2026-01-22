import os
from colorama import Fore, Style, init
import requests
import threading

import time
import asyncio
import aiohttp
init(autoreset=True)

import time

text = "AUTHOUR: Owis   "  



def boot():
    print("started")
    os.system("clear")
    print("started")
    
boot() 





while True:
    name = input(
        "just for using this tool you agree that is for educational purposes only "
        "if you agree press enter, else Ctrl+Z"
    )
    if name == "":
        break
    else:
        print("\033[91mPlease press Enter only!\033[0m")

RED = "\033[91m"
RESET = "\033[0m"
print(Fore.YELLOW + "warning")
print(RED + " you agreed using tool for educational purposes only " + RESET, name)
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.BLUE, Fore.RED,Fore.GREEN,Fore.BLACK,Fore.CYAN,Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.BLUE,Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.BLUE, Fore.RED,Fore.GREEN,Fore.BLACK,Fore.CYAN,Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE,Fore.CYAN]

target_line = 5  


for color in colors:
          
    print(f"\033[{target_line};0H" + color + text + Style.RESET_ALL, end="")
    time.sleep(0.1)

host = input("target host or url: ")

if not host.startswith(("http://", "https://")):
    host = "https://" + host

if not host:
    print(Fore.RED + "you should enter target host or url")
    host = input("target full url: ")
    time.sleep(3)
if not host:
    print(Fore.RED + "you should enter url")
    host = input("target full url: ")

if not host:
     print(Fore.RED+ "you should enter url")
     host = input("target full url: ")

ingored1= ("login", "signin", "auth")
valid = {200,301,302,307,401,403,429}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
ingored = (".jpg", ".png", ".css", ".js", ".svg", ".ico")

baseline = None   

r = requests.get(host)
print("status ",r.status_code)

wordlist = input("wordlist file: ")
if not wordlist:
    print(Fore.RED + "You should enter an paths file")
    password = input("wordlist file: ")

word = (Fore.GREEN + " wordlist: ")
base = host.rstrip("/") + "/"
print("trying with url "+ host + word ,wordlist)

sem = asyncio.Semaphore(30)

def status_color(code):
    if code == 200:
        return Fore.GREEN
    elif code in (301, 302, 307):
        return Fore.YELLOW
    elif code in (429,500):
        return Fore.RED
    elif code in (401, 403):
        return Fore.CYAN
    else:
        return Fore.WHITE


async def check(session, p):
    global baseline

    p = p.strip()

    if p.endswith(ingored):
        return

    async with sem:
        try:
            async with session.get(
                base + p.strip(),
                timeout=aiohttp.ClientTimeout(total=3.7),
                allow_redirects=False,
                headers=headers
            ) as r:

                
                location = ""
                

                if r.status in (301, 302, 307):
                    location = r.headers.get("Location", "").lower()

                if location in ("/", "/login", "/index.php"):
                    return

               
                body = await r.read()
                length = len(body)
             

                if baseline and length == baseline:
                        return

                if r.status in valid and r.status != 204:
                    color = status_color(r.status)
                    print(f"{color}{base+p} {r.status}{Fore.RESET}")

        except Exception:
            pass


async def run():
    global baseline

    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(connector=connector) as session:

        
        try:
            async with session.get(
                base + "random_not_exist_123456789",
                timeout=aiohttp.ClientTimeout(total=3.7),
                allow_redirects=False,
                headers=headers
            ) as r:
                baseline = len(await r.read())
               
        except:
            baseline = None
       

        with open(wordlist, errors="ignore") as f:
            batch = []
            batch_size = 60

            for line in f:
                batch.append(line)
                if len(batch) == batch_size:
                    await asyncio.gather(*(check(session, p) for p in batch))
                    batch.clear()

            if batch:
                await asyncio.gather(*(check(session, p) for p in batch))


asyncio.run(run())
