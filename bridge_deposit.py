import json
import time
import signal
import sys
from decimal import Decimal
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style
from assets.banner import show_banner

init(autoreset=True)

# Load config
with open("config.json") as f:
    config = json.load(f)

PRIVATE_KEY = config["PRIVATE_KEY"]
RPC_URL = "https://ethereum-sepolia.publicnode.com"
BRIDGE_CONTRACT = "0xAFdF5cb097D6FB2EB8B1FFbAB180e667458e18F4"
DEPOSIT_AMOUNT = Web3.to_wei(0.0001, 'ether')
CHECK_INTERVAL = 60  # seconds

# Setup web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
wallet_address = account.address

# Handle exit
running = True
def handle_exit(sig, frame):
    global running
    running = False
    print(Fore.RED + "\n\n[✋] Dihentikan oleh user. Bye!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Mini delay function that checks for KeyboardInterrupt
def sleep_with_interrupt(seconds):
    for _ in range(seconds):
        if not running:
            break
        time.sleep(1)

# Show banner
show_banner()
print(Fore.GREEN + f"[✓] Terhubung ke RPC: {w3.provider.endpoint_uri}\n")
print(Fore.CYAN + f"[+] Wallet: {wallet_address}")

# Start loop
total_tx = 0
total_sent = Decimal('0')

while running:
    try:
        balance = w3.eth.get_balance(wallet_address)
        eth_balance = Web3.from_wei(balance, 'ether')
        print(Fore.CYAN + f"[+] Saldo ETH: {eth_balance} ETH")

        if balance > DEPOSIT_AMOUNT:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = {
                'nonce': nonce,
                'to': BRIDGE_CONTRACT,
                'value': DEPOSIT_AMOUNT,
                'gas': 21000,
                'gasPrice': w3.to_wei('2', 'gwei'),
                'chainId': 11155111  # Sepolia chain ID
            }
            signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hex = tx_hash.hex()
            print(Fore.GREEN + f"[✓] Transaksi dikirim! TX Hash: {tx_hex}")
            total_tx += 1
            total_sent += Decimal(Web3.from_wei(DEPOSIT_AMOUNT, 'ether'))
        else:
            print(Fore.YELLOW + "[!] Saldo tidak mencukupi untuk deposit.")

        print(Fore.MAGENTA + f"[📊] Total transaksi: {total_tx} | Total terkirim: {total_sent} ETH")
        print(Fore.YELLOW + f"[⏳] Menunggu {CHECK_INTERVAL} detik sebelum cek ulang...\n")
        sleep_with_interrupt(CHECK_INTERVAL)

    except KeyboardInterrupt:
        handle_exit(None, None)
    except Exception as e:
        print(Fore.RED + f"[!] Gagal kirim transaksi: {e}")
        print(Fore.YELLOW + f"[⏳] Menunggu {CHECK_INTERVAL} detik sebelum cek ulang...\n")
        sleep_with_interrupt(CHECK_INTERVAL)
