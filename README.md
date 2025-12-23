# 🕵️ AutoRecon-X

> An automated reconnaissance tool for modern penetration testers. Built with Python.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)

## 🔥 Why this tool?
I built **AutoRecon** to automate the tedious parts of the initial engagement phase. Instead of manually running Nmap, creating directories, and taking screenshots, this tool handles the workflow automatically, allowing pentesters to focus on analyzing vulnerabilities.

## 🚀 Features
* **Smart Target Check:** Verifies target availability before scanning.
* **Organized Workspace:** Automatically creates structured directories for each target.
* **Nmap Integration:** Performs service version detection (`-sV`) and default script scanning (`-sC`).
* **Intelligent Gobuster:** automatically detects web ports (80/443) and runs directory brute-forcing only when appropriate.
* **Automated Screenshots:** Uses **Selenium (Headless Chrome)** to capture screenshots of discovered web services (HTTP/HTTPS).

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JentleJ/AutoRecon.git
   cd AutoRecon
   ```
2. **Install Python dependencies**
    ```
    pip3 install -r requirements.txt
    ```
3. **System Requirements (Kali Linux recommended)**
    ```
    sudo apt install nmap gobuster chromium chromium-driver
    ```

## Usage
```
# Basic usage
python3 recon.py -t target.com

# Specify output directory
python3 recon.py -t target.com -o my_scan_result
```

## Result
![alt text](<Screenshot 2025-12-23 170516.png>)

---

**⚠️ Disclaimer:**
This tool is for educational purposes and authorized security testing only. I am not responsible for any misuse.