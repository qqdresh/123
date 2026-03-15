import random

print(" Добро пожаловать в:")
print("=" * 40)
print("           МАТH MASTER")
print("=" * 40)
print("Пример: 5 * 7 = 'Ваш ответ")
print("Для выхода введите 'exit'")

score = 0
attempts = 0

while True:
    # Генерируем два случайных числа от 2 до 9
    num1 = random.randint(2, 9)
    num2 = random.randint(2, 9)
    
    # Загадываем пример
    correct = num1 * num2
    
    # Спрашиваем пользователя
    user_input = input(f"{num1} * {num2} = ")
    
    # Проверка на выход
    if user_input.lower() == 'exit':
        break
    
    # Проверка, что ввели число
    if not user_input.isdigit():
        print(" Введите число или 'exit'!")
        continue
    
    answer = int(user_input)
    attempts += 1
    
    # Проверка ответа
    if answer == correct:
        print(" Верно! Молодец!")
        score += 1
    else:
        print(f" Неверно! Правильный ответ: {correct}")

# Итоги
print("-" * 30)
print(f"Игра окончена! 🏁")
print(f"Попыток: {attempts}")
print(f"Правильных ответов: {score}")
if attempts > 0:
    print(f"Процент успеха: {score / attempts * 100:.1f}%")
