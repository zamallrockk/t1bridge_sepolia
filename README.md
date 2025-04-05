# 🪙 t1bridge-bot

An automated bot to deposit ETH into the T1 Protocol bridge (devnet).

---

## 🚀 Features
- Real-time ETH balance check
- Auto deposit to the bridge contract when balance meets the minimum
- Logs TX hash for every transaction
- Automatic loop with interval
- Safe exit with Ctrl+C handling

---

## 📁 Project Structure
```
t1bridge-bot/
├── bridge_deposit.py        # Main bot script (looping, balance, tx hash, UI)
├── config.json              # Stores PRIVATE_KEY (excluded from Git)
├── requirements.txt         # Dependencies (web3, colorama, eth-account)
├── README.md                # Project description
├── .gitignore               # Ignore config.json & __pycache__/
└── assets/
    └── banner.py            # ASCII banner loader
```

---

## ⚙️ Usage
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `config.json` file:
   ```json
   {
     "PRIVATE_KEY": "0xYOUR_PRIVATE_KEY"
   }
   ```
4. Run the bot:
   ```bash
   python bridge_deposit.py
   ```

---

## ⚠️ Disclaimer
This bot is intended for educational and experimental use on the T1 Protocol testnet/devnet. Use on mainnet is at your own risk.

---

## 🧠 Created by
**zamallrock** – 2025

> Auto deposit bot to T1 Protocol bridge – by zamallrock

