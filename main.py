import tkinter as tk
from tkinter import messagebox, simpledialog
import time


class DangerousDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dangerous Writing Desktop App")
        self.root.geometry("800x500")

        # Default settings
        self.inactivity_limit = 5  # Seconds before text deletion
        self.timer_running = False  # Writing session state

        # Title
        self.title_label = tk.Label(root, text="Dangerous Writing App", font=("Arial", 20), fg="black")
        self.title_label.pack(pady=10)

        # Main text area
        self.text_area = tk.Text(root, wrap='word', font=("Arial", 16), state=tk.DISABLED)
        self.text_area.pack(expand=True, fill='both', padx=20, pady=20)

        # Timer and status labels
        self.timer_label = tk.Label(root, text="Time left: Not started", font=("Arial", 12), fg="blue")
        self.timer_label.pack(pady=10)

        # Control buttons
        button_style = {"font": ("Arial", 14), "width": 15, "height": 2}  # Bigger button style
        self.start_button = tk.Button(root, text="Start Writing", **button_style, command=self.start_session)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.pause_button = tk.Button(root, text="Pause Timer", **button_style, state=tk.DISABLED,
                                      command=self.toggle_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.settings_button = tk.Button(root, text="Settings", **button_style, command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10, pady=10)

    def start_session(self):
        """Start the writing session and timer."""
        self.timer_running = True
        self.last_keypress_time = time.time()
        self.text_area.config(state=tk.NORMAL)  # Enable typing
        self.text_area.bind('<Key>', self.reset_timer)  # Start tracking keypresses
        self.start_button.config(state=tk.DISABLED)  # Disable start button
        self.pause_button.config(state=tk.NORMAL)  # Enable pause button
        self.update_timer()  # Start the timer

    def toggle_timer(self):
        """Pause or resume the timer."""
        self.timer_running = not self.timer_running
        self.pause_button.config(text="Resume Timer" if not self.timer_running else "Pause Timer")
        if self.timer_running:
            self.update_timer()  # Resume timer

    def reset_timer(self, event=None):
        """Reset the inactivity timer on keypress."""
        self.last_keypress_time = time.time()

    def update_timer(self):
        """Update the inactivity timer and check remaining time."""
        if self.timer_running:
            elapsed = time.time() - self.last_keypress_time
            remaining = max(0, self.inactivity_limit - int(elapsed))

            # Update timer label with color-coded feedback
            if remaining > 2:
                self.timer_label.config(text=f"Time left: {remaining}s", fg="green")
            elif remaining > 0:
                self.timer_label.config(text=f"Time left: {remaining}s", fg="orange")
            else:
                self.timer_label.config(text="Time left: 0s", fg="red")
                self.text_area.delete('1.0', tk.END)  # Clear text
                messagebox.showwarning("Oops!", "You stopped writing! All text has been deleted.")
                self.last_keypress_time = time.time()  # Reset timer

            # Call this method again after 1 second
            self.root.after(1000, self.update_timer)

    def open_settings(self):
        """Open a settings dialog to customize app behavior."""
        inactivity = simpledialog.askinteger("Settings", "Set inactivity limit (seconds):", minvalue=3, maxvalue=10)
        if inactivity is not None:
            self.inactivity_limit = inactivity
            messagebox.showinfo("Settings Updated", f"Inactivity Limit set to {self.inactivity_limit} seconds.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousDesktopApp(root)
    root.mainloop()
