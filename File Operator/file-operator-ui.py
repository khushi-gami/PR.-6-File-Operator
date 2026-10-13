import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Journal file is stored next to this script (folder is created automatically if needed)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOURNAL_DIR = os.path.join(BASE_DIR, "PR. 6 File Operator")
FILE_PATH = os.path.join(JOURNAL_DIR, "journal.txt")

TIMESTAMP_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s*$", re.MULTILINE)


class JournalManager:
    """Handles all file operations (same file format as the console version)."""

    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.isfile(self.path):
            open(self.path, "a", encoding="utf-8").close()

    def add_entry(self, entry):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] \n ")
            f.write(f"{entry} \n\n")

    def get_entries(self):
        """Returns a list of (timestamp, text) tuples."""
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = list(TIMESTAMP_RE.finditer(content))
        entries = []
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            text = content[m.end():end].strip()
            entries.append((m.group(1), text))
        return entries

    def search(self, keyword):
        kw = keyword.lower()
        return [e for e in self.get_entries() if kw in e[0].lower() or kw in e[1].lower()]

    def delete_all(self):
        with open(self.path, "w", encoding="utf-8"):
            pass


class JournalApp(tk.Tk):
    BG = "#f4f6fb"
    PRIMARY = "#4f46e5"
    PRIMARY_DARK = "#4338ca"
    DANGER = "#dc2626"
    DANGER_DARK = "#b91c1c"
    CARD = "#ffffff"
    TEXT = "#1f2937"
    MUTED = "#6b7280"

    def __init__(self):
        super().__init__()
        self.title("Personal Journal Manager")
        self.geometry("820x620")
        self.minsize(700, 520)
        self.configure(bg=self.BG)

        self.manager = JournalManager(FILE_PATH)

        self._setup_styles()
        self._build_header()
        self._build_tabs()
        self._build_statusbar()

        self.refresh_view()

    # ---------- Styling ----------
    def _setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.CARD)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=self.CARD, foreground=self.MUTED, font=("Segoe UI", 9))

        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 8), font=("Segoe UI", 10, "bold"),
                        background="#e5e7eb", foreground=self.MUTED)
        style.map("TNotebook.Tab",
                  background=[("selected", self.CARD)],
                  foreground=[("selected", self.PRIMARY)])

        style.configure("Primary.TButton", background=self.PRIMARY, foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=(16, 8), borderwidth=0)
        style.map("Primary.TButton", background=[("active", self.PRIMARY_DARK)])

        style.configure("Danger.TButton", background=self.DANGER, foreground="white",
                        font=("Segoe UI", 10, "bold"), padding=(16, 8), borderwidth=0)
        style.map("Danger.TButton", background=[("active", self.DANGER_DARK)])

        style.configure("Secondary.TButton", background="#e5e7eb", foreground=self.TEXT,
                        font=("Segoe UI", 10), padding=(14, 8), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#d1d5db")])

        style.configure("TEntry", padding=6)

    # ---------- Layout ----------
    def _build_header(self):
        header = tk.Frame(self, bg=self.PRIMARY, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📓  Personal Journal Manager", bg=self.PRIMARY, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=24)

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(14, 6))

        self.tab_add = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        self.tab_view = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        self.tab_search = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)

        self.notebook.add(self.tab_add, text="➕  Add Entry")
        self.notebook.add(self.tab_view, text="📖  View Entries")
        self.notebook.add(self.tab_search, text="🔍  Search")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self._build_add_tab()
        self._build_view_tab()
        self._build_search_tab()

    def _make_text_area(self, parent, height=15, state="normal"):
        frame = ttk.Frame(parent, style="Card.TFrame")
        text = tk.Text(frame, wrap="word", height=height, font=("Segoe UI", 11),
                       bg="#fafafa", fg=self.TEXT, relief="solid", bd=1,
                       padx=10, pady=10, highlightthickness=0)
        scroll = ttk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        text.configure(state=state)
        return frame, text

    def _build_add_tab(self):
        ttk.Label(self.tab_add, text="Write your journal entry", style="Card.TLabel",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(self.tab_add, text="Date and time are added automatically.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 10))

        frame, self.entry_text = self._make_text_area(self.tab_add, height=14)
        frame.pack(fill="both", expand=True)

        btns = ttk.Frame(self.tab_add, style="Card.TFrame")
        btns.pack(fill="x", pady=(14, 0))
        ttk.Button(btns, text="Save Entry", style="Primary.TButton",
                   command=self.add_entry).pack(side="left")
        ttk.Button(btns, text="Clear", style="Secondary.TButton",
                   command=lambda: self.entry_text.delete("1.0", "end")).pack(side="left", padx=8)

    def _build_view_tab(self):
        top = ttk.Frame(self.tab_view, style="Card.TFrame")
        top.pack(fill="x", pady=(0, 10))
        ttk.Label(top, text="All journal entries", style="Card.TLabel",
                  font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Button(top, text="🗑  Delete All", style="Danger.TButton",
                   command=self.delete_entries).pack(side="right")
        ttk.Button(top, text="⟳ Refresh", style="Secondary.TButton",
                   command=self.refresh_view).pack(side="right", padx=8)

        frame, self.view_text = self._make_text_area(self.tab_view, state="disabled")
        frame.pack(fill="both", expand=True)
        self._configure_tags(self.view_text)

    def _build_search_tab(self):
        ttk.Label(self.tab_search, text="Search by keyword or date (yyyy-mm-dd)",
                  style="Card.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        row = ttk.Frame(self.tab_search, style="Card.TFrame")
        row.pack(fill="x", pady=(0, 10))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(row, textvariable=self.search_var, font=("Segoe UI", 11))
        entry.pack(side="left", fill="x", expand=True, ipady=3)
        entry.bind("<Return>", lambda e: self.search_entry())
        ttk.Button(row, text="Search", style="Primary.TButton",
                   command=self.search_entry).pack(side="left", padx=(8, 0))

        self.search_info = ttk.Label(self.tab_search, text="", style="Muted.TLabel")
        self.search_info.pack(anchor="w", pady=(0, 6))

        frame, self.search_text = self._make_text_area(self.tab_search, state="disabled")
        frame.pack(fill="both", expand=True)
        self._configure_tags(self.search_text)

    def _build_statusbar(self):
        self.status = tk.StringVar(value="Ready")
        bar = tk.Label(self, textvariable=self.status, anchor="w", bg="#e5e7eb",
                       fg=self.MUTED, font=("Segoe UI", 9), padx=12, pady=4)
        bar.pack(fill="x", side="bottom")

    def _configure_tags(self, widget):
        widget.tag_configure("ts", foreground=self.PRIMARY, font=("Segoe UI", 10, "bold"))
        widget.tag_configure("body", foreground=self.TEXT, font=("Segoe UI", 11),
                             lmargin1=10, lmargin2=10)
        widget.tag_configure("sep", foreground="#d1d5db")
        widget.tag_configure("empty", foreground=self.MUTED, font=("Segoe UI", 11, "italic"))
        widget.tag_configure("hit", background="#fde68a")

    # ---------- Helpers ----------
    def _show_entries(self, widget, entries, highlight=None):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        for ts, body in entries:
            widget.insert("end", f"🕒 {ts}\n", "ts")
            start = widget.index("end-1c")
            widget.insert("end", f"{body}\n", "body")
            if highlight:
                self._highlight(widget, start, highlight)
            widget.insert("end", "─" * 70 + "\n\n", "sep")
        widget.configure(state="disabled")

    def _highlight(self, widget, start, word):
        idx = start
        while True:
            idx = widget.search(word, idx, stopindex="end", nocase=True)
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            widget.tag_add("hit", idx, end)
            idx = end

    def _show_message(self, widget, message):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", message, "empty")
        widget.configure(state="disabled")

    def _on_tab_change(self, _event):
        if self.notebook.index("current") == 1:
            self.refresh_view()

    # ---------- Actions ----------
    def add_entry(self):
        entry = self.entry_text.get("1.0", "end").strip()
        if not entry:
            messagebox.showwarning("Empty entry", "This field cannot be empty.")
            return
        try:
            self.manager.add_entry(entry)
        except PermissionError:
            messagebox.showerror("Permission denied", "Permission denied while writing to the journal file.")
            return
        except OSError as e:
            messagebox.showerror("Error", f"OSError : {e}")
            return

        self.entry_text.delete("1.0", "end")
        self.status.set("Entry added successfully!")
        messagebox.showinfo("Success", "Entry added successfully!")
        self.refresh_view()

    def refresh_view(self):
        try:
            entries = self.manager.get_entries()
        except PermissionError:
            self._show_message(self.view_text, "Permission denied while reading the journal file.")
            return
        except OSError as e:
            self._show_message(self.view_text, f"OSError : {e}")
            return

        if not entries:
            self._show_message(self.view_text,
                               "No journal entries found. Please add some entries to view them.")
        else:
            self._show_entries(self.view_text, entries)
        self.status.set(f"{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} in journal")

    def search_entry(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("Empty search", "This field cannot be empty.")
            return

        try:
            if not self.manager.get_entries():
                self.search_info.config(text="")
                self._show_message(self.search_text,
                                   "No journal entries found. Please add some entries to search.")
                return
            results = self.manager.search(keyword)
        except PermissionError:
            messagebox.showerror("Permission denied", "Permission denied while searching the journal file.")
            return
        except OSError as e:
            messagebox.showerror("Error", f"OSError : {e}")
            return

        if results:
            self.search_info.config(text=f"{len(results)} matching entr{'y' if len(results) == 1 else 'ies'} found")
            self._show_entries(self.search_text, results, highlight=keyword)
        else:
            self.search_info.config(text="")
            self._show_message(self.search_text,
                               f"No entries were found for the date or keyword : {keyword}")
        self.status.set(f"Search done for '{keyword}'")

    def delete_entries(self):
        try:
            if not self.manager.get_entries():
                messagebox.showinfo("Nothing to delete",
                                    "No journal entries to delete. Please add some entries first.")
                return
        except OSError as e:
            messagebox.showerror("Error", f"OSError : {e}")
            return

        if messagebox.askyesno("Confirm delete",
                               "Are you sure you want to delete all entries?\nThis cannot be undone.",
                               icon="warning"):
            try:
                self.manager.delete_all()
            except PermissionError:
                messagebox.showerror("Permission denied", "Permission denied while deleting journal entries.")
                return
            except OSError as e:
                messagebox.showerror("Error", f"OSError : {e}")
                return
            self.status.set("All journal entries have been deleted.")
            messagebox.showinfo("Deleted", "All journal entries have been deleted.")
            self.refresh_view()
            self._show_message(self.search_text, "")
            self.search_info.config(text="")
        else:
            self.status.set("Deletion cancelled! Your entries are safe!")


if __name__ == "__main__":
    JournalApp().mainloop()