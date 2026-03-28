import threading
import pyotp
import time
import json
import requests
import subprocess
import sqlite3
import shutil
import pytz
import traceback
import random
import psutil
import sys
import gc
import os
from rich.live import Live
from datetime import datetime, timezone
from rich.table import Table #type: ignore
from rich.panel import Panel #type: ignore
from rich.text import Text #type: ignore
from rich.align import Align #type: ignore
from rich.box import ROUNDED #type: ignore
from rich.console import Console #type: ignore
from threading import Lock, Event
from psutil import boot_time, process_iter, cpu_percent, virtual_memory, Process, NoSuchProcess, AccessDenied, ZombieProcess

try:
    from prettytable import PrettyTable #type: ignore
except ImportError:
    os.system("pip install prettytable")
    from prettytable import PrettyTable #type: ignore

package_lock = Lock()
status_lock = Lock()
rejoin_lock = Lock()
bot_instance = None
bot_thread = None
socket_server = None
stop_webhook_thread = False
webhook_thread = None
webhook_url = None
device_name = None
webhook_interval = None
reset_tab_interval = None
close_and_rejoin_delay = None
codex_bypass_enabled = False
codex_bypass_thread = None
try:
    # Tenta ler o tempo real, se falhar (Permission Denied), usa o tempo atual
    BOOT_TIME = psutil.boot_time()
except Exception:
    BOOT_TIME = time.time()

auto_android_id_enabled = False
auto_android_id_thread = None
auto_android_id_value = None

globals()["_disable_ui"] = "0"
globals()["package_statuses"] = {}
globals()["_uid_"] = {}
globals()["_user_"] = {}
globals()["_change_acc"] = "0"
globals()["is_runner_ez"] = False
globals()["check_exec_enable"] = "1"
globals()["codex_bypass_active"] = False

executors = {
    "Fluxus": "/storage/emulated/0/Fluxus/",
    "Codex": "/storage/emulated/0/Codex/",
    "Codex Clone 001": "/storage/emulated/0/RobloxClone001/Codex/",
    "Codex Clone 002": "/storage/emulated/0/RobloxClone002/Codex/",
    "Codex Clone 003": "/storage/emulated/0/RobloxClone003/Codex/",
    "Codex Clone 004": "/storage/emulated/0/RobloxClone004/Codex/",
    "Codex Clone 005": "/storage/emulated/0/RobloxClone005/Codex/",
    "Codex Clone 006": "/storage/emulated/0/RobloxClone006/Codex/",
    "Codex Clone 007": "/storage/emulated/0/RobloxClone007/Codex/",
    "Codex Clone 008": "/storage/emulated/0/RobloxClone008/Codex/",
    "Codex Clone 009": "/storage/emulated/0/RobloxClone009/Codex/",
    "Codex Clone 010": "/storage/emulated/0/RobloxClone010/Codex/",
    "Codex Clone 011": "/storage/emulated/0/RobloxClone011/Codex/",
    "Codex Clone 012": "/storage/emulated/0/RobloxClone012/Codex/",
    "Codex Clone 013": "/storage/emulated/0/RobloxClone013/Codex/",
    "Codex Clone 014": "/storage/emulated/0/RobloxClone014/Codex/",
    "Codex Clone 015": "/storage/emulated/0/RobloxClone015/Codex/",
    "Codex Clone 016": "/storage/emulated/0/RobloxClone016/Codex/",
    "Codex Clone 017": "/storage/emulated/0/RobloxClone017/Codex/",
    "Codex Clone 018": "/storage/emulated/0/RobloxClone018/Codex/",
    "Codex Clone 019": "/storage/emulated/0/RobloxClone019/Codex/",
    "Codex Clone 020": "/storage/emulated/0/RobloxClone020/Codex/",
    "Codex VNG Clone 001": "/storage/emulated/0/RobloxVNGClone001/Codex/",
    "Codex VNG Clone 002": "/storage/emulated/0/RobloxVNGClone002/Codex/",
    "Codex VNG Clone 003": "/storage/emulated/0/RobloxVNGClone003/Codex/",
    "Codex VNG Clone 004": "/storage/emulated/0/RobloxVNGClone004/Codex/",
    "Codex VNG Clone 005": "/storage/emulated/0/RobloxVNGClone005/Codex/",
    "Codex VNG Clone 006": "/storage/emulated/0/RobloxVNGClone006/Codex/",
    "Codex VNG Clone 007": "/storage/emulated/0/RobloxVNGClone007/Codex/",
    "Codex VNG Clone 008": "/storage/emulated/0/RobloxVNGClone008/Codex/",
    "Codex VNG Clone 009": "/storage/emulated/0/RobloxVNGClone009/Codex/",
    "Codex VNG Clone 010": "/storage/emulated/0/RobloxVNGClone010/Codex/",
    "Codex VNG Clone 011": "/storage/emulated/0/RobloxVNGClone011/Codex/",
    "Codex VNG Clone 012": "/storage/emulated/0/RobloxVNGClone012/Codex/",
    "Codex VNG Clone 013": "/storage/emulated/0/RobloxVNGClone013/Codex/",
    "Codex VNG Clone 014": "/storage/emulated/0/RobloxVNGClone014/Codex/",
    "Codex VNG Clone 015": "/storage/emulated/0/RobloxVNGClone015/Codex/",
    "Codex VNG Clone 016": "/storage/emulated/0/RobloxVNGClone016/Codex/",
    "Codex VNG Clone 017": "/storage/emulated/0/RobloxVNGClone017/Codex/",
    "Codex VNG Clone 018": "/storage/emulated/0/RobloxVNGClone018/Codex/",
    "Codex VNG Clone 019": "/storage/emulated/0/RobloxVNGClone019/Codex/",
    "Codex VNG Clone 020": "/storage/emulated/0/RobloxVNGClone020/Codex/",
    "Arceus X": "/storage/emulated/0/Arceus X/",
    "Arceus X Clone 001": "/storage/emulated/0/RobloxClone001/Arceus X/",
    "Arceus X Clone 002": "/storage/emulated/0/RobloxClone002/Arceus X/",
    "Arceus X Clone 003": "/storage/emulated/0/RobloxClone003/Arceus X/",
    "Arceus X Clone 004": "/storage/emulated/0/RobloxClone004/Arceus X/",
    "Arceus X Clone 005": "/storage/emulated/0/RobloxClone005/Arceus X/",
    "Arceus X Clone 006": "/storage/emulated/0/RobloxClone006/Arceus X/",
    "Arceus X Clone 007": "/storage/emulated/0/RobloxClone007/Arceus X/",
    "Arceus X Clone 008": "/storage/emulated/0/RobloxClone008/Arceus X/",
    "Arceus X Clone 009": "/storage/emulated/0/RobloxClone009/Arceus X/",
    "Arceus X Clone 010": "/storage/emulated/0/RobloxClone010/Arceus X/",
    "Arceus X Clone 011": "/storage/emulated/0/RobloxClone011/Arceus X/",
    "Arceus X Clone 012": "/storage/emulated/0/RobloxClone012/Arceus X/",
    "Arceus X Clone 013": "/storage/emulated/0/RobloxClone013/Arceus X/",
    "Arceus X Clone 014": "/storage/emulated/0/RobloxClone014/Arceus X/",
    "Arceus X Clone 015": "/storage/emulated/0/RobloxClone015/Arceus X/",
    "Arceus X Clone 016": "/storage/emulated/0/RobloxClone016/Arceus X/",
    "Arceus X Clone 017": "/storage/emulated/0/RobloxClone017/Arceus X/",
    "Arceus X Clone 018": "/storage/emulated/0/RobloxClone018/Arceus X/",
    "Arceus X Clone 019": "/storage/emulated/0/RobloxClone019/Arceus X/",
    "Arceus X Clone 020": "/storage/emulated/0/RobloxClone020/Arceus X/",
    "Arceus X VNG Clone 001": "/storage/emulated/0/RobloxVNGClone001/Arceus X/",
    "Arceus X VNG Clone 002": "/storage/emulated/0/RobloxVNGClone002/Arceus X/",
    "Arceus X VNG Clone 003": "/storage/emulated/0/RobloxVNGClone003/Arceus X/",
    "Arceus X VNG Clone 004": "/storage/emulated/0/RobloxVNGClone004/Arceus X/",
    "Arceus X VNG Clone 005": "/storage/emulated/0/RobloxVNGClone005/Arceus X/",
    "Arceus X VNG Clone 006": "/storage/emulated/0/RobloxVNGClone006/Arceus X/",
    "Arceus X VNG Clone 007": "/storage/emulated/0/RobloxVNGClone007/Arceus X/",
    "Arceus X VNG Clone 008": "/storage/emulated/0/RobloxVNGClone008/Arceus X/",
    "Arceus X VNG Clone 009": "/storage/emulated/0/RobloxVNGClone009/Arceus X/",
    "Arceus X VNG Clone 010": "/storage/emulated/0/RobloxVNGClone010/Arceus X/",
    "Arceus X VNG Clone 011": "/storage/emulated/0/RobloxVNGClone011/Arceus X/",
    "Arceus X VNG Clone 012": "/storage/emulated/0/RobloxVNGClone012/Arceus X/",
    "Arceus X VNG Clone 013": "/storage/emulated/0/RobloxVNGClone013/Arceus X/",
    "Arceus X VNG Clone 014": "/storage/emulated/0/RobloxVNGClone014/Arceus X/",
    "Arceus X VNG Clone 015": "/storage/emulated/0/RobloxVNGClone015/Arceus X/",
    "Arceus X VNG Clone 016": "/storage/emulated/0/RobloxVNGClone016/Arceus X/",
    "Arceus X VNG Clone 017": "/storage/emulated/0/RobloxVNGClone017/Arceus X/",
    "Arceus X VNG Clone 018": "/storage/emulated/0/RobloxVNGClone018/Arceus X/",
    "Arceus X VNG Clone 019": "/storage/emulated/0/RobloxVNGClone019/Arceus X/",
    "Arceus X VNG Clone 020": "/storage/emulated/0/RobloxVNGClone020/Arceus X/",
    "RonixExploit": "/storage/emulated/0/RonixExploit/",
    "RonixExploit Clone 001": "/storage/emulated/0/RobloxClone001/RonixExploit/",
    "RonixExploit Clone 002": "/storage/emulated/0/RobloxClone002/RonixExploit/",
    "RonixExploit Clone 003": "/storage/emulated/0/RobloxClone003/RonixExploit/",
    "RonixExploit Clone 004": "/storage/emulated/0/RobloxClone004/RonixExploit/",
    "RonixExploit Clone 005": "/storage/emulated/0/RobloxClone005/RonixExploit/",
    "RonixExploit Clone 006": "/storage/emulated/0/RobloxClone006/RonixExploit/",
    "RonixExploit Clone 007": "/storage/emulated/0/RobloxClone007/RonixExploit/",
    "RonixExploit Clone 008": "/storage/emulated/0/RobloxClone008/RonixExploit/",
    "RonixExploit Clone 009": "/storage/emulated/0/RobloxClone009/RonixExploit/",
    "RonixExploit Clone 010": "/storage/emulated/0/RobloxClone010/RonixExploit/",
    "RonixExploit Clone 011": "/storage/emulated/0/RobloxClone011/RonixExploit/",
    "RonixExploit Clone 012": "/storage/emulated/0/RobloxClone012/RonixExploit/",
    "RonixExploit Clone 013": "/storage/emulated/0/RobloxClone013/RonixExploit/",
    "RonixExploit Clone 014": "/storage/emulated/0/RobloxClone014/RonixExploit/",
    "RonixExploit Clone 015": "/storage/emulated/0/RobloxClone015/RonixExploit/",
    "RonixExploit Clone 016": "/storage/emulated/0/RobloxClone016/RonixExploit/",
    "RonixExploit Clone 017": "/storage/emulated/0/RobloxClone017/RonixExploit/",
    "RonixExploit Clone 018": "/storage/emulated/0/RobloxClone018/RonixExploit/",
    "RonixExploit Clone 019": "/storage/emulated/0/RobloxClone019/RonixExploit/",
    "RonixExploit Clone 020": "/storage/emulated/0/RobloxClone020/RonixExploit/",
    "RonixExploit VNG Clone 001": "/storage/emulated/0/RobloxVNGClone001/RonixExploit/",
    "RonixExploit VNG Clone 002": "/storage/emulated/0/RobloxVNGClone002/RonixExploit/",
    "RonixExploit VNG Clone 003": "/storage/emulated/0/RobloxVNGClone003/RonixExploit/",
    "RonixExploit VNG Clone 004": "/storage/emulated/0/RobloxVNGClone004/RonixExploit/",
    "RonixExploit VNG Clone 005": "/storage/emulated/0/RobloxVNGClone005/RonixExploit/",
    "RonixExploit VNG Clone 006": "/storage/emulated/0/RobloxVNGClone006/RonixExploit/",
    "RonixExploit VNG Clone 007": "/storage/emulated/0/RobloxVNGClone007/RonixExploit/",
    "RonixExploit VNG Clone 008": "/storage/emulated/0/RobloxVNGClone008/RonixExploit/",
    "RonixExploit VNG Clone 009": "/storage/emulated/0/RobloxVNGClone009/RonixExploit/",
    "RonixExploit VNG Clone 010": "/storage/emulated/0/RobloxVNGClone010/RonixExploit/",
    "RonixExploit VNG Clone 011": "/storage/emulated/0/RobloxVNGClone011/RonixExploit/",
    "RonixExploit VNG Clone 012": "/storage/emulated/0/RobloxVNGClone012/RonixExploit/",
    "RonixExploit VNG Clone 013": "/storage/emulated/0/RobloxVNGClone013/RonixExploit/",
    "RonixExploit VNG Clone 014": "/storage/emulated/0/RobloxVNGClone014/RonixExploit/",
    "RonixExploit VNG Clone 015": "/storage/emulated/0/RobloxVNGClone015/RonixExploit/",
    "RonixExploit VNG Clone 016": "/storage/emulated/0/RobloxVNGClone016/RonixExploit/",
    "RonixExploit VNG Clone 017": "/storage/emulated/0/RobloxVNGClone017/RonixExploit/",
    "RonixExploit VNG Clone 018": "/storage/emulated/0/RobloxVNGClone018/RonixExploit/",
    "RonixExploit VNG Clone 019": "/storage/emulated/0/RobloxVNGClone019/RonixExploit/",
    "RonixExploit VNG Clone 020": "/storage/emulated/0/RobloxVNGClone020/RonixExploit/",
    "Delta": "/storage/emulated/0/Delta/",
    "Cryptic": "/storage/emulated/0/Cryptic/",
    "KRNL": "/storage/emulated/0/krnl/",
    "Trigon": "/storage/emulated/0/Trigon/",
    "Cubix": "/storage/emulated/0/Cubix/",
    "FrostWare": "/storage/emulated/0/FrostWare/",
    "Evon": "/storage/emulated/0/Evon/",
    "h202": "/storage/emulated/0/h202/",
}
# Lista baseada nos executores padrão
workspace_paths = [f"{base_path}Workspace" for base_path in executors.values()] + \
                  [f"{base_path}workspace" for base_path in executors.values()]

# Adicione os caminhos reais dos dados dos clones
clones_internos = ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv"]
for pkg in clones_internos:
    workspace_paths.append(f"/data/data/{pkg}/files/workspace")
    workspace_paths.append(f"/data/data/{pkg}/files/Workspace")

if not os.path.exists("Shouko.dev"):
    os.makedirs("Shouko.dev", exist_ok=True)
SERVER_LINKS_FILE = "Shouko.dev/server-links.txt"
ACCOUNTS_FILE = "Shouko.dev/accounts.txt"
CONFIG_FILE = "Shouko.dev/config.json"

version = "2.2.5 | Customized by Shouko.dev"

def login_gboard_estavel():
    print("\n\033[1;34m[ ! ] Iniciando Login (Modo Gboard)\033[0m")
    contas = [
        {"user": "saitama0000432", "pass": "saitama32", "pkg": "ywcw.lnu.exhl"},
        {"user": "saitama0000436", "pass": "saitama36", "pkg": "ub.wnjb.bzz"},
        {"user": "saitama0000437", "pass": "saitama37", "pkg": "ixq.vf.jlr"},
        {"user": "saitama0000447", "pass": "saitama47", "pkg": "srl.mvn.gv"}
    ]

    for i, conta in enumerate(contas, 1):
        print(f"\n\033[1;36m[ {i}/4 ] Abrindo: {conta['pkg']}\033[0m")
        
        # 1. Abre o app (Com o nome da categoria corrigido)
        os.system(f"su -c 'monkey -p {conta['pkg']} -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1'")
        
        # 2. Tempo para você preparar a tela
        print("   -> PREPARAÇÃO MANUAL:")
        print("      1. Clique em 'Log In'")
        print("      2. Clique no campo de 'Username' (Teclado deve subir)")
        
        for t in range(25, 0, -1):
            print(f"      -> Injetando em: {t}s   ", end="\r")
            time.sleep(1)

        
        # 3. Injeção de dados (MÉTODO DA SETA - GBOARD)
        print(f"\n   -> Injetando dados no {conta['pkg']}...")
        
        # PASSO 1: Escreve o Usuário
        os.system(f"su -c 'input text {conta['user']}'")
        time.sleep(2.0) 
        
        # PASSO 2: Simula o clique na 'Seta' (Próximo)
        print("      * Clicando na Seta para pular...")
        os.system(f"su -c 'input keyevent 66'") 
        time.sleep(2.5) # Pausa para o cursor sair de uma caixa e entrar na outra
        
        # PASSO 3: Escreve a Senha
        # Se ele logar direto sem escrever a senha, avise aqui!
        print(f"      * Escrevendo senha...")
        os.system(f"su -c 'input text {conta['pass']}'")
        time.sleep(1.5)
        
        # PASSO 4: Enter Final para Logar
        os.system(f"su -c 'input keyevent 66'")

    print("\n\033[1;32m[ SUCESSO ] Todas as contas foram processadas!\033[0m")
class Utilities:
    @staticmethod
    def collect_garbage():
        gc.collect()

    @staticmethod
    def log_error(error_message):
        with open("error_log.txt", "a") as error_log:
            error_log.write(f"{error_message}\n\n")

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_hwid_codex():
        return subprocess.run(["settings", "get", "secure", "android_id"], capture_output=True, text=True, check=True).stdout.strip()

    @staticmethod
    def calculate_time_left(expiry_timestamp):
        current_time = int(time.time())
        time_left = expiry_timestamp / 1000 - current_time
        return time_left

    @staticmethod
    def format_time_left(time_left):
        hours, remainder = divmod(time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02} hour(s) {int(minutes):02} minute(s) {int(seconds):02} second(s)"

    @staticmethod
    def convert_to_ho_chi_minh_time(expiry_timestamp):
        ho_chi_minh_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        expiry_datetime = datetime.fromtimestamp(expiry_timestamp / 1000, pytz.utc)
        expiry_datetime = expiry_datetime.astimezone(ho_chi_minh_tz)
        return expiry_datetime.strftime("%Y-%m-%d %H:%M:%S")

class FileManager:
    SERVER_LINKS_FILE = "Shouko.dev/server-link.txt"
    ACCOUNTS_FILE = "Shouko.dev/account.txt"
    CONFIG_FILE = "Shouko.dev/config-wh.json"

    @staticmethod
    def save_server_links(server_links):
        try:
            os.makedirs(os.path.dirname(FileManager.SERVER_LINKS_FILE), exist_ok=True)
            with open(FileManager.SERVER_LINKS_FILE, "w") as file:
                for package, link in server_links:
                    file.write(f"{package},{link}\n")
            print("\033[1;32m[ Shouko.dev ] - Server links saved successfully.\033[0m")
        except IOError as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error saving server links: {e}\033[0m")
            Utilities.log_error(f"Error saving server links: {e}")

    @staticmethod
    def load_server_links():
        server_links = []
        if os.path.exists(FileManager.SERVER_LINKS_FILE):
            with open(FileManager.SERVER_LINKS_FILE, "r") as file:
                for line in file:
                    if "," in line:
                        package, link = line.strip().split(",", 1)
                        server_links.append((package, link))
        return server_links

    @staticmethod
    def save_accounts(accounts):
        os.makedirs(os.path.dirname(FileManager.ACCOUNTS_FILE), exist_ok=True)
        with open(FileManager.ACCOUNTS_FILE, "w") as file:
            for package, user_id in accounts:
                file.write(f"{package},{user_id}\n")

    @staticmethod
    def load_accounts():
        accounts = []
        if os.path.exists(FileManager.ACCOUNTS_FILE):
            with open(FileManager.ACCOUNTS_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if "," in line:
                        try:
                            package, user_id = line.split(",", 1)
                            globals()["_user_"][package] = user_id
                            accounts.append((package, user_id))
                        except ValueError:
                            continue
        return accounts

    @staticmethod
    def find_userid_from_file(file_path):
        try:
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'r') as file:
                content = file.read()
                userid_start = content.find('"UserId":"')
                if userid_start == -1: return None
                userid_start += len('"UserId":"')
                userid_end = content.find('"', userid_start)
                return content[userid_start:userid_end]
        except Exception:
            return None

    @staticmethod
    def get_username(user_id):
        user = FileManager.load_saved_username(user_id)
        if user: return user
        # Simplificado para evitar erros de importação de requests no exemplo
        return f"User_{user_id}"

    @staticmethod
    def save_username(user_id, username):
        try:
            data = {}
            if os.path.exists("usernames.json"):
                with open("usernames.json", "r") as file:
                    try: data = json.load(file)
                    except: data = {}
            data[user_id] = username
            with open("usernames.json", "w") as file:
                json.dump(data, file)
        except: pass

    @staticmethod
    def load_saved_username(user_id):
        try:
            with open("usernames.json", "r") as file:
                return json.load(file).get(user_id)
        except: return None

    @staticmethod
    def download_file(url, destination, binary=False):
        try:
            import requests
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                mode = 'wb' if binary else 'w'
                with open(destination, mode) as file:
                    if binary: shutil.copyfileobj(response.raw, file)
                    else: file.write(response.text)
                return destination
        except: return None

    @staticmethod
    def _load_config():
        global webhook_url, device_name, webhook_interval
        try:
            if os.path.exists(FileManager.CONFIG_FILE):
                with open(FileManager.CONFIG_FILE, "r") as file:
                    config = json.load(file)
                    webhook_url = config.get("webhook_url")
                    device_name = config.get("device_name")
                    webhook_interval = config.get("interval", 60)
        except: pass

    @staticmethod
    def save_config():
        try:
            config = {"webhook_url": webhook_url, "device_name": device_name}
            with open(FileManager.CONFIG_FILE, "w") as file:
                json.dump(config, file, indent=4)
        except: pass

    @staticmethod
    def get_uptime():
        try:
            import psutil
            uptime_seconds = time.time() - psutil.boot_time()
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        except: return "N/A"

    @staticmethod
    def get_system_info():
        try:
            import psutil
            return {
                "cpu": psutil.cpu_percent(),
                "mem": psutil.virtual_memory().percent
            }
        except: return False
    
class RobloxManager:
    @staticmethod
    def check_user_online(user_id):
        url = "https://presence.roblox.com/v1/presence/last-online"
        body = {"userIds": [int(user_id)]}
        # Headers básicos para a Roblox não bloquear o Termux
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    
        try:
            import requests
            res = requests.post(url, json=body, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get("lastOnlinePresences"):
                    presence = data["lastOnlinePresences"][0]
                    # Se o status for 2 (In-Game), ele está farmando
                    if presence.get("userPresenceType", 0) == 2:
                        return 2 
            return 0 # Caso contrário, está Offline ou no Menu
        except:
            return None

    @staticmethod
    def get_roblox_packages():
        return ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv", "kxm.ak.qyfi"]

    @staticmethod
    def kill_roblox_processes():
        # Usamos a função de cima para garantir que a lista é a mesma!
        clones = RobloxManager.get_roblox_packages()
        # Adicionamos o oficial só por segurança
        clones.append("com.roblox.client") 
        
        for p in clones:
            print(f"\033[1;31m[ Shouko.dev ] - Finalizando: {p}\033[0m")
            # Comando simplificado e direto para Cloud Phones
            os.system(f"su -c 'am force-stop {p}'")
            # O 'pkill' às vezes buga se o processo já morreu, então o force-stop é melhor sozinho
        
        time.sleep(2)
    
    @staticmethod
    def kill_roblox_process(package_name):
        print(f"\033[1;96m[ Shouko.dev ] - Killing Roblox process for {package_name}...\033[0m")
        try:
            # O comando abaixo deve estar exatamente alinhado
            subprocess.run(
                ["su", "-c", f"am force-stop {package_name}"],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"\033[1;32m[ Shouko.dev ] - Killed process for {package_name}\033[0m")
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error killing process for {package_name}: {e}\033[0m")
            Utilities.log_error(f"Error killing process for {package_name}: {e}")

    @staticmethod
    def delete_cache_for_package(package_name):
        cache_path = f'/data/data/{package_name}/cache/'
        if os.path.exists(cache_path):
            os.system(f"su -c 'rm -rf {cache_path}'")
            print(f"\033[1;32m[ Shouko.dev ] - Cache cleared for {package_name}\033[0m")
        else:
            print(f"\033[1;93m[ Shouko.dev ] - No cache found for {package_name}\033[0m")

    @staticmethod
    def launch_roblox(package_name, server_link):
        try:
            RobloxManager.kill_roblox_process(package_name)
            time.sleep(2)

            with status_lock:
                globals()["_uid_"][globals()["_user_"][package_name]] = time.time()
                globals()["package_statuses"][package_name]["Status"] = f"\033[1;36mOpening Roblox for {package_name}...\033[0m"
                UIManager.update_status_table()

            subprocess.run([
                'am', 'start',
                '-a', 'android.intent.action.MAIN',
                '-n', f'{package_name}/com.roblox.client.startup.ActivitySplash'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(10)

            with status_lock:
                globals()["package_statuses"][package_name]["Status"] = f"\033[1;36mJoining Roblox for {package_name}...\033[0m"
                UIManager.update_status_table()

            subprocess.run([
                'am', 'start',
                '-a', 'android.intent.action.VIEW',
                '-n', f'{package_name}/com.roblox.client.ActivityProtocolLaunch',
                '-d', server_link
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(20)
            with status_lock:
                globals()["package_statuses"][package_name]["Status"] = "\033[1;32mJoined Roblox\033[0m"
                UIManager.update_status_table()

        except Exception as e:
            error_message = f"Error launching Roblox for {package_name}: {e}"
            with status_lock:
                globals()["package_statuses"][package_name]["Status"] = f"\033[1;31m{error_message}\033[0m"
                UIManager.update_status_table()
            print(f"\033[1;31m[ Shouko.dev ] - {error_message}\033[0m")
            Utilities.log_error(error_message)

    @staticmethod
    @staticmethod
    @staticmethod
    def format_server_link(input_link):
        if 'roblox.com' in input_link:
            return input_link
        elif input_link.isdigit():
            return f'roblox://placeID={input_link}'
        else:
            print("\033[1;31m[ Shouko.dev ] - Invalid input! Please enter a valid game ID or private server link.\033[0m")
            return None

    
console = Console()
# --- COLOQUE AS SUAS 4 CHAVES AQUI ---
contas_roblox = {
    "saitama0000432": "WDVIZJ7HSPZUVP7UWVESIB6YC4",
    "saitama0000436": "WFTXXSZIGPAUXGHQSREGYHLB6Y",
    "saitama0000437": "MJ5LFHYBDGIUZJKUA3UUGZJSOQ",
    "saitama0000447": "5DS46QIDSXOUPKV4PUCQBRGURQ"
}

# Variável para controlar quando parar a atualização
parar_atualizacao = False

def atualizar_tabela_viva():
    # Dicionário com as senhas para facilitar a visualização
    senhas_roblox = {
        "saitama0000432": "saitama32",
        "saitama0000436": "saitama36",
        "saitama0000437": "saitama37",
        "saitama0000447": "saitama47"
    }

    with Live(refresh_per_second=1, screen=False) as live:
        while not parar_atualizacao:
            table = Table(title="🔐 GERADOR DE ACESSO RÁPIDO (ROBLOX)")
            table.add_column("Conta/User", style="cyan", no_wrap=True)
            table.add_column("Senha", style="magenta")
            table.add_column("Código 2FA", style="bold yellow", justify="center")
            table.add_column("Expira em", style="red")

            for nome, secret in contas_roblox.items():
                try:
                    # Gera o código 2FA
                    totp = pyotp.TOTP(secret.replace(" ", ""))
                    codigo = totp.now()
                    tempo_restante = 30 - (int(time.time()) % 30)
                    codigo_formatado = f"{codigo[0:3]} {codigo[3:6]}"
                    
                    # Pega a senha do dicionário acima
                    senha = senhas_roblox.get(nome, "N/A")
                    
                    table.add_row(nome, senha, codigo_formatado, f"{tempo_restante}s")
                except:
                    table.add_row(nome, "???", "ERRO NA CHAVE", "--")

            live.update(table)
            time.sleep(1)

# --- EXECUÇÃO DO 2FA E ABERTURA DOS CLONES ---

# 1. Pergunta ANTES de iniciar a tabela infinita
console.print("\n[bold yellow]🚀 MENU DE INICIALIZAÇÃO[/bold yellow]")
acao = input("[ Shouko.dev ] -> Digite [ 1 ] para abrir os 4 Clones ou [ ENTER ] para ver apenas os códigos: ").strip()

if acao == "1":
    
    # --- ABERTURA DOS CLONES ---
    clones_lista = ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv"]
    for p_clone in clones_lista:
        console.print(f"[cyan]>> Abrindo: {p_clone}[/cyan]")
        # Dá um 'force-stop' antes para garantir que ele abra do zero e limpo
        os.system(f"su -c 'am force-stop {p_clone}'")
        time.sleep(0.5)
        os.system(f"su -c 'monkey -p {p_clone} -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1'")
        time.sleep(5)
    
# 2. Inicia o "fio" (Thread) que atualiza a tabela no fundo
t = threading.Thread(target=atualizar_tabela_viva)
t.daemon = True
t.start()

# 3. Trava aqui para você ver os códigos enquanto faz o login
console.print("\n[bold green]✅ CÓDIGOS ATIVOS![/bold green] (Tabela acima)")
input("\n>>> APÓS LOGAR EM TUDO, APERTE [ ENTER ] PARA IR AO MENU PRINCIPAL...")

# 4. Finaliza a atualização e segue para o resto do bot
parar_atualizacao = True
time.sleep(0.5)

# --- O RESTO DO SEU CÓDIGO DO BOT COMEÇA AQUI ---
print("\nIniciando o bot...")
# Exemplo: import seu_modulo_do_bot

class UIManager:
    last_update_time = 0
    update_interval = 5
    @staticmethod
    def print_header(version):
        console = Console()
        header = Text(r"""
      _                 _             _            
     | |               | |           | |           
  ___| |__   ___  _   _| | _____   __| | _____   __
 / __| '_ \ / _ \| | | | |/ / _ \ / _` |/ _ \ \ / /
 \__ \ | | | (_) | |_| |   < (_) | (_| |  __/\ V / 
 |___/_| |_|\___/ \__,_|_|\_\___(_)__,_|\___| \_/  
        """, style="bold yellow")

        config_file = os.path.join("Shouko.dev", "config.json")
        check_executor = "1"
        global codex_bypass_enabled

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    check_executor = config.get("check_executor", "0")
            except Exception as e:
                console.print(f"[bold red][ Shouko.dev ] - Error reading {config_file}: {e}[/bold red]")

        console.print(header)
        console.print(f"[bold yellow]- Version: [/bold yellow][bold white]{version}[/bold white]")
        console.print(f"[bold yellow]- Credit: [/bold yellow][bold white]Shouko.dev[/bold white]")

        if check_executor == "1":
            console.print("[bold yellow]- Method: [/bold yellow][bold white]Check Executor[/bold white]")
        else:
            console.print("[bold yellow]- Method: [/bold yellow][bold white]Check Online[/bold white]")

        codex_status = "Enabled" if codex_bypass_enabled else "Disabled"
        console.print(f"[bold yellow]- Codex Bypass: [/bold yellow][bold white]{codex_status}[/bold white]\n")

    @staticmethod
    def create_dynamic_menu(options):
        console = Console()

        table = Table(
            header_style="bold white",
            border_style="bright_white",
            box=ROUNDED
        )
        table.add_column("No", justify="center", style="bold cyan", width=6)
        table.add_column("Service Name", style="bold magenta", justify="left")

        for i, service in enumerate(options, start=1):
            table.add_row(f"[bold yellow][ {i} ][/bold yellow]", f"[bold blue]{service}[/bold blue]")

        panel = Panel(
            table,
            title="[bold yellow]discord.gg/ghmaDgNzDa - Beta Edition[/bold yellow]",
            border_style="yellow",
            box=ROUNDED
        )

        console.print(Align.left(panel))

    @staticmethod
    def create_dynamic_table(headers, rows):
        table = PrettyTable(field_names=headers, border=True, align="l")
        for huy in rows:
            table.add_row(list(huy))
        print(table)

    last_update_time = 0
    update_interval = 5

    @staticmethod
    def update_status_table():
        current_time = time.time()
        
        # Agora acessamos usando UIManager.
        if current_time - UIManager.last_update_time < UIManager.update_interval:
            return

        UIManager.last_update_time = current_time
        
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_info = psutil.virtual_memory()
            ram = round(memory_info.used / memory_info.total * 100, 2)
            title = f"CPU: {cpu_usage}% | RAM: {ram}%"
        except Exception:
            title = "CPU: N/A | RAM: N/A (Cloud Mode)"

        table_packages = PrettyTable(
            field_names=["Package", "Username", "Package Status"],
            title=title,
            border=True,
            align="l"
        )

        for package, info in globals().get("package_statuses", {}).items():
            username = str(info.get("Username", "Unknown"))

            if username != "Unknown":
                obfuscated_username = "******" + username[6:] if len(username) > 6 else "******"
                username = obfuscated_username

            table_packages.add_row([
                str(package),
                username,
                str(info.get("Status", "Unknown"))
            ])

        Utilities.clear_screen()
        UIManager.print_header(version)
        print(table_packages)

class ExecutorManager:
    @staticmethod
    def detect_executors():
        """
        Detecta a pasta global do Delta (/sdcard/Delta/Autoexecute) 
        e vincula a todos os clones instalados.
        """
        console = Console()
        detected_packages = []
    
        # Lista de pacotes dos seus 4 clones (ywcw.lnu.exhl, etc)
        packages = RobloxManager.get_roblox_packages()
    
        # Caminho EXATO da sua Screenshot
        GLOBAL_DELTA_PATH = "/sdcard/Delta"
        AUTOEXEC_PATH = f"{GLOBAL_DELTA_PATH}/Autoexecute"
        WORKSPACE_PATH = f"{GLOBAL_DELTA_PATH}/workspace"

        # Verifica se a pasta existe (usamos su -c mkdir como garantia se nao existir)
        if not os.path.exists(AUTOEXEC_PATH):
            os.system(f"su -c 'mkdir -p {AUTOEXEC_PATH}'")
            os.system(f"su -c 'mkdir -p {WORKSPACE_PATH}'")

        if os.path.exists(AUTOEXEC_PATH):
            for package in packages:
                # Vincula cada clone a pasta central do Delta
                detected_packages.append({
                    "package": package,
                    "autoexec_path": AUTOEXEC_PATH,
                    "workspace_path": WORKSPACE_PATH
                })
                console.print(f"[bold green][ Shouko.dev ] - Vinculando Delta Central ao Clone: {package}[/bold green]")
        else:
            console.print(f"[bold red][ Shouko.dev ] - ERRO: Nao foi possivel acessar {AUTOEXEC_PATH}[/bold red]")

        return detected_packages
    
    @staticmethod
    def write_lua_script(detected_executors):
        console = Console()
    
        # Este script apenas avisa o Python que o executor ligou.
        # O seu farm ja esta na pasta e vai rodar junto com este.
        lua_content = """
repeat task.wait() until game:IsLoaded()
local lp = game:GetService("Players").LocalPlayer
repeat task.wait() until lp and lp.UserId ~= 0
local myId = tostring(lp.UserId)

-- Grava o sinal em TODOS os lugares possiveis para o Python achar
pcall(function() writefile(myId .. ".main", "online") end)
pcall(function() writefile("workspace/" .. myId .. ".main", "online") end)

print("[Shouko.dev] SINAL DE VIDA ENVIADO: " .. myId)
    """

        # Pasta base do seu Delta conforme a Screenshot
        target_path = "/sdcard/Delta/Autoexecute"

        try:
            os.makedirs(target_path, exist_ok=True)
            # Nomeamos com 00_ para o Delta carregar este PRIMEIRO
            lua_script_path = os.path.join(target_path, "00_shouko_check.lua")

            # Tenta escrita normal
            with open(lua_script_path, "w") as f:
                f.write(lua_content)
        
            console.print(f"[bold green][✓] Script de sinal criado em: {lua_script_path}[/bold green]")

        except Exception:
            # Se falhar (comum em Cloud Phone), força via Root
            try:
                os.system(f"su -c 'echo \"{lua_content}\" > {lua_script_path}'")
                console.print(f"[bold yellow][!] Script de sinal gravado via Root![/bold yellow]")
            except Exception as e:
                console.print(f"[bold red][X] Erro ao gravar script: {e}[/bold red]")
    @staticmethod
    
    def check_executor_status(package_name, max_wait_time=180):
        user_id = globals().get("_user_", {}).get(package_name)
        if not user_id: return False

        # Lista de caminhos possíveis que o Delta usa no VMOS/UGPhone
        possible_files = [
            f"/sdcard/Delta/workspace/{user_id}.main",      # Caminho mais provável
            f"/sdcard/Delta/{user_id}.main",                # Raiz da pasta Delta
            f"/storage/emulated/0/Delta/workspace/{user_id}.main",
            f"/storage/emulated/0/Delta/{user_id}.main"
        ]

        timeout = time.time() + max_wait_time
        while time.time() < timeout:
            for signal_file in possible_files:
                if os.path.exists(signal_file):
                    # Se achou, printa no console do Termux para você ver
                    print(f"\033[1;32m[✓] Sinal detectado em: {signal_file}\033[0m")
                    return True
        
            time.sleep(10) 
        return False
            
    @staticmethod
    def check_executor_and_rejoin(package_name, server_link, next_package_event):
        while True:  # <--- O Loop Infinito começa AQUI
            time.sleep(5) 
            user_id = globals().get("_user_", {}).get(package_name)
        
            # Inicia a checagem visual na tabela
            globals()["package_statuses"][package_name]["Status"] = "\033[1;33mChecking executor...\033[0m"
            UIManager.update_status_table()
        
            start_time = time.time()
            executor_loaded = False

            # FASE 1: Espera o Executor injetar (Limite de 3 min)
            while time.time() - start_time < 180:
                if ExecutorManager.check_executor_status(package_name):
                    globals()["package_statuses"][package_name]["Status"] = "\033[1;32mFarming (30m)...\033[0m"
                    UIManager.update_status_table()
                    executor_loaded = True
                
                    # SUCESSO: Libera a fila para a PRÓXIMA conta abrir enquanto esta farma
                    next_package_event.set() 
                    break 

                time.sleep(10)

            if executor_loaded:
                # FASE 2: O Tempo de Farm (30 minutos colhendo frutos)
                time.sleep(1800) 
                print(f"\033[1;36m[ Shouko.dev ] - Tempo de 30min esgotado para {package_name}. Resetando...\033[0m")
            else:
                # FASE 3: Se der Timeout (3 min sem sinal), pula para o reset para tentar de novo
                print(f"\033[1;31m[ Shouko.dev ] - Timeout no executor de {package_name}!\033[0m")
                next_package_event.set() # Libera a fila para não travar o bot inteiro

            # FASE 4: O Reset e Reinicialização
            globals()["package_statuses"][package_name]["Status"] = "\033[1;31mResetting...\033[0m"
            UIManager.update_status_table()
        
            # Limpa o arquivo .main para o proximo check ser real
            ExecutorManager.reset_executor_file(package_name)
        
            # Fecha o Roblox
            RobloxManager.kill_roblox_process(package_name)
        
            time.sleep(5) # Pausa para o Android processar o fechamento
        
            # !!! O QUE FALTAVA: MANDAR ABRIR O ROBLOX DE NOVO !!!
            # Isso faz o "while True" recomeçar com o jogo abrindo do zero
            print(f"\033[1;34m[ Shouko.dev ] - Reiniciando {package_name} para novo ciclo.\033[0m")
            RobloxManager.launch_roblox(package_name, server_link)
            def reset_executor_file(package_name):
                """
                Remove o arquivo de sinal do ID específico na pasta central do Delta 
                antes de iniciar uma nova rodada no farm.
                """
                try:
                    # Pega o ID da conta vinculada a esse clone (ywcw.lnu.exhl, etc)
                    user_id = globals().get("_user_", {}).get(package_name)
                    if not user_id: 
                        return

                    # Caminhos centralizados (Workspace e Raiz do Delta)
                    possible_paths = [
                        f"/sdcard/Delta/workspace/{user_id}.main",
                        f"/sdcard/Delta/{user_id}.main"
                    ]

                    for path in possible_paths:
                        if os.path.exists(path):
                            try:
                                # Tenta remover direto pelo Python
                                os.remove(path)
                            except:
                                # Se der erro de permissao, usa o Root do Cloud Phone
                                os.system(f"su -c 'rm {path}'")
                
                            print(f"\033[1;32m[ Shouko.dev ] - Sinal do ID {user_id} limpo com sucesso!\033[0m")
                            # Nao damos 'return' aqui para garantir que ele tente limpar 
                            # ambos os caminhos se existirem duplicatas.

                except Exception as e:
                    print(f"Erro ao resetar sinal do executor: {e}")

class Runner:

    def launch_package_sequentially(server_links):
        next_package_event = Event()
        next_package_event.set()
        packages_to_launch = []
        for package_name, server_link in server_links:
            user_id = globals()["_user_"].get(package_name, "Unknown")
            if user_id == "Unknown":
                print(f"\033[1;31m[ Shouko.dev ] - No UserID found for {package_name}, skipping...\033[0m")
                continue
            username = FileManager.get_username(user_id)
            with status_lock:
                globals()["package_statuses"][package_name] = {
                    "Username": username,
                    "Status": "\033[1;33mWaiting to Join\033[0m"
                }
            packages_to_launch.append((package_name, server_link))
        total_packages = len(packages_to_launch)
        for index, (package_name, server_link) in enumerate(packages_to_launch):
            next_package_event.clear()
            print(f"\033[1;32m[ Shouko.dev ] - Launching package {index + 1}/{total_packages}: {package_name}\033[0m")
            try:
                RobloxManager.launch_roblox(package_name, server_link)
                if globals()["check_exec_enable"] == "1":
                    detected_executors = ExecutorManager.detect_executors()
                    if len(detected_executors) > 0:
                        ExecutorManager.write_lua_script(detected_executors)
                    else:
                        print(f"\033[1;33m[ Shouko.dev ] - No executors detected for {package_name}\033[0m")
            except Exception as e:
                Utilities.log_error(f"Error launching Roblox for {package_name}: {e}\n{traceback.format_exc()}")
                print(f"\033[1;31mError launching Roblox for {package_name}: {e}\033[0m")
                globals()["package_statuses"][package_name]["Status"] = "\033[1;31mLaunch failed\033[0m"
                UIManager.update_status_table()
            if globals()["check_exec_enable"] == "1":
                threading.Thread(
                    target=ExecutorManager.check_executor_and_rejoin,
                    args=(package_name, server_link, next_package_event),
                    daemon=True
                ).start()
            else:
                next_package_event.set()
            next_package_event.wait()

    @staticmethod
    def monitor_presence(server_links, stop_event):
        in_game_status = {package_name: False for package_name, _ in server_links}
            
        while not stop_event.is_set():
            try:
                if globals()["check_exec_enable"] == "0":
                    for package_name, server_link in server_links:
                        ckhuy = FileManager.xuat(f"/data/data/{package_name}/app_webview/Default/Cookies")
                        user_id = globals()["_user_"][package_name]
                            
                        presence_type = RobloxManager.check_user_online(user_id, ckhuy)
                        
                        if not in_game_status[package_name]:
                            if presence_type == 2:
                                with status_lock:
                                    globals()["package_statuses"][package_name]["Status"] = "\033[1;32mIn-Game\033[0m"
                                    UIManager.update_status_table()
                                in_game_status[package_name] = True
                                print(f"\033[1;32m[ Shouko.dev ] - {user_id} is now In-Game, monitoring started.\033[0m")
                            continue 
                            
                        if presence_type != 2:
                            with status_lock:
                                globals()["package_statuses"][package_name]["Status"] = "\033[1;31mNot In-Game, Rejoining!\033[0m"
                                UIManager.update_status_table()
                            print(f"\033[1;31m[ Shouko.dev ] - {user_id} confirmed offline, rejoining...\033[0m")
                            RobloxManager.kill_roblox_process(package_name)
                            RobloxManager.delete_cache_for_package(package_name)
                            time.sleep(2)
                            threading.Thread(target=RobloxManager.launch_roblox, args=[package_name, server_link], daemon=True).start()
                        else:
                            with status_lock:
                                globals()["package_statuses"][package_name]["Status"] = "\033[1;32mIn-Game\033[0m"
                                UIManager.update_status_table()
                time.sleep(60)
            except Exception as e:
                Utilities.log_error(f"Error in presence monitor: {e}")
                time.sleep(60)

    @staticmethod
    def force_rejoin(server_links, interval_minutes, stop_event):
        """
        Gerencia o reset individual de cada clone para evitar sobrecarga na Cloud.
        """
        console = Console()
        
        # Converte minutos para segundos (Padrão 30 min = 1800s)
        try:
            rejoin_interval = float(interval_minutes) * 60
        except:
            rejoin_interval = 1800.0

        # Dicionário para controlar o tempo de cada conta separadamente
        last_rejoin_times = {package: time.time() for package, _ in server_links}

        console.print(f"[bold cyan][ Shouko.dev ] - Cronômetro de {interval_minutes} min iniciado para {len(server_links)} contas.[/bold cyan]")

        while not stop_event.is_set():
            current_time = time.time()

            for package_name, server_link in server_links:
                elapsed = current_time - last_rejoin_times[package_name]

                if elapsed >= rejoin_interval:
                    console.print(f"[bold red][ ! ] Limite atingido para {package_name}. Resetando individualmente...[/bold red]")
                    
                    try:
                        # 1. Atualiza o status na tabela do UIManager
                        with status_lock:
                            globals()["package_statuses"][package_name]["Status"] = "\033[1;31mForcing Rejoin\033[0m"
                        UIManager.update_status_table()

                        # 2. Fecha apenas este clone específico via ROOT (su -c)
                        # O comando 'am force-stop' é o mais limpo para Cloud Phones
                        os.system(f"su -c 'am force-stop {package_name}'")
                        
                        # 3. Pequena pausa para o Android respirar
                        time.sleep(3)

                        # 4. Limpa o sinal antigo para o executor não se confundir
                        ExecutorManager.reset_executor_file(package_name)

                        # 5. Reabre apenas este clone com o link do mapa (Fisch/Adopt Me)
                        RobloxManager.launch_roblox(package_name, server_link)

                        # 6. Verifica se o executor carregou antes de seguir para a próxima conta
                        # Isso evita que o script tente resetar a Conta 2 enquanto a 1 ainda está abrindo
                        next_event = threading.Event()
                        threading.Thread(
                            target=ExecutorManager.check_executor_and_rejoin,
                            args=(package_name, server_link, next_event),
                            daemon=True
                        ).start()
                        
                        # Espera um sinal de que a abertura iniciou com sucesso ou timeout
                        next_event.wait(timeout=60) 

                        # 7. Reseta o cronômetro apenas desta conta
                        last_rejoin_times[package_name] = time.time()
                        
                        console.print(f"[bold green][✓] {package_name} resetado e monitorando![/bold green]")

                    except Exception as e:
                        console.print(f"[bold red]Erro no reset de {package_name}: {e}[/bold red]")
                        Utilities.log_error(f"Force Rejoin Error ({package_name}): {e}")

            # Verifica a cada 15 segundos se alguma conta precisa de reset
            time.sleep(15)

def check_activation_status():
    try:
        response = requests.get("https://raw.githubusercontent.com/nghvit/module/refs/heads/main/status/customize", timeout=5)
        response.raise_for_status()
        content = response.text.strip()
        if content == "true":
            print("\033[1;32m[ Shouko.dev ] - Activation status: Enabled. Proceeding with tool execution.\033[0m")
            return True
        elif content == "false":
            print("\033[1;31m[ Shouko.dev ] - Activation status: Disabled. Tool execution halted.\033[0m")
            return False
        else:
            print(f"\033[1;31m[ Shouko.dev ] - Invalid activation status received: {content}. Halting execution.\033[0m")
            Utilities.log_error(f"Invalid activation status: {content}")
            return False
    except requests.RequestException as e:
        print(f"\033[1;31m[ Shouko.dev ] - Error checking activation status: {e}\033[0m")
        Utilities.log_error(f"Error checking activation status: {e}")
        return False

def set_android_id(android_id):
    try:
        subprocess.run(["settings", "put", "secure", "android_id", android_id], check=True)
    except Exception as e:
        Utilities.log_error(f"Failed to set Android ID: {e}")

def auto_change_android_id():
    global auto_android_id_enabled, auto_android_id_value
    while auto_android_id_enabled:
        if auto_android_id_value:
            set_android_id(auto_android_id_value)
        time.sleep(2)  

def main():
    global stop_webhook_thread, webhook_interval, codex_bypass_enabled, codex_bypass_thread, codex_bypass_active
    global auto_android_id_enabled, auto_android_id_thread, auto_android_id_value

    if not check_activation_status():
        print("\033[1;31m[ Shouko.dev ] - Exiting due to activation status check failure.\033[0m")
        return
    
    FileManager._load_config()
    
    if not globals().get("command_8_configured", False):
        globals()["check_exec_enable"] = "1"
        globals()["lua_script_template"] = 'loadstring(game:HttpGet("https://repo.rokidmanager.com/RokidManager/neyoshiiuem/main/checkonline.lua"))()'
        config_file = os.path.join("Shouko.dev", "checkui.lua")
        try:
            os.makedirs("Shouko.dev", exist_ok=True)
            with open(config_file, "w") as f:
                f.write(globals()["lua_script_template"])
            print("\033[1;32m[ Shouko.dev ] - Default script saved to checkui.lua\033[0m")
        except Exception as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error saving default script to {config_file}: {e}\033[0m")
            Utilities.log_error(f"Error saving default script to {config_file}: {e}")
        FileManager.save_config()

    if webhook_interval is None:
        print("\033[1;31m[ Shouko.dev ] - Webhook interval not set, disabled.\033[0m")
        webhook_interval = float('inf')
    if webhook_url and device_name and webhook_interval != float('inf'):
        WebhookManager.start_webhook_thread()
    else:
        print("\033[1;33m[ Shouko.dev ] - Webhook not configured or disabled.\033[0m")

    stop_main_event = threading.Event()

    while True:
        Utilities.clear_screen()
        UIManager.print_header(version)
        

        menu_options = [
            "Start Auto Rejoin",
            "Auto Setup User IDs",
            "Auto Check User Setup",
            "Configure AutoExecute",
            "Start All Clones"
        ]

        UIManager.create_dynamic_menu(menu_options)
        setup_type = input("\033[1;93m[ Shouko.dev ] - Enter command: \033[0m")
        codex_bypass_active = False

        if setup_type == "1":
            try:
                server_links = FileManager.load_server_links()
                globals()["accounts"] = FileManager.load_accounts()
                globals()["_uid_"] = {}

                if not globals()["accounts"]:
                    print("\033[1;31m[ Shouko.dev ] - No user IDs set up.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue
                if not server_links:
                    print("\033[1;31m[ Shouko.dev ] - No game ID or server link set up.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue

                force_rejoin_input = input(...)

                if not force_rejoin_input:
                    force_rejoin_input = ""

                if force_rejoin_input.lower() == 'q':
                    force_rejoin_interval = float('inf')
                else:
                    force_rejoin_interval = int(force_rejoin_input) * 60
                if force_rejoin_interval <= 0:
                    print("\033[1;31m[ Shouko.dev ] - Interval must be positive.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue

                codex_bypass_active = True

                if codex_bypass_active and codex_bypass_enabled:
                    print("\033[1;32m[ Shouko.dev ] - Codex bypass enabled.\033[0m")

                RobloxManager.kill_roblox_processes()
                time.sleep(5)
                Runner.launch_package_sequentially(server_links)
                globals()["is_runner_ez"] = True

                for task in [
                    (Runner.monitor_presence, (server_links, stop_main_event)),
                    (Runner.force_rejoin, (server_links, force_rejoin_interval, stop_main_event)),
                    (Runner.update_status_table_periodically, ())
                ]:
                    threading.Thread(target=task[0], args=task[1], daemon=True).start()

                while not stop_main_event.is_set():
                    time.sleep(500)
                    with status_lock:
                        UIManager.update_status_table()
                    Utilities.collect_garbage()

            except Exception as e:
                print(f"\033[1;31m[ Shouko.dev ] - Error: {e}\033[0m")
                Utilities.log_error(f"Setup error: {e}")
                input("\033[1;32mPress Enter to return...\033[0m")
                continue

        elif setup_type == "2":
            try:
                login_gboard_estavel()
                time.sleep(9.0)
            # --------------------------------------------------------------
                print("\033[1;32m[ Shouko.dev ] - Auto Setup User IDs from appStorage.json...\033[0m")
                packages = ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv", "kxm.ak.qyfi"]
                accounts = []

                for package_name in packages:
                    file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'
                    try:
                        user_id = FileManager.find_userid_from_file(file_path)
                        if user_id and user_id != "-1":
                            accounts.append((package_name, user_id))
                            print(f"\033[96m[ Shouko.dev ] - Found UserId for {package_name}: {user_id}\033[0m")
                        else:
                            print(f"\033[1;31m[ Shouko.dev ] - UserId not found for {package_name}.\033[0m")
                    except Exception as e:
                        print(f"\033[1;31m[ Shouko.dev ] - Error reading file for {package_name}: {e}\033[0m")
                        Utilities.log_error(f"Error reading appStorage.json for {package_name}: {e}")

                if accounts:
                    FileManager.save_accounts(accounts)
                    print("\033[1;32m[ Shouko.dev ] - User IDs saved!\033[0m")
                else:
                    print("\033[1;31m[ Shouko.dev ] - No User IDs found.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue

                print("\033[93m[ Shouko.dev ] - Select game:\033[0m")
                games = [
                    "1. Blox Fruits", "2. Anime Defenders", "3. King Legacy", "4. Fisch",
                    "5. Bee Swarm Simulator", "6. Anime Vanguards", "7. Pet GO",
                    "8. Pet Simulator 99", "9. Meme Sea", "10. Anime Adventures",
                    "11. Anime Last Stand", "12. Da Hood", "13. Da Hood VC", "14. Arise Crossover",
                    "15. Bubble Gum Simulator", "16. Anime Ranger X", "17. Other game or Private Server Link"
                ]
                for game in games:
                    print(f"\033[96m{game}\033[0m")

                choice = input("\033[93m[ Shouko.dev ] - Enter choice: \033[0m").strip()
                game_ids = {
                    "1": "2753915549", "2": "17017769292", "3": "4520749081", "4": "16732694052",
                    "5": "1537690962", "6": "16146832113", "7": "18901165922", "8": "8737899170",
                    "9": "10260193230", "10": "8304191830", "11": "12886143095", "12": "2788229376",
                    "13": "7213786345", "14": "87039211657390", "15": "85896571713843", "16": "72829404259339"
                }

                if choice in game_ids:
                    server_link = game_ids[choice]
                elif choice == "17":
                    server_link = input("\033[93m[ Shouko.dev ] - Enter game ID or private server link: \033[0m")
                else:
                    print("\033[1;31m[ Shouko.dev ] - Invalid choice.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue

                formatted_link = RobloxManager.format_server_link(server_link)
                if formatted_link:
                    server_links = [(package_name, formatted_link) for package_name, _ in accounts]
                    FileManager.save_server_links(server_links)
                    print("\033[1;32m[ Shouko.dev ] - Game ID or server link saved!\033[0m")
                else:
                    print("\033[1;31m[ Shouko.dev ] - Invalid server link.\033[0m")
            except Exception as e:
                print(f"\033[1;31m[ Shouko.dev ] - Error: {e}\033[0m")
                Utilities.log_error(f"Setup error: {e}")
                input("\033[1;32mPress Enter to return...\033[0m")
                continue
            input("\033[1;32mPress Enter to return...\033[0m")
            continue

        elif setup_type == "3":
            try:
                print("\033[1;35m[1]\033[1;32m Executor Check\033[0m \033[1;35m[2]\033[1;36m Online Check\033[0m")
                config_choice = input("\033[1;93m[ Shouko.dev ] - Select check method (1-2, 'q' to keep default): \033[0m").strip()

                if config_choice.lower() == "q":
                    globals()["check_exec_enable"] = "1"
                    globals()["lua_script_template"] = 'loadstring(game:HttpGet("https://repo.rokidmanager.com/RokidManager/neyoshiiuem/main/checkonline.lua"))()'
                    print("\033[1;32m[ Shouko.dev ] - Default set: Executor + Shouko Check\033[0m")
                elif config_choice == "1":
                    globals()["check_exec_enable"] = "1"
                    globals()["lua_script_template"] = 'loadstring(game:HttpGet("https://repo.rokidmanager.com/RokidManager/neyoshiiuem/main/checkonline.lua"))()'
                    print("\033[1;32m[ Shouko.dev ] - Set to Executor + Shouko Check\033[0m")
                elif config_choice == "2":
                    globals()["check_exec_enable"] = "0"
                    globals()["lua_script_template"] = None
                    print("\033[1;36m[ Shouko.dev ] - Set to Online Check.\033[0m")
                else:
                    print("\033[1;31m[ Shouko.dev ] - Invalid choice. Keeping default.\033[0m")
                    globals()["check_exec_enable"] = "1"
                    globals()["lua_script_template"] = 'loadstring(game:HttpGet("https://repo.rokidmanager.com/RokidManager/neyoshiiuem/main/checkonline.lua"))()'

                config_file = os.path.join("Shouko.dev", "checkui.lua")
                if globals()["lua_script_template"]:
                    try:
                        os.makedirs("Shouko.dev", exist_ok=True)
                        with open(config_file, "w") as f:
                            f.write(globals()["lua_script_template"])
                        print(f"\033[1;36m[ Shouko.dev ] - Script saved to {config_file}\033[0m")
                    except Exception as e:
                        print(f"\033[1;31m[ Shouko.dev ] - Error saving script: {e}\033[0m")
                        Utilities.log_error(f"Error saving script to {config_file}: {e}")
                else:
                    if os.path.exists(config_file):
                        try:
                            os.remove(config_file)
                            print(f"\033[1;36m[ Shouko.dev ] - Removed {config_file} for Online Check.\033[0m")
                        except Exception as e:
                            print(f"\033[1;31m[ Shouko.dev ] - Error removing {config_file}: {e}\033[0m")
                            Utilities.log_error(f"Error removing {config_file}: {e}")

                globals()["command_8_configured"] = True

                FileManager.save_config()
                print("\033[1;32m[ Shouko.dev ] - Check method configuration saved.\033[0m")
            except Exception as e:
                print(f"\033[1;31m[ Shouko.dev ] - Error setting up check method: {e}\033[0m")
                Utilities.log_error(f"Check method setup error: {e}")
                input("\033[1;32mPress Enter to return...\033[0m")
                continue
            input("\033[1;32mPress Enter to return...\033[0m")
            continue

        elif setup_type == "4":
            console = Console()
            console.print("\n[bold yellow]📝 CONFIGURADOR DE AUTO-EXECUTE (DELTA)[/bold yellow]")
        
            # Pergunta a Key específica
            key_usuario = input("[ Shouko.dev ] - Cole a KEY do seu script: ").strip()
        
            # Monta o conteúdo do arquivo com quebra de linha real
            conteudo = f'script_key = "{key_usuario}"\nloadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/875033288c5e99d576622aced60a0c44.lua"))()'
        
            caminho_pasta = "/storage/emulated/0/Delta/Autoexecute"
            arquivo_final = f"{caminho_pasta}/script.txt"
        
            try:
                # 1. Cria a pasta e dá permissão total via sistema
                os.system(f"mkdir -p {caminho_pasta} && chmod 777 {caminho_pasta}")
            
                # 2. Escreve o arquivo txt
                with open(arquivo_final, "w") as f:
                    f.write(conteudo)
            
                # 3. Garante que o arquivo também tenha permissão para o Delta ler
                os.system(f"chmod 777 {arquivo_final}")
                
                console.print(f"\n[bold green][✓][/bold green] Arquivo [white]script.txt[/white] configurado!")
                console.print(f"[bold green][✓][/bold green] Local: [cyan]{arquivo_final}[/cyan]")
                console.print("[yellow]DICA: Agora é só abrir os Clones e o farm iniciará sozinho.[/yellow]")
            except Exception as e:
                console.print(f"\n[bold red][!] Erro ao criar arquivo: {e}[/bold red]")
            
            input("\n[bold cyan]Pressione ENTER para voltar ao menu...[/bold cyan]")
            continue
        
        elif setup_type == "5":
            global auto_android_id_enabled, auto_android_id_thread, auto_android_id_value
            if not auto_android_id_enabled:
                android_id = input("\033[1;93m[ Shouko.dev ] - Enter Android ID to spam set: \033[0m").strip()
                if not android_id:
                    print("\033[1;31m[ Shouko.dev ] - Android ID cannot be empty.\033[0m")
                    input("\033[1;32mPress Enter to return...\033[0m")
                    continue
                auto_android_id_value = android_id
                auto_android_id_enabled = True
                if auto_android_id_thread is None or not auto_android_id_thread.is_alive():
                    auto_android_id_thread = threading.Thread(target=auto_change_android_id, daemon=True)
                    auto_android_id_thread.start()
                print("\033[1;32m[ Shouko.dev ] - Auto change Android ID enabled.\033[0m")
            else:
                auto_android_id_enabled = False
                print("\033[1;31m[ Shouko.dev ] - Auto change Android ID disabled.\033[0m")
            input("\033[1;32mPress Enter to return...\033[0m")
            continue
            
            
        elif setup_type == "6":
            console = Console()
            console.print("\n[bold yellow]🚀 INICIANDO TODOS OS CLONES (MODO FORÇADO)...[/bold yellow]")
        
            clones = [
                "ywcw.lnu.exhl",
                "ub.wnjb.bzz",
                "ixq.vf.jlr",
                "srl.mvn.gv"
            ]
        
            for pacote in clones:
                console.print(f"[cyan]>> Acordando clone: {pacote}...[/cyan]")
            
            # Primeiro, limpamos qualquer processo travado
                os.system(f"su -c 'am force-stop {pacote}'")
                time.sleep(1)
            
            # Agora tentamos abrir usando o monkey (método mais estável)
                comando = f"su -c 'monkey -p {pacote} -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1'"
                os.system(comando)
            
            # Espera 10 segundos para o Cloud Phone não travar
                time.sleep(10)
            
                console.print("\n[bold green][✓] Tentativa de abertura concluída![/bold green]")
                console.print("[yellow]DICA: Se algum não abriu, clique nele manualmente uma vez para 'ativar'.[/yellow]")
            input("\n[bold cyan]Pressione ENTER para voltar...[/bold cyan]")
            continue

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[1;31m[ Shouko.dev ] - Error during initialization: {e}\033[0m")
        Utilities.log_error(f"Initialization error: {e}")
        raise
