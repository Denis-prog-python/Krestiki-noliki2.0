import tkinter as tk
from tkinter import messagebox, font

# Настройки цветовой схемы
BG_COLOR = "#2c3e50"
BUTTON_COLOR = "#34495e"
X_COLOR = "#e74c3c"
O_COLOR = "#3498db"
TEXT_COLOR = "#ecf0f1"
RESET_COLOR = "#16a085"
WIN_COLOR = "#2ecc71"
SELECT_COLOR = "#9b59b6"

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x500")
window.configure(bg=BG_COLOR)

# Настройка шрифтов
custom_font = font.Font(family="Helvetica", size=24, weight="bold")
reset_font = font.Font(family="Helvetica", size=14, weight="bold")
status_font = font.Font(family="Helvetica", size=12)
title_font = font.Font(family="Helvetica", size=16, weight="bold")

current_player = "X"
player_symbol = "X"  # Символ, который выбрал игрок
buttons = []
game_started = False

def start_game(symbol):
    global player_symbol, game_started, current_player
    player_symbol = symbol
    game_started = True
    current_player = "X"  # Всегда начинают крестики
    choice_frame.pack_forget()
    game_frame.pack()
    update_status(f"Ход игрока: {current_player}")

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            highlight_winner(i, 0, i, 1, i, 2)
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            highlight_winner(0, i, 1, i, 2, i)
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        highlight_winner(0, 0, 1, 1, 2, 2)
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        highlight_winner(0, 2, 1, 1, 2, 0)
        return True

    return False

def highlight_winner(r1, c1, r2, c2, r3, c3):
    buttons[r1][c1].config(bg=WIN_COLOR)
    buttons[r2][c2].config(bg=WIN_COLOR)
    buttons[r3][c3].config(bg=WIN_COLOR)

def is_board_full():
    for row in buttons:
        for button in row:
            if button["text"] == "":
                return False
    return True

def on_click(row, col):
    global current_player

    if not game_started or buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player
    buttons[row][col]['fg'] = X_COLOR if current_player == "X" else O_COLOR

    if check_winner():
        winner = "Вы" if current_player == player_symbol else "Компьютер"
        update_status(f"{winner} победили!")
        messagebox.showinfo("Игра окончена", f"{winner} победили!")
        reset_game()
        return
    elif is_board_full():
        update_status("Ничья!")
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
        return

    current_player = "O" if current_player == "X" else "X"
    update_status(f"Ход: {'Ваш' if current_player == player_symbol else 'Компьютера'}")

def reset_game():
    global current_player, game_started
    game_started = False
    current_player = "X"
    for row in buttons:
        for button in row:
            button.config(text="", bg=BUTTON_COLOR)
    game_frame.pack_forget()
    choice_frame.pack()
    status_label.config(text="Выберите символ для игры")

def update_status(message):
    status_label.config(text=message)

# Главный фрейм для выбора символа
choice_frame = tk.Frame(window, bg=BG_COLOR)
choice_frame.pack(pady=50)

tk.Label(choice_frame, text="Выберите символ для игры",
        font=title_font, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

btn_frame = tk.Frame(choice_frame, bg=BG_COLOR)
btn_frame.pack()

x_btn = tk.Button(btn_frame, text="X", font=custom_font, width=3, height=1,
                 bg=SELECT_COLOR, fg=TEXT_COLOR, relief="flat",
                 command=lambda: start_game("X"))
x_btn.pack(side=tk.LEFT, padx=10)

o_btn = tk.Button(btn_frame, text="O", font=custom_font, width=3, height=1,
                 bg=SELECT_COLOR, fg=TEXT_COLOR, relief="flat",
                 command=lambda: start_game("O"))
o_btn.pack(side=tk.LEFT, padx=10)

# Фрейм для игрового поля
game_frame = tk.Frame(window, bg=BG_COLOR)

# Статусная строка
status_label = tk.Label(game_frame, text="Выберите символ для игры",
                       font=status_font, bg=BG_COLOR, fg=TEXT_COLOR)
status_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), sticky="ew")

# Создаем игровое поле
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=custom_font, width=3, height=1,
                       bg=BUTTON_COLOR, fg=TEXT_COLOR, relief="flat",
                       activebackground="#2c3e50", activeforeground=TEXT_COLOR,
                       command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
        row.append(btn)
    buttons.append(row)

# Кнопка сброса
reset_btn = tk.Button(game_frame, text="Новая игра", font=reset_font,
                     bg=RESET_COLOR, fg=TEXT_COLOR, relief="flat",
                     activebackground=RESET_COLOR, activeforeground=TEXT_COLOR,
                     command=reset_game)
reset_btn.grid(row=5, column=0, columnspan=3, pady=(10, 15), padx=20, sticky="nsew")

# Настраиваем расширение строк/колонок
for i in range(1, 4):
    game_frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    game_frame.grid_columnconfigure(i, weight=1)

window.mainloop()