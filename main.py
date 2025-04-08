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

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x450")
window.configure(bg=BG_COLOR)

# Настройка шрифтов
custom_font = font.Font(family="Helvetica", size=24, weight="bold")
reset_font = font.Font(family="Helvetica", size=14, weight="bold")
status_font = font.Font(family="Helvetica", size=12)

current_player = "X"
buttons = []

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

    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player
    buttons[row][col]['fg'] = X_COLOR if current_player == "X" else O_COLOR

    if check_winner():
        update_status(f"Игрок {current_player} победил!")
        messagebox.showinfo("Игра окончена", f"Игрок {current_player} победил!")
        reset_game()
        return
    elif is_board_full():
        update_status("Ничья!")
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
        return

    current_player = "O" if current_player == "X" else "X"
    update_status(f"Ход игрока: {current_player}")

def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for button in row:
            button.config(text="", bg=BUTTON_COLOR)
    update_status(f"Ход игрока: {current_player}")

def update_status(message):
    status_label.config(text=message)

# Создаем статусную строку
status_label = tk.Label(window, text=f"Ход игрока: {current_player}",
                       font=status_font, bg=BG_COLOR, fg=TEXT_COLOR)
status_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), sticky="ew")

# Создаем игровое поле
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=custom_font, width=3, height=1,
                       bg=BUTTON_COLOR, fg=TEXT_COLOR, relief="flat",
                       activebackground="#2c3e50", activeforeground=TEXT_COLOR,
                       command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
        row.append(btn)
    buttons.append(row)

# Добавляем кнопку сброса
reset_btn = tk.Button(window, text="Новая игра", font=reset_font,
                     bg=RESET_COLOR, fg=TEXT_COLOR, relief="flat",
                     activebackground=RESET_COLOR, activeforeground=TEXT_COLOR,
                     command=reset_game)
reset_btn.grid(row=5, column=0, columnspan=3, pady=(10, 15), padx=20, sticky="nsew")

# Настраиваем расширение строк/колонок
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

window.mainloop()