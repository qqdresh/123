import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import datetime
import os

class MathApp:
    def __init__(self):
        # Первое окно - ввод имени
        self.window1 = tk.Tk()
        self.window1.title("Вход")
        self.window1.geometry("300x150")
        
        tk.Label(self.window1, text="Введите ваше имя:", font=("Arial", 12)).pack(pady=10)
        self.name_entry = tk.Entry(self.window1, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        self.name_entry.bind('<Return>', lambda e: self.start_app())
        
        tk.Button(self.window1, text="Начать", command=self.start_app, font=("Arial", 10)).pack(pady=10)
        
        self.window1.mainloop()
    
    def start_app(self):
        self.username = self.name_entry.get().strip()
        if not self.username:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите имя!")
            return
        
        self.window1.destroy()  # Закрываем окно ввода
        
        # Второе окно - основное с примерами
        self.window2 = tk.Tk()
        self.window2.title("Математические примеры")
        self.window2.geometry("500x400")
        
        # Третье окно - лог
        self.window3 = tk.Tk()
        self.window3.title("История результатов")
        self.window3.geometry("400x300")
        
        # Настройка окна с логом
        self.log_text = scrolledtext.ScrolledText(self.window3, wrap=tk.WORD, width=50, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Загружаем историю из файла
        self.load_log()
        
        # Основное окно
        self.operation = tk.StringVar(value="*")  # * или /
        self.current_answer = None
        
        tk.Label(self.window2, text=f"Привет, {self.username}!", font=("Arial", 14)).pack(pady=10)
        
        # Выбор операции
        frame_choice = tk.Frame(self.window2)
        frame_choice.pack(pady=10)
        tk.Label(frame_choice, text="Выберите операцию:", font=("Arial", 11)).pack(side=tk.LEFT)
        tk.Radiobutton(frame_choice, text="Умножение (×)", variable=self.operation, value="*", command=self.new_example).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_choice, text="Деление (÷)", variable=self.operation, value="/", command=self.new_example).pack(side=tk.LEFT, padx=5)
        
        # Пример
        self.example_label = tk.Label(self.window2, text="", font=("Arial", 20, "bold"))
        self.example_label.pack(pady=20)
        
        # Поле для ответа
        self.answer_entry = tk.Entry(self.window2, font=("Arial", 14), justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # Кнопка проверки
        tk.Button(self.window2, text="Проверить", command=self.check_answer, font=("Arial", 12), bg="lightblue").pack(pady=5)
        
        # Кнопка нового примера
        tk.Button(self.window2, text="Новый пример", command=self.new_example, font=("Arial", 10)).pack(pady=5)
        
        # Статус
        self.status_label = tk.Label(self.window2, text="Введите ответ и нажмите Enter", font=("Arial", 10), fg="gray")
        self.status_label.pack(pady=10)
        
        # Генерируем первый пример
        self.new_example()
        
        self.window2.mainloop()
    
    def generate_example(self):
        """Генерирует пример в зависимости от выбранной операции"""
        if self.operation.get() == "*":
            self.num1 = random.randint(2, 9)
            self.num2 = random.randint(2, 9)
            self.correct_answer = self.num1 * self.num2
            return f"{self.num1} × {self.num2} = ?"
        else:  # деление
            self.num2 = random.randint(2, 9)
            self.correct_answer = random.randint(2, 9)
            self.num1 = self.num2 * self.correct_answer
            return f"{self.num1} ÷ {self.num2} = ?"
    
    def new_example(self):
        """Обновляет пример"""
        self.example_label.config(text=self.generate_example())
        self.answer_entry.delete(0, tk.END)
        self.status_label.config(text="Введите ответ и нажмите Enter", fg="gray")
        self.answer_entry.focus()
    
    def check_answer(self):
        """Проверяет ответ пользователя"""
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.status_label.config(text="✓ Правильно! Отлично!", fg="green")
                result_text = f"✓ {self.example_label.cget('text')} {user_answer} (верно)"
            else:
                self.status_label.config(text=f"✗ Неправильно. Правильно: {self.correct_answer}", fg="red")
                result_text = f"✗ {self.example_label.cget('text')} {user_answer} (ошибка, правильно: {self.correct_answer})"
            
            # Сохраняем в лог
            self.save_to_log(result_text)
            self.update_log_display(result_text)
            
            # Автоматически генерируем новый пример через 1.5 секунды
            self.answer_entry.config(state="disabled")
            self.window2.after(1500, self.enable_and_next)
            
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите число!")
    
    def enable_and_next(self):
        """Включает поле ввода и генерирует новый пример"""
        self.answer_entry.config(state="normal")
        self.new_example()
    
    def save_to_log(self, result):
        """Сохраняет результат в файл log.txt"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {self.username}: {result}\n")
    
    def load_log(self):
        """Загружает и отображает историю из log.txt"""
        if os.path.exists("log.txt"):
            with open("log.txt", "r", encoding="utf-8") as f:
                content = f.read()
                self.log_text.insert(tk.END, content)
        else:
            self.log_text.insert(tk.END, "История пуста. Решайте примеры!\n")
        self.log_text.see(tk.END)
    
    def update_log_display(self, new_entry):
        """Обновляет отображение в окне лога"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {self.username}: {new_entry}\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    app = MathApp()
