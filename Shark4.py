print("SharkBuster")
try:
    import requests, os, colorama, threading, time, asyncio, aiohttp, shutil
except ImportError:
            
            print("Error: missing libraries")
            while True:
                req = input("Do you want install required things? (yes/no): ").lower()
                if req == "yes":
                    print("installing...")
                    print("installing speed depends on your internet speed")
                    os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-requests python3-colorama python3-aiohttp")
                    print("if you have an error  if its still report it in issues")
                    break
                elif req == "no":
                    print("you must install required things for running tool correctly.")
                    exit()
                    break
                else:
                    print( "You must type yes or no ")
                    print(req) 
import os
from colorama import Fore, Style, init
import requests
import threading
import sys
import time
import asyncio
import aiohttp
import atexit, signal
import random
ANDROID_UA = [
    f"Mozilla/5.0 (Linux; Android {v}; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
    for v in range(7, 16)
]

IOS_UA = [
    f"Mozilla/5.0 (iPhone; CPU iPhone OS {v}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v}.0 Mobile/15E148 Safari/604.1"
    for v in range(6, 18)
]

DESKTOP_UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

USER_AGENTS = ANDROID_UA + IOS_UA + DESKTOP_UA
init(autoreset=True)
results = []
def save_progress():
    if results:
        with open("results.txt", "w") as f:
            f.write("\n".join(results))
        print("\nsaved progress results in results.txt")
atexit.register(save_progress)
signal.signal(signal.SIGTSTP, lambda s, f: exit())
signal.signal(signal.SIGTERM, lambda s, f: exit())        

        

def boot():
    print("started")
    os.system("clear")
    print("started")
    
boot() 


                          

    
text = "AUTHOUR: Owis          "  





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

end_time = time.time() + 3.3
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

while not host:
    print(Fore.RED + "you should enter target host or url")
    host = input("target full url: ")
    time.sleep(3)
    

ingored1= ("login", "signin", "auth")
valid = {200,301,302,307,401,403,429}

ingored = (".jpg", ".png", ".css", ".js", ".svg", ".ico")

baseline = None   
tested = 0
loaded = 0
r = requests.get(host)
print("status ",r.status_code)

wordlist = input("wordlist file: ")
while not wordlist or not os.path.isfile(wordlist):
    k = "please check that you moved paths wordlist to SharkBuster file or wordlist exist"
    print(Fore.RED + "Invalid wordlist file")
    print(Fore.YELLOW + k)
    wordlist = input("wordlist file: ")

word = (Fore.GREEN + " wordlist: ")
base = host.rstrip("/") + "/"
print("trying with url "+ host + word ,wordlist)
print()
sys.stdout.write("\033[s")  
sys.stdout.flush()

sem = asyncio.Semaphore(200)
lock = asyncio.Lock()
start_time = time.time()
def print_counter():
    speed = tested / max(time.time() - start_time, 1)
    sys.stdout.write("\033[u")  
    sys.stdout.write("\033[2K")   
    sys.stdout.write(
        f"[>] Tried: {tested} | Loaded: {loaded} | Speed: {int(speed)} req/s"
    )
    sys.stdout.flush()
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
    global baseline, loaded, tested

    p = p.strip()

    if p.endswith(ingored):
        return

    async with sem:
        try:
            async with lock:
                tested += 1
                print_counter()
 
                
            headers = {
               "User-Agent": random.choice(USER_AGENTS)
            }
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
                    url = f"{base+p} {r.status}"
                    if url not in results:
                        results.append(url)
                        sys.stdout.write("\n" + f"{color}{url}{Fore.RESET}")  
                        sys.stdout.flush()
                        
        except Exception:
            pass


async def run():
    global baseline, loaded

    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(
        connector=connector,
        headers={"User-Agent": random.choice(USER_AGENTS)}
    ) as session:

        try:
            async with session.get(
                base + "random_not_exist_123456789",
                timeout=aiohttp.ClientTimeout(total=3.7),
                allow_redirects=False,
                headers={"User-Agent": random.choice(USER_AGENTS)}
            ) as r:
                baseline = len(await r.read())
               
        except:
            baseline = None
       

        with open(wordlist, errors="ignore") as f:
            batch = []
            batch_size = 200

            for line in f:
                batch.append(line)
                loaded += 1

                if len(batch) == batch_size:
                    await asyncio.gather(*(check(session, p) for p in batch))
                    batch.clear()

            if batch:
                await asyncio.gather(*(check(session, p) for p in batch))



def main():
    asyncio.run(run())
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
    finally:
        input("\nPress Enter to return to launcher...")
