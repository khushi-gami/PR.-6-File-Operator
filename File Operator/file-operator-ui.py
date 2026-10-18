import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk

# -------------------- File Setup --------------------

FOLDER = "File Operator"
FILE_PATH = os.path.join(FOLDER, "journal.txt")
X_DEMO_PATH = os.path.join(FOLDER, "x_mode_demo.txt")
W_DEMO_PATH = os.path.join(FOLDER, "w_mode_demo.txt")


def setup_files():
    """Create folder and journal file (without touching existing entries)."""
    os.makedirs(FOLDER, exist_ok=True)
    with open(FILE_PATH, "a", encoding="utf-8"):
        pass


# -------------------- Journal Logic (no UI here) --------------------

class JournalManager:

    def add_entry(self, entry):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # a mode: append a new entry.
        with open(FILE_PATH, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}]\n")
            file.write(f"{entry}\n\n")

    def read_all(self):
        """Return full file content ('' if file is missing or empty)."""
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def search(self, keyword):
        content = self.read_all()
        keyword = keyword.lower()
        return [
            block.strip()
            for block in content.split("\n\n")
            if block.strip() and keyword in block.lower()
        ]

    def count_entries(self):
        return len([b for b in self.read_all().split("\n\n") if b.strip()])

    def delete_all(self):
        # Delete the actual file instead of clearing its contents.
        if os.path.isfile(FILE_PATH):
            os.remove(FILE_PATH)
            return True
        return False

    def x_mode(self):
        os.makedirs(FOLDER, exist_ok=True)
        # x mode creates a new file only if it does not already exist.
        with open(X_DEMO_PATH, "x", encoding="utf-8") as file:
            file.write("This file demonstrates x mode.\n")

    def w_mode(self):
        os.makedirs(FOLDER, exist_ok=True)
        # w mode creates a file or overwrites its existing content.
        with open(W_DEMO_PATH, "w", encoding="utf-8") as file:
            file.write("This file demonstrates w mode.\n")


# -------------------- GUI --------------------

class JournalApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Personal Journal Manager")
        self.geometry("760x560")
        self.minsize(640, 480)

        self.journal = JournalManager()

        self._build_style()
        self._build_header()
        self._build_tabs()
        self._build_statusbar()

        self.refresh_view()
        self.set_status("Welcome to Personal Journal Manager!")

    # ---------- Layout ----------

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#555")
        style.configure("TButton", padding=6)

    def _build_header(self):
        header = ttk.Frame(self, padding=(12, 10, 12, 4))
        header.pack(fill="x")
        ttk.Label(header, text="Personal Journal Manager", style="Header.TLabel").pack(anchor="w")
        self.count_label = ttk.Label(header, text="", style="Sub.TLabel")
        self.count_label.pack(anchor="w")

    def _build_tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=6)

        self.add_tab = ttk.Frame(self.tabs, padding=12)
        self.view_tab = ttk.Frame(self.tabs, padding=12)
        self.search_tab = ttk.Frame(self.tabs, padding=12)
        self.tools_tab = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.add_tab, text="Add Entry")
        self.tabs.add(self.view_tab, text="View Entries")
        self.tabs.add(self.search_tab, text="Search")
        self.tabs.add(self.tools_tab, text="Tools")

        self._build_add_tab()
        self._build_view_tab()
        self._build_search_tab()
        self._build_tools_tab()

        self.tabs.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _build_add_tab(self):
        ttk.Label(self.add_tab, text="Enter your journal entry:").pack(anchor="w")

        self.entry_text = scrolledtext.ScrolledText(
            self.add_tab, wrap="word", height=10, font=("Segoe UI", 11)
        )
        self.entry_text.pack(fill="both", expand=True, pady=8)

        buttons = ttk.Frame(self.add_tab)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Save Entry", command=self.add_entry).pack(side="left")
        ttk.Button(buttons, text="Clear", command=self.clear_entry_box).pack(side="left", padx=8)

    def _build_view_tab(self):
        self.view_box = scrolledtext.ScrolledText(
            self.view_tab, wrap="word", state="disabled", font=("Consolas", 10)
        )
        self.view_box.pack(fill="both", expand=True)
        ttk.Button(self.view_tab, text="Refresh", command=self.refresh_view).pack(anchor="e", pady=(8, 0))

    def _build_search_tab(self):
        top = ttk.Frame(self.search_tab)
        top.pack(fill="x")
        ttk.Label(top, text="Keyword or date (yyyy-mm-dd):").pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=8)
        search_entry.bind("<Return>", lambda _e: self.search_entries())
        ttk.Button(top, text="Search", command=self.search_entries).pack(side="left")

        self.search_box = scrolledtext.ScrolledText(
            self.search_tab, wrap="word", state="disabled", font=("Consolas", 10)
        )
        self.search_box.pack(fill="both", expand=True, pady=(10, 0))

    def _build_tools_tab(self):
        danger = ttk.LabelFrame(self.tools_tab, text="Danger Zone", padding=10)
        danger.pack(fill="x", pady=(0, 12))
        ttk.Label(danger, text="Permanently delete the journal file and all entries.").pack(anchor="w")
        ttk.Button(danger, text="Delete All Entries", command=self.delete_entries).pack(anchor="w", pady=(6, 0))

        demo = ttk.LabelFrame(self.tools_tab, text="File Mode Demos", padding=10)
        demo.pack(fill="x", pady=(0, 12))
        ttk.Label(
            demo,
            text="x mode: creates a new file, fails if it already exists.\n"
                 "w mode: creates a file or overwrites its existing content.",
            justify="left",
        ).pack(anchor="w")
        row = ttk.Frame(demo)
        row.pack(anchor="w", pady=(6, 0))
        ttk.Button(row, text="Demonstrate x Mode", command=self.demo_x_mode).pack(side="left")
        ttk.Button(row, text="Demonstrate w Mode", command=self.demo_w_mode).pack(side="left", padx=8)

        ttk.Button(self.tools_tab, text="Exit", command=self.exit_app).pack(anchor="w")

    def _build_statusbar(self):
        self.status_var = tk.StringVar()
        bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=(8, 3))
        bar.pack(fill="x", side="bottom")

    # ---------- Helpers ----------

    def set_status(self, message):
        self.status_var.set(message)

    def update_count(self):
        n = self.journal.count_entries()
        self.count_label.config(text=f"{n} entr{'y' if n == 1 else 'ies'} saved")

    @staticmethod
    def _set_text(widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def _on_tab_change(self, _event):
        if self.tabs.select() == str(self.view_tab):
            self.refresh_view()

    # ---------- Actions ----------

    def add_entry(self):
        entry = self.entry_text.get("1.0", "end").strip()
        if not entry:
            messagebox.showwarning("Empty entry", "This field cannot be empty.")
            return
        try:
            self.journal.add_entry(entry)
        except OSError as e:
            messagebox.showerror("Error", f"Could not save entry:\n{e}")
            return
        self.clear_entry_box()
        self.refresh_view()
        self.set_status("Entry added successfully!")
        messagebox.showinfo("Saved", "Entry added successfully!")

    def clear_entry_box(self):
        self.entry_text.delete("1.0", "end")

    def refresh_view(self):
        content = self.journal.read_all()
        if content.strip():
            text = "Your Journal Entries:\n" + "-" * 32 + "\n" + content
        else:
            text = "No journal entries found. Please add some entries."
        self._set_text(self.view_box, text)
        self.update_count()

    def search_entries(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("Empty search", "This field cannot be empty.")
            return

        if not self.journal.read_all().strip():
            self._set_text(self.search_box, "No journal entries found. Please add some entries.")
            self.set_status("Nothing to search.")
            return

        matches = self.journal.search(keyword)
        if matches:
            text = "Matching Entries:\n" + "-" * 32 + "\n" + "\n\n".join(matches)
            self.set_status(f"{len(matches)} match(es) found for '{keyword}'.")
        else:
            text = f"No entries were found for the date or keyword : {keyword}"
            self.set_status("No matches found.")
        self._set_text(self.search_box, text)

    def delete_entries(self):
        if not self.journal.read_all().strip():
            messagebox.showinfo("Delete", "No journal entries to delete.")
            return
        if not messagebox.askyesno(
            "Confirm delete", "Are you sure you want to delete all entries?", icon="warning"
        ):
            self.set_status("Deletion cancelled! Your entries are safe!")
            return
        try:
            self.journal.delete_all()
        except PermissionError:
            messagebox.showerror("PermissionError", "Permission denied during file operation.")
            return
        except OSError as e:
            messagebox.showerror("OSError", str(e))
            return
        self.refresh_view()
        self._set_text(self.search_box, "")
        self.set_status("All journal entries have been deleted.")

    def demo_x_mode(self):
        try:
            self.journal.x_mode()
            self.set_status("File created successfully using x mode.")
            messagebox.showinfo("x mode", "File created successfully using x mode.")
        except FileExistsError:
            messagebox.showwarning(
                "FileExistsError",
                "The x-mode demo file already exists. It was not overwritten.",
            )
        except PermissionError:
            messagebox.showerror("PermissionError", "Permission denied during file operation.")
        except OSError as e:
            messagebox.showerror("OSError", str(e))

    def demo_w_mode(self):
        try:
            self.journal.w_mode()
            self.set_status("Write mode demonstrated successfully.")
            messagebox.showinfo("w mode", "Write mode demonstrated successfully.")
        except PermissionError:
            messagebox.showerror("PermissionError", "Permission denied during file operation.")
        except OSError as e:
            messagebox.showerror("OSError", str(e))

    def exit_app(self):
        if messagebox.askyesno("Exit", "Thank you for using Personal Journal Manager.\nExit now?"):
            self.destroy()


# -------------------- Run --------------------

if __name__ == "__main__":
    setup_files()
    JournalApp().mainloop()