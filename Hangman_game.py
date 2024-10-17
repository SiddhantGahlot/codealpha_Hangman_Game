import tkinter as tk
import random

# List of cricket-related words and hints
words_and_hints = {
    'batsman': 'A player who scores runs by hitting the ball with a bat.',
    'bowler': 'A player who delivers the ball to the batsman.',
    'wicket': 'The set of three stumps and two bails.',
    'umpire': 'An official who makes decisions during the game.',
    'boundary': 'A hit that reaches or crosses the edge of the playing field.',
    'century': 'A player scoring 100 runs in a single innings.',
    'yorker': 'A ball bowled so that it pitches at or near the batsman’s feet.',
    'allrounder': 'A player good at both batting and bowling.',
    'googly': 'A deceptive ball bowled by a leg-spinner.',
    'sixer': 'A shot that goes over the boundary without touching the ground.',
    'maiden': 'An over in which no runs are scored off the bat.',
    'bouncer': 'A fast, short-pitched ball aimed at the batsman’s head.',
    'overs': 'A set of six balls bowled by a single bowler.',
    'stumping': 'Dismissing a batsman by breaking the stumps while they are out of the crease.',
    'spin': 'A type of bowling that makes the ball turn when it bounces.',
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Hangman Game")

        # Initialize game state
        self.initialize_game()

        # Create GUI elements
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack(pady=20)

        self.word_label = tk.Label(root, text=" ".join(self.guessed_word), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.hint_label = tk.Label(root, text=f"Hint: {self.hint}", font=("Helvetica", 14), fg="blue")
        self.hint_label.pack(pady=10)

        self.attempts_label = tk.Label(root, text=f"Remaining attempts: {self.attempts}", font=("Helvetica", 14))
        self.attempts_label.pack(pady=10)

        self.guess_label = tk.Label(root, text="Guess a letter:", font=("Helvetica", 14))
        self.guess_label.pack(pady=5)

        self.guess_entry = tk.Entry(root, font=("Helvetica", 14))
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", self.make_guess)  # Bind Enter key to submit guess

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.feedback_label.pack(pady=10)

        # Create Restart Button
        self.restart_button = tk.Button(root, text="Restart Game", font=("Helvetica", 14), command=self.restart_game)
        self.restart_button.pack(pady=20)

    def initialize_game(self):
        """Initialize or reset the game state."""
        self.word, self.hint = random.choice(list(words_and_hints.items()))  # Choose a random word and hint
        self.guessed_word = ['_'] * len(self.word)  # Initialize the guessed word with underscores
        self.guessed_letters = []  # Store guessed letters
        self.attempts = 6  # Set number of attempts
        self.hangman_stages = [  # Hangman animation stages
            "",
            "O",
            "O\n | ",
            "O\n/| ",
            "O\n/|\\",
            "O\n/|\\ \n/",
            "O\n/|\\ \n/ \\"
        ]

    def draw_hangman(self):
        """Draw the current hangman stage based on remaining attempts."""
        self.canvas.delete("all")  # Clear the canvas
        hangman_stage = self.hangman_stages[6 - self.attempts]  # Select the current hangman stage
        self.canvas.create_text(100, 100, text=hangman_stage, font=("Helvetica", 24), fill="black")

    def make_guess(self, event):
        """Handle letter guesses."""
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)  # Clear input field after submission

        # Input validation: Check if it's a single valid letter
        if not guess.isalpha() or len(guess) != 1:
            self.feedback_label.config(text="Please enter a single valid letter.")
            return

        # Check if the letter has already been guessed
        if guess in self.guessed_letters:
            self.feedback_label.config(text=f"You already guessed '{guess}'. Try another letter.")
            return

        # Add the guessed letter to the list of guessed letters
        self.guessed_letters.append(guess)

        # Check if the guess is correct
        if guess in self.word:
            self.feedback_label.config(text=f"Good guess! '{guess}' is in the word.")
            for idx, letter in enumerate(self.word):
                if letter == guess:
                    self.guessed_word[idx] = guess
        else:
            self.attempts -= 1
            self.feedback_label.config(text=f"Wrong guess! '{guess}' is not in the word.")
            self.draw_hangman()  # Animate hangman drawing

        # Update the displayed word and attempts
        self.word_label.config(text=" ".join(self.guessed_word))
        self.attempts_label.config(text=f"Remaining attempts: {self.attempts}")

        # Check if the game is over
        self.check_game_over()

    def check_game_over(self):
        """Check if the game is over and handle game over conditions."""
        if "_" not in self.guessed_word:
            self.feedback_label.config(text="Congratulations! You've guessed the word!")
            self.guess_entry.config(state="disabled")  # Disable input after win
        elif self.attempts == 0:
            self.feedback_label.config(text=f"Game Over! The word was '{self.word}'.")
            self.guess_entry.config(state="disabled")  # Disable input after loss

    def restart_game(self):
        """Restart the game by resetting the game state and UI elements."""
        self.initialize_game()  # Reset game variables
        self.canvas.delete("all")  # Clear the hangman drawing
        self.word_label.config(text=" ".join(self.guessed_word))  # Reset word display
        self.hint_label.config(text=f"Hint: {self.hint}")  # Update hint
        self.attempts_label.config(text=f"Remaining attempts: {self.attempts}")  # Reset attempts display
        self.feedback_label.config(text="")  # Clear feedback messages
        self.guess_entry.config(state="normal")  # Re-enable input


# Create the application window
root = tk.Tk()
game = HangmanGame(root)

# Run the Tkinter event loop
root.mainloop()
