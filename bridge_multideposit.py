import json
import time
import signal
import sys
from decimal import Decimal
from web3 import Web3
from eth_account import Account
from colorama import init, Fore
from assets.banner import show_banner

init(autoreset=True)

with open("config.json") as f:
    config = json.load(f)

ACCOUNTS = config["ACCOUNTS"]
RPC_URL = "https://ethereum-sepolia.publicnode.com"
BRIDGE_CONTRACT = "0xAFdF5cb097D6FB2EB8B1FFbAB180e667458e18F4"
DEPOSIT_AMOUNT = Web3.to_wei(0.00005, 'ether')
CHECK_INTERVAL = 60  # detik

# Load ABI
with open("bridge_abi.json") as f:
    bridge_abi = json.load(f)

w3 = Web3(Web3.HTTPProvider(RPC_URL))
bridge = w3.eth.contract(address=BRIDGE_CONTRACT, abi=bridge_abi)

running = True
def handle_exit(sig, frame):
    global running
    running = False
    print(Fore.RED + "\n\n[✋] Dihentikan oleh user. Bye!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

def sleep_with_interrupt(seconds):
    for _ in range(seconds):
        if not running:
            break
        time.sleep(1)

# Konstanta fungsi bridge
SEND_VALUE = 0
MESSAGE = b''
GAS_LIMIT = 200000
DEST_CHAIN_ID = 1001

# Banner
show_banner()
print(Fore.GREEN + f"[✓] Terhubung ke RPC: {w3.provider.endpoint_uri}\n")

# Statistik
total_tx = 0
total_sent = Decimal('0')

while running:
    for entry in ACCOUNTS:
        try:
            PRIVATE_KEY = entry["PRIVATE_KEY"]
            account = Account.from_key(PRIVATE_KEY)
            address = account.address

            balance = w3.eth.get_balance(address)
            eth_balance = Web3.from_wei(balance, 'ether')
            print(Fore.CYAN + f"[+] Wallet: {address} | Saldo: {eth_balance} ETH")

            gas_price = w3.to_wei('2', 'gwei')
            estimated_cost = DEPOSIT_AMOUNT + (gas_price * 300000)

            if balance < estimated_cost:
                print(Fore.YELLOW + f"[!] Saldo tidak cukup (butuh {Web3.from_wei(estimated_cost, 'ether')} ETH) ➜ Lewatkan {address}\n")
                continue  # <--- auto-skip akun

            nonce = w3.eth.get_transaction_count(address)

            tx = bridge.functions.sendMessage(
                address,
                SEND_VALUE,
                MESSAGE,
                GAS_LIMIT,
                DEST_CHAIN_ID
            ).build_transaction({
                'from': address,
                'value': DEPOSIT_AMOUNT,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': gas_price,
                'chainId': 11155111
            })

            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

            print(Fore.GREEN + f"[✓] TX dikirim dari {address}! TX Hash: {tx_hash.hex()}")
            total_tx += 1
            total_sent += Decimal(Web3.from_wei(DEPOSIT_AMOUNT, 'ether'))

        except Exception as e:
            print(Fore.RED + f"[!] Error di akun {entry['PRIVATE_KEY'][:10]}...: {e}")

    print(Fore.MAGENTA + f"[📊] Total TX: {total_tx} | Total terkirim: {total_sent} ETH")
    print(Fore.YELLOW + f"[⏳] Menunggu {CHECK_INTERVAL} detik...\n")
    sleep_with_interrupt(CHECK_INTERVAL)
