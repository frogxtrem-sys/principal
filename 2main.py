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
import platform
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
clones_internos = ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv", "kxm.ak.qyfi", "tk.lisa.cqt", 
                   "jpaclone.anya.lh", "jpaclone.anya.li", "jpaclone.anya.lj"
]
for pkg in clones_internos:
    workspace_paths.append(f"/data/data/{pkg}/files/workspace")
    workspace_paths.append(f"/data/data/{pkg}/files/Workspace")

if not os.path.exists("Shouko.dev"):
    os.makedirs("Shouko.dev", exist_ok=True)
SERVER_LINKS_FILE = "Shouko.dev/server-links.txt"
ACCOUNTS_FILE = "Shouko.dev/accounts.txt"
CONFIG_FILE = "Shouko.dev/config.json"

version = "2.2.5 | Customized by Shouko.dev"


def blindar_termux():
    print("\033[1;33m[ 🛡️ ] Blindando Termux contra fechamento...\033[0m")
    # Tenta dar prioridade máxima (OOM Score)
    os.system("su -c 'echo -1000 > /proc/$(pgrep com.termux)/oom_score_adj'")
    
    # Tenta desativar limites de processos em segundo plano (específico para VMs)
    os.system("su -c 'settings put global max_phantom_processes 2147483647'")
    os.system("su -c 'setprop persist.sys.max_processes 100'")
    
    # Impede que o sistema hiberne o processo (se suportado)
    os.system("su -c 'cmd deviceidle whitelist +com.termux'")
    
    print("\033[1;32m[ ✓ ] Proteções aplicadas!\033[0m")

def su_cmd(comando):
    os.system(f"su -c '{comando}'")

def enviar_para_discord(link_delta):
    """Envia o link formatado para o seu bot do Discord via Webhook."""
    webhook_url = "https://discord.com/api/webhooks/1376758923431903414/_Ek7PIg2uXc59ds8pkp5EUsKNZYpniGJKl92J1iYTzmQcC-qqG5XHmvwQUqDCoKFrvcE"
    
    # Formata a mensagem exatamente como o seu bot precisa para o comando de slash
    # Nota: Se o seu bot for um bot de comandos reais, ele pode precisar que 
    # você escreva a mensagem comum, mas via Webhook ele apenas 'posta' o texto.
    conteudo = {
        "content": f"/bypass url:{link_delta}"
    }
    
    try:
        response = requests.post(webhook_url, json=conteudo)
        if response.status_code == 204 or response.status_code == 200:
            print("\n\033[1;32m[ 📡 ] Link enviado para o Discord com sucesso!\033[0m")
        else:
            print(f"\n\033[1;31m[ ! ] Erro ao enviar Webhook: {response.status_code}\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[ ! ] Falha na conexão com Discord: {e}\033[0m")

def pegar_link_delta():
    """Lê o clipboard para pegar o link que o Delta copiou."""
    cmd = "su -c 'service call clipboard 2 | cut -d\"'\" -f2 | sed \"s/ //g\"'"
    return os.popen(cmd).read().strip()

def login_gboard_estavel(lista_de_contas, nome_set):
    # --- COORDENADAS (Ajustadas conforme sua última mensagem) ---
    BTN_LOG_IN_INICIAL = "623 451" 
    CAMPO_USER = "612 381" 
    BTN_GET_KEY = "901 417" 

    LINK_FIXO = "https://www.roblox.com/share?code=90856ea1bf5ed54785ce8c39ee168245&type=Server"

    total = len(lista_de_contas)

    # --- PASSO 1: LOGINS ---
    print(f"\n\033[1;34m[ 1/3 ] Realizando Logins de {nome_set}...\033[0m")
    for i, conta in enumerate(lista_de_contas, 1):
        pkg = conta['pkg']
        user = conta['user']
        pw = conta['pass']

        print(f"   > [{i}/{total}] Logando: {user}")
        
        # Fecha antes de abrir para garantir que caia na tela de Login
        su_cmd(f"am force-stop {pkg}")
        time.sleep(1)
        su_cmd(f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1")
        
        time.sleep(20) 
        su_cmd(f"input tap {BTN_LOG_IN_INICIAL}")
        time.sleep(5)
        su_cmd(f"input tap {CAMPO_USER}")
        time.sleep(1)
        su_cmd(f"input text {user}")
        time.sleep(1)
        su_cmd(f"input keyevent 66") # Próximo campo (Senha)
        time.sleep(2.5) 
        su_cmd(f"input text {pw}")
        time.sleep(1)
        su_cmd(f"input keyevent 66") # Confirmar Login
        
        print(f"   \033[1;32m[ ✓ ] Login enviado. Mantendo {pkg} aberto...\033[0m")
        time.sleep(8) # Tempo para o login processar antes de ir pro próximo
        
        # REMOVIDO: su_cmd(f"am force-stop {pkg}") -> Agora a conta fica aberta!

    # --- PASSO 2: LINK FIXO ---
    print(f"\n\033[1;35m[ 2/3 ] Salvando Link de Farm...\033[0m")
    with open("game_link.txt", "w") as f:
        f.write(LINK_FIXO)

    # --- ETAPA 3: ABRIR O PRIMEIRO CLONE E PEGAR KEY ---
    print(f"\n\033[1;36m[ Passo 3 ] Indo para o primeiro clone pegar a Key...\033[0m")
    primeiro_pkg = lista_de_contas[0]['pkg']
    
    # Abre o jogo no primeiro clone (que já está aberto no lobby)
    su_cmd(f"am start -a android.intent.action.VIEW -d '{LINK_FIXO}' {primeiro_pkg}")
    
    print("   -> Aguardando o mapa carregar (40s)...")
    time.sleep(40) 

    # Sequência de 2 cliques no Get Key
    print("   -> 1º Clique no Get Key (Checkpoint)...")
    su_cmd(f"input tap {BTN_GET_KEY}")
    time.sleep(4) 

    print("   -> 2º Clique no Get Key (Copiando link)...")
    su_cmd(f"input tap {BTN_GET_KEY}")
    time.sleep(3) 

    link_delta = pegar_link_delta()
    
    if "plato" in link_delta or "gateway" in link_delta:
        print(f"\033[1;32m   [🔗] Sucesso! Enviando para o Discord...\033[0m")
        enviar_para_discord(link_delta)
    else:
        print("\033[1;31m   [ ! ] Clipboard vazio ou link inválido.\033[0m")

    print(f"\n\033[1;32m[ FINALIZADO ] Todos os clones estão logados e prontos!\033[0m")
    input("\033[1;33mPressione Enter para voltar...\033[0m")
def menu_login_opcoes():
    """
    Menu para escolher qual grupo de contas logar e retornar os pacotes para o setup.
    """
    # GRUPO 01 (Suas contas da Cloud principal)
    contas_set_1 = [
        {"user": "saitama0000432", "pass": "saitama32", "pkg": "ywcw.lnu.exhl"},
        {"user": "saitama0000436", "pass": "saitama36", "pkg": "ub.wnjb.bzz"},
        {"user": "saitama0000437", "pass": "saitama37", "pkg": "ixq.vf.jlr"},
        {"user": "saitama0000447", "pass": "saitama47", "pkg": "srl.mvn.gv"}
    ]

    # GRUPO 02 (Suas contas da segunda Cloud / Novos Clones)
    # SUBSTITUA PELOS SEUS DADOS REAIS ABAIXO:
    contas_set_2 = [
        {"user": "saitama0000428", "pass": "saitama028", "pkg": "ywcw.lnu.exhl"},
        {"user": "saitama0000443", "pass": "saitama43", "pkg": "ub.wnjb.bzz"},
        {"user": "saitama0000448", "pass": "saitama48", "pkg": "ixq.vf.jlr"},
        {"user": "saitama0000449", "pass": "saitama49", "pkg": "srl.mvn.gv"}
    ]

    while True:
        Utilities.clear_screen()
        print("\033[1;35m========================================\033[0m")
        print("\033[1;37m       GERENCIADOR DE LOGIN GBOARD      \033[0m")
        print("\033[1;35m========================================\033[0m")
        print("\n\033[1;34m[ 1 ]\033[0m Logar SET 01 (Contas 1-4)")
        print("\033[1;34m[ 2 ]\033[0m Logar SET 02 (Contas 5-8)")
        print("\033[1;31m[ B ]\033[0m Voltar ao Menu Principal")
        
        opcao = input("\n\033[1;32mEscolha o grupo de contas: \033[0m").lower()

        if opcao == '1':
            login_gboard_estavel(contas_set_1, "SET 01")
            # Retorna a lista de pacotes do SET 01 para o setup automático de IDs
            return ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv"], "SET 01"

        elif opcao == '2':
            login_gboard_estavel(contas_set_2, "SET 02")
            # Retorna a lista de pacotes do SET 02 (Troque pelos nomes reais dos pacotes)
            return ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv"], "SET 02"

        elif opcao == 'b':
            return None, None
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
        return ["ywcw.lnu.exhl", "ub.wnjb.bzz", "ixq.vf.jlr", "srl.mvn.gv", "kxm.ak.qyfi", "tk.lisa.cqt", 
                "jpaclone.anya.lh", "jpaclone.anya.li", "jpaclone.anya.lj"
        ]

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
    def format_server_link(input_link):
        """Garante que o link esteja no formato correto para o Android abrir o Roblox."""
        if 'roblox.com' in input_link:
            return input_link
        elif input_link.isdigit():
            return f'roblox://placeID={input_link}'
        else:
            print("\n\033[1;31m[ ! ] Link/ID inválido!\033[0m")
            return None

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
        
        if current_time - UIManager.last_update_time < UIManager.update_interval:
            return

        UIManager.last_update_time = current_time
        
        try:
            # Tenta o psutil primeiro (Método padrão)
            cpu_val = psutil.cpu_percent(interval=0.1)
            mem_val = psutil.virtual_memory().percent
            
            # Se o psutil retornar 0.0 (indicando bloqueio ou erro de leitura)
            if cpu_val == 0.0:
                # Tenta ler via comando shell direto (mais difícil de bloquear)
                cpu_shell = os.popen("top -n 1 | grep 'User' | awk '{print $2}'").read().strip().replace('%', '')
                cpu_val = cpu_shell if cpu_shell else "0.0"

            # Se a RAM estiver cravada ou zerada, tenta o cálculo manual
            if mem_val == 0 or mem_val == 31.0:
                m = psutil.virtual_memory()
                mem_val = round((m.used / m.total) * 100, 1)

            title = f"SISTEMA: CPU: {cpu_val}% | RAM: {mem_val}%"

        except Exception:
            # Se TUDO falhar, pelo menos mostramos que está tentando
            title = "SISTEMA: MONITORIZANDO (Aguardando Dados...)"
            
        table_packages = PrettyTable(
            field_names=["Package", "Username", "Package Status"],
            title=title,
            border=True,
            align="l"
        )

        # Preenchimento da tabela (Lógica de ofuscação mantida)
        statuses = globals().get("package_statuses", {})
        for package, info in statuses.items():
            username = str(info.get("Username", "Unknown"))
            if username != "Unknown":
                obfuscated = "******" + username[6:] if len(username) > 6 else "******"
                username = obfuscated

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

        possible_files = [
            f"/sdcard/Delta/workspace/{user_id}.main",
            f"/sdcard/Delta/{user_id}.main"
        ]

        timeout = time.time() + max_wait_time
        while time.time() < timeout:
            for signal_file in possible_files:
                # Root check para evitar o 'Permission Denied'
                check_cmd = os.system(f"su -c 'ls {signal_file}' > /dev/null 2>&1")
                if check_cmd == 0:
                    print(f"\033[1;32m[✓] SINAL DETECTADO: {signal_file}\033[0m")
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
    @staticmethod
    def reset_executor_file(package_name):
        try:
            user_id = globals().get("_user_", {}).get(package_name)
            if not user_id: return
            
            # Limpa o sinal via Root para o próximo ciclo começar do zero
            os.system(f"su -c 'rm -f /sdcard/Delta/workspace/{user_id}.main'")
            os.system(f"su -c 'rm -f /sdcard/Delta/{user_id}.main'")
            print(f"\033[1;32m[ Shouko.dev ] - Reset concluído para ID {user_id}\033[0m")
        except Exception as e:
            print(f"Erro no reset: {e}")

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
                next_package_event.wait(45)
            else:
                next_package_event.set()
            next_package_event.wait()

    @staticmethod
    def monitor_presence(server_links, stop_event):
        # Este print CONFIRMA que o monitor ligou.
        print("\033[1;34m[ DEBUG ] Monitor Anti-Crash (Runner) VIVO!\033[0m")
    
        while not stop_event.is_set():
            try:
                # Pegamos as chaves do dicionário para iterar com segurança
                packages = list(server_links.keys()) if isinstance(server_links, dict) else [item[0] for item in server_links]

                for package_name in packages:
                    # 1. Pergunta ao Android de forma leve: "Esse clone está rodando?"
                    # Usamos check_output por ser mais rápido que o popen para o Termux
                    try:
                        check_pid = subprocess.check_output(['su', '-c', f'pidof {package_name}']).decode().strip()
                    except:
                        check_pid = ""

                    if not check_pid:
                        # Se entrar aqui, significa que o processo REALMENTE sumiu
                        print(f"\n\033[1;31m[ Watchdog ] DETECTADO DOWN: {package_name}\033[0m")
                    
                        # 2. Resgate do Link
                        # Garante que pegamos o link correto independente do formato da lista/dict
                        server_link = server_links[package_name] if isinstance(server_links, dict) else next((item[1] for item in server_links if item[0] == package_name), None)

                        # 3. Executa a reabertura usando a função mestre (launch_roblox)
                        # NÃO usamos 'monkey' aqui, pois ele ignora as flags de isolamento de tarefas
                        if server_link:
                            print(f"\033[1;33m[ Watchdog ] Reiniciando {package_name} com isolamento...\033[0m")
                            launch_roblox(package_name, server_link)
                        
                            # 4. PAUSA CRÍTICA (O segredo contra o looping)
                            # Após reabrir UM clone, o monitor dorme por 2 minutos.
                            # Isso dá tempo do clone injetar o script e estabilizar a CPU 
                            # antes de checar se o PRÓXIMO clone caiu.
                            time.sleep(120)

                # Ronda a cada 45 segundos (Mais lento = Menos lag no farm)
                time.sleep(45)
            
                # Limpeza leve de Cache da Cloud (echo 1 em vez de 3 para não dar freeze)
                os.system("su -c 'sync; echo 1 > /proc/sys/vm/drop_caches'")
            
            except Exception as e:
                print(f"\033[1;31m[ Erro Monitor ] {e}\033[0m")
                time.sleep(20)
            
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
            "Auto login IDs",
            "Auto IDs",
            "Auto Check User Setup",
            "Configure AutoExecute",
            "Start All Clones"
        ]

        UIManager.create_dynamic_menu(menu_options)
        
        # --- LÓGICA DE AUTO-START PARA REBOOT ---
        print("\n\033[1;93m[ AUTO ] Iniciando Opção 1 em 5 segundos... (Ctrl+C para manual)\033[0m")
        try:
            # Espera 5 segundos. Se você não apertar Ctrl+C, ele define como "1"
            for i in range(5, 0, -1):
                print(f" Aguardando... {i}", end="\r")
                time.sleep(1)
            setup_type = "1"
        except KeyboardInterrupt:
            # Se você apertar Ctrl+C, ele deixa você digitar o que quiser
            setup_type = input("\n\033[1;93m[ Shouko.dev ] - Enter command: \033[0m").strip()
        codex_bypass_active = False

        if setup_type == "1":
            try:
                # 1. Blindagem (Evita que o Android mate o Termux por falta de RAM)
                os.system("su -c 'echo -1000 > /proc/$(pgrep com.termux)/oom_score_adj'")
                
                server_links = FileManager.load_server_links()
                globals()["accounts"] = FileManager.load_accounts()

                if not globals().get("accounts") or not server_links:
                    print("\033[1;31m[ Erro ] Links ou Contas não encontrados!\033[0m")
                    time.sleep(3)
                    return # Volta ao menu em vez de fechar tudo

                # 2. Configurações Automáticas
                f_interval = 30 * 60  # Force Rejoin a cada 30 min
                print(f"\033[93m[ AUTO ] Force Rejoin definido para: 30 minutos\033[0m")

                # 3. Limpeza e Início Sequencial (O motor do farm)
                print("\033[1;33m[ Shouko.dev ] - Limpando processos antigos...\033[0m")
                RobloxManager.kill_roblox_processes()
                time.sleep(2)
                
                # Abre um por um com o tempo de espera que definimos no launch_package
                Runner.launch_package_sequentially(server_links)

                # 4. Ativa apenas a Thread de Force Rejoin por enquanto
                stop_main_event.clear()
                threading.Thread(target=Runner.force_rejoin, args=(server_links, f_interval, stop_main_event), daemon=True).start()

                # 5. Janela de Descanso Inicial (A "Cura" para o Looping)
                # Esperamos 3 minutos antes de ligar o Watchdog para que todos os clones 
                # terminem de injetar o script e estabilizem a CPU.
                print("\033[1;33m[ ! ] Aguardando 180s para estabilização total antes de ligar o Vigia...\033[0m")
                time.sleep(180) 

                print("\033[1;32m[ ✓ ] Monitoramento de Processos Ativado agora!\033[0m")
                
                # 6. Loop Infinito: Tabela + Watchdog Inteligente
                while not stop_main_event.is_set():
                    for package_name in list(server_links.keys()):
                        # Checagem rigorosa
                        if not is_roblox_running(package_name):
                            # Pequena pausa para confirmar se não é apenas um lag do pgrep
                            time.sleep(10)
                            
                            if not is_roblox_running(package_name):
                                print(f"\n\033[1;31m[ Watchdog ] Detectado: {package_name} fechou!\033[0m")
                                
                                # Limpa qualquer resquício do processo "zumbi"
                                os.system(f"su -c 'am force-stop {package_name}'")
                                time.sleep(2)
                                
                                # Reabre usando o link salvo
                                link = server_links[package_name]
                                launch_roblox(package_name, link)
                                
                                # Pausa o loop do Watchdog por 120s para este clone carregar em paz
                                # Isso impede que ele tente checar o próximo clone enquanto a CPU está em 100%
                                print(f"\033[1;33m[ ! ] Aguardando 2 min para {package_name} estabilizar...\033[0m")
                                time.sleep(120)

                    # Atualização da Tabela Visual
                    with status_lock:
                        UIManager.update_status_table()
                    
                    # Limpeza de memória do Python e espera curta entre rodadas de vigia
                    gc.collect()
                    time.sleep(30) 
                    
            except Exception as e:
                print(f"\033[1;31mErro Crítico Setup 1: {e}\033[0m")
                time.sleep(10)

        elif setup_type == "2":
            try:
                # 1. Chama o menu de login e recebe os pacotes e o nome do SET
                packages, current_set_name = menu_login_opcoes()
                
                if not packages:
                    continue

                print(f"\n\033[1;32m[ Shouko.dev ] - Login concluído. Buscando IDs do {current_set_name}...\033[0m")
                time.sleep(2.0)

                # 2. Extração de User IDs (Necessário para o Farm)
                print(f"\033[93m[ Shouko.dev ] - Extraindo IDs do sistema...\033[0m")
                accounts = []

                for package_name in packages:
                    file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'
                    try:
                        user_id = FileManager.find_userid_from_file(file_path)
                        if user_id and user_id != "-1":
                            accounts.append((package_name, user_id))
                            print(f"\033[96m[ ✓ ] Sucesso: {package_name} -> {user_id}\033[0m")
                        else:
                            print(f"\033[1;31m[ ✗ ] Falha: UserId não encontrado em {package_name}\033[0m")
                    except Exception as e:
                        print(f"\033[1;31m[ ! ] Erro ao ler {package_name}: {e}\033[0m")

                # 3. Salva os IDs e aplica o Link Fixo Automaticamente
                if accounts:
                    FileManager.save_accounts(accounts)
                    
                    # --- CONFIGURAÇÃO AUTOMÁTICA DO LINK ---
                    fixed_link = "https://www.roblox.com/share?code=90856ea1bf5ed54785ce8c39ee168245&type=Server"
                    
                    print(f"\n\033[1;35m[ Shouko.dev ] - Aplicando Link Fixo do Servidor...\033[0m")
                    
                    # Usa a função de formatação para garantir que o link seja aceito pelo Android
                    formatted_link = RobloxManager.format_server_link(fixed_link)
                    
                    if formatted_link:
                        # Associa o link formatado a todos os pacotes das contas encontradas
                        server_links = [(pkg, formatted_link) for pkg, _ in accounts]
                        FileManager.save_server_links(server_links)
                        print("\033[1;32m[ ✓ ] Link configurado e salvo com sucesso para o Farm!\033[0m")
                    else:
                        print("\033[1;31m[ ! ] Erro ao formatar o link padrão.\033[0m")
                    
                else:
                    print("\033[1;31m[ Shouko.dev ] - Nenhuma conta detectada. Verifique o login.\033[0m")
                    input("\033[1;32mPressione Enter para voltar...\033[0m")
                    continue

            except Exception as e:
                print(f"\033[1;31m[ Shouko.dev ] - Erro Crítico: {e}\033[0m")
                input("\033[1;32mPressione Enter para voltar...\033[0m")
                continue
            
            input("\n\033[1;32m[ FINALIZADO ] Tudo pronto. Pressione Enter para voltar ao menu principal...\033[0m")
            continue

        elif setup_type == "3":  # NOVA OPÇÃO: Registro Rápido de IDs
            print(f"\n\033[1;34m[ Shouko.dev ] - Iniciando Registro Rápido (Sem Login)\033[0m")
            
            # Aqui usamos a sua lista que já tem os 6 da Anya + os 3 novos do Arceus
            # Se você ainda não definiu 'clones_lista' no topo, defina-a aqui:
            # clones_lista = ["com.roblox.client.cl1", "com.pacote.aleatorio1", ...]
            
            accounts = []
            print(f"\033[93m[ Shouko.dev ] - Escaneando pastas do sistema...\033[0m")

            for package_name in clones_internos:
                file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'
                try:
                    # Tenta ler o ID direto do arquivo sem abrir o jogo
                    user_id = FileManager.find_userid_from_file(file_path)
                    
                    if user_id and user_id != "-1":
                        accounts.append((package_name, user_id))
                        print(f"\033[96m[ ✓ ] Detectado: {package_name} -> {user_id}\033[0m")
                    else:
                        print(f"\033[1;31m[ ✗ ] Vazio: {package_name} (Conta não logada ou pasta inacessível)\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[ ! ] Erro em {package_name}: {e}\033[0m")

            if accounts:
                FileManager.save_accounts(accounts)
                
                # Aplica o Link Fixo Automaticamente para não ter que digitar
                fixed_link = "https://www.roblox.com/share?code=90856ea1bf5ed54785ce8c39ee168245&type=Server"
                formatted_link = RobloxManager.format_server_link(fixed_link)
                
                if formatted_link:
                    server_links = [(pkg, formatted_link) for pkg, _ in accounts]
                    FileManager.save_server_links(server_links)
                    print("\033[1;32m[ ✓ ] IDs e Links salvos com sucesso para todas as contas detectadas!\033[0m")
            else:
                print("\033[1;31m[ ! ] Nenhuma conta logada encontrada nos clones.\033[0m")
            
            input("\n\033[1;32m[ FINALIZADO ] Pressione Enter para voltar...\033[0m")
            continue

        elif setup_type == "4":
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

        elif setup_type == "5":
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
        
        elif setup_type == "6":
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
            
            
        elif setup_type == "7":
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
