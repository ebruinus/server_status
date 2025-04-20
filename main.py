import subprocess
import json
import os
import sys
from jinja2 import Template

# Bestandsnaam voor opslaan van serverlijst
SERVER_FILE = "servers.json"

# Functie om de serverlijst in te lezen of een lege lijst te geven als het bestand nog niet bestaat
def load_servers():
    if os.path.exists(SERVER_FILE):
        with open(SERVER_FILE, "r") as f:
            return json.load(f)
    return []

# Functie om de serverlijst op te slaan
def save_servers():
    with open(SERVER_FILE, "w") as f:
        json.dump(SERVERS, f, indent=4)

# Globale lijst van servers
SERVERS = load_servers()

def add_server(ip):
    # Voeg de server toe met een standaard status van 'unreachable'
    if not any(s['ip'] == ip for s in SERVERS):  # Controleer of de server al bestaat
        server = {"ip": ip, "status": "unreachable"}
        SERVERS.append(server)
        save_servers()
        print(f"Server {ip} toegevoegd.")
    else:
        print(f"Server {ip} is al toegevoegd.")

def remove_server(ip):
    global SERVERS
    # Verwijder de server als deze bestaat
    SERVERS = [s for s in SERVERS if s['ip'] != ip]
    save_servers()
    print(f"Server {ip} verwijderd.")

def list_servers():
    if SERVERS:
        print("Lijst van servers:")
        for server in SERVERS:
            print(f"- {server['ip']} | Status: {server['status']}")
    else:
        print("Er zijn geen servers in de lijst.")

def ping(ip):
    """Ping een server en retourneer True als het succesvol is."""
    try:
        result = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0  # Als de returncode 0 is, is de server bereikbaar
    except Exception as e:
        print(f"Error tijdens pingen van {ip}: {e}")
        return False

# Functie voor het genereren van de HTML-rapport
def generate_html_report(servers, log):
    with open("template.html", "r") as f:
        template = Template(f.read())
    
    # Render de template met de servers en logboek
    rendered_html = template.render(servers=servers, log=log)
    
    # Sla het bestand op als server_status_report.html
    with open("server_status_report.html", "w") as f:
        f.write(rendered_html)
    print("Rapport gegenereerd: server_status_report.html")

# Functie om te controleren of de server lijst leeg is
def check_servers():
    if SERVERS:
        print("Er zijn servers in de lijst, genereer HTML.")
        generate_html_report(SERVERS, ["Server statuses geüpdatet."])  # Hier kun je logbestanden toevoegen als je dat wilt
    else:
        print("Geen servers gevonden om een rapport van te maken.")

# Beheer modus via sys.argv
if len(sys.argv) > 1:
    command = sys.argv[1]

    match command:
        case "1":  # Voeg server toe
            if len(sys.argv) > 2:
                add_server(sys.argv[2])
            else:
                print("Geef een IP op om toe te voegen.")
        case "2":  # Verwijder server
            if len(sys.argv) > 2:
                remove_server(sys.argv[2])
            else:
                print("Geef een IP op om te verwijderen.")
        case "3":  # Toon servers
            list_servers()
        case "4":  # Ping een server
            if len(sys.argv) > 2:
                server = sys.argv[2]
                if ping(server):
                    print(f"Server {server} is bereikbaar!")
                else:
                    print(f"Server {server} is niet bereikbaar.")
            else:
                print("Geef een IP op om te pingen.")
        case "0":  # Stoppen
            sys.exit()
        case _:
            print("Ongeldig commando. Gebruik: 1 <ip>, 2 <ip>, 3, 4 <ip>, 0.")

    sys.exit()

# Interactieve modus
while True:
    ans = input("1) Voeg server toe, 2) Verwijder server, 3) Toon servers, 4) Ping server, 5) Genereer HTML rapport, 0) Stoppen : [1/2/3/4/5/0] ")

    match ans:
        case "1":
            ip = input("Voer het IP van de server in om toe te voegen: ")
            add_server(ip)
    
        case "2":
            ip = input("Voer het IP van de server in om te verwijderen: ")
            remove_server(ip)
        
        case "3":
            list_servers()
        
        case "4":
            ip = input("Voer het IP van de server in: ")
            if ping(ip):
                print(f"Server {ip} is bereikbaar!")
            else:
                print(f"Server {ip} is niet bereikbaar.")
        
        case "5":
            check_servers()  # Genereer de HTML
        case "0":
            quit()
