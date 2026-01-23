import os
from colorama import Fore, Style, init
import requests
import threading
import sys
import time
import asyncio
import aiohttp
init(autoreset=True)

        

def boot():
    print("started")
    os.system("clear")
    print("started")
    
boot() 

try:
    import requests, os, colorama, threading, time, asyncio, aiohttp
except ImportError:
            print(Fore.RED + "Error: missing libraries")
            while True:
                req = input("Do you want install required things? (yes/no): ").lower()
                if req == "yes":
                    print(Fore.CYAN + "installing...")
                    print(Fore.YELLOW + "installing speed depends on your internet speed")
                    os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-requests python3-colorama python3-aiohttp")
                    break
                elif req == "no":
                    exit()
                    break
                else:
                    print(Fore.RED + "You must type yes or no")
                    print(req) 
                          

def customize():
    os.system("clear")
boot()
os.system("clear")
text = "AUTHOUR: Owis          "  
V = "1.0.0"

def check_update():
    try:
        url = "https://raw.githubusercontent.com/oppoornose-jpg/SharkBuster/main/version.txt"
        remote_version = requests.get(url, timeout=3).text.strip()

        if remote_version != V:
            print("[*] Update found, updating...")
            # تأكد أن المشروع git repo
            if os.path.isdir(".git"):
                os.system("git pull")
                print("[*] Update completed, restart the tool")
            else:
                print("[!] Can't auto-update, this folder is not a git repository")
            sys.exit(0)  # بديل آمن لـ exit()
        else:
            print("[*] Tool is up-to-date!")
    except Exception as e:
        print(f"[!] Update check failed: {e}")

check_update()
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
time.sleep(2.5)


target_line = 7
colors = list(range(0, 256))

end_time = time.time() + 2.9
while time.time() < end_time:
    out = ""
    for i, c in enumerate(text):
        color = colors[i % len(colors)]
        out += f"\033[38;5;{color}m{c}"
    sys.stdout.write("\r" + out + "\033[0m")
    sys.stdout.flush()
    colors = colors[1:] + colors[:1]  
    time.sleep(0.05)


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

sem = asyncio.Semaphore(32)

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
            batch_size = 62

            for line in f:
                batch.append(line)
                if len(batch) == batch_size:
                    await asyncio.gather(*(check(session, p) for p in batch))
                    batch.clear()

            if batch:
                await asyncio.gather(*(check(session, p) for p in batch))


asyncio.run(run())
