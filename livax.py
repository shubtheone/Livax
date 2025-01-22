#!/usr/bin/env python3

import argparse
import requests
import concurrent.futures
import sys
import os
from datetime import datetime
from urllib.parse import urlparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.panel import Panel
from rich.text import Text

class WaybackScanner:
    def __init__(self):
        self.console = Console()
        self.base_url = "https://web.archive.org/cdx/search/cdx"
        self.session = requests.Session()
        self.results = []

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

    def show_help(self):
        help_text = """
[bold white]Usage:[/bold white]
  livax.py -u <target> [options]

[bold white]Options:[/bold white]
  -u, --url         Target URL (e.g., example.com)
  -o, --output      Save results to file
  -t, --threads     Number of threads (default: 10)
  -v, --verbose     Show detailed output
  --sensitive-only  Only show sensitive content
  --file-types      Specific file types to search (default: pdf,doc,etc)
  --timeout         Request timeout in seconds (default: 30)
  --exclude         Exclude URLs matching patterns

[bold white]Examples:[/bold white]
  livax.py -u example.com
  livax.py -u example.com -o results.txt
  livax.py -u example.com -t 20 --sensitive-only
  livax.py -u example.com --file-types pdf,doc,xls

[bold white]Note:[/bold white]
  Use -h or --help for more detailed information
"""
        self.console.print(help_text)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', '--help', action='store_true')
        parser.add_argument('-u', '--url')
        parser.add_argument('-o', '--output')
        parser.add_argument('-t', '--threads', type=int, default=10)
        parser.add_argument('--file-types', default='pdf,doc,docx,xls,xlsx,txt,sql,config,env,backup')
        parser.add_argument('--sensitive-only', action='store_true')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('--timeout', type=int, default=30)
        parser.add_argument('--exclude')
        
        args, unknown = parser.parse_known_args()
        return args

    # ... [rest of the class methods remain the same] ...

    def run(self):
        self.print_banner()
        args = self.parse_arguments()

        # Show help menu if no arguments or help flag
        if len(sys.argv) == 1 or args.help:
            self.show_help()
            return

        # Check if URL is provided
        if not args.url:
            self.console.print("[red]Error: URL is required (-u or --url)[/red]")
            self.show_help()
            return

        # ... [rest of the run method remains the same] ...

if __name__ == "__main__":
    try:
        scanner = WaybackScanner()
        scanner.run()
    except KeyboardInterrupt:
        print("\n[yellow]Scan interrupted by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)