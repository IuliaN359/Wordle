import customtkinter as ctk
from wordle import Wordle

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

appWidth, appHeight = 600, 750

KeyboardLayout=[["Q","W","E","R","T","Y","U","I","O","P"],["A","S","D","F","G","H","J","K","L"],["ENTER","Z","X","C","V","B","N","M","BACK"]]

class App(ctk.CTk):
    light_grey = "#7a7a84"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = Wordle()
        self.game.choosing_word("possible_words.txt")

        self.current_row = 0
        self.current_col = 0
        self.current_guess = []
        self.already_guessed=[]
        self.game_over=False

        self.title("Wordle")
        self.geometry(f"{appWidth}x{appHeight}")

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True)
        self.grid_labels = []

        self.keyboard=ctk.CTkFrame(self,fg_color="transparent")
        self.keyboard.pack(expand=True)

        for row in range(6):
            row_cells = []
            for col in range(5):
                tile = ctk.CTkLabel(self.grid_frame, text="", font=("Arial", 28, "bold"), width=60, height=60,
                                    fg_color=self.light_grey, corner_radius=4)
                tile.grid(row=row, column=col, padx=5, pady=5)
                row_cells.append(tile)
            self.grid_labels.append(row_cells)

        self.key_buttons={}
        for row_idx, row in enumerate(KeyboardLayout):
            row_frame=ctk.CTkFrame(self.keyboard, fg_color="transparent")
            row_frame.pack(pady=4)
            for key in row:
                if key=="ENTER":
                    cmd=self.guess
                    w=75
                elif key=="BACK":
                    cmd=lambda: self.handle_key(type('Event', (object,), {'keysym': 'BackSpace'})())
                    w=75
                else:
                    cmd=lambda k=key: self.keypress(k)
                    w=50

                btn=ctk.CTkButton(row_frame,text=key,width=w,height=50, fg_color=self.light_grey, text_color="white", font=("Arial",16, "bold"),command=cmd)
                btn.pack(side="left",padx=3)

                if len(key)==1:
                    self.key_buttons[key.lower()]=btn


        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 26), text_color=self.game.dark_grey)
        self.status_label.pack(pady=10,ipady=10)

        self.reset_button=ctk.CTkButton(self, text="Play again",font=("Arial", 26), command=self.set_game)

        self.set_game()
        self.bind("<Key>",self.handle_key)

    def set_game(self):
        self.game.choosing_word("possible_words.txt")

        self.current_row = 0
        self.current_col = 0
        self.current_guess = []
        self.already_guessed=[]
        self.game_over=False

        self.reset_button.pack_forget()
        self.status_label.configure(text="")

        for row in range(6):
            for col in range(5):
                self.grid_labels[row][col].configure(text="",fg_color=self.light_grey)

        for btn in self.key_buttons.values():
            btn.configure(fg_color=self.light_grey)

    def clear_status_label(self):
        if not self.game_over:
            self.status_label.configure(text="")

    def keypress(self, letter):
        if self.current_col < 5:
            self.current_guess.append(letter)
            row = self.current_row
            col = self.current_col
            self.grid_labels[row][col].configure(text=letter)
            self.current_col += 1

    def handle_key(self, event):
        if self.game_over:
            return

        if event.keysym =="BackSpace":
            if self.current_col>0:
                self.current_col-=1
                self.grid_labels[self.current_row][self.current_col].configure(text="")
                self.current_guess.pop()

        elif event.keysym=="Return":
            self.guess()

        elif event.char.isalpha() and len(event.char)==1:
            self.keypress(event.char.upper())

    def guess(self):
        guess = "".join(self.current_guess).lower()
        if len(guess) != 5:
            self.status_label.configure(text="Not enough letters!", text_color="red")
            self.after(1300, self.clear_status_label)
            return
        if guess in self.already_guessed:
            self.status_label.configure(text="Already tried this one", text_color="red")
            self.after(1300, self.clear_status_label)
            return
        with open("all_words.txt", "r") as file:
            words=file.read().split()
        if guess not in words:
            self.status_label.configure(text="Not in word list", text_color="red")
            self.after(1300, self.clear_status_label)
            return

        self.already_guessed.append(guess)
        colors = self.game.game_logic(guess)
        for col in range(5):
            letter=guess[col]
            tile_color = colors[col]
            self.grid_labels[self.current_row][col].configure(fg_color=tile_color)

            if letter in self.key_buttons:
                btn=self.key_buttons[letter]
                current_color=btn.cget("fg_color")
                if current_color!=self.game.green:
                    if tile_color==self.game.green:
                        btn.configure(fg_color=self.game.green)
                    elif tile_color==self.game.yellow and current_color!=self.game.yellow:
                        btn.configure(fg_color=self.game.yellow)
                    elif tile_color==self.game.dark_grey and current_color==self.light_grey:
                        btn.configure(fg_color=self.game.dark_grey)

        if all(color==self.game.green for color in colors):
            self.status_label.configure(text="You won", text_color="#00a832")
            self.game_over=True
            self.reset_button.pack(pady=10)
            return

        self.current_row += 1
        self.current_col = 0
        self.current_guess = []

        if self.current_row==6:
            self.status_label.configure(text=f"Game over!\nThe word was {self.game.word}", text_color="#b31f10")
            self.game_over=True
            self.reset_button.pack(pady=10)



def main():
    app = App()
    app.mainloop()


main()
