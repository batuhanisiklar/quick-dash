import subprocess
import json
import re

def get_network_info():
    network_info = []

    try:
        # 'ipconfig' komutunu çalıştırarak ağ bilgilerini alalım
        result = subprocess.run("ipconfig /all", capture_output=True, encoding='cp437', shell=True)
        
        if result.stdout is None:
            return network_info

        # ipconfig çıktısını satırlara ayıralım
        output = result.stdout.splitlines()

        interface = None
        for line in output:
            # IP adresini ve MAC adresini bulmak için
            if "Ethernet adapter" in line or "Wireless LAN adapter" in line:
                interface = line.strip().replace("adapter", "").strip()  # Arayüz ismini al
                network_info.append({"Interface": interface, "IP_Address": "N/A", "MAC_Address": "N/A"})

            elif "IPv4 Address" in line and interface:  # Interface geçerli ise IP al
                # IP adresini al
                ip_address = line.split(":")[1].strip()
                for item in network_info:
                    if item["Interface"] == interface:
                        item["IP_Address"] = ip_address

            elif "Physical Address" in line and interface:  # Interface geçerli ise MAC al
                # MAC adresini al
                mac_address = line.split(":")[1].strip()
                for item in network_info:
                    if item["Interface"] == interface:
                        item["MAC_Address"] = mac_address

    except Exception as e:
        print(f"Network info error: {str(e)}")
        return network_info

    return network_info


def get_program_names_from_tasklist():
    """Tasklist komutunu çalıştırarak çalışan programların PID ve isim eşleştirmesini döndürür"""
    try:
        result = subprocess.run(['tasklist'], capture_output=True, encoding='cp437')
        program_map = {}

        if result.stdout is None:
            return program_map

        for line in result.stdout.splitlines()[3:]:  # Başlık satırlarını atla
            if not line:
                continue

            program_name = line[:25].strip()
            pid = line[26:35].strip()

            if pid.isdigit():
                program_map[pid] = program_name

    except Exception as e:
        print(f"Error getting program names: {str(e)}")
        return {}

    return program_map


def parse_netstat_line(line, program_map):
    """Netstat çıktısındaki tek bir satırı ayrıştırır ve sözlük olarak döndürür"""
    pid_match = re.search(r'\d+$', line.strip())
    if not pid_match:
        return None

    pid = pid_match.group()
    program_name = program_map.get(pid, "Unknown")
    parts = re.split(r'\s+', line.strip())

    if len(parts) < 4:
        return None

    return {
        "Proto": parts[0],
        "Local_Address": parts[1],
        "Foreign_Address": parts[2],
        "State": parts[3] if len(parts) > 4 else "",
        "PID": pid,
        "Program_Name": program_name
    }


def get_netstat_data():
    try:
        result = subprocess.run(['netstat', '-anob'], capture_output=True, encoding='cp437')
        if result.stdout is None:
            return ""
        return result.stdout
    except Exception as e:
        print(f"Error getting netstat data: {str(e)}")
        return ""


def get_port_info():
    program_map = get_program_names_from_tasklist()
    netstat_data = get_netstat_data()
    port_info = []

    for line in netstat_data.splitlines():
        if not line or "Active Connections" in line:
            continue

        parsed_line = parse_netstat_line(line, program_map)
        if parsed_line:
            port_info.append(parsed_line)

    return port_info