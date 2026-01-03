import os
import requests
import json
import time
import random
import uuid
from eth_account import Account
from web3 import Web3
from datetime import datetime, timedelta
import pytz
from colorama import Fore, Style, init
from typing import Optional, Dict, Any
import warnings
import sys
import subprocess

os.system('clear' if os.name == 'posix' else 'cls')

warnings.filterwarnings('ignore')

if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False
    print("⚠️  Installing zstandard...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "zstandard"])
    import zstandard as zstd
    HAS_ZSTD = True

class TwoCaptchaSolver:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://2captcha.com"
    
    def solve_recaptcha(self, website_url: str, website_key: str, invisible: bool = False) -> Optional[str]:
        create_task_url = f"{self.base_url}/in.php"
        payload = {
            "key": self.api_key,
            "method": "userrecaptcha",
            "googlekey": website_key,
            "pageurl": website_url,
            "invisible": 1 if invisible else 0,
            "json": 1
        }
        
        try:
            response = requests.post(create_task_url, data=payload, timeout=30)
            result = response.json()
            
            if result.get("status") != 1:
                return None
            
            task_id = result.get("request")
            return self._get_captcha_result(task_id)
            
        except Exception:
            return None
    
    def _get_captcha_result(self, task_id: str, max_wait: int = 120) -> Optional[str]:
        get_result_url = f"{self.base_url}/res.php"
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)
            
            try:
                params = {
                    "key": self.api_key,
                    "action": "get",
                    "id": task_id,
                    "json": 1
                }
                
                response = requests.get(get_result_url, params=params, timeout=30)
                result = response.json()
                
                if result.get("status") == 1:
                    return result.get("request")
                elif result.get("request") == "CAPCHA_NOT_READY":
                    continue
                else:
                    return None
                    
            except Exception:
                return None
        
        return None

class PolariseBot:
    def __init__(self, proxy=None, captcha_api_key=None):
        self.base_url = "https://apia.polarise.org/api/app/v1"
        self.app_url = "https://app.polarise.org"
        self.faucet_url = "https://apifaucet-t.polarise.org/claim"
        self.faucet_website = "https://faucet.polarise.org"
        self.faucet_sitekey = "6Le97hIsAAAAAFsmmcgy66F9YbLnwgnWBILrMuqn"
        
        self.rpc_url = "https://chainrpc.polarise.org/"
        self.chain_id = 23758
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        self.session = requests.Session()
        self.proxy = proxy
        self.access_token = None
        self.auth_token = None
        self.user_id = None
        self.captcha_solver = TwoCaptchaSolver(captcha_api_key) if captcha_api_key else None
        
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer',
            'content-type': 'application/json',
            'origin': self.app_url,
            'priority': 'u=1, i',
            'referer': f'{self.app_url}/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        }
        
        self.session.headers.update(self.headers)
        
        self.random_descriptions = [
            "Just exploring the blockchain world! 🚀",
            "Learning about Web3 every day",
            "Excited to be part of this community",
            "Building the future of decentralized tech",
            "Crypto enthusiast and developer",
            "Blockchain is the future!",
            "Decentralization for the win",
            "Web3 explorer and early adopter",
            "Supporting the ecosystem growth",
            "Passionate about DeFi and NFTs",
            "Innovation in blockchain space",
            "Community driven development",
            "Exploring new opportunities in crypto",
            "Digital nomad in the metaverse",
            "Believer in decentralized systems",
            "Tech enthusiast and blockchain advocate",
            "Building on-chain solutions",
            "Crypto journey continues",
            "Empowering through technology",
            "Next generation of finance"
        ]
        
        self.random_titles = [
            "Hello everyone!",
            "Good morning guys",
            "Hey there!",
            "Greetings folks",
            "What's up everyone",
            "Hello world",
            "Hi there friends",
            "Good day all",
            "Hey guys!",
            "Welcome everyone",
            "Hello community",
            "Hey folks!",
            "Good vibes today",
            "Hi everyone!",
            "Greetings all",
            "Hello team",
            "Hey community!",
            "Good to be here",
            "Hi guys!",
            "Hello friends"
        ]
        
        self.random_comments = [
            "lfg",
            "gm",
            "nice!",
            "amazing",
            "great work",
            "awesome!",
            "love it",
            "interesting",
            "cool stuff",
            "well done",
            "fantastic",
            "impressive",
            "good job",
            "excited!",
            "nice post",
            "keep it up",
            "wonderful",
            "brilliant",
            "excellent",
            "incredible"
        ]
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def generate_access_token(self):
        self.access_token = str(uuid.uuid4())
        return self.access_token
    
    def get_nonce(self, wallet_address):
        url = f"{self.base_url}/profile/getnonce"
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        
        payload = {
            "wallet": wallet_address,
            "chain_name": "polarise"
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                return data.get('signed_nonce')
            return None
                
        except Exception:
            return None
    
    def generate_biz_id(self, wallet_address):
        url = f"{self.base_url}/discussion/generatebizid"
        
        if not self.access_token:
            self.generate_access_token()
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        
        payload = {
            "biz_input": wallet_address.lower(),
            "biz_type": "subscription_question",
            "chain_name": "polarise"
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                return data.get('data', {}).get('Biz_Id')
            return None
                
        except Exception:
            return None
    
    def login(self, wallet_address, private_key, nonce, sub_id, inviter_code=""):
        url = f"{self.base_url}/profile/login"
        
        if not self.access_token:
            self.generate_access_token()
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        
        from eth_account.messages import encode_defunct
        w3 = Web3()
        
        message_to_sign = f"Nonce to confirm: {nonce}"
        message = encode_defunct(text=message_to_sign)
        
        signed = w3.eth.account.sign_message(message, private_key=private_key)
        signature = signed.signature.hex()
        
        payload = {
            "chain_name": "polarise",
            "inviter_code": inviter_code,
            "name": wallet_address[:6],
            "nonce": nonce,
            "sid": self.access_token,
            "signature": signature,
            "sub_id": sub_id,
            "wallet": wallet_address
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                auth_token = data.get('data', {}).get('auth_token_info', {}).get('auth_token')
                user_id = data.get('data', {}).get('user_id')
                self.auth_token = auth_token
                self.user_id = user_id
                return auth_token
            return None
                
        except Exception:
            return None
    
    def send_polar_transaction(self, private_key, to_address, amount_polar):
        try:
            account = Account.from_key(private_key)
            address = account.address
            
            nonce = self.w3.eth.get_transaction_count(address)
            value = self.w3.to_wei(amount_polar, 'ether')
            
            gas_price = self.w3.eth.gas_price
            
            tx = {
                'nonce': nonce,
                'to': self.w3.to_checksum_address(to_address),
                'value': value,
                'gas': 21000,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            }
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            raw_tx = getattr(signed_tx, 'rawTransaction', getattr(signed_tx, 'raw_transaction', None))
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            return None

    def complete_task(self, wallet_address, task_id, extra_info_dict=None):
        url = f"{self.base_url}/points/completetask"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        payload = {
            "chain_name": "polarise",
            "task_id": task_id,
            "user_wallet": wallet_address
        }
        
        if extra_info_dict:
            payload["extra_info"] = json.dumps(extra_info_dict, separators=(',', ':'))
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                return data.get('data')
            else:
                return None
                
        except Exception:
            return None

    def save_post(self, wallet_address):
        url = f"{self.base_url}/posts/savepost"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        random_description = random.choice(self.random_descriptions)
        current_timestamp = int(time.time() * 1000)
        
        payload = {
            "user_id": self.user_id,
            "chain_name": "polarise",
            "community_id": 0,
            "community_name": "",
            "title": "",
            "tags": [],
            "description": random_description,
            "is_subscribe_enable": False,
            "media_links": "[]",
            "published_time": current_timestamp
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                post_id = data.get('data', {}).get('id')
                return {"success": True, "post_id": post_id, "description": random_description}
            else:
                return None
                
        except Exception:
            return None
    
    def save_post_with_title(self, wallet_address):
        url = f"{self.base_url}/posts/savepost"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        random_title = random.choice(self.random_titles)
        current_timestamp = int(time.time() * 1000)
        
        payload = {
            "user_id": self.user_id,
            "chain_name": "polarise",
            "community_id": 0,
            "community_name": "",
            "title": random_title,
            "tags": [],
            "description": "",
            "is_subscribe_enable": False,
            "media_links": "[]",
            "published_time": current_timestamp
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                post_id = data.get('data', {}).get('id')
                return {"success": True, "post_id": post_id, "title": random_title}
            else:
                return None
                
        except Exception:
            return None
    
    def save_comment(self, wallet_address, post_id):
        url = f"{self.base_url}/posts/savecomment"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        random_comment = random.choice(self.random_comments)
        current_timestamp = int(time.time() * 1000)
        
        payload = {
            "user_id": self.user_id,
            "post_id": post_id,
            "content": random_comment,
            "tags": [],
            "published_time": current_timestamp,
            "chain_name": "polarise"
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                comment_id = data.get('data', {}).get('id')
                return {"success": True, "comment_id": comment_id, "content": random_comment}
            else:
                return None
                
        except Exception:
            return None
    
    def get_random_users(self):
        url = f"{self.base_url}/profile/getfollowinglist"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        
        payload = {
            "chain_name": "polarise",
            "page_index": 1,
            "page_size": 50
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            if data.get('code') == '200':
                users = data.get('data', {}).get('list', [])
                return users if users else []
            return []
                
        except Exception:
            return []
    
    def follow_user(self, wallet_address, target_user_id, target_user_name):
        url = f"{self.base_url}/profile/followtoggle"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        actor_name = wallet_address[:6]
        
        payload = {
            "actor_user_id": self.user_id,
            "actor_user_name": actor_name,
            "target_user_id": target_user_id,
            "target_user_name": target_user_name,
            "chain_name": "polarise",
            "desired": True
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                applied = data.get('data', {}).get('applied')
                return {"success": True, "applied": applied}
            else:
                return None
                
        except Exception:
            return None
    
    def save_subscription(self, wallet_address, subed_addr, sub_id):
        url = f"{self.base_url}/subscription/savesuborder"
        
        headers = self.session.headers.copy()
        headers['accesstoken'] = self.access_token
        headers['authorization'] = f"Bearer {self.auth_token} {self.access_token} {wallet_address} polarise"
        
        order_time = int(time.time())
        
        payload = {
            "subed_addr": subed_addr,
            "chain_name": "polarise",
            "order_time": order_time,
            "sub_id": sub_id
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data.get('code') == '200':
                return {"success": True}
            else:
                return None
                
        except Exception:
            return None

    def claim_faucet(self, address: str) -> Dict[str, Any]:
        if not self.captcha_solver:
            return {"success": False, "error": "No captcha solver"}
        
        self.log("Solving captcha...", "INFO")
        captcha_token = self.captcha_solver.solve_recaptcha(
            self.faucet_website,
            self.faucet_sitekey,
            invisible=False
        )
        
        if not captcha_token:
            return {"success": False, "error": "Failed to solve captcha"}
        
        self.log("Captcha solved!", "SUCCESS")
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": self.faucet_website,
            "referer": f"{self.faucet_website}/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        payload = {
            "address": address,
            "denom": "uluna",
            "response": captcha_token
        }
        
        try:
            proxies = None
            if self.proxy:
                proxies = {
                    "http": self.proxy,
                    "https": self.proxy
                }
            
            response = requests.post(
                self.faucet_url,
                headers=headers,
                json=payload,
                proxies=proxies,
                timeout=30
            )
            
            result = response.json()
            
            if result.get("code") == 200:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": result}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def auto_login_from_private_key(self, private_key: str):
        try:
            account = Account.from_key(private_key)
            wallet_address = account.address
            
            short_address = f"{wallet_address[:6]}...{wallet_address[-4:]}"
            self.log(f"{short_address}", "INFO")
            
            self.generate_access_token()
            time.sleep(random.uniform(0.5, 1))
            
            nonce = self.get_nonce(wallet_address)
            if not nonce:
                return {'success': False, 'wallet': wallet_address, 'private_key': private_key}
            
            time.sleep(random.uniform(1, 2))
            
            biz_id = self.generate_biz_id(wallet_address.lower())
            if not biz_id:
                return {'success': False, 'wallet': wallet_address, 'private_key': private_key}
            
            time.sleep(random.uniform(1, 2))
            
            auth_token = self.login(wallet_address, private_key, nonce, biz_id)
            
            if not auth_token:
                return {'success': False, 'wallet': wallet_address, 'private_key': private_key}
            
            time_str = self.get_wib_time()
            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
            
            return {
                'success': True,
                'wallet': wallet_address,
                'private_key': private_key,
                'auth_token': auth_token
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

def read_file_lines(filename: str) -> list:
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
    except Exception:
        return []

def print_banner():
    banner = f"""
{Fore.CYAN}POLARISE AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
    print(banner)

def countdown_timer(hours=24):
    total_seconds = hours * 3600
    
    try:
        for remaining in range(total_seconds, 0, -1):
            hours_left = remaining // 3600
            minutes_left = (remaining % 3600) // 60
            seconds_left = remaining % 60
            
            timer_str = f"{hours_left:02d}:{minutes_left:02d}:{seconds_left:02d}"
            print(f"\r{Fore.YELLOW}[COUNTDOWN] Next cycle in: {timer_str}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(1)
        
        print()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Countdown interrupted by user.{Style.RESET_ALL}")
        raise

def main():
    print_banner()
    
    private_keys = read_file_lines('accounts.txt')
    
    if not private_keys:
        print(f"{Fore.RED}[ERROR] No private keys found in accounts.txt!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[INFO] Please add private keys to accounts.txt (one per line){Style.RESET_ALL}")
        return
    
    captcha_keys = read_file_lines('2captcha.txt')
    captcha_key = captcha_keys[0] if captcha_keys else None
    
    if not captcha_key:
        print(f"{Fore.RED}[ERROR] No 2Captcha key found in 2captcha.txt!{Style.RESET_ALL}")
        return
    
    proxies = read_file_lines('proxy.txt')
    
    print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Run with proxy")
    print(f"2. Run without proxy{Style.RESET_ALL}")
    print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
            if choice in ['1', '2']:
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
            exit(0)
    
    use_proxy = choice == '1'
    
    if use_proxy:
        if proxies:
            print(f"{Fore.GREEN}[INFO] Running with proxy{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[INFO] Loaded {len(proxies)} proxies{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[WARNING] No proxies found, running without proxy{Style.RESET_ALL}")
            use_proxy = False
    else:
        print(f"{Fore.GREEN}[INFO] Running without proxy{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}[INFO] Loaded {len(private_keys)} accounts successfully{Style.RESET_ALL}")
    
    while True:
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        success_count = 0
        fail_count = 0
        
        for i, private_key in enumerate(private_keys):
            print(f"{Fore.CYAN}[INFO] Account #{i+1}/{len(private_keys)}{Style.RESET_ALL}")
            
            proxy = proxies[i % len(proxies)] if (use_proxy and proxies) else None
            
            if proxy:
                print(f"{Fore.CYAN}[INFO] Proxy: {proxy}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}[INFO] Proxy: No Proxy{Style.RESET_ALL}")
            
            try:
                bot = PolariseBot(proxy=proxy, captcha_api_key=captcha_key)
                
                login_result = bot.auto_login_from_private_key(private_key)
                
                if not login_result['success']:
                    bot.log("Login failed!", "ERROR")
                    fail_count += 1
                    if i < len(private_keys) - 1:
                        print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                        time.sleep(2)
                    continue
                
                wallet_address = login_result['wallet']
                auth_token = login_result['auth_token']
                
                with open('registered_accounts.txt', 'a') as f:
                    f.write(f"{wallet_address}|{private_key}|{auth_token}|{bot.access_token}\n")
                
                with open('address.txt', 'a') as f:
                    f.write(f"{wallet_address}\n")
                
                time.sleep(random.uniform(2, 3))
                
                bot.log("Processing Task:", "INFO")
                
                claim_result = bot.claim_faucet(wallet_address)
                
                if claim_result.get("success"):
                    data = claim_result.get("data", {})
                    amount = data.get("amount", "0")
                    
                    time_str = bot.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Claim Success! Amount: {amount} POLAR{Style.RESET_ALL}")
                    
                    time.sleep(5)
                    max_retries = 10
                    has_balance = False
                    for retry in range(max_retries):
                        balance = bot.w3.eth.get_balance(wallet_address)
                        if balance > 0:
                            has_balance = True
                            break
                        time.sleep(5)
                    
                    tx_hash = None
                    to_address = "0x9c4324156ba59a70ffbc67b98ee2ef45aee4e19f"
                    if has_balance:
                        tx_hash = bot.send_polar_transaction(private_key, to_address, 0.001)
                        if tx_hash:
                            time.sleep(random.uniform(5, 10))
                    
                    bot.log("Completing Tasks:", "INFO")
                    task_success = 0
                    
                    if tx_hash:
                        bot.log("Task (On-chain Transaction)...", "INFO")
                        extra_info = {"tx_hash": tx_hash, "from": wallet_address, "to": to_address, "value": "1000000000000000"}
                        if bot.complete_task(wallet_address, 1, extra_info):
                            time_str = bot.get_wib_time()
                            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task completed!{Style.RESET_ALL}")
                            task_success += 1
                        time.sleep(random.uniform(5, 10))
                        
                        bot.log("Task (On-chain Transaction)...", "INFO")
                        if bot.complete_task(wallet_address, 2, extra_info):
                            time_str = bot.get_wib_time()
                            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task completed!{Style.RESET_ALL}")
                            task_success += 1
                        time.sleep(random.uniform(5, 10))
                    
                    bot.log("Task (Create Post with Title)...", "INFO")
                    post_title_result = bot.save_post_with_title(wallet_address)
                    created_post_id = None
                    if post_title_result and post_title_result.get("success"):
                        time_str = bot.get_wib_time()
                        title = post_title_result.get("title", "")
                        created_post_id = post_title_result.get("post_id")
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Post created: {title}{Style.RESET_ALL}")
                        task_success += 1
                    time.sleep(random.uniform(5, 10))
                    
                    if created_post_id:
                        bot.log("Task (Save Comment)...", "INFO")
                        comment_result = bot.save_comment(wallet_address, created_post_id)
                        if comment_result and comment_result.get("success"):
                            time_str = bot.get_wib_time()
                            content = comment_result.get("content", "")
                            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Comment created: {content}{Style.RESET_ALL}")
                            task_success += 1
                        time.sleep(random.uniform(5, 10))
                    
                    bot.log("Task (Follow User)...", "INFO")
                    random_users = [
                        {"user_id": 780538, "user_name": "0x5bE6"},
                        {"user_id": 705990, "user_name": "0x2bf1"},
                        {"user_id": 791861, "user_name": "0xC43C"},
                        {"user_id": 123456, "user_name": "0xABC1"},
                        {"user_id": 234567, "user_name": "0xDEF2"}
                    ]
                    target_user = random.choice(random_users)
                    follow_result = bot.follow_user(wallet_address, target_user["user_id"], target_user["user_name"])
                    if follow_result and follow_result.get("success"):
                        time_str = bot.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Followed user: {target_user['user_name']}{Style.RESET_ALL}")
                        task_success += 1
                    time.sleep(random.uniform(5, 10))
                    
                    bot.log("Task (Subscription)...", "INFO")
                    random_addresses = [
                        "0xbe56d0d5b1a62f38d1412c4c6e55e6c70f7b7aed",
                        "0x9c4324156ba59a70ffbc67b98ee2ef45aee4e19f",
                        "0x742d35cc6634c0532925a3b844bc454e4438f44e"
                    ]
                    target_address = random.choice(random_addresses)
                    sub_id_generated = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')[:32]
                    sub_result = bot.save_subscription(wallet_address, target_address, sub_id_generated)
                    if sub_result and sub_result.get("success"):
                        time_str = bot.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Subscription created!{Style.RESET_ALL}")
                        task_success += 1
                    time.sleep(random.uniform(5, 10))
                    
                    bot.log("Task (Email)...", "INFO")
                    email = f"user_{wallet_address[2:10].lower()}@gmail.com"
                    if bot.complete_task(wallet_address, 3, {"email": email}):
                        time_str = bot.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task completed!{Style.RESET_ALL}")
                        task_success += 1
                    time.sleep(random.uniform(5, 10))
                    
                    for task_id in [4, 5, 6, 8, 10, 11]:
                        bot.log("Task (Social Task)...", "INFO")
                        if bot.complete_task(wallet_address, task_id):
                            time_str = bot.get_wib_time()
                            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task completed!{Style.RESET_ALL}")
                            task_success += 1
                        time.sleep(random.uniform(5, 10))
                    
                    time_str = bot.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] All Tasks Completed !{Style.RESET_ALL}")
                    
                    success_count += 1
                    
                else:
                    error = claim_result.get("error", "Unknown error")
                    bot.log(f"Claim Failed: {error}", "ERROR")
                    fail_count += 1
                
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to process account: {str(e)}{Style.RESET_ALL}")
                fail_count += 1
            
            if i < len(private_keys) - 1:
                print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                time.sleep(2)
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[INFO] Process Complete | Success: {success_count}/{len(private_keys)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        countdown_timer(24)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
        exit(0)
