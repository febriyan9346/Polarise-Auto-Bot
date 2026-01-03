# Polarise Auto Bot

**🔗 Join Polarise: [https://app.polarise.org/?code=7cwPHE](https://app.polarise.org/?code=7cwPHE)**

---

## 📋 Description

Polarise Auto Bot is an automated tool for interacting with the Polarise blockchain ecosystem. This bot automates various tasks including:

- 🔐 Automatic wallet login
- 💧 Faucet claiming with captcha solving
- 💸 On-chain transactions
- 📝 Post creation and commenting
- 👥 User following
- 📧 Email verification
- 🎯 Social task completion
- 📊 Subscription management

---

## ✨ Features

- **Multi-Account Support**: Process multiple accounts sequentially
- **Proxy Support**: Optional proxy configuration for enhanced privacy
- **Automated Captcha Solving**: Integration with 2Captcha service
- **Task Automation**: Complete all available tasks automatically
- **24-Hour Loop**: Continuous operation with countdown timer
- **Detailed Logging**: Color-coded console output with timestamps
- **Error Handling**: Robust error management and retry mechanisms

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Clone Repository

```bash
git clone https://github.com/febriyan9346/Polarise-Auto-Bot.git
cd Polarise-Auto-Bot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install web3 eth-account requests colorama pytz zstandard
```

---

## ⚙️ Configuration

### 1. Setup Account Private Keys

Create a file named `accounts.txt` in the root directory and add your private keys (one per line):

```
0xYourPrivateKey1
0xYourPrivateKey2
0xYourPrivateKey3
```

⚠️ **Security Warning**: Never share your private keys with anyone!

### 2. Setup 2Captcha API Key

Create a file named `2captcha.txt` and add your 2Captcha API key:

```
your_2captcha_api_key_here
```

Get your API key from: [https://2captcha.com](https://2captcha.com)

### 3. Setup Proxies (Optional)

Create a file named `proxy.txt` if you want to use proxies (one per line):

```
http://user:pass@ip:port
http://user:pass@ip:port
socks5://user:pass@ip:port
```

---

## 🎮 Usage

### Run the Bot

```bash
python bot.py
```

### Select Mode

When prompted, choose your preferred mode:
- **1**: Run with proxy (requires `proxy.txt`)
- **2**: Run without proxy

### Bot Operation

The bot will:
1. Load all accounts from `accounts.txt`
2. Process each account sequentially
3. Complete all available tasks
4. Wait 24 hours before the next cycle
5. Repeat indefinitely

---

## 📁 Output Files

The bot creates the following files:

- `registered_accounts.txt`: Stores wallet addresses, private keys, and auth tokens
- `address.txt`: List of all processed wallet addresses

---

## 🎯 Available Tasks

The bot automatically completes:

1. ✅ Faucet claim
2. ✅ On-chain transactions (2 tasks)
3. ✅ Create post with title
4. ✅ Create comment on post
5. ✅ Follow random user
6. ✅ Create subscription
7. ✅ Email verification
8. ✅ Social tasks (Twitter, Discord, etc.)

---

## 🛠️ Troubleshooting

### Common Issues

**Bot fails to login:**
- Check if private keys are correct
- Ensure internet connection is stable
- Verify proxy settings if using proxies

**Captcha solving fails:**
- Check 2Captcha API key balance
- Ensure 2Captcha service is operational

**Transaction errors:**
- Ensure wallet has sufficient gas fees
- Check RPC endpoint status

### Error Logs

Check console output for detailed error messages with color-coded severity:
- 🔵 **INFO**: General information
- 🟢 **SUCCESS**: Successful operations
- 🟡 **WARNING**: Non-critical issues
- 🔴 **ERROR**: Failed operations

---

## ⚠️ Disclaimer

- This bot is for educational purposes only
- Use at your own risk
- Always keep your private keys secure
- Respect the Polarise platform's terms of service
- The author is not responsible for any losses or damages

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**FEBRIYAN**

- GitHub: [@febriyan9346](https://github.com/febriyan9346)

---

## 💖 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

Your support helps us maintain and improve this project! 🙏

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/febriyan9346/Polarise-Auto-Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/febriyan9346/Polarise-Auto-Bot/discussions)

---

## 🔄 Updates

Stay tuned for updates and new features! Star ⭐ this repository to get notifications.

---

**Made with ❤️ by FEBRIYAN**