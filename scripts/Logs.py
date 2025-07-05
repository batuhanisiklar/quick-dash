import win32evtlog
from datetime import datetime
import asyncio
import json

def get_system_logs():
    logs = []
    server = None
    log_type = "System"

    level_mapping = {
        1: "Critical", 
        2: "Error",
        3: "Warning",
        4: "Information",
        5: "Audit Success",
        6: "Audit Failure"
    }

    try:
        log_handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_records = win32evtlog.GetNumberOfEventLogRecords(log_handle)

        while True:
            events = win32evtlog.ReadEventLog(log_handle, flags, 0)
            if not events:
                break

            for event in events:
                level = level_mapping.get(event.EventType, "Unknown")

                parsed_time = datetime.strptime(event.TimeGenerated.Format(), "%a %b %d %H:%M:%S %Y")
                formatted_time = parsed_time.strftime("%d-%m-%Y %H:%M:%S")

                logs.append({
                    "SourceName": event.SourceName,
                    "EventID": event.EventID & 0xFFFF,
                    "Level": level,
                    "TimeGenerated": formatted_time
                })

    except Exception as e:
        print(f"Olayları çekerken hata oluştu: {e}")
    finally:
        if 'log_handle' in locals():
            win32evtlog.CloseEventLog(log_handle)

    return logs

def get_application_logs():
    logs = []
    server = None
    log_type = "Application"

    level_mapping = {
        1: "Critical",
        2: "Error", 
        3: "Warning",
        4: "Information",
        5: "Audit Success",
        6: "Audit Failure"
    }

    try:
        log_handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_records = win32evtlog.GetNumberOfEventLogRecords(log_handle)

        while True:
            events = win32evtlog.ReadEventLog(log_handle, flags, 0)
            if not events:
                break

            for event in events:
                level = level_mapping.get(event.EventType, "Unknown")

                parsed_time = datetime.strptime(event.TimeGenerated.Format(),
                                                "%a %b %d %H:%M:%S %Y")
                formatted_time = parsed_time.strftime("%d-%m-%Y %H:%M:%S")

                logs.append({
                    "SourceName": event.SourceName,
                    "EventID": event.EventID & 0xFFFF,
                    "Level": level,
                    "TimeGenerated": formatted_time
                })

    except Exception as e:
        print(f"Olayları çekerken hata oluştu: {e}")
    finally:
        if 'log_handle' in locals():
            win32evtlog.CloseEventLog(log_handle)

    return logs

def get_security_logs():
    logs = []
    server = None
    log_type = "Security"

    try:
        log_handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_records = win32evtlog.GetNumberOfEventLogRecords(log_handle)

        while True:
            events = win32evtlog.ReadEventLog(log_handle, flags, 0)
            if not events:
                break

            for event in events:
                date_time = event.TimeGenerated.Format()
                date_time = datetime.strptime(date_time, "%a %b %d %H:%M:%S %Y")
                formatted_time = date_time.strftime("%d-%m-%Y %H:%M:%S")

                logs.append({
                    "EventID": event.EventID & 0xFFFF,
                    "EventType": event.EventType,
                    "TimeGenerated": formatted_time,
                    "Message": event.StringInserts
                })

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'log_handle' in locals():
            win32evtlog.CloseEventLog(log_handle)

    return logs