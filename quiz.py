import tkinter as tk
from tkinter import messagebox
import json
import random

# Load questions from JSON file
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("700x500")
        self.root.configure(bg="#2c3e50")  # Background color

        self.questions = load_questions()
        self.selected_questions = []
        self.current_question_index = 0
        self.score = 0
        self.timer = 10
        self.timer_running = False
        self.total_questions = 0
        self.username = ""

        self.create_widgets()

    def create_widgets(self):
        # Welcome screen widgets
        self.title_label = tk.Label(self.root, text="🧠 Welcome to the Quiz App!", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.title_label.pack(pady=20)

        self.name_label = tk.Label(self.root, text="Enter your name:", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14), width=30)
        self.name_entry.pack(pady=5)

        self.num_label = tk.Label(self.root, text="How many questions do you want to attempt?", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1")
        self.num_label.pack()
        self.num_entry = tk.Entry(self.root, font=("Helvetica", 14), width=10)
        self.num_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Quiz", font=("Helvetica", 16, "bold"), bg="#27ae60", fg="black", command=self.start_quiz)
        self.start_button.pack(pady=20)

        # Quiz widgets (initially hidden)
        self.question_label = tk.Label(self.root, text="", wraplength=650, font=("Helvetica", 16), bg="#2c3e50", fg="white", justify="left")

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", font=("Helvetica", 14), bg="#3498db", fg="black", width=50, command=lambda i=i: self.check_answer(i))
            self.option_buttons.append(btn)

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#e74c3c")

    def start_quiz(self):
        self.username = self.name_entry.get().strip()
        try:
            self.total_questions = int(self.num_entry.get())
            if not (1 <= self.total_questions <= len(self.questions)):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid number of questions.")
            return

        # Hide intro widgets
        self.title_label.pack_forget()
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.num_label.pack_forget()
        self.num_entry.pack_forget()
        self.start_button.pack_forget()

        # Shuffle and select questions
        random.shuffle(self.questions)
        self.selected_questions = self.questions[:self.total_questions]

        # Show quiz widgets
        self.question_label.pack(pady=20)
        for btn in self.option_buttons:
            btn.pack(pady=5)
        self.timer_label.pack(pady=10)

        # Start the first question
        self.show_question()

    def show_question(self):
        self.timer = 10
        self.timer_running = True
        self.update_timer()

        question = self.selected_questions[self.current_question_index]
        self.question_label.config(text=f"Q{self.current_question_index + 1}: {question['question']}")

        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=option, state="normal", bg="#3498db", fg="black")

    def update_timer(self):
        self.timer_label.config(text=f"⏰ Time left: {self.timer}s")
        if self.timer > 0 and self.timer_running:
            self.timer -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer == 0:
            self.timer_running = False
            self.disable_buttons()
            self.show_correct_answer()
            self.root.after(1500, self.next_question)

    def disable_buttons(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")

    def check_answer(self, selected_index):
        if not self.timer_running:
            return  # Ignore if time ran out

        self.timer_running = False  # Stop timer
        question = self.selected_questions[self.current_question_index]
        selected_option = question["options"][selected_index]

        if selected_option == question["answer"]:
            self.option_buttons[selected_index].config(bg="#2ecc71", fg="black")  # Green
            self.score += 1
        else:
            self.option_buttons[selected_index].config(bg="#e74c3c", fg="black")  # Red
            self.show_correct_answer()

        self.disable_buttons()
        self.root.after(1500, self.next_question)

    def show_correct_answer(self):
        correct_answer = self.selected_questions[self.current_question_index]["answer"]
        for btn in self.option_buttons:
            if btn["text"] == correct_answer:
                btn.config(bg="#2ecc71", fg="black")

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < self.total_questions:
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        # Hide quiz widgets
        self.question_label.pack_forget()
        self.timer_label.pack_forget()
        for btn in self.option_buttons:
            btn.pack_forget()

        # Show score
        result_text = f"🎉 Quiz Completed!\n{self.username}, you scored {self.score} out of {self.total_questions}."
        result_label = tk.Label(self.root, text=result_text, font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="#f1c40f")
        result_label.pack(pady=50)

        quit_btn = tk.Button(self.root, text="Exit", font=("Helvetica", 14), bg="#c0392b", fg="black", command=self.root.quit)
        quit_btn.pack(pady=20)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
