import random
import tkinter as tk
from tkinter import messagebox

class MathMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Master - Тренажёр таблицы умножения")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Переменные для статистики
        self.score = 0
        self.attempts = 0
        self.current_correct = 0
        
        # Настройка цветовой схемы
        self.root.configure(bg='#2C3E50')
        
        # Заголовок
        self.create_header()
        
        # Основной игровой блок
        self.create_game_area()
        
        # Блок статистики
        self.create_stats_area()
        
        # Генерируем первый пример
        self.new_question()
    
    def create_header(self):
        """Создание шапки приложения"""
        header_frame = tk.Frame(self.root, bg='#34495E', height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        title = tk.Label(
            header_frame, 
            text="МАТH MASTER", 
            font=('Arial', 24, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            header_frame,
            text="Тренажёр таблицы умножения",
            font=('Arial', 12),
            fg='#BDC3C7',
            bg='#34495E'
        )
        subtitle.pack()
    
    def create_game_area(self):
        """Создание игровой области"""
        game_frame = tk.Frame(self.root, bg='#2C3E50')
        game_frame.pack(expand=True)
        
        # Вопрос
        self.question_label = tk.Label(
            game_frame,
            text="5 * 7 = ?",
            font=('Arial', 32, 'bold'),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        self.question_label.pack(pady=20)
        
        # Поле для ввода
        self.entry = tk.Entry(
            game_frame,
            font=('Arial', 18),
            width=10,
            justify='center',
            bd=5,
            relief='ridge'
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda event: self.check_answer())
        
        # Кнопка проверки
        self.check_button = tk.Button(
            game_frame,
            text="Проверить ✅",
            font=('Arial', 14, 'bold'),
            bg='#27AE60',
            fg='white',
            padx=20,
            pady=10,
            command=self.check_answer
        )
        self.check_button.pack(pady=10)
        
        # Кнопка нового вопроса
        self.new_button = tk.Button(
            game_frame,
            text="Новый вопрос 🔄",
            font=('Arial', 12),
            bg='#3498DB',
            fg='white',
            padx=15,
            pady=5,
            command=self.new_question
        )
        self.new_button.pack(pady=5)
        
        # Сообщение о результате
        self.result_label = tk.Label(
            game_frame,
            text="",
            font=('Arial', 14),
            bg='#2C3E50',
            fg='#F1C40F'
        )
        self.result_label.pack(pady=10)
    
    def create_stats_area(self):
        """Создание области статистики"""
        stats_frame = tk.Frame(self.root, bg='#34495E', height=80)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        # Счетчики
        self.stats_label = tk.Label(
            stats_frame,
            text="Правильно: 0 | Попыток: 0 | %: 0%",
            font=('Arial', 12, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        )
        self.stats_label.pack(side='left', padx=20, pady=10)
        
        # Кнопка выхода
        exit_button = tk.Button(
            stats_frame,
            text="Выйти",
            font=('Arial', 10),
            bg='#E74C3C',
            fg='white',
            command=self.exit_app
        )
        exit_button.pack(side='right', padx=20)
    
    def new_question(self):
        """Генерация нового вопроса"""
        self.num1 = random.randint(2, 9)
        self.num2 = random.randint(2, 9)
        self.current_correct = self.num1 * self.num2
        
        self.question_label.config(text=f"{self.num1} * {self.num2} = ?")
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.entry.focus()
    
    def check_answer(self):
        """Проверка ответа"""
        user_input = self.entry.get().strip()
        
        # Проверка на пустой ввод
        if not user_input:
            self.result_label.config(text="Введите ответ!", fg='#E74C3C')
            return
        
        # Проверка на число
        if not user_input.isdigit():
            self.result_label.config(text="Введите ЧИСЛО!", fg='#E74C3C')
            self.entry.delete(0, tk.END)
            return
        
        answer = int(user_input)
        self.attempts += 1
        
        # Проверка правильности
        if answer == self.current_correct:
            self.score += 1
            self.result_label.config(
                text="✅ ВЕРНО! Молодец!", 
                fg='#2ECC71'
            )
        else:
            self.result_label.config(
                text=f"❌ Неверно! Правильно: {self.current_correct}", 
                fg='#E74C3C'
            )
        
        # Обновление статистики
        self.update_stats()
        
        # Автоматически новый вопрос через 1 секунду
        self.root.after(1000, self.new_question)
    
    def update_stats(self):
        """Обновление статистики"""
        if self.attempts > 0:
            percent = (self.score / self.attempts) * 100
            stats_text = f"✅ Правильно: {self.score} | "
            stats_text += f"📊 Попыток: {self.attempts} | "
            stats_text += f"📈 %: {percent:.1f}%"
        else:
            stats_text = "✅ Правильно: 0 | 📊 Попыток: 0 | 📈 %: 0%"
        
        self.stats_label.config(text=stats_text)
    
    def exit_app(self):
        """Выход из приложения с показом итогов"""
        if self.attempts > 0:
            percent = (self.score / self.attempts) * 100
            result_text = f"Игра окончена!\n\n"
            result_text += f"Правильных ответов: {self.score}\n"
            result_text += f"Всего попыток: {self.attempts}\n"
            result_text += f"Процент успеха: {percent:.1f}%"
            
            messagebox.showinfo("Итоги игры", result_text)
        
        self.root.quit()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MathMasterApp(root)
    root.mainloop()
