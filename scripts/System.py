import psutil
import GPUtil
import wmi
import platform
from datetime import datetime
import math
import subprocess
import re
import pythoncom

def get_cpu_usage():
    cpu_percent = round(psutil.cpu_percent(interval=1))
    return {
        "cpu": cpu_percent
    }

def get_gpu_usage():
    try:
        pythoncom.CoInitialize()
        w = wmi.WMI(namespace="root\\CIMV2")
        gpu_info = w.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()

        if len(gpu_info) > 0:
            gpu_usage = round(float(gpu_info[0].UtilizationPercentage), 2)
            return {"gpu": gpu_usage}
        else:
            gpus = GPUtil.getGPUs()
            if len(gpus) > 0:
                gpu = gpus[0]
                gpu_usage = round(gpu.load * 100, 2)
                return {"gpu": gpu_usage}
            return {"gpu": 0}

    except Exception as e:
        print(f"GPU usage error: {str(e)}")
        return {"gpu": 0}
    finally:
        pythoncom.CoUninitialize()

def donutChart():
    total_disk_space = 0
    used_disk_space = 0
    for partition in psutil.disk_partitions():
        try:
            disk = psutil.disk_usage(partition.mountpoint)
            total_disk_space += disk.total / (1024 * 1024 * 1024)
            used_disk_space += disk.used / (1024 * 1024 * 1024)
        except:
            continue

    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 * 1024 * 1024)
    memory_available = memory.available / (1024 * 1024 * 1024)

    return {
        "disk": {
            "used": round(used_disk_space, 2),
            "available": round(total_disk_space - used_disk_space, 2)
        },
        "memory": {
            "used": round(memory_used, 2),
            "available": round(memory_available, 2)
        }
    }

def get_connected_bluetooth_devices():
    try:
        result = subprocess.run(['powershell', 'Get-PnpDevice -Class Bluetooth'], capture_output=True, encoding='cp437')
        
        if result.stdout is None:
            return []

        device_list = []
        devices = result.stdout.splitlines()
        
        for device in devices:
            if "Bluetooth" in device and "AVRCP" not in device and "Transport" not in device:
                match = re.search(r"Bluetooth\s+([A-Za-z0-9\s\(\)\-]+)", device)
                if match:
                    device_name = match.group(1).strip()
                    device_name = re.sub(r"\s+(BTH|USB|BTHENUM)[\s\S]*", "", device_name).strip()
                    if device_name:
                        device_list.append({"Type": "Bluetooth", "ID": device_name})
    except Exception as e:
        print(f"Error fetching Bluetooth devices: {str(e)}")
        return []
        
    return device_list

def get_connected_usb_devices():
    try:
        result = subprocess.run(['powershell', 'Get-PnpDevice -Class USB'], capture_output=True, encoding='cp437')
        
        if result.stdout is None:
            return []

        device_list = []
        devices = result.stdout.splitlines()
        device_set = set()
        
        for device in devices:
            parts = device.split(" ", 3)
            if len(parts) > 3:
                device_name = parts[3].strip()
                if device_name.startswith("USB"):
                    device_name = device_name[3:].strip()
                if len(device_name.split("  ")) > 1:
                    device_name = device_name.split("  ")[0]
                if device_name and device_name not in device_set:
                    device_set.add(device_name)
                    device_list.append({"Type": "USB", "ID": device_name})
    except Exception as e:
        print(f"Error fetching USB devices: {str(e)}")
        return []
        
    return device_list

def get_connected_device():
    return get_connected_bluetooth_devices()+get_connected_usb_devices()

def get_system_info():
    try:
        pythoncom.CoInitialize()
        w = wmi.WMI()
        cpu_info = w.Win32_Processor()[0]
        cpu_name = cpu_info.Name.strip()

        os_info = platform.system() + " " + platform.release()
        architecture = platform.machine()
        boot_time = psutil.boot_time()
        uptime = str(datetime.now() - datetime.fromtimestamp(boot_time)).split('.')[0]

        bios = w.Win32_BIOS()[0]
        bios_name = bios.Name.strip()
        bios_version = bios.Version.strip()
        manufacturer = bios.Manufacturer.strip()
        release_date = datetime.strptime(bios.ReleaseDate[:8], '%Y%m%d').strftime('%d/%m/%Y')

        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_name = gpu.name.strip()
            gpu_temp = str(gpu.temperature)
        else:
            gpu_name = "N/A"
            gpu_temp = "N/A"

        total_disk = 0
        for disk in psutil.disk_partitions():
            try:
                total_disk += psutil.disk_usage(disk.mountpoint).total
            except:
                continue
        total_disk_gb = str(total_disk // (1024 ** 3))

        total_ram = math.ceil(psutil.virtual_memory().total / (1024 ** 3))

        return {
            "cpuName": cpu_name,
            "os": os_info,
            "architecture": architecture,
            "uptime": uptime,
            "name": bios_name,
            "biosVersion": bios_version,
            "manufacturer": manufacturer,
            "releaseDate": release_date,
            "gpuName": gpu_name,
            "gpuTemperature": gpu_temp,
            "totalDiskCapacity": total_disk_gb,
            "totalMemoryCapacity": str(total_ram)
        }
    except Exception as e:
        print(f"System info error: {str(e)}")
        return {}
    finally:
        pythoncom.CoUninitialize()