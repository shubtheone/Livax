Livax - Wayback Machine Content Scanner (by shubtheone)
Livax is an advanced Python-based tool designed to extract and analyze archived web content from the Wayback Machine, helping security researchers, penetration testers, and developers identify sensitive information leaks, outdated files, and potential vulnerabilities.

Features
Multithreaded Scanning: Speed up the process with concurrent requests.
Custom File Type Search: Target specific file extensions like pdf, doc, txt, sql, env, etc.
Sensitive Content Detection: Option to filter and highlight sensitive files automatically.
Exclusion Filters: Avoid scanning unnecessary URLs with pattern-based exclusions.
Timeout Handling: Configure request timeouts for better control.
User-Friendly Interface: Rich CLI output with a beautiful banner and progress bars.
Verbose Mode: Provides detailed logging and insights into the scanning process.
Save Results: Option to save output to a file for later analysis.


Requirements:
pip3 install requests rich

Installation:

git clone https://github.com/shubtheone/livax.git
cd livax
pip install -r requirements.txt
