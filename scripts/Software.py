import win32service
import win32serviceutil
import winreg
import json
import pythoncom

def get_services():
    services = []
    try:
        # COM'u başlat
        pythoncom.CoInitialize()
        
        # SCManager sadece bir kez açılır
        service_manager = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ENUMERATE_SERVICE)
        # Servis bilgilerini tek seferde almak
        service_statuses = win32service.EnumServicesStatus(service_manager)

        status_mapping = {
            win32service.SERVICE_STOPPED: "Stopped",
            win32service.SERVICE_START_PENDING: "Start Pending",
            win32service.SERVICE_STOP_PENDING: "Stop Pending",
            win32service.SERVICE_RUNNING: "Running",
            win32service.SERVICE_CONTINUE_PENDING: "Continue Pending",
            win32service.SERVICE_PAUSE_PENDING: "Pause Pending",
            win32service.SERVICE_PAUSED: "Paused",
        }

        for service in service_statuses:
            service_name = service[0]
            display_name = service[1]

            try:
                service_status = win32serviceutil.QueryServiceStatus(service_name)[1]
                service_details = win32service.QueryServiceStatusEx(
                    win32service.OpenService(service_manager, service_name, win32service.SERVICE_QUERY_STATUS)
                )
                pid = service_details['ProcessId']
            except Exception:
                service_status = win32service.SERVICE_STOPPED
                pid = "N/A"

            status = status_mapping.get(service_status, "Unknown")

            services.append({
                "ServiceName": service_name,
                "PID": pid,
                "Description": display_name,
                "Status": status
            })

    except Exception as e:
        print(f"Error getting services: {str(e)}")
        return []
    finally:
        pythoncom.CoUninitialize()

    return services

def get_installed_programs():
    programs = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in registry_paths:
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(0, winreg.QueryInfoKey(registry_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(registry_key, i)
                    subkey = winreg.OpenKey(registry_key, subkey_name)
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    publisher = winreg.QueryValueEx(subkey, "Publisher")[0]

                    try:
                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                    except WindowsError:
                        install_location = "N/A"

                    programs.append({
                        'Program': display_name,
                        'Version': display_version,
                        'Publisher': publisher,
                        'InstallLocation': install_location
                    })
                except WindowsError:
                    pass
        except WindowsError:
            pass

    return programs