import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import font
import threading


class SpotlightDownloaderApp(tb.Window):
    def __init__(self, start_callback=None):
        self.current_theme = "flatly"  # light theme by default
        super().__init__(themename=self.current_theme)
        self.withdraw()
        self.title("Windows Spotlight Downloader")
        self.minsize(800, 600)
        self.start_callback = start_callback
        self.center_window()
        self.deiconify()
        self.start_font = font.Font(family="Tahoma", size=16, weight="bold")
        self.create_widgets()
        self.working_colors = ["red", "orange", "magenta", "purple", "blue", "#FFA500", "#8A2BE2", "#20B2AA", "#FF69B4"]
        self.working_color_index = 0
        self.working_animation_running = True
        self.setup_context_menu()
        self.working_status = False
        self.configure_custom_styles()
        # Bind the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_custom_styles(self):
        # Redefine custom styles
        self.style.configure("success.TButton", font=self.start_font)
        self.style.configure("Red.TFrame", background="lightcoral")
        self.style.configure("Blue.TFrame", background="lightblue")
        self.style.configure("Green.TFrame", background="lightgreen")
        # Style when working
        self.style.configure("working.TButton", font=self.start_font)
        self.style.map("working.TButton", foreground=[("disabled", "red")])
        self.style.configure("working_dynamic.TButton", font=self.start_font)
        self.style.map("working_dynamic.TButton", foreground=[("disabled", "red")])  # initial color
        self.style.configure(
            "done.TButton",
            font=self.start_font,
            foreground="blue",
            background="lightblue",
            bordercolor="#2196F3",
            borderwidth=2,
            relief="ridge",
        )

        self.style.map(
            "done.TButton",
            foreground=[("disabled", "blue")],
            bordercolor=[("disabled", "#2196F3")],
            background=[("disabled", "lightblue")],
        )

        if self.dark_mode_var.get():
            self.log_text.config(bg="#2b2b2b", fg="white", insertbackground="white", state="normal")
            self.log_text.tag_configure("even", background="#333333")
            self.log_text.tag_configure("odd", background="#2b2b2b")
            self.log_text.tag_config("sel", foreground="#f5f789")
        else:
            self.log_text.config(bg="white", fg="black", insertbackground="black", state="normal")
            self.log_text.tag_configure("even", background="#f0f0f0")
            self.log_text.tag_configure("odd", background="#ffffff")
            # Highlight selected text
            self.log_text.tag_config("sel", foreground="#002fff")

        self.log_text.config(state="disabled")

    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            new_theme = "darkly"  # dark theme
        else:
            new_theme = "flatly"  # light theme

        self.style.theme_use(new_theme)
        self.current_theme = new_theme
        self.configure_custom_styles()

    def on_closing(self):
        if self.working_status:
            result = messagebox.askyesno("Confirm Exit", "Program is working.\nAre you sure you want to exit?")
            if result:
                self.destroy()
        else:
            self.destroy()

    def animate_working(self):
        if not self.working_animation_running:
            return

        # Get the current color
        current_color = self.working_colors[self.working_color_index]
        style_name = "working_dynamic.TButton"
        self.style.configure(style_name, font=self.start_font)
        self.style.map(style_name, foreground=[("disabled", current_color)])

        self.start_button.config(style=style_name)

        # Change the color
        self.working_color_index = (self.working_color_index + 1) % len(self.working_colors)

        # Reschedule the next animation
        self.start_button.after(500, self.animate_working)

    def add_log_line(self, *args):
        self.log_text.config(state="normal")
        message = " ".join(str(arg) for arg in args)
        line_count = int(self.log_text.index("end-1c").split(".")[0])
        tag_name = "even" if line_count % 2 == 0 else "odd"
        self.log_text.insert("end", message + "\n", tag_name)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def on_start(self):
        if self.start_callback:
            for child in self.mode_frame.winfo_children():
                if isinstance(child, tb.Radiobutton):
                    child.configure(state="disabled")

            self.start_button.config(text="Working...", state="disabled")
            self.working_status = True
            self.working_animation_running = True
            self.working_color_index = 0
            self.animate_working()
            threading.Thread(target=self.start_callback).start()

    def center_window(self):
        self.update_idletasks()
        width = 800
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_selection(self):
        try:
            selected_text = self.log_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.log_text.clipboard_clear()
            self.log_text.clipboard_append(selected_text)
        except tk.TclError:
            pass  # Nothing selected

    def select_all_and_copy(self):
        self.log_text.tag_add("sel", "1.0", "end-1c")  # select all
        self.copy_selection()

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.log_text, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selection)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All & Copy", command=self.select_all_and_copy)
        self.log_text.bind("<Button-3>", self.show_context_menu)  # right-click

    def create_widgets(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Stylish Elements
        # style = tb.Style()

        # Top Frame
        top_frame = tb.Frame(self)
        top_frame.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)

        # Start button with style
        self.start_button = tb.Button(top_frame, text="Start", bootstyle="success", width=10, command=self.on_start)
        self.start_button.grid(row=0, column=2, sticky="nesw", padx=(0, 0), pady=(8, 0))

        # Mode Frame
        self.mode_frame = tb.LabelFrame(top_frame, text="   Mode Selector   ")
        self.mode_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)

        self.mode_var = tk.StringVar(value="both")

        rb1 = tb.Radiobutton(
            self.mode_frame,
            text="Both (Landscape And Portrait)",
            variable=self.mode_var,
            value="both",
        )
        rb2 = tb.Radiobutton(self.mode_frame, text="Landscape Only", variable=self.mode_var, value="landscape")
        rb3 = tb.Radiobutton(self.mode_frame, text="Portrait Only", variable=self.mode_var, value="portrait")

        rb1.grid(row=0, column=0, padx=10, pady=5, ipadx=12, ipady=5, sticky="w")
        rb2.grid(row=0, column=1, padx=10, pady=5, ipadx=12, ipady=5, sticky="w")
        rb3.grid(row=0, column=2, padx=10, pady=5, ipadx=12, ipady=5, sticky="w")

        self.dark_mode_var = tk.BooleanVar(value=False)
        dark_mode_switch = tb.Checkbutton(
            top_frame,
            text="Dark Mode",
            variable=self.dark_mode_var,
            command=self.toggle_dark_mode,
            bootstyle="square-toggle",
        )
        dark_mode_switch.grid(row=0, column=1, padx=15, sticky="nesw", pady=(8, 0))

        # Log Frame
        log_frame = tb.LabelFrame(self, text="   Log   ")
        log_frame.grid(row=1, column=0, rowspan=4, sticky="nsew", padx=10, pady=(0, 10))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        # Container Frame for Textbox و Scrollbar
        log_container = tb.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_container.rowconfigure(0, weight=1)
        log_container.columnconfigure(0, weight=1)

        self.log_text = tk.Text(log_container, height=10, wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar beside Textbox
        self.scrollbar = tb.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Connecting scrollbar to Textbox
        self.log_text.config(yscrollcommand=self.scrollbar.set)


if __name__ == "__main__":
    app = SpotlightDownloaderApp()
    app.mainloop()
