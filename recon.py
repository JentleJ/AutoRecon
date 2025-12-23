
import sys
import os
import subprocess
import argparse
from datetime import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# สีสันเพื่อให้ Output ดู Pro (Ansi Escape Codes)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, type="INFO"):
    """
    Helper function เพื่อ print ข้อความสวยๆ
    Type: INFO, SUCCESS, ERROR
    """
    if type == "INFO":
        print(f"{Colors.BLUE}[*] {message}{Colors.ENDC}")
    elif type == "SUCCESS":
        print(f"{Colors.GREEN}[+] {message}{Colors.ENDC}")
    elif type == "ERROR":
        print(f"{Colors.FAIL}[!] {message}{Colors.ENDC}")
        
def take_screenshot(url, output_path):
    print_status(f"Taking screenshot of {url}...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"
    
    driver = None
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(15)
        driver.get(url)
        time.sleep(2)  # รอให้หน้าโหลด
        driver.save_screenshot(output_path)
        print_status(f"Screenshot saved to {output_path}", "SUCCESS")
    except Exception as e:
        print_status(f"Failed to take screenshot of {url}: {e}", "ERROR")
    finally:
        if driver:
            driver.quit()

def get_arguments():
    """
    ส่วนรับค่า Argument จาก user
    เช่น python3 recon.py -t 192.168.1.1 -o my_scan
    """
    parser = argparse.ArgumentParser(description="Automated Recon Tool for 0.01% Pentester")
    parser.add_argument("-t", "--target", dest="target", help="Target IP or Domain", required=True)
    parser.add_argument("-o", "--output", dest="output_dir", help="Output Directory Name", required=False)
    # มึงอาจจะเพิ่ม flag -q (quiet) หรือ -v (verbose) ทีหลังก็ได้
    return parser.parse_args()

# --- Main Execution Block ---
if __name__ == "__main__":
    args = get_arguments()
    
    # ดึงค่ามาใช้
    target = args.target
    # ถ้า user ไม่ตั้งชื่อ output folder ให้ใช้ชื่อ target เป็นชื่อ folder
    output_folder = args.output_dir if args.output_dir else target
    
    # --- เริ่ม Logic ของมึงตรงนี้ ---
    print(f"{Colors.HEADER}--- Starting Recon on {target} ---{Colors.ENDC}")
    
    is_alive = subprocess.call(["ping", "-c", "1", args.target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if is_alive == 0:
        print_status(f"Target {target} is alive. Proceeding with scans.", "SUCCESS")
    else:
        print_status(f"Target {target} is not reachable. Exiting.", "ERROR")
        sys.exit(1)
        
    if os.path.exists(output_folder):
        print_status(f"Output directory '{output_folder}' already exists. Exiting to prevent overwrite.", "ERROR")
        sys.exit(1)
    else:
        os.makedirs(output_folder)
        print_status(f"Created output directory: {output_folder}", "SUCCESS")
    
    # ตัวอย่างการรัน nmap scan
    output_file = os.path.join(output_folder, "nmap_scan")
    
    print_status(f"Running nmap scan on {target}...")
    nmap_command = ["nmap", "-sS", "-sV", "-oA", output_file, target]
    
    try:
        subprocess.run(nmap_command, check=True)
        print_status(f"Nmap scan completed. Results saved in {output_folder}", "SUCCESS")
    except subprocess.CalledProcessError as e:
        print_status(f"Nmap scan failed: {e}", "ERROR")
        sys.exit(1)
    
    # check open ports from nmap output
    nmap_grepable = f"{output_file}.gnmap"
    web_ports = []
    
    if os.path.exists(nmap_grepable):
        with open(nmap_grepable, 'r') as f:
            content = f.read()
            if "80/open" in content:
                web_ports.append("http")
            if "443/open" in content:
                web_ports.append("https")
    else:
        print_status(f"Nmap grepable output not found: {nmap_grepable}", "ERROR")
        sys.exit(1)
    

    if web_ports:    
        # Gobuster
        wordlist_path = "/usr/share/wordlists/dirb/common.txt"
        if not os.path.exists(wordlist_path):
             print_status(f"Wordlist not found at {wordlist_path}. Skipping Gobuster.", "ERROR")
        for proto in web_ports:
            base_url = f"{proto}://{target}"
            print(f"\n{Colors.HEADER}--- Processing {base_url} ---{Colors.ENDC}")
            
            screenshot_filename = f"screenshot_{proto}.png"
            screenshot_path = os.path.join(output_folder, screenshot_filename)
            take_screenshot(base_url, screenshot_path)
            
            print_status(f"Running Gobuster on {target}...")
            gobuster_output = os.path.join(output_folder, f"gobuster_{proto}.txt")
            gobuster_command = ["gobuster", "dir", "-u", base_url, "-w", wordlist_path, "-o", gobuster_output, "-k"]
        
            try:
                subprocess.run(gobuster_command, check=True)
                print_status(f"Gobuster scan completed. Results saved in {gobuster_output}", "SUCCESS")
            except subprocess.CalledProcessError as e:
                print_status(f"Gobuster scan failed: {e}", "ERROR")
                
    else:
        print_status(f"No web ports found on {target}. Skipping Gobuster scan.", "INFO")
        
    
    
print(f"{Colors.HEADER}--- Recon Completed on {target} ---{Colors.ENDC}")
