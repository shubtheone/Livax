import requests
import re
import sys
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# List of sensitive keywords
SENSITIVE_KEYWORDS = [
    "internal use only", "confidential", "strictly private", 
    "personal & confidential", "private", "restricted", 
    "internal", "not for distribution", "do not share", 
    "proprietary", "trade secret", "classified", "sensitive", 
    "bank statement", "invoice", "salary", "contract", 
    "agreement", "non disclosure", "passport", 
    "social security", "ssn", "date of birth", 
    "credit card", "identity", "id number", 
    "company confidential", "staff only", 
    "management only", "internal only"
]

class WaybackScanner:
    def __init__(self):
        self.console = Console()

    def print_banner(self):
        banner = """[bold cyan]
░█─── ▀█▀ ░█──░█ ─█▀▀█ ▀▄░▄▀ 
░█─── ░█─ ─░█░█─ ░█▄▄█ ─░█── 
░█▄▄█ ▄█▄ ──▀▄▀─ ░█─░█ ▄▀░▀▄
[/bold cyan]"""
        
        author = "\n[bold white]by blackthorns (@shubtheone)[/bold white]"
        version = "[bold red]Version 1.1[/bold red]"
        
        panel = Panel(
            Text.from_markup(f"{banner}\n{author}\n{version}"),
            subtitle="[bold green]Wayback Machine Content Scanner[/bold green]",
            border_style="blue"
        )
        self.console.print(panel)

    def search_wayback_archive(self, url_pattern):
        """
        Search Wayback Machine for URLs matching the given pattern
        """
        base_url = "https://web.archive.org/cdx/search/cdx"
        
        # Parameters for the search
        params = {
            "url": url_pattern,
            "collapse": "urlkey",
            "output": "text",
            "fl": "original",
            "filter": "original:.*\\.(xls|xml|xlsx|json|pdf|sql|doc|docx|ppt|txt|git|zip|tar\\.gz|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|env|apk|msi|dmg|tmp|crt|pem|key|pub|asc)$"
        }
        
        try:
            # Send GET request to Wayback Machine CDX API
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Get the URLs
            urls = response.text.strip().split('\n')
            
            return urls
        
        except requests.RequestException as e:
            self.console.print(f"[bold red]Error occurred: {e}[/bold red]", file=sys.stderr)
            return []

    def is_url_accessible(self, url, timeout=5):
        """
        Check if the URL is accessible
        """
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except (requests.RequestException, Exception):
            return False

    def extract_text_from_pdf(self, url):
        """
        Extract text from a PDF file downloaded from a URL
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with BytesIO(response.content) as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            return ""

    def search_sensitive_keywords(self, text):
        """
        Search for sensitive keywords in the given text
        """
        for keyword in SENSITIVE_KEYWORDS:
            if re.search(keyword, text, re.IGNORECASE):
                return True
        return False

    def process_urls(self, urls):
        """
        Process URLs for accessibility and sensitive content
        """
        # Track accessible and sensitive URLs
        accessible_urls = []
        sensitive_urls = []
        
        # Process URLs with a progress bar
        self.console.print("\n[bold yellow]Checking URL accessibility and scanning files...[/bold yellow]")
        for url in tqdm(urls, desc="Processing URLs", unit="url"):
            # Check URL accessibility first
            if not self.is_url_accessible(url):
                continue
            
            accessible_urls.append(url)
            
            try:
                # Extract text based on file extension
                if url.endswith('.pdf'):
                    file_text = self.extract_text_from_pdf(url)
                else:
                    continue
                
                # Check for sensitive keywords
                if self.search_sensitive_keywords(file_text):
                    sensitive_urls.append(url)
                    self.console.print(f"\n[bold red]Sensitive info found in: {url}[/bold red]")
            
            except Exception as e:
                continue
        
        # Save accessible URLs to a file
        with open('accessible_urls.txt', 'w') as f:
            for url in accessible_urls:
                f.write(f"{url}\n")
        
        # Save sensitive URLs to a file
        if sensitive_urls:
            with open('sensitive_urls.txt', 'w') as f:
                for url in sensitive_urls:
                    f.write(f"{url}\n")
            self.console.print(f"\n[bold green]Found {len(sensitive_urls)} URLs with sensitive information.[/bold green]")
            self.console.print("[bold green]Sensitive URLs saved to sensitive_urls.txt[/bold green]")
        else:
            self.console.print("\n[bold yellow]No sensitive URLs found.[/bold yellow]")
        
        # Print summary
        self.console.print(f"\n[bold white]Total URLs checked: {len(urls)}[/bold white]")
        self.console.print(f"[bold white]Accessible URLs: {len(accessible_urls)}[/bold white]")
        self.console.print(f"[bold white]URLs with sensitive information: {len(sensitive_urls)}[/bold white]")

    def run(self):
        # Print banner
        self.print_banner()
        
        # Prompt user for URL pattern
        url_pattern = input("Enter the URL pattern to search (e.g., *.example.com/*): ")
        
        # Search Wayback Archive
        urls = self.search_wayback_archive(url_pattern)
        
        # Write all URLs to output file
        output_file = "output.txt"
        with open(output_file, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        
        self.console.print(f"\n[bold green]Total URLs found: {len(urls)}[/bold green]")
        self.console.print(f"[bold green]URLs have been saved to {output_file}[/bold green]")
        
        # Ask if user wants to scan for sensitive content
        scan_choice = input("\nDo you want to scan for sensitive content? (y/n): ").lower()
        if scan_choice == 'y':
            self.process_urls(urls)

def main():
    scanner = WaybackScanner()
    scanner.run()

if __name__ == "__main__":
    main()
