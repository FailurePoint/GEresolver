import argparse
import requests
import sys
import time
import colorama

colorama.init(autoreset=True)
textcol = colorama.Fore

GITHUB_API = "https://api.github.com/search/commits"
HEADERS = {
    "Accept": "application/vnd.github.cloak-preview",
    "User-Agent": "GitHubEmailLookup"
    # You can add Authorization header here if needed
    # "Authorization": "Bearer YOUR_TOKEN"
}

def resolve_email(email):
    url = f"{GITHUB_API}?q=author-email:{email}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        if data.get("items"):
            for item in data["items"]:
                author = item.get("author")
                if author and author.get("html_url"):
                    print(f"found pofile at: {textcol.GREEN}{author["html_url"]} {textcol.BLUE}({email})")
                    break
        else:
            print(f"{textcol.RED}No profile found for {textcol.BLUE}{email}")
    elif response.status_code == 403:
        print(f"{textcol.RED}Rate limited or unauthorized.")
    else:
         print(f"{textcol.RED}Error: {response.status_code} - {response.text}")

def process_list(file_path):
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
            print(f"{textcol.BLUE}Checking {textcol.RED}{len(emails)}{textcol.BLUE} from: {textcol.RED}{file_path}")
        for email in emails:
            resolve_email(email)
    except FileNotFoundError:
        print(f"{textcol.RED}Cannot find list file at: {file_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Command line tool for resolving email addresses to GitHub accounts."
    )
    parser.add_argument('-e', '--email', help='Single email address to search.')
    parser.add_argument('-l', '--list', help='Path to a file containing email addresses (one per line).')
    args = parser.parse_args()

    print(textcol.GREEN + r"""
  ___________________                           .__      /\               
 /  _____/\_   _____/______   ____   __________ |  |___  || ___________ 
/   \  ___ |    __)_\_  __ \_/ __ \ /  ___/  _ \|  |\  \/ // __ \_  __ \
\    \_\  \|        \|  | \/\  ___/ \___ (  <_> )  |_\   /\  ___/|  | \/
 \______  /_______  /|__|    \___  >____  >____/|____/\_/  \___  >__|   
        ||        ||             ||     ||                     ||
        \/        \/             \/     \/    Br0k3nPix3l      \/       
""")

    if args.email:
        print(f'{textcol.BLUE}Running oneoff email resolution...\nChecking email address: {textcol.RED}{args.email}')
        resolve_email(args.email)
    elif args.list:
        print(f"{textcol.BLUE}Starting in list mode...")
        process_list(args.list)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
