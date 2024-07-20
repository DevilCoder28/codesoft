import tkinter as tk
import random
from PIL import Image, ImageTk
import threading
import pygame
import os

class RockPaperScissorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("950x630")
        self.root.configure(bg="#2e3f4f")

        self.win_count = 0
        self.loss_count = 0
        self.tie_count = 0
        self.round_count = 0
        self.sound_enabled = True

        pygame.mixer.init()  

        self.load_images()
        self.create_widgets()

    def load_images(self):
        self.images = {
            "Rock": ImageTk.PhotoImage(Image.open("rock.png").resize((150, 150))),
            "Paper": ImageTk.PhotoImage(Image.open("paper.png").resize((150, 150))),
            "Scissor": ImageTk.PhotoImage(Image.open("scissor.png").resize((150, 150))),
            "vs": ImageTk.PhotoImage(Image.open("vs.png").resize((100, 100))),
            "win": ImageTk.PhotoImage(Image.open("win.png").resize((100, 100))),
            "lose": ImageTk.PhotoImage(Image.open("lose.png").resize((100, 100))),
            "tie": ImageTk.PhotoImage(Image.open("tie.png").resize((100, 100)))
        }

    def create_widgets(self):
        title = tk.Label(self.root, text="Rock Paper Scissors", font=("Helvetica", 30, "bold"), bg="#2e3f4f", fg="#ffffff")
        title.pack(pady=20)

        self.player_choice_label = tk.Label(self.root, text="Your Selection:", font=("Helvetica", 20), bg="#2e3f4f", fg="#ffffff")
        self.player_choice_label.place(relx=0.15, rely=0.3)

        self.computer_choice_label = tk.Label(self.root, text="Computer Selection:", font=("Helvetica", 20), bg="#2e3f4f", fg="#ffffff")
        self.computer_choice_label.place(relx=0.55, rely=0.3)

        self.player_choice_image = tk.Label(self.root, bg="#2e3f4f")
        self.player_choice_image.place(relx=0.05, rely=0.45)

        self.vs_image = tk.Label(self.root, image=self.images["vs"], bg="#2e3f4f")
        self.vs_image.place(relx=0.42, rely=0.45)

        self.computer_choice_image = tk.Label(self.root, bg="#2e3f4f")
        self.computer_choice_image.place(relx=0.7, rely=0.45)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 20), bg="#2e3f4f", fg="#ffffff")
        self.result_label.place(relx=0.4, rely=0.7)

        rock_button = tk.Button(self.root, text="Rock", command=lambda: self.player("Rock"), font=("Helvetica", 16), bg="#4f5b66", fg="#ffffff", activebackground="#7f8c8d")
        rock_button.place(relx=0.3, rely=0.9)

        paper_button = tk.Button(self.root, text="Paper", command=lambda: self.player("Paper"), font=("Helvetica", 16), bg="#4f5b66", fg="#ffffff", activebackground="#7f8c8d")
        paper_button.place(relx=0.38, rely=0.9)

        scissor_button = tk.Button(self.root, text="Scissors", command=lambda: self.player("Scissor"), font=("Helvetica", 16), bg="#4f5b66", fg="#ffffff", activebackground="#7f8c8d")
        scissor_button.place(relx=0.47, rely=0.9)

        self.stats_label = tk.Label(self.root, text="Stats:", font=("Helvetica", 20, "bold"), bg="#2e3f4f", fg="#ffffff")
        self.stats_label.place(relx=0.1, rely=0.1)

        self.stats_info_label = tk.Label(self.root, text="", font=("Helvetica", 16), bg="#2e3f4f", fg="#ffffff")
        self.stats_info_label.place(relx=0.1, rely=0.15)

        self.update_stats()

        instructions = tk.Label(self.root, text="Instructions:\nRock beats Scissors\nScissors beats Paper\nPaper beats Rock", 
                                font=("Helvetica", 14), bg="#2e3f4f", fg="#ffffff", justify="left")
        instructions.place(relx=0.6, rely=0.1)

        self.sound_button = tk.Button(self.root, text="Sound: ON", command=self.toggle_sound, font=("Helvetica", 14), bg="#4f5b66", fg="#ffffff", activebackground="#7f8c8d")
        self.sound_button.place(relx=0.8, rely=0.05)

        reset_button = tk.Button(self.root, text="Reset Stats", command=self.reset_stats, font=("Helvetica", 14), bg="#4f5b66", fg="#ffffff", activebackground="#7f8c8d")
        reset_button.place(relx=0.8, rely=0.15)

    def player(self, option):
        self.round_count += 1

        if self.sound_enabled:
            sound_file = f"{option.lower()}.mp3"
            threading.Thread(target=self.play_sound, args=(sound_file,)).start()

        computer_choices = ["Rock", "Paper", "Scissor"]
        computer_choice = random.choice(computer_choices)

        self.animate_choice(self.player_choice_image, self.images[option])
        self.animate_choice(self.computer_choice_image, self.images[computer_choice])

        self.player_choice_label.config(text=f"Your Selection: {option}")
        self.computer_choice_label.config(text=f"Computer Selection: {computer_choice}")

        result = self.determine_result(option, computer_choice)
        self.display_result(result)

        self.update_stats()

    def animate_choice(self, label, image):
        label.configure(image=None)
        label.image = image
        label.configure(image=image)

    def determine_result(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            self.tie_count += 1
            return "tie"
        elif (player_choice == "Rock" and computer_choice == "Scissor") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissor" and computer_choice == "Paper"):
            self.win_count += 1
            return "win"
        else:
            self.loss_count += 1
            return "lose"

    def display_result(self, result):
        if result == "win":
            self.result_label.config(image=self.images["win"])
            if self.sound_enabled:
                threading.Thread(target=self.play_sound, args=("win.mp3",)).start()
        elif result == "lose":
            self.result_label.config(image=self.images["lose"])
            if self.sound_enabled:
                threading.Thread(target=self.play_sound, args=("lose.mp3",)).start()
        else:
            self.result_label.config(image=self.images["tie"])
            if self.sound_enabled:
                threading.Thread(target=self.play_sound, args=("tie.mp3",)).start()

    def update_stats(self):
        stats_text = f"Rounds played: {self.round_count}\n"
        stats_text += f"Wins: {self.win_count}\n"
        stats_text += f"Losses: {self.loss_count}\n"
        stats_text += f"Ties: {self.tie_count}"
        self.stats_info_label.config(text=stats_text)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_button.config(text=f"Sound: {'ON' if self.sound_enabled else 'OFF'}")

    def reset_stats(self):
        self.win_count = 0
        self.loss_count = 0
        self.tie_count = 0
        self.round_count = 0
        self.update_stats()

    def play_sound(self, sound_file):
        if os.path.isfile(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        else:
            print(f"Sound file '{sound_file}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorGame(root)
    root.mainloop()
