import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import base64
from cryptography.fernet import Fernet
import random

filectx = ""

def select_file():
    global file_path, filectx
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.configure(text=file_path)
        try:
            with open(file_path, "r") as okumak:
                filectx = okumak.read()
            print(filectx)
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {e}")

def button_event():
    if filectx: 
        base64ed = base64.b64encode(filectx.encode('utf-8')).decode('utf-8')

        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        encrypted_data = cipher_suite.encrypt(base64ed.encode('utf-8')).decode('utf-8')

        yazmakicinkey = key.decode('utf-8')

        with open("obfuscated_code.py", "w") as obf:
            obf.write(f"""
import base64
from cryptography.fernet import Fernet

cipher_suite = Fernet('{yazmakicinkey}')

encrypted_data = '''{encrypted_data}'''
decrypted_data = cipher_suite.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
original_data = base64.b64decode(decrypted_data).decode('utf-8')

exec(original_data)
""")
        scs_label = ctk.CTkLabel(root, text="obfuscated_code.py'ye kaydedildi!")
        scs_label.place(x=100, y=100)
    else:
        scs_label = ctk.CTkLabel(root, text="Önce bir dosya seçmelisiniz")
        scs_label.place(x=125, y=100)

root = ctk.CTk()
root.geometry("400x120")
builder.title("AylakFUD")
builder.iconbitmap(r"util\favicon.ico")

select_button = ctk.CTkButton(root, text="Dosya Seç", command=select_file)
select_button.place(x=10, y=10)

file_label = ctk.CTkLabel(root, text="Seçilen dosya yolu burada görünecek")
file_label.place(x=160, y=10)

build_button = ctk.CTkButton(root, text="Şifrele!", command=button_event)
build_button.place(x=125, y=70)

root.mainloop()
