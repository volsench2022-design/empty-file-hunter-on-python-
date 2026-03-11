# Імпортуємо модуль os для роботи з файлами, папками та шляхами.
from importlib.resources import files, path
from logging import root
import os
# Імпортуємо shutil для видалення директорій.
import shutil
# Імпортуємо tkinter як tk для змінних інтерфейсу (StringVar).
import tkinter as tk
# Імпортуємо готові діалоги: вибір папки та повідомлення.
from tkinter import filedialog, messagebox
from unittest import result

# Імпортуємо modern GUI-бібліотеку customtkinter.
import customtkinter as ctk

class EmptyFileHunterApp(ctk.CTk):
    IGNORED_DIRS = {"$RECYCLE.BIN", "System Volume Information"}
    def __init__(self):
        super().__init__()
        self.title("Empty File Hunter")
        self.geometry("760x520")
        self.selected_path = ""
        # Створюємо інтерфейс користувача
        self._build_ui()
        # Створення і розміщення віджетів у вікні.
    def _build_ui(self):
        # Дозволяємо головному стовпцю розтягуватись по ширині.
        self.grid_columnconfigure(0, weight=1)
        # Дозволяємо рядку зі списком розтягуватись по висоті.
        self.grid_rowconfigure(2, weight=1)
        # Створюємо заголовок програми.
        title = ctk.CTkLabel(
            self,
            text="Simple Empty Folder Hunter",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        # Розміщуємо заголовок у верхній частині вікна.
        title.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="w")
        
        # Створюємо верхню панель для вибору папки.
        top = ctk.CTkFrame(self)
        # Розміщуємо верхню панель.
        top.grid(row=1, column=0, padx=12, pady=6, sticky="ew")
        # Дозволяємо полю шляху розтягуватись.
        top.grid_columnconfigure(1, weight=1)
        
        # Кнопка вибору папки.
        select_btn = ctk.CTkButton(top, text="Select Folder", command=self.select_folder)
        # Розміщуємо кнопку на панелі.
        select_btn.grid(row=0, column=0, padx=8, pady=8)
        
        # Створюємо змінну для тексту шляху.
        self.path_var = tk.StringVar(value="Оберіть папку для сканування")
        # Створюємо поле для відображення вибраного шляху.
        path_entry = ctk.CTkEntry(top, textvariable=self.path_var)
        # Розміщуємо поле праворуч від кнопки.
        path_entry.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="ew")
        
        # Створюємо текстове поле для показу результатів.
        self.results_box = ctk.CTkTextbox(self)
        # Розміщуємо поле в центральній частині вікна.
        self.results_box.grid(row=2, column=0, padx=12, pady=6, sticky="nsew")
        # Показуємо стартовий підказуючий текст.
        self.results_box.insert("1.0", "Тут з'являться знайдені порожні папки ... ")
        # Робимо поле тільки для читання (щоб користувач не редагував текст).
        self.results_box. configure(state="disabled")
        
        # Створюємо нижню панель з кнопками дій.
        bottom = ctk.CTkFrame(self)
        # Розміщуємо нижню панель.
        bottom.grid(row=3, column=0, padx=12, pady=(6, 12), sticky="ew")
        # Дозволяємо комірці статусу займати вільне місце.
        bottom.grid_columnconfigure(2, weight=1)

        # Кнопка запуску сканування.
        scan_btn = ctk. CTkButton(
            bottom,
            text="Scan",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.scan,
        )
        # Розміщуємо кнопку Scan.
        scan_btn.grid(row=0, column=0, padx=(8, 6), pady=8)

        # Кнопка видалення знайдених порожніх папок.
        clean_btn = ctk. CTkButton(
            bottom,
            text="Clean All",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.clean_all,
        )
        # Розміщуємо кнопку Clean All.
        clean_btn.grid(row=0, column=1, padx=(0, 8), pady=8)

        # (Duplicate placement removed)
        # Створюємо змінну для статус-бару.
        self.status_var = tk.StringVar(value="Знайдено папок: 0")
        # Створюємо віджет статусного тексту.
        status = ctk.CTkLabel(bottom, textvariable=self.status_var, anchor="w")
        # Розміщуємо статус праворуч.
        status.grid(row=0, column=2, padx=8, pady=8, sticky="ew")

    # Вибір стартової директорії для сканування.
    def select_folder(self):
        # Короткий опис методу.
        """Вибір стартової папки. """
        # Відкриваємо системне вікно вибору директорії.
        folder = filedialog.askdirectory(title="Оберіть папку")
        # Якщо користувач справді вибрав папку.
        if folder:
            
            # Записуємо вибраний шлях у пам'ять програми.
            self.selected_path = folder
            # Оновлюємо поле шляху в інтерфейсі.
            self.path_var.set(folder)
            # Очищаємо старий список знайдених папок.
            self.empty_folders = [ ]
            # Очищаємо/оновлюємо область результатів.
            self._show_results([])
            # Скидаємо лічильник у статусі.
            self.status_var.set("Знайдено папок: 0")
    
    # Пошук порожніх папок рекурсивним обходом.
    def find_empty_folders(self, start_path):
        # Короткий опис методу.
        """Шукає порожні папки (обхід знизу догори)."""
        # Сюди будемо складати знайдені порожні директорії.
        result = [ ]

        # Обходимо всі папки, починаючи з найглибших (topdown=False).
        for root, dirs, files in os.walk(start_path, topdown=False):
            # Беремо тільки назву поточної папки.
            folder_name = os .path. basename (root)
            # Якщо це системна папка - пропускаємо.
            if folder_name in self.IGNORED_DIRS:
                continue

            # Формуємо список підпапок без системних директорій.
            normal_dirs = [d for d in dirs if d not in self. IGNORED_DIRS]
            # Якщо немає файлів і немає звичайних підпапок - папка порожня.
            if not files and not normal_dirs:
                # Додаємо її до результату.
                result.append(root)
        
        # Повертаємо весь список знайдених порожніх папок.
        return result
    # Запуск сканування після натискання кнопки Scan.
    def scan(self):
        # Короткий опис методу.
        """Запуск пошуку порожніх папок."""
        # Якщо папку ще не вибрано - попереджаємо користувача.
        if not self.selected_path:
            messagebox.showwarning("Увага", "Спочатку натисніть Select Folder.")
            return

        # Якщо шлях більше не існує - показуємо помилку.
        if not os.path.isdir(self.selected_path):
            messagebox. showerror("Помилка", "Обрана папка недоступна.")
            return

        # Запускаємо пошук порожніх папок.
        self.empty_folders = self.find_empty_folders(self.selected_path)
        # Показуємо знайдені шляхи в текстовому полі.
        self._show_results(self.empty_folders)
        # Оновлюємо статус із кількістю знайдених папок.
        self.status_var.set(f"Знайдено папок: {len(self.empty_folders)}")
    
    # Видалення всіх знайдених порожніх папок.
    def clean_all(self):
        # Короткий опис методу.
        """Видаляє всі знайдені порожні папки після підтвердження."""
        # Якщо список порожній - видаляти нічого.
        if not self.empty_folders:
            messagebox. showinfo("Інформація", "Немає папок для видалення.")
            return

        # Питаємо підтвердження перед видаленням.
        оk = messagebox.askyesno("Підтвердження", "Видалити всі знайдені порожні папки?")
        # Якщо користувач натиснув "Hi" - перериваємо операцію.
        if not ok:
            return

        # Лічильник успішно видалених папок.
        deleted = 0
        # Проходимо всі знайдені порожні папки.
        for path in self.empty_folders:
            # Пробуємо видалити поточну папку.
            try:
                # Видаляємо директорію.
                shutil.rmtree(path)
                # Якщо все добре - збільшуємо лічильник.
                deleted += 1
            # Якщо папка вже зникла/немає прав/інша ОС-помилка - пропускаємо.
            except (FileNotFoundError, PermissionError, OSError):
                pass

        # Після видалення очищаємо список у пам'яті.
        self.empty_folders = []
        # Оновлюємо текстове поле результатів.
        self._show_results([])
        # Скидаємо статус кількості.
        self.status_var.set("Знайдено папок: 0")
        
        # Показуємо підсумок користувачу.
        messagebox.showinfo("Готово", f"Видалено {deleted} порожніх папок.")

    # Виведення результатів у текстове поле.
    def _show_results(self, paths):
        # Короткий опис методу.
        """Показує результати в текстовому полі."""
        # Тимчасово вмикаємо редагування поля, щоб змінити вміст.
        self.results_box. configure(state="normal")
        # Очищаємо попередній текст повністю.
        self.results_box.delete("1.0", "end")

        # Якщо список непорожній - показуємо всі шляхи построчно.
        if paths:
            self.results_box. insert("end", "\n".join(paths))
        # Якщо порожній - показуємо пояснювальне повідомлення.
        else:
            self.results_box.insert("end", "Порожніх папок не знайдено.")
        
        # Повертаємо режим тільки для читання.
        self.results_box. configure(state="disabled")

# Код нижче виконається лише при прямому запуску цього файлу.
if __name__ == "__main__":
    print("Starting EmptyFileHunterApp...")
    # Увімкнути темний режим інтерфейсу.
    ctk.set_appearance_mode("dark")
    # Увімкнути синю тему віджетів.
    ctk.set_default_color_theme("blue")

    # Створити об'єкт програми.
    app = EmptyFileHunterApp()
    # Запустити нескінченний цикл обробки подій GUI.
    app.mainloop()
    print("Mainloop exited")