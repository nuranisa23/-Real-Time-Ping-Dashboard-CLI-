import os
import platform
import re
import time
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Daftar host yang dipantau
hosts = [
    "8.8.8.8",          # Google DNS
    "1.1.1.1",          # Cloudflare DNS
    "google.com",       # Google Website
    "facebook.com",     # Facebook
    "github.com",       # GitHub
    "bing.com"          # Bing
]

# Tentukan parameter ping berdasarkan OS
param = "-n" if platform.system().lower() == "windows" else "-c"

def ping_host(host):
    """Melakukan ping ke host dan mengembalikan status & latency."""
    response = os.popen(f"ping {param} 1 {host}").read()
    if "ttl" in response.lower():
        match = re.search(r"time[=<]([\d\.]+)", response)
        latency = match.group(1) + " ms" if match else "unknown"
        return True, latency
    return False, "-"

def show_dashboard(results):
    """Menampilkan dashboard dengan warna dan ringkasan status."""
    os.system("clear" if platform.system() != "Windows" else "cls")
    print(Fore.CYAN + "===== 🌐 REAL-TIME PING DASHBOARD =====" + Style.RESET_ALL)
    print(f"{'HOST':<20}{'STATUS':<10}{'LATENCY':<10}")
    print("-" * 45)

    up_count = 0
    down_count = 0

    for host, (status, latency) in results.items():
        if status:
            print(f"{host:<20}{Fore.GREEN}UP{Style.RESET_ALL:<10}{latency:<10}")
            up_count += 1
        else:
            print(f"{host:<20}{Fore.RED}DOWN{Style.RESET_ALL:<10}{latency:<10}")
            down_count += 1

    print("-" * 45)
    print(Fore.YELLOW + f"Total Host: {len(results)} | UP: {up_count} | DOWN: {down_count}" + Style.RESET_ALL)
    print("Update:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 45)

def main():
    print("Tekan Ctrl + C untuk menghentikan program.\n")
    time.sleep(1)

    try:
        while True:
            results = {}
            for host in hosts:
                status, latency = ping_host(host)
                results[host] = (status, latency)
            show_dashboard(results)
            time.sleep(2)  # refresh tiap 2 detik
    except KeyboardInterrupt:
        print("\nMonitoring dihentikan.")

if __name__ == "__main__":
    main()
