# Импорт библиотек
from yt_dlp import YoutubeDL
import importlib.util
import subprocess
import sys
import re
import ctypes
#from pytube import *
#from pytubefix import *
import os
import tkinter as tk
from tkinter import PhotoImage, filedialog, messagebox

# Функция для установки и проверки пакетов
def install_package(package_name):
    if importlib.util.find_spec(package_name) is None:
        print(f'Устанавливаю {package_name}...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
    else:
        print(f'{package_name} уже установлен.')

# Проверяем и устанавливаем необходимые библиотеки
#install_package('pytubefix')
#install_package('pytube')
install_package('spotdl')
install_package('yt-dlp')
install_package('tkinter')
install_package('ctypes')

# Функция для скачивания видео с Youtube
def youtube_download():
    url = url_entry.get()
    res = resolution_entry.get()
    if not res:
        messagebox.showerror("Ошибка", "Введите качество видео!")
        return
    if not url:
        messagebox.showerror("Ошибка", "Введите URL видео!")
        return
    try:
        ydl_opts = {
            "format": f"bestvideo[height<={res}]+bestaudio/best",  # Скачиваем лучшее видео и аудио
            'outtmpl': 'videos/%(title)s.%(ext)s',  # Название файла
            'quiet': True,  # Отключаем вывод в консоль
            'no_warnings': True,  # Отключаем предупреждения
            'merge_output_format': 'mp4',  # Объединяем видео и аудио в MP4
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Успех", f"Видео загружено с качеством {res}!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить видео: {e}")


# Функция для конвертации аудиофайла
def converter():
    path = filedialog.askopenfilename(title="Выберите MP4 файл", filetypes=[("MP4 файлы", "*.mp4")])
    if not path:
        messagebox.showerror("Ошибка", "Выберите путь к файлу!")
        return
    try:
        output_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF файлы", "*.gif")])
        if not output_path:
            return
        
        # Команда для конвертации MP4 в GIF через ffmpeg
        # command = [
        #     "ffmpeg",
        #     "-i", path,          # Входной файл
        #     "-vf", "fps=20,scale=640:-1:flags=lanczos",  # Частота кадров и масштабирование
        #     "-c:v", "gif",       # Кодек для GIF
        #     output_path          # Выходной файл
        # ] 
        first_command = [
            "ffmpeg", "-i", path, "-filter_complex", "[0:v] palettegen", 'palette.png'
        ] 
        second_command = [
            "ffmpeg", "-i", path, "-i", 'palette.png', "-filter_complex", "[0:v] fps=30,scale=650:-1 [new];[new][1:v] paletteuse", output_path
        ] 
        # ffmpeg -i path.mp4 -filter_complex "[0:v] palettegen" palette.png
        # ffmpeg -i path.mp4 -i palette.png -filter_complex "[0:v] fps=30,scale=650:-1 [new];[new][1:v] paletteuse" output_trimmed.gif
        
        # Выполняем команду
        subprocess.run(first_command, check=True)
        subprocess.run(second_command, check=True)
        messagebox.showinfo("Успех", f"Файл успешно конвертирован в {output_path}!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Не удалось конвертировать файл: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для скачивания песни с Spotify (не работает в России)
def spotdl_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Ошибка", "Введите URL песни!")
        return
    try:
        os.popen(f"spotdl {url}")
        messagebox.showinfo("Успех", "Песня загружена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить песню: {e}")


# Создание графического интерфейса
root = tk.Tk()
root.title("Rendix")
icon = PhotoImage(file = "favicon.png")
root.iconphoto(True, icon)
root.geometry('600x300')
root.minsize(500,400)
root.attributes("-alpha", 0.9)
#root.resizable(False, False)

# Установка иконки для панели задач (только для Windows)
app_id = "mycompany.myapp.converter"  # Уникальный идентификатор приложения
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

# Стили
header_font = ("Arial", 16, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Заголовок
header = tk.Label(root, text="Downloader", font=header_font, fg="White", bg="black")
header.pack(pady=10)

# Поле для ввода URL
url_frame = tk.Frame(root, bg="black")
url_frame.pack(pady=10)
tk.Label(url_frame, text="Введите URL:", font=label_font, fg="White", bg="black").grid(row=0, column=0, padx=5)
url_entry = tk.Entry(url_frame, width=40)
url_entry.grid(row=0, column=1, padx=5)
url_entry.focus()  # Устанавливаем фокус на поле ввода

# Поле для ввода качества видео
resolution_frame = tk.Frame(root, bg="black")
resolution_frame.pack(pady=10)
tk.Label(resolution_frame, text="Введите качество видео, например 1080:", font=label_font, fg="White", bg="black").grid(row=0, column=0, padx=5)
resolution_entry = tk.Entry(resolution_frame, width=40)
resolution_entry.grid(row=0, column=1, padx=5)
resolution_entry.focus()  # Устанавливаем фокус на поле ввода

# Кнопки для действий
button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Скачать видео с YouTube", font=button_font, command=youtube_download, bg="IndianRed1").grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Скачать песню с Spotify", font=button_font, command=spotdl_download, bg="lightgreen").grid(row=0, column=1, padx=10, pady=5)

# Кнопка для конвертации
tk.Button(root, text="Конвертировать mp4 в GIF", font=button_font, command=converter, bg="lightyellow").pack(pady=10)

# Цвета
root["bg"] = "black"
# header["bg"] = "black"
# url_frame["bg"] = "black"
# button_frame["bg"] = "black"
# format_frame["bg"] = "black"

# Запуск приложения
root.mainloop()