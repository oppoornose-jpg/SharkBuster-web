try:
    import requests
except ImportError:
    print("[!] Missing library: requests")
    c = input("Install requests now? (yes/no): ").lower()
    if c == "yes":
        os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-requests")
        print("[+] Installed. Restart the tool.")
        sys.exit(0)
    else:
        print("[-] Cannot continue without requests.")
        sys.exit(1)
import os
import sys
import requests
def install_whisker_menu():
    os.system("clear")
    
    import shutil

    home = os.path.expanduser("~")
    app_dir = os.path.join(home, ".local/share/applications")
    icon_dir = os.path.join(home, ".local/share/icons")

    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(icon_dir, exist_ok=True)

    desktop_path = os.path.join(app_dir, "sharkbuster-web.desktop")
    icon_target = os.path.join(icon_dir, "sharkbuster-web.png")

    
    if os.path.isfile(desktop_path):
        return

    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_source = os.path.join(script_dir, "image.png")

    if not os.path.isfile(icon_source):
        print("Icon image.png not found")
        return

    shutil.copy(icon_source, icon_target)

    desktop_entry = f"""[Desktop Entry]
Name=SharkBuster Web
Comment=Web scanning,recon,more  tool
Exec=python3 {os.path.abspath(__file__)}
Icon=sharkbuster-web
Terminal=true
Type=Application
Categories=Reconnaissance;Utility;
"""

    with open(desktop_path, "w") as f:
        f.write(desktop_entry)


install_whisker_menu()
os.system("mkdir -p ~/.local/share/desktop-directories ~/.config/menus")

os.system("""echo '[Desktop Entry]
Name=Reconnaissance
Icon=security-high
Type=Directory' > ~/.local/share/desktop-directories/kali-recon.directory""")

os.system("""[ -f ~/.config/menus/applications.menu ] || \
cp /etc/xdg/menus/applications.menu ~/.config/menus/""")

os.system("""grep -q sharkbuster-web.desktop ~/.config/menus/applications.menu || \
sed -i '/<\/Menu>/i \
<Menu>\
<Name>Reconnaissance</Name>\
<Directory>kali-recon.directory</Directory>\
<Include><Filename>sharkbuster-web.desktop</Filename></Include>\
</Menu>' ~/.config/menus/applications.menu""")

os.system("xfce4-panel -r")      

if os.path.isfile("version.txt"):
    with open("version.txt", "r") as f:
        V = f.read().strip()
else:
    V = "2.2.7"


def check_update():
    try:
        url = "https://raw.githubusercontent.com/oppoornose-jpg/SharkBuster/main/version.txt"
        remote_version = requests.get(url, timeout=3).text.strip()

        if remote_version != V:
            print(f"[*] Update found! Local: {V} | Remote: {remote_version}")

            if os.path.isdir(".git"):
                print("[*] Updating tool to latest version...")
                os.system("git pull")
                
                if os.path.isfile("version.txt"):
                    with open("version.txt", "r") as f:
                        V_local = f.read().strip()
                    print(f"[*] Updated to version {V_local}")
                else:
                    print("[!] version.txt not found after update")
                
                print( "[*] updated  Please restart the tool manually.")
                sys.exit(0)

            else:
                print("[!] Cannot auto-update, folder is not a git repository")
                print("[*] If updated manually, please restart the tool.")
                sys.exit(0)

        else:
            print(f"[*] Tool is up-to-date (version {V})")

    except Exception as e:
        print(f"[!] Update check failed: {e}")
        sys.exit(0)

check_update()

GREEN   = "\033[92m"
CYAN    = "\033[96m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
RESET   = "\033[0m"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def run(tool):
    try:
        os.system(f"python3 {tool}")
    except KeyboardInterrupt:
        print(RED + "\n[!] Stopped by user" + RESET)
        input("Press Enter to return...")

while True:
    clear()
   
    print(f"{GREEN}")
    print("███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗")
    print("██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝")
    print("███████╗███████║███████║██████╔╝█████╔╝ ")
    print("╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗ ")
    print("███████║██║  ██║██║  ██║██║  ██║██║  ██╗")
    print("╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝")
    print(RESET)

    
    print(YELLOW + "=== Shark Tools Launcher ===" + RESET)
    print(f"{CYAN}1){RESET} SharkBuster-web - Web Discovery Fast Tool for finding scret web paths like gobuster")
    print(f"{CYAN}2){RESET} SharkScan-web - tool for testing and scanning websites")
    print(f"{CYAN}0){RESET} Exit")
    
    print(GREEN + "This tool automatically checks for updates and keeps itself up-to-date."
Enjoy using it without any worries!
    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        os.system("python3 Shark4.py")
    elif choice == "2":
        os.system("python3 Shark3.py")
    elif choice == "0":
        print(GREEN + "exited" + RESET)
        sys.exit()
    else:
        input(RED + "Invalid choice, press Enter..." + RESET)
