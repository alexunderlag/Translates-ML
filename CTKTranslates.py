import customtkinter as ctk
from tkinter import Text, END, messagebox, StringVar
import requests

# Настройка окна приложения
root = ctk.CTk()
root.title ("Переводчик")


# Загрузите токенизатор и модель для работы оффлайн

current_language = StringVar(value="ru-en")

def translate():
    try:
        text = text_to_translate.get("1.0", END)
        language = current_language.get()
        
        # Отправка запроса на сервер
        response = requests.post("http://77.73.68.140:5000/translate", json={"text": text, "lang": language})
        data = response.json()
        
        translated_text_display.delete("1.0", END)
        translated_text_display.insert(END, data["translation"])
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создаем пользовательский интерфейс
input_frame = ctk.CTkFrame(root, corner_radius=10)
input_frame.pack(pady=20, padx=20)

ctk.CTkLabel(input_frame, text="Введите текст для перевода:", font=("Arial", 12)).pack(pady=(0, 10))
text_to_translate = Text(input_frame, height=10, width=50, bd=0, highlightthickness=0)
text_to_translate.pack()



output_frame = ctk.CTkFrame(root, corner_radius=10)
output_frame.pack(pady=(0, 20), padx=20)

ctk.CTkLabel(output_frame, text="Перевод:", font=("Arial", 12)).pack(pady=(0, 10))
translated_text_display = Text(output_frame, height=10, width=50, bd=0, highlightthickness=0)
translated_text_display.pack()
# Создание интерфейса для переключения языка перевода

language_frame = ctk.CTkFrame(root, corner_radius=10)
language_frame.pack(pady=(0, 0), padx=15, ipadx=10)

button = ctk.CTkRadioButton(language_frame, text="Русский -> Английский", variable=current_language, value="ru-en").pack(side="left")
ctk.CTkRadioButton(language_frame, text="Английский -> Русский", variable=current_language, value="en-ru").pack(side="right")

translate_button = ctk.CTkButton(root, text="Перевести", command=translate, corner_radius=10, width=100)
translate_button.pack(pady=20,side="right", padx=20)

# Запускаем главное окно приложения
root.mainloop()