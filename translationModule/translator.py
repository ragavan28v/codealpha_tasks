import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from google.cloud import translate_v2 as translate
from PIL import Image, ImageTk
import keyboard

def create_translate_client():
    try:
        return translate.Client()
    except Exception as e:
        messagebox.showerror("Error", f"Google Cloud API initialization failed:\n{e}")
        return None
class FloatingTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry("70x70+1200+50")
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')

        # Load and display floating icon
        self.icon_image = Image.open("C:\\Users\\HP\\Downloads\\icon1.png").resize((35, 35))
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)

        self.canvas = tk.Canvas(root, width=70, height=70, bg="white", highlightthickness=0)
        self.canvas.create_image(0, 0, anchor="nw", image=self.icon_photo)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.open_translation_window)
        self.dragging = False
        self.canvas.bind("<B1-Motion>", self.move_bubble)

        # Enable hotkey to open the translator (ctrl+shift+t)
        keyboard.add_hotkey("alt+t", self.open_translation_window)

        self.clipboard_history = []
        self.last_clipboard_content = None

    def move_bubble(self, event):
        x = self.root.winfo_x() + event.x
        y = self.root.winfo_y() + event.y
        self.root.geometry(f"70x70+{x}+{y}")

    def open_translation_window(self, event=None):
        if hasattr(self, 'translation_window') and self.translation_window.winfo_exists():
            self.translation_window.deiconify()  # Restore window if already open
            return

        self.translation_window = tk.Toplevel(self.root)
        self.translation_window.title("Translator")

        # Get screen width and height dynamically
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window width and height
        window_width = 380
        window_height = 400

        # Calculate the center position
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2

        # Set new position dynamically at the center
        self.translation_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.translation_window.attributes('-topmost', True)

        # Prevent minimization when clicking outside
        self.translation_window.bind("<FocusOut>", self.minimize_window)

        # Toggle dark mode
        self.is_dark_mode = False
        self.dark_mode_button = tk.Button(self.translation_window, text="🌙", font=("Arial", 16), relief="flat", bg="#444", fg="white", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(pady=5)

        # Source and Translated Text Alignment (One below another)
        frame = tk.Frame(self.translation_window, bg="#222")
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.source_text_label = tk.Label(frame, text="Source Text:", font=("Arial", 12), fg="#fff", bg="#222")
        self.source_text_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_text = tk.Text(frame, height=5, width=50, font=("Arial", 12), bg="#333", fg="#fff", bd=0, wrap="word", insertbackground="white")
        self.source_text.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.source_text.bind("<KeyRelease>", self.update_translation)

        self.translated_text_label = tk.Label(frame, text="Translated Text:", font=("Arial", 12), fg="#fff", bg="#222")
        self.translated_text_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.translated_text = tk.Text(frame, height=5, width=50, font=("Arial", 12), bg="#333", fg="#fff", bd=0, wrap="word", insertbackground="white")
        self.translated_text.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        frame.grid_columnconfigure(0, weight=1)

        # Language and Detected Language (Swapped positions)
        self.language_frame = tk.Frame(self.translation_window, bg="#222")
        self.language_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(self.language_frame, text="Detected Language:", font=("Arial", 10), fg="#fff", bg="#222").pack(side="left", padx=5)
        self.detected_lang_label = tk.Label(self.language_frame, text="Not detected", font=("Arial", 10), fg="#fff", bg="#222")
        self.detected_lang_label.pack(side="left", padx=5)

        tk.Label(self.language_frame, text="Target Language:", font=("Arial", 10), fg="#fff", bg="#222").pack(side="left", padx=5)
        self.target_lang = ttk.Combobox(self.language_frame, values=["en", "ta", "es", "fr", "de", "hi", "zh", "ja"], font=("Arial", 10), width=10, state="readonly", justify="center")
        self.target_lang.pack(side="left", padx=5)
        self.target_lang.set("en")
        self.target_lang.bind("<<ComboboxSelected>>", self.update_translation)
        self.target_lang.bind("<Return>", self.update_translation)

        # Clipboard History Section within the same window
        self.clipboard_frame = tk.Frame(self.translation_window, bg="#222")
        self.clipboard_frame.pack(pady=10, padx=10, fill="x")

        self.clipboard_history_listbox = tk.Listbox(self.clipboard_frame, height=5, width=80, font=("Arial", 10), bg="#333", fg="#fff", bd=0)
        self.clipboard_history_listbox.pack(padx=5, pady=5, fill="x")
        self.clipboard_history_listbox.bind("<Double-1>", self.select_clipboard_text)

        self.check_clipboard()

    def minimize_window(self, event=None):
        if not self.translation_window.focus_get():  # Minimize only if focus is lost
            self.translation_window.withdraw()

    def check_clipboard(self):
        new_text = pyperclip.paste().strip()
        if new_text and new_text != self.last_clipboard_content:
            self.last_clipboard_content = new_text
            self.clipboard_history.append(new_text)
            self.clipboard_history_listbox.insert(tk.END, f"{len(self.clipboard_history)}. {new_text}")
            self.source_text.delete("1.0", tk.END)
            self.source_text.insert(tk.END, new_text)
            self.update_translation()

        # Keep checking clipboard every 1 second for new selections
        self.root.after(1000, self.check_clipboard)

    def update_translation(self, event=None):
        client = create_translate_client()
        if client is None:
            return

        source_text = self.source_text.get("1.0", tk.END).strip()
        if not source_text:
            return

        target_language = self.target_lang.get()

        try:
            result = client.translate(source_text, target_language=target_language)
            translated_text = result["translatedText"]
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, translated_text)

            # Update detected language
            self.detected_lang_label.config(text=result["detectedSourceLanguage"])
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed:\n{e}")

    def toggle_dark_mode(self):
        if not self.is_dark_mode:
            self.translation_window.configure(bg="#1e1e1e")
            self.source_text.configure(bg="#2e2e2e", fg="#ffffff")
            self.translated_text.configure(bg="#2e2e2e", fg="#ffffff")
            self.target_lang.configure(background="#2e2e2e", foreground="#ffffff")
            self.detected_lang_label.configure(bg="#2e2e2e", fg="#ffffff")
            self.clipboard_history_listbox.configure(bg="#2e2e2e", fg="#ffffff")
            self.dark_mode_button.config(bg="#333", fg="#fff")
            self.is_dark_mode = True
        else:
            self.translation_window.configure(bg="white")
            self.source_text.configure(bg="white", fg="black")
            self.translated_text.configure(bg="white", fg="black")
            self.target_lang.configure(background="white", foreground="black")
            self.detected_lang_label.configure(bg="white", fg="black")
            self.clipboard_history_listbox.configure(bg="white", fg="black")
            self.dark_mode_button.config(bg="#444", fg="white")
            self.is_dark_mode = False

    def select_clipboard_text(self, event=None):
        selected_text = self.clipboard_history_listbox.get(tk.ACTIVE).split('. ', 1)[-1]  # Get the actual text
        self.source_text.delete("1.0", tk.END)
        self.source_text.insert(tk.END, selected_text)
        self.update_translation()

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingTranslatorApp(root)
    root.mainloop()