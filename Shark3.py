import os
os.system("clear")
import os, sys

REQUIRED = ["aiohttp"]

missing = []
for lib in REQUIRED:
    try:
        __import__(lib)
    except ImportError:
        missing.append(lib)

if missing:
    print("Missing libraries:", ", ".join(missing))
    while True:
        c = input("Install required libraries? (yes/no): ").lower()
        if c == "yes":
            os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-aiohttp")
            print("Done. Restart the tool.")
            sys.exit(0)
        elif c == "no":
            print("Cannot run without required libraries.")
            sys.exit(1)

import asyncio, aiohttp, ssl, socket, time
from urllib.parse import urlparse

RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
CYAN="\033[96m"; PURPLE="\033[95m"; RESET="\033[0m"

TIMEOUT=aiohttp.ClientTimeout(total=5)
WORDLIST_FILE="oli.txt"

WAF_SIG={
    "Cloudflare":"cloudflare",
    "Akamai":"akamai",
    "Sucuri":"sucuri",
    "Imperva":"incapsula",
    "F5":"big-ip"
}

SEC_HEADERS=[
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy"
]

results=[]
SEM=None
WORDLIST=[]
ENABLE_DIRLIST=False
ENABLE_METHODS=False
TLS_DEEP=False

def gradient_author():
    text="AUTHOUR : Owis"
    colors=list(range(0,256))
    end=time.time()+3.2
    while time.time()<end:
        out=""
        for i,c in enumerate(text):
            out+=f"\033[38;5;{colors[i%len(colors)]}m{c}"
        sys.stdout.write("\r"+out+RESET)
        sys.stdout.flush()
        colors=colors[1:]+colors[:1]
        time.sleep(0.05)
    print(RESET)

def banner():
    print(GREEN+"""
███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝
███████╗███████║███████║██████╔╝█████╔╝ 
╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗ 
███████║██║  ██║██║  ██║██║  ██║██║  ██╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""+RESET)
    gradient_author()

def choose_mode():
    print("""
1) Bug‑Bounty Mode (Legal / Safe)
2) Full Search (Recon‑Only)
0) Exit
""")
    c=input("Select mode: ").strip()
    if c=="1": return "BUG"
    if c=="2": return "FULL"
    if c=="0": sys.exit()
    return None

def validate_target(t):
    if not t: return None
    if not t.startswith(("http://","https://")):
        t="https://"+t
    p=urlparse(t)
    if not p.netloc or "." not in p.netloc:
        return None
    return t.rstrip("/")

def load_wordlist():
    if not os.path.isfile(WORDLIST_FILE):
        print(RED+f"Wordlist not found: {WORDLIST_FILE}"+RESET)
        sys.exit(1)
    with open(WORDLIST_FILE, errors="ignore") as f:
        return ["/"+l.strip().lstrip("/") for l in f if l.strip()]

async def fetch(session,url):
    async with SEM:
        try:
            async with session.get(url,allow_redirects=False) as r:
                return r, await r.read()
        except:
            return None,None

def risk(l): return {"Low":3,"Medium":6,"High":9}.get(l,0)

async def scan_wordlist(session,base,baseline):
    for p in WORDLIST:
        r,b=await fetch(session,base+p)
        if r and r.status in (200,401,403) and len(b)!=baseline:
            results.append(("secret Path",p,"Medium"))

async def scan_headers(session,base):
    r,_=await fetch(session,base)
    if not r: return
    miss=[h for h in SEC_HEADERS if h not in r.headers]
    if miss:
        results.append(("Missing Security Headers",", ".join(miss),"Medium"))

async def scan_server(session,base):
    r,_=await fetch(session,base)
    if not r: return
    srv=r.headers.get("Server","")
    if any(x in srv for x in ("Apache/2.2","nginx/1.0","PHP/5")):
        results.append(("Outdated Server",srv,"High"))
    elif srv:
        results.append(("Server Info",srv,"Low"))

async def scan_waf(session,base):
    r,_=await fetch(session,base)
    if not r: return
    h=" ".join(r.headers.values()).lower()
    for n,s in WAF_SIG.items():
        if s in h:
            results.append(("WAF Detected",n,"Low"))
            return

def scan_tls(host):
    try:
        ctx=ssl.create_default_context()
        with socket.create_connection((host,443),timeout=4) as sock:
            with ctx.wrap_socket(sock,server_hostname=host) as s:
                v=s.version()
                if v in ("TLSv1","TLSv1.1"):
                    results.append(("Weak TLS Version",v,"High"))
                else:
                    results.append(("TLS Version",v,"Low"))
    except: pass

async def main():
    banner()
    mode=None
    while not mode:
        mode=choose_mode()

    global SEM, WORDLIST
    WORDLIST=load_wordlist()

    if mode=="BUG":
        SEM=asyncio.Semaphore(32)
        WORDLIST=WORDLIST[:64]
        print(CYAN+"Mode: Bug‑Bounty (Safe)\n"+RESET)
    else:
        SEM=asyncio.Semaphore(60)
        print(CYAN+"Mode: Full Search (Recon‑Only)\n"+RESET)

    t=input("Target: ").strip()
    base=validate_target(t)
    if not base:
        print(RED+"Invalid target"+RESET); sys.exit(1)

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        r,b=await fetch(session,base+"/__404_test__")
        baseline=len(b) if b else 0
        await asyncio.gather(
            scan_wordlist(session,base,baseline),
            scan_headers(session,base),
            scan_server(session,base),
            scan_waf(session,base)
        )

    scan_tls(urlparse(base).hostname)

    score=sum(risk(x[2]) for x in results)
    level="Low" if score<10 else "Medium" if score<20 else "High"

    print(CYAN+"\n=== Security Report ==="+RESET)
    for r in results:
        print(f"{YELLOW}[{r[0]}]{RESET} {r[1]}  Risk:{r[2]}")
    print(GREEN+f"\nOverall Risk: {level} ({score})"+RESET)

if __name__=="__main__":
    asyncio.run(main())
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
    finally:
        input("\nended Press Enter if you want  return to launcher...")
