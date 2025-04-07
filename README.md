# 🪙 t1bridge-bot Multi 

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
t1bridge_sepolia_multi/
├── bridge_multideposit.py        
├── config.json              
├── requirements.txt        
├── README.md                
├── .gitignore               
└── assets/
    └── banner.py            
```

---

## ⚙️ Usage
1. Clone this repository
   ```bash
   git clone https://github.com/zamallrockk/t1bridge_sepolia_multi.git
   cd t1bridge_sepolia_multi
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `config.json` file:
   ```bash
   {
     "ACCOUNTS": [
      {
        "PRIVATE_KEY": "0x....."
      },
      {
        "PRIVATE_KEY": "0x....."
      }
      
    ]
   }

   
   ```
4. Run the bot:
   ```bash
   python bridge_multideposit.py
   ```

---

## ⚠️ Disclaimer
This bot is intended for educational and experimental use on the T1 Protocol testnet/devnet. Use on mainnet is at your own risk.

---
## Badges

[![Donate](https://img.shields.io/badge/Buy_Me_a_Coffee-ko--fi-FF5E5B?logo=ko-fi&logoColor=white&style=flat-square)](https://ko-fi.com/zamallrock)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🧠 Created by
**zamallrock** – 2025

> Auto deposit bot to T1 Protocol bridge – by zamallrock
