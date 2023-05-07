import tkinter as tk
import subprocess
import ctypes

try:
    import wmi
except ImportError:
    wmi = None
    
# Получение текущей яркости экрана
if wmi is not None:
    current_brightness = [x.CurrentBrightness for x in wmi.WMI(namespace='root/WMI').WmiMonitorBrightness()][0]

# Установка яркости экрана на ноль
subprocess.run(["powershell.exe", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,0)"])

# Блокировка поворота экрана
ctypes.windll.user32.SetDisplayAutoRotationPreferences(1, 0)
# Создание главного окна
root = tk.Tk()
root.withdraw()

# Создание и настройка прозрачного окна
window = tk.Toplevel(root)
window.attributes("-alpha", 1.0)
window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+500+500")
window.attributes("-fullscreen", True)
window.attributes("-topmost", True)
window.configure(bg="black")

# Ожидание нажатия на кнопку громкости звука
def check_volume(event):
    if event.keysym in ("XF86AudioRaiseVolume", "XF86AudioLowerVolume"):
        # Восстановление яркости экрана и разблокировка поворота экрана
        if wmi is not None:
            subprocess.run(["powershell.exe", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{current_brightness})"])
        ctypes.windll.user32.SetDisplayAutoRotationPreferences(1, 1)
        root.destroy()
    
window.bind("<KeyPress>", check_volume)

# Запуск главного цикла окна
window.mainloop()
