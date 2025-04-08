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
SCORE_COLOR = "#f39c12"

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x550")
window.configure(bg=BG_COLOR)

# Настройка шрифтов
custom_font = font.Font(family="Helvetica", size=24, weight="bold")
reset_font = font.Font(family="Helvetica", size=14, weight="bold")
status_font = font.Font(family="Helvetica", size=12)
title_font = font.Font(family="Helvetica", size=16, weight="bold")
score_font = font.Font(family="Helvetica", size=14)

# Игровые переменные
current_player = "X"
player_symbol = "X"
buttons = []
game_started = False
player_wins = 0
computer_wins = 0
draws = 0


def start_game(symbol):
    global player_symbol, game_started, current_player
    player_symbol = symbol
    game_started = True
    current_player = "X"
    choice_frame.pack_forget()
    game_frame.pack()
    update_status(f"Ход игрока: {current_player}")
    update_score()


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
    global current_player, player_wins, computer_wins, draws

    if not game_started or buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player
    buttons[row][col]['fg'] = X_COLOR if current_player == "X" else O_COLOR

    if check_winner():
        if current_player == player_symbol:
            player_wins += 1
            winner = "Вы"
        else:
            computer_wins += 1
            winner = "Компьютер"

        update_status(f"{winner} победили!")
        messagebox.showinfo("Игра окончена", f"{winner} победили!")
        update_score()
        reset_board()
        return
    elif is_board_full():
        draws += 1
        update_status("Ничья!")
        messagebox.showinfo("Игра окончена", "Ничья!")
        update_score()
        reset_board()
        return

    current_player = "O" if current_player == "X" else "X"
    update_status(f"Ход: {'Ваш' if current_player == player_symbol else 'Компьютера'}")


def reset_board():
    global current_player
    current_player = "X"
    for row in buttons:
        for button in row:
            button.config(text="", bg=BUTTON_COLOR)
    update_status(f"Ход игрока: {current_player}")


def reset_game():
    global game_started, player_wins, computer_wins, draws
    game_started = False
    player_wins = 0
    computer_wins = 0
    draws = 0
    reset_board()
    game_frame.pack_forget()
    choice_frame.pack()
    status_label.config(text="Выберите символ для игры")
    update_score()


def update_status(message):
    status_label.config(text=message)


def update_score():
    score_label.config(text=f"Вы: {player_wins}  Компьютер: {computer_wins}  Ничьи: {draws}")


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

# Счетчик побед
score_label = tk.Label(game_frame,
                       text="Вы: 0  Компьютер: 0  Ничьи: 0",
                       font=score_font, bg=BG_COLOR, fg=SCORE_COLOR)
score_label.grid(row=0, column=0, columnspan=3, pady=(5, 5), sticky="ew")

# Статусная строка
status_label = tk.Label(game_frame, text="",
                        font=status_font, bg=BG_COLOR, fg=TEXT_COLOR)
status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="ew")

# Создаем игровое поле
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=custom_font, width=3, height=1,
                        bg=BUTTON_COLOR, fg=TEXT_COLOR, relief="flat",
                        activebackground="#2c3e50", activeforeground=TEXT_COLOR,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i + 2, column=j, padx=5, pady=5, sticky="nsew")
        row.append(btn)
    buttons.append(row)

# Кнопки управления
button_frame = tk.Frame(game_frame, bg=BG_COLOR)
button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0), sticky="nsew")

new_game_btn = tk.Button(button_frame, text="Новая партия", font=reset_font,
                         bg=RESET_COLOR, fg=TEXT_COLOR, relief="flat",
                         command=reset_board)
new_game_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

reset_score_btn = tk.Button(button_frame, text="Сбросить счет", font=reset_font,
                            bg="#c0392b", fg=TEXT_COLOR, relief="flat",
                            command=reset_game)
reset_score_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

# Настраиваем расширение строк/колонок
for i in range(2, 5):
    game_frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    game_frame.grid_columnconfigure(i, weight=1)

window.mainloop()