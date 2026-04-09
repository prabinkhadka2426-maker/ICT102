import tkinter as tk
from tkinter import ttk, messagebox
import datetime


# ═══════════════════════════════════════════════════════════════
#  COLOUR PALETTE  – Warm Ivory + Midnight Gold
# ═══════════════════════════════════════════════════════════════
C = {
    "bg":         "#FAF7F2",
    "sidebar":    "#1C1A14",
    "sidebar_h":  "#2C2920",
    "panel":      "#FFFFFF",
    "panel2":     "#F5F1EA",
    "gold":       "#C9A84C",
    "gold_light": "#E8C97A",
    "gold_dk":    "#A07830",
    "green":      "#2E7D52",
    "green_bg":   "#EAF7F0",
    "red":        "#C0392B",
    "red_bg":     "#FDEEEC",
    "blue":       "#2563EB",
    "text":       "#1A1612",
    "text2":      "#6B6456",
    "text3":      "#9C9080",
    "border":     "#E5DDD0",
    "border2":    "#D0C8B8",
    "row_odd":    "#FAF7F2",
    "row_even":   "#F5F1EA",
    "select":     "#FDF3DC",
    "shadow":     "#D0C8B8",
}

FONT_TITLE  = ("Georgia",       20, "bold")
FONT_HEAD   = ("Georgia",       13, "bold")
FONT_SUB    = ("Georgia",       10, "italic")
FONT_BODY   = ("Helvetica",     10)
FONT_BODY_B = ("Helvetica",     10, "bold")
FONT_MONO   = ("Courier New",    9)
FONT_NAV    = ("Helvetica",     11)
FONT_NAV_B  = ("Helvetica",     11, "bold")
FONT_BTN    = ("Helvetica",     10, "bold")
FONT_BADGE  = ("Helvetica",      8, "bold")

GENRES = ["Fiction", "Non-Fiction", "Science", "History",
          "Technology", "Biography", "Mystery", "Other"]


# ═══════════════════════════════════════════════════════════════
#  DATA STORE
# ═══════════════════════════════════════════════════════════════
books:      list = []
borrow_log: list = []


# ═══════════════════════════════════════════════════════════════
#  HELPERS – Data-type checks
# ═══════════════════════════════════════════════════════════════
def is_valid_string(value: str) -> bool:
    """Return True only when value is a non-empty string."""
    return isinstance(value, str) and len(value.strip()) > 0


def is_valid_year(value: str) -> bool:
    """Return True only when value is a 4-digit numeric year."""
    if not isinstance(value, str):
        return False
    return value.strip().isdigit() and 1000 <= int(value.strip()) <= datetime.date.today().year


# ═══════════════════════════════════════════════════════════════
#  CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def add_book(title: str, author: str, genre: str, year: str) -> str:
    """
    Validate inputs then append a new book dict to the global list.
    Demonstrates: if/elif, for loop, match/case, operators.
    """
    if not is_valid_string(title):
        return "ERROR: Title cannot be empty."
    elif not is_valid_string(author):
        return "ERROR: Author cannot be empty."
    elif not is_valid_year(year):
        return "ERROR: Year must be a valid number (e.g. 2020)."

    # FOR loop – duplicate check (case-insensitive)
    for book in books:
        if book["title"].lower() == title.strip().lower():
            return f"ERROR: '{title}' already exists in the library."

    # match / case
    match genre:
        case "Fiction":     code = "FIC"
        case "Non-Fiction": code = "NFC"
        case "Science":     code = "SCI"
        case "History":     code = "HIS"
        case "Technology":  code = "TEC"
        case "Biography":   code = "BIO"
        case "Mystery":     code = "MYS"
        case _:             code = "OTH"

    book_id = f"{code}-{len(books) + 1:03d}"

    books.append({
        "id":          book_id,
        "title":       title.strip(),
        "author":      author.strip(),
        "genre":       genre,
        "year":        int(year.strip()),
        "available":   True,
        "borrowed_by": None,
        "borrow_date": None,
    })
    return f"SUCCESS: '{title.strip()}' added with ID {book_id}."


def view_books(filter_genre: str = "All",
               filter_available: str = "All") -> list:
    """Return filtered book list."""
    result = []
    for book in books:
        if filter_genre != "All" and book["genre"] != filter_genre:
            continue
        if filter_available == "Available" and not book["available"]:
            continue
        if filter_available == "Borrowed" and book["available"]:
            continue
        result.append(book)
    return result


def borrow_book(book_id: str, borrower_name: str) -> str:
    """Mark a book as borrowed."""
    if not is_valid_string(borrower_name):
        return "ERROR: Borrower name cannot be empty."

    target = None
    index  = 0

    while index < len(books):
        if books[index]["id"] == book_id:
            target = books[index]
            break
        index += 1

    if target is None:
        return f"ERROR: Book ID '{book_id}' not found."
    elif not target["available"]:
        return f"ERROR: Already borrowed by {target['borrowed_by']}."
    else:
        target["available"]   = False
        target["borrowed_by"] = borrower_name.strip()
        target["borrow_date"] = datetime.date.today().isoformat()

        borrow_log.append({
            "action":  "BORROW",
            "book_id": book_id,
            "title":   target["title"],
            "person":  borrower_name.strip(),
            "date":    target["borrow_date"],
        })
        return f"SUCCESS: '{target['title']}' borrowed by {borrower_name.strip()}."


def return_book(book_id: str) -> str:
    """Mark a book as returned."""
    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                return f"ERROR: '{book['title']}' is already in the library."

            prev = book["borrowed_by"]
            book["available"]   = True
            book["borrowed_by"] = None
            book["borrow_date"] = None

            borrow_log.append({
                "action":  "RETURN",
                "book_id": book_id,
                "title":   book["title"],
                "person":  prev,
                "date":    datetime.date.today().isoformat(),
            })
            return f"SUCCESS: '{book['title']}' returned by {prev}."
    return f"ERROR: Book ID '{book_id}' not found."


def search_books(keyword: str) -> list:
    """Search by title, author, or genre."""
    kw = keyword.strip().lower()
    results = []
    for book in books:
        for field in ["title", "author", "genre"]:
            if kw in str(book[field]).lower():
                if book not in results:
                    results.append(book)
                break
    return results


def get_statistics() -> dict:
    """Return counts."""
    total = available = borrowed = 0
    for book in books:
        total += 1
        if book["available"]:
            available += 1
        else:
            borrowed += 1
    return {"total": total, "available": available, "borrowed": borrowed}


# ═══════════════════════════════════════════════════════════════
#  GUI HELPERS
# ═══════════════════════════════════════════════════════════════

def _styled_button(parent, text, command, style="gold",
                   padx=18, pady=8, font=FONT_BTN):
    """Factory for consistently styled buttons."""
    palettes = {
        "gold":  (C["gold"],   C["text"],  C["gold_dk"]),
        "green": (C["green"],  "#FFFFFF",  "#1A5C38"),
        "red":   (C["red"],    "#FFFFFF",  "#922B21"),
        "ghost": (C["panel2"], C["text2"], C["border"]),
    }
    bg, fg, hover = palettes.get(style, palettes["gold"])

    btn = tk.Label(parent, text=text, bg=bg, fg=fg,
                   font=font, cursor="hand2",
                   padx=padx, pady=pady,
                   relief="flat")
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>",    lambda e: btn.config(bg=hover))
    btn.bind("<Leave>",    lambda e: btn.config(bg=bg))
    return btn


def _badge(parent, text, kind="available"):
    bg = C["green_bg"] if kind == "available" else C["red_bg"]
    fg = C["green"]    if kind == "available" else C["red"]
    return tk.Label(parent, text=text, bg=bg, fg=fg,
                    font=FONT_BADGE, padx=6, pady=2, relief="flat")


# ═══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

class LibraryApp:
    """Tkinter GUI – Warm Ivory / Midnight Gold theme."""

    _active_nav: tk.Frame = None   # tracks currently highlighted nav frame

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📚  Library Book Manager  —  ICT102")
        self.root.geometry("1160x720")
        self.root.minsize(960, 620)
        self.root.configure(bg=C["bg"])

        self._configure_ttk_styles()
        self._load_sample_data()
        self._build_layout()
        # Show dashboard without going through the nav click cycle
        self._activate_nav(0)
        self._render_dashboard()

    # ── TTK style sheet ───────────────────────────────────────
    def _configure_ttk_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("Lib.Treeview",
                    background=C["row_even"],
                    fieldbackground=C["row_even"],
                    foreground=C["text"],
                    rowheight=32,
                    font=FONT_BODY,
                    bordercolor=C["border"],
                    relief="flat")
        s.configure("Lib.Treeview.Heading",
                    background=C["panel2"],
                    foreground=C["gold_dk"],
                    font=FONT_BODY_B,
                    relief="flat",
                    padding=(8, 6))
        s.map("Lib.Treeview",
              background=[("selected", C["select"])],
              foreground=[("selected", C["text"])])

        s.configure("Lib.Vertical.TScrollbar",
                    background=C["panel2"],
                    troughcolor=C["bg"],
                    bordercolor=C["border"],
                    arrowcolor=C["text3"],
                    relief="flat")

        s.configure("Lib.TCombobox",
                    fieldbackground=C["panel"],
                    background=C["panel"],
                    foreground=C["text"],
                    selectbackground=C["select"],
                    selectforeground=C["text"],
                    font=FONT_BODY)
        s.map("Lib.TCombobox",
              fieldbackground=[("readonly", C["panel"])],
              background=[("readonly", C["panel"])])

    # ── Sample seed data ──────────────────────────────────────
    def _load_sample_data(self):
        samples = [
            ("The Great Gatsby",        "F. Scott Fitzgerald", "Fiction",     "1925"),
            ("A Brief History of Time", "Stephen Hawking",     "Science",     "1988"),
            ("Clean Code",              "Robert C. Martin",    "Technology",  "2008"),
            ("Sapiens",                 "Yuval Noah Harari",   "History",     "2011"),
            ("Gone Girl",               "Gillian Flynn",       "Mystery",     "2012"),
            ("Steve Jobs",              "Walter Isaacson",     "Biography",   "2011"),
            ("Atomic Habits",           "James Clear",         "Non-Fiction", "2018"),
        ]
        for args in samples:
            add_book(*args)

    # ─────────────────────────────────────────────────────────
    #  LAYOUT SKELETON
    # ─────────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=C["sidebar"], width=230)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg=C["sidebar"], pady=28)
        logo_frame.pack(fill="x")

        tk.Label(logo_frame, text="📚", font=("Helvetica", 28),
                 bg=C["sidebar"], fg=C["gold"]).pack()
        tk.Label(logo_frame, text="Library",
                 font=("Georgia", 17, "bold"),
                 bg=C["sidebar"], fg=C["gold_light"]).pack()
        tk.Label(logo_frame, text="Book Manager",
                 font=("Georgia", 10, "italic"),
                 bg=C["sidebar"], fg=C["text3"]).pack()

        tk.Frame(self.sidebar, bg=C["gold_dk"], height=1).pack(fill="x", padx=20, pady=4)

        tk.Label(self.sidebar, text="M E N U",
                 font=("Helvetica", 8, "bold"),
                 bg=C["sidebar"], fg=C["text3"],
                 padx=20).pack(anchor="w", pady=(14, 6))

        # Nav items – commands call _switch_page to avoid recursion
        self._nav_items = []
        nav_defs = [
            ("🏠", "Dashboard",   self._render_dashboard),
            ("📋", "All Books",   self._render_view_books),
            ("➕", "Add Book",    self._render_add_book),
            ("📤", "Borrow Book", self._render_borrow),
            ("📥", "Return Book", self._render_return),
            ("🔍", "Search",      self._render_search),
            ("📜", "History",     self._render_history),
        ]

        for idx, (icon, label, cmd) in enumerate(nav_defs):
            self._make_nav_item(icon, label, cmd, idx)

        tk.Frame(self.sidebar, bg=C["gold_dk"], height=1).pack(
            fill="x", padx=20, pady=(16, 0))
        tk.Label(self.sidebar,
                 text="ICT102  •  Mini Project",
                 font=("Helvetica", 8), bg=C["sidebar"],
                 fg=C["text3"]).pack(pady=12)

        # Main content area
        self.main = tk.Frame(self.root, bg=C["bg"])
        self.main.pack(fill="both", expand=True)

        self.topbar = tk.Frame(self.main, bg=C["panel"], height=56)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        tk.Frame(self.main, bg=C["gold"], height=2).pack(fill="x")

        self.page_title_var = tk.StringVar(value="Dashboard")
        self.topbar_title = tk.Label(self.topbar,
                                     textvariable=self.page_title_var,
                                     font=("Georgia", 14, "bold"),
                                     bg=C["panel"], fg=C["text"],
                                     padx=24)
        self.topbar_title.pack(side="left", fill="y")

        self.stat_var = tk.StringVar()
        tk.Label(self.topbar, textvariable=self.stat_var,
                 font=FONT_MONO, bg=C["panel"],
                 fg=C["text3"], padx=20).pack(side="right", fill="y")

        # Scrollable content canvas
        self.canvas = tk.Canvas(self.main, bg=C["bg"], highlightthickness=0)
        self.vsb = ttk.Scrollbar(self.main, orient="vertical",
                                 style="Lib.Vertical.TScrollbar",
                                 command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=C["bg"])
        self._canvas_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw")

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.content.bind("<Configure>", self._on_frame_configure)

        # Mouse-wheel scrolling (cross-platform)
        self.canvas.bind_all("<MouseWheel>",   self._on_mousewheel)
        self.canvas.bind_all("<Button-4>",     self._on_mousewheel)
        self.canvas.bind_all("<Button-5>",     self._on_mousewheel)

        # Status bar
        sb = tk.Frame(self.root, bg=C["panel2"], height=26)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        tk.Frame(sb, bg=C["gold"], width=3).pack(side="left", fill="y")
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(sb, textvariable=self.status_var,
                 font=FONT_MONO, bg=C["panel2"],
                 fg=C["text3"], padx=10).pack(side="left", fill="y")

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Scroll canvas with mouse wheel – works on Windows, macOS, Linux."""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Sidebar nav item factory ──────────────────────────────
    def _make_nav_item(self, icon: str, label: str, command, index: int):
        frame = tk.Frame(self.sidebar, bg=C["sidebar"], cursor="hand2")
        frame.pack(fill="x", padx=12, pady=2)

        icon_lbl = tk.Label(frame, text=icon,
                            font=("Helvetica", 13),
                            bg=C["sidebar"], fg=C["text3"], width=2)
        icon_lbl.pack(side="left", padx=(8, 0), pady=10)

        text_lbl = tk.Label(frame, text=label,
                            font=FONT_NAV,
                            bg=C["sidebar"], fg=C["text3"], anchor="w")
        text_lbl.pack(side="left", padx=8, fill="x", expand=True)

        accent = tk.Frame(frame, bg=C["sidebar"], width=3)
        accent.pack(side="right", fill="y")

        def on_click(event=None):
            self._activate_nav(index)
            command()

        def on_enter(event=None):
            if self._active_nav is not frame:
                frame.config(bg=C["sidebar_h"])
                icon_lbl.config(bg=C["sidebar_h"])
                text_lbl.config(bg=C["sidebar_h"])

        def on_leave(event=None):
            if self._active_nav is not frame:
                frame.config(bg=C["sidebar"])
                icon_lbl.config(bg=C["sidebar"])
                text_lbl.config(bg=C["sidebar"])

        for widget in (frame, icon_lbl, text_lbl):
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>",    on_enter)
            widget.bind("<Leave>",    on_leave)

        # Store tuple: (frame, icon_lbl, text_lbl, accent)
        self._nav_items.append((frame, icon_lbl, text_lbl, accent))

    def _activate_nav(self, index: int):
        """
        Visually highlight nav item at `index`.
        Only updates styling – does NOT call any page command.
        This breaks the recursion that existed in the original code.
        """
        for i, (frame, icon_lbl, text_lbl, accent) in enumerate(self._nav_items):
            if i == index:
                frame.config(bg=C["sidebar_h"])
                icon_lbl.config(bg=C["sidebar_h"], fg=C["gold_light"])
                text_lbl.config(bg=C["sidebar_h"], fg=C["gold_light"], font=FONT_NAV_B)
                accent.config(bg=C["gold"])
                self._active_nav = frame
            else:
                # Only reset items that are not already in their default state
                if self._active_nav is not frame:
                    frame.config(bg=C["sidebar"])
                    icon_lbl.config(bg=C["sidebar"], fg=C["text3"])
                    text_lbl.config(bg=C["sidebar"], fg=C["text3"], font=FONT_NAV)
                    accent.config(bg=C["sidebar"])

    # ── Utility helpers ───────────────────────────────────────
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        # Reset scroll position to top on page change
        self.canvas.yview_moveto(0)

    def _set_page_title(self, title: str):
        self.page_title_var.set(title)

    def _update_stats(self):
        s = get_statistics()
        self.stat_var.set(
            f"Total: {s['total']}    Available: {s['available']}    Borrowed: {s['borrowed']}")

    def _set_status(self, msg: str, ok: bool = True):
        self.status_var.set(f"  {msg}")

    def _section_label(self, parent, text: str, sub: str = ""):
        tk.Label(parent, text=text,
                 font=FONT_HEAD, bg=C["panel"],
                 fg=C["text"]).pack(anchor="w")
        if sub:
            tk.Label(parent, text=sub,
                     font=FONT_SUB, bg=C["panel"],
                     fg=C["text3"]).pack(anchor="w", pady=(0, 12))
        else:
            tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", pady=8)

    def _input_row(self, parent, label: str):
        """Returns (row_frame, StringVar)."""
        row = tk.Frame(parent, bg=C["panel"])
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, width=13, anchor="w",
                 font=FONT_BODY_B, bg=C["panel"],
                 fg=C["text2"]).pack(side="left")
        var = tk.StringVar()
        ent = tk.Entry(row, textvariable=var, width=34,
                       bg=C["panel2"], fg=C["text"],
                       insertbackground=C["gold"],
                       relief="flat", font=FONT_BODY,
                       highlightthickness=1,
                       highlightcolor=C["gold"],
                       highlightbackground=C["border"])
        ent.pack(side="left", ipady=7, padx=(0, 4))
        return row, var

    def _combo_row(self, parent, label: str, values: list):
        row = tk.Frame(parent, bg=C["panel"])
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, width=13, anchor="w",
                 font=FONT_BODY_B, bg=C["panel"],
                 fg=C["text2"]).pack(side="left")
        var = tk.StringVar(value=values[0])
        cb = ttk.Combobox(row, textvariable=var, values=values,
                          state="readonly", width=32,
                          style="Lib.TCombobox", font=FONT_BODY)
        cb.pack(side="left", ipady=4)
        return row, var

    def _scrollable_listbox(self, parent, items: list,
                             fg=C["text"], select_bg=C["select"]):
        """Returns (frame, listbox)."""
        frame = tk.Frame(parent, bg=C["panel"],
                         highlightthickness=1,
                         highlightbackground=C["border"])
        frame.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical",
                           style="Lib.Vertical.TScrollbar")
        sb.pack(side="right", fill="y")

        lb = tk.Listbox(frame, bg=C["panel2"], fg=fg,
                        selectbackground=select_bg,
                        selectforeground=C["text"],
                        font=FONT_BODY, relief="flat",
                        yscrollcommand=sb.set,
                        activestyle="none",
                        selectmode="single",
                        borderwidth=0)
        sb.config(command=lb.yview)
        lb.pack(fill="both", expand=True)

        for item in items:
            lb.insert("end", item)
        return frame, lb

    def _treeview(self, parent, cols: tuple, widths: tuple):
        """Returns (frame, tree)."""
        frame = tk.Frame(parent, bg=C["panel"])
        frame.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical",
                           style="Lib.Vertical.TScrollbar")
        sb.pack(side="right", fill="y")

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Lib.Treeview",
                            yscrollcommand=sb.set)
        sb.config(command=tree.yview)

        tree.tag_configure("odd",           background=C["row_odd"])
        tree.tag_configure("even",          background=C["row_even"])
        tree.tag_configure("available",     foreground=C["green"])
        tree.tag_configure("borrowed",      foreground=C["red"])
        tree.tag_configure("borrow_action", foreground="#B7700A")
        tree.tag_configure("return_action", foreground=C["green"])

        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w,
                        anchor="center" if col in
                        ("ID", "Year", "Status", "Action", "Date") else "w")

        tree.pack(fill="both", expand=True)
        return frame, tree

    # ═══════════════════════════════════════════════════════
    #  PAGE RENDERERS
    #  All page methods are prefixed _render_* to make it
    #  clear they only draw content; they do NOT activate nav.
    # ═══════════════════════════════════════════════════════

    # ── DASHBOARD ─────────────────────────────────────────
    def _render_dashboard(self):
        self._clear_content()
        self._set_page_title("Dashboard")
        self._update_stats()

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        # Stat cards row
        stats_row = tk.Frame(outer, bg=C["bg"])
        stats_row.pack(fill="x", pady=(0, 20))

        s = get_statistics()
        stat_defs = [
            ("📚", "Total Books",   str(s["total"]),       C["gold"]),
            ("✅", "Available",     str(s["available"]),   C["green"]),
            ("📤", "Currently Out", str(s["borrowed"]),    C["red"]),
            ("📜", "Transactions",  str(len(borrow_log)),  C["blue"]),
        ]

        for icon, label, value, colour in stat_defs:
            card = tk.Frame(stats_row, bg=C["panel"],
                            highlightthickness=1,
                            highlightbackground=C["border"])
            card.pack(side="left", fill="x", expand=True, padx=(0, 14))

            tk.Frame(card, bg=colour, width=4).pack(side="left", fill="y")

            inner = tk.Frame(card, bg=C["panel"], padx=18, pady=16)
            inner.pack(fill="both", expand=True)

            tk.Label(inner, text=icon, font=("Helvetica", 18),
                     bg=C["panel"], fg=colour).pack(anchor="w")
            tk.Label(inner, text=value,
                     font=("Georgia", 26, "bold"),
                     bg=C["panel"], fg=C["text"]).pack(anchor="w")
            tk.Label(inner, text=label, font=FONT_BODY,
                     bg=C["panel"], fg=C["text3"]).pack(anchor="w")

        # Recent activity + Quick actions
        bottom = tk.Frame(outer, bg=C["bg"])
        bottom.pack(fill="both", expand=True)

        left_panel = tk.Frame(bottom, bg=C["panel"],
                              highlightthickness=1,
                              highlightbackground=C["border"])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 14))

        tk.Label(left_panel, text="Recent Books",
                 font=FONT_HEAD, bg=C["panel"],
                 fg=C["text"], padx=20, pady=14).pack(anchor="w")
        tk.Frame(left_panel, bg=C["border"], height=1).pack(fill="x")

        recent = books[-5:][::-1]
        for book in recent:
            row = tk.Frame(left_panel, bg=C["panel"], padx=20, pady=10)
            row.pack(fill="x")
            tk.Label(row, text=book["title"],
                     font=FONT_BODY_B, bg=C["panel"],
                     fg=C["text"]).pack(anchor="w")
            tk.Label(row,
                     text=f"{book['author']}  •  {book['genre']}  •  {book['year']}",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"]).pack(anchor="w")
            status_text = "Available" if book["available"] else "Borrowed"
            kind = "available" if book["available"] else "borrowed"
            _badge(row, status_text, kind).pack(anchor="w", pady=(2, 0))
            tk.Frame(left_panel, bg=C["border"], height=1).pack(fill="x", padx=20)

        if not recent:
            tk.Label(left_panel,
                     text="No books in library yet.",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"], pady=20).pack()

        # Quick-actions panel
        right_panel = tk.Frame(bottom, bg=C["panel"],
                               highlightthickness=1,
                               highlightbackground=C["border"],
                               width=200)
        right_panel.pack(side="left", fill="y")
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Quick Actions",
                 font=FONT_HEAD, bg=C["panel"],
                 fg=C["text"], padx=20, pady=14).pack(anchor="w")
        tk.Frame(right_panel, bg=C["border"], height=1).pack(fill="x")

        # Each quick-action calls _activate_nav then the render method
        actions = [
            ("➕  Add Book",  2, self._render_add_book,  "gold"),
            ("📤  Borrow",    3, self._render_borrow,    "ghost"),
            ("📥  Return",    4, self._render_return,    "ghost"),
            ("🔍  Search",    5, self._render_search,    "ghost"),
        ]
        for label, nav_idx, renderer, style in actions:
            def make_cmd(i=nav_idx, r=renderer):
                self._activate_nav(i)
                r()
            _styled_button(right_panel, label, make_cmd,
                           style=style, padx=16, pady=10,
                           font=FONT_NAV).pack(fill="x", padx=16, pady=6)

        self._set_status("Welcome to Library Book Manager.")

    # ── ALL BOOKS ─────────────────────────────────────────
    def _render_view_books(self, fg="All", fa="All"):
        self._clear_content()
        self._set_page_title("All Books")
        self._update_stats()

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        # Filter bar card
        fcard = tk.Frame(outer, bg=C["panel"],
                         highlightthickness=1,
                         highlightbackground=C["border"],
                         padx=20, pady=14)
        fcard.pack(fill="x", pady=(0, 14))

        tk.Label(fcard, text="Filter:", font=FONT_BODY_B,
                 bg=C["panel"], fg=C["text2"]).pack(side="left", padx=(0, 8))

        self._fg_var = tk.StringVar(value=fg)
        ttk.Combobox(fcard, textvariable=self._fg_var,
                     values=["All"] + GENRES,
                     state="readonly", width=14,
                     style="Lib.TCombobox").pack(side="left", ipady=4, padx=(0, 10))

        self._fa_var = tk.StringVar(value=fa)
        ttk.Combobox(fcard, textvariable=self._fa_var,
                     values=["All", "Available", "Borrowed"],
                     state="readonly", width=12,
                     style="Lib.TCombobox").pack(side="left", ipady=4, padx=(0, 10))

        _styled_button(fcard, "Apply",
                       lambda: self._render_view_books(
                           self._fg_var.get(), self._fa_var.get()),
                       style="gold", padx=14, pady=6).pack(side="left")

        # Table card
        tcard = tk.Frame(outer, bg=C["panel"],
                         highlightthickness=1,
                         highlightbackground=C["border"])
        tcard.pack(fill="both", expand=True)

        cols = ("ID", "Title", "Author", "Genre", "Year", "Status", "Borrowed By")
        _, tree = self._treeview(tcard, cols, (80, 220, 155, 105, 55, 95, 130))

        book_list = view_books(fg, fa)
        for i, book in enumerate(book_list):
            status  = "✅  Available" if book["available"] else "📤  Borrowed"
            row_tag = "odd" if i % 2 == 0 else "even"
            clr_tag = "available" if book["available"] else "borrowed"
            tree.insert("", "end", values=(
                book["id"], book["title"], book["author"],
                book["genre"], book["year"], status,
                book["borrowed_by"] or "—"
            ), tags=(row_tag, clr_tag))

        if not book_list:
            tk.Label(tcard, text="No books match the selected filters.",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"], pady=30).pack()

        self._set_status(f"Showing {len(book_list)} book(s).")

    # ── ADD BOOK ──────────────────────────────────────────
    def _render_add_book(self):
        self._clear_content()
        self._set_page_title("Add New Book")

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(padx=28, pady=24, anchor="nw")

        card = tk.Frame(outer, bg=C["panel"],
                        highlightthickness=1,
                        highlightbackground=C["border"],
                        padx=32, pady=28)
        card.pack()

        self._section_label(card, "Add a New Book",
                            "Fill in the details below and click Add Book.")

        _, self._add_title  = self._input_row(card, "Book Title *")
        _, self._add_author = self._input_row(card, "Author *")
        _, self._add_genre  = self._combo_row(card, "Genre *", GENRES)
        _, self._add_year   = self._input_row(card, "Year *")

        self._add_fb = tk.Label(card, text="",
                                font=FONT_BODY, bg=C["panel"],
                                fg=C["green"], wraplength=420)
        self._add_fb.pack(anchor="w", pady=(12, 4))

        btn_row = tk.Frame(card, bg=C["panel"])
        btn_row.pack(anchor="w")
        _styled_button(btn_row, "  ➕  Add Book  ",
                       self._do_add_book,
                       style="gold", padx=20, pady=10,
                       font=FONT_BODY_B).pack(side="left", padx=(0, 10))
        _styled_button(btn_row, "Clear",
                       self._clear_add_form,
                       style="ghost", padx=14, pady=10).pack(side="left")

    def _do_add_book(self):
        msg = add_book(
            self._add_title.get(),
            self._add_author.get(),
            self._add_genre.get(),
            self._add_year.get(),
        )
        ok = msg.startswith("SUCCESS")
        self._add_fb.config(text=msg, fg=C["green"] if ok else C["red"])
        self._set_status(msg, ok)
        if ok:
            self._clear_add_form()
            self._update_stats()

    def _clear_add_form(self):
        for var in (self._add_title, self._add_author, self._add_year):
            var.set("")
        self._add_genre.set(GENRES[0])
        self._add_fb.config(text="")

    # ── BORROW BOOK ───────────────────────────────────────
    def _render_borrow(self):
        self._clear_content()
        self._set_page_title("Borrow a Book")

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        card = tk.Frame(outer, bg=C["panel"],
                        highlightthickness=1,
                        highlightbackground=C["border"],
                        padx=28, pady=24)
        card.pack(fill="both", expand=True)

        self._section_label(card, "Borrow a Book",
                            "Select an available book then enter your name.")

        self._avail_books = view_books(filter_available="Available")

        if not self._avail_books:
            tk.Label(card,
                     text="No books are currently available for borrowing.",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"], pady=20).pack()
            return

        items = [
            f"  {b['id']}   {b['title']}  —  {b['author']}  ({b['year']})"
            for b in self._avail_books
        ]
        _, self._borrow_lb = self._scrollable_listbox(card, items, fg=C["green"])

        name_row = tk.Frame(card, bg=C["panel"])
        name_row.pack(fill="x", pady=(16, 8))
        tk.Label(name_row, text="Your Name:", font=FONT_BODY_B,
                 bg=C["panel"], fg=C["text2"]).pack(side="left", padx=(0, 10))
        self._borrower_var = tk.StringVar()
        tk.Entry(name_row, textvariable=self._borrower_var, width=30,
                 bg=C["panel2"], fg=C["text"],
                 insertbackground=C["gold"],
                 relief="flat", font=FONT_BODY,
                 highlightthickness=1,
                 highlightcolor=C["gold"],
                 highlightbackground=C["border"]).pack(side="left", ipady=7)

        self._borrow_fb = tk.Label(card, text="",
                                   font=FONT_BODY,
                                   bg=C["panel"], fg=C["green"])
        self._borrow_fb.pack(anchor="w", pady=(4, 8))

        _styled_button(card, "  📤  Confirm Borrow  ",
                       self._do_borrow, style="gold",
                       padx=18, pady=10).pack(anchor="w")

    def _do_borrow(self):
        sel = self._borrow_lb.curselection()
        if not sel:
            messagebox.showwarning("No Selection",
                                   "Please select a book from the list.")
            return
        book = self._avail_books[sel[0]]
        msg  = borrow_book(book["id"], self._borrower_var.get())
        ok   = msg.startswith("SUCCESS")
        if ok:
            self._update_stats()
            self._render_borrow()   # refresh list after successful borrow
        else:
            self._borrow_fb.config(text=msg, fg=C["red"])
        self._set_status(msg, ok)

    # ── RETURN BOOK ───────────────────────────────────────
    def _render_return(self):
        self._clear_content()
        self._set_page_title("Return a Book")

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        card = tk.Frame(outer, bg=C["panel"],
                        highlightthickness=1,
                        highlightbackground=C["border"],
                        padx=28, pady=24)
        card.pack(fill="both", expand=True)

        self._section_label(card, "Return a Book",
                            "Select the book you are returning.")

        self._out_books = view_books(filter_available="Borrowed")

        if not self._out_books:
            tk.Label(card,
                     text="No books are currently borrowed.",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"], pady=20).pack()
            return

        items = [
            f"  {b['id']}   {b['title']}  —  borrowed by: {b['borrowed_by']}"
            for b in self._out_books
        ]
        _, self._return_lb = self._scrollable_listbox(card, items, fg=C["red"])

        self._return_fb = tk.Label(card, text="",
                                   font=FONT_BODY,
                                   bg=C["panel"], fg=C["green"])
        self._return_fb.pack(anchor="w", pady=(16, 8))

        _styled_button(card, "  📥  Confirm Return  ",
                       self._do_return, style="green",
                       padx=18, pady=10).pack(anchor="w")

    def _do_return(self):
        sel = self._return_lb.curselection()
        if not sel:
            messagebox.showwarning("No Selection",
                                   "Please select a book to return.")
            return
        book = self._out_books[sel[0]]
        msg  = return_book(book["id"])
        ok   = msg.startswith("SUCCESS")
        if ok:
            self._update_stats()
            self._render_return()   # refresh list after successful return
        else:
            self._return_fb.config(text=msg, fg=C["red"])
        self._set_status(msg, ok)

    # ── SEARCH ────────────────────────────────────────────
    def _render_search(self):
        self._clear_content()
        self._set_page_title("Search Books")

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        scard = tk.Frame(outer, bg=C["panel"],
                         highlightthickness=1,
                         highlightbackground=C["border"],
                         padx=24, pady=18)
        scard.pack(fill="x", pady=(0, 14))

        self._section_label(scard, "Search Books",
                            "Search by title, author, or genre.")

        srow = tk.Frame(scard, bg=C["panel"])
        srow.pack(fill="x")

        self._search_var = tk.StringVar()
        ent = tk.Entry(srow, textvariable=self._search_var, width=40,
                       bg=C["panel2"], fg=C["text"],
                       insertbackground=C["gold"],
                       relief="flat", font=("Helvetica", 12),
                       highlightthickness=1,
                       highlightcolor=C["gold"],
                       highlightbackground=C["border"])
        ent.pack(side="left", ipady=9, padx=(0, 10))
        ent.bind("<Return>", lambda e: self._do_search())
        ent.focus_set()

        _styled_button(srow, "  🔍  Search  ",
                       self._do_search,
                       style="gold", padx=16, pady=9).pack(side="left")

        self._search_count = tk.Label(scard, text="",
                                      font=FONT_BODY, bg=C["panel"],
                                      fg=C["text3"])
        self._search_count.pack(anchor="w", pady=(8, 0))

        # Results table
        rcard = tk.Frame(outer, bg=C["panel"],
                         highlightthickness=1,
                         highlightbackground=C["border"])
        rcard.pack(fill="both", expand=True)

        cols = ("ID", "Title", "Author", "Genre", "Year", "Status")
        _, self._search_tree = self._treeview(
            rcard, cols, (80, 240, 155, 105, 55, 95))

    def _do_search(self):
        kw = self._search_var.get()
        if not kw.strip():
            messagebox.showinfo("Empty", "Please enter a keyword.")
            return

        results = search_books(kw)

        # Clear existing rows safely
        for row in self._search_tree.get_children():
            self._search_tree.delete(row)

        for i, book in enumerate(results):
            status  = "✅  Available" if book["available"] else "📤  Borrowed"
            row_tag = "odd" if i % 2 == 0 else "even"
            clr_tag = "available" if book["available"] else "borrowed"
            self._search_tree.insert("", "end", values=(
                book["id"], book["title"], book["author"],
                book["genre"], book["year"], status
            ), tags=(row_tag, clr_tag))

        n = len(results)
        self._search_count.config(
            text=f"Found {n} result{'s' if n != 1 else ''} for '{kw}'")
        self._set_status(f"Search: {n} result(s).")

    # ── HISTORY ───────────────────────────────────────────
    def _render_history(self):
        self._clear_content()
        self._set_page_title("Transaction History")

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        card = tk.Frame(outer, bg=C["panel"],
                        highlightthickness=1,
                        highlightbackground=C["border"])
        card.pack(fill="both", expand=True)

        header = tk.Frame(card, bg=C["panel"], padx=24, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="Transaction History",
                 font=FONT_HEAD, bg=C["panel"],
                 fg=C["text"]).pack(side="left")
        tk.Label(header,
                 text=f"{len(borrow_log)} record(s)",
                 font=FONT_BODY, bg=C["panel"],
                 fg=C["text3"]).pack(side="right")
        tk.Frame(card, bg=C["border"], height=1).pack(fill="x")

        cols = ("Action", "Book ID", "Title", "Person", "Date")
        _, tree = self._treeview(card, cols, (90, 90, 240, 160, 110))

        for i, entry in enumerate(reversed(borrow_log)):
            tag      = "borrow_action" if entry["action"] == "BORROW" else "return_action"
            row_tag  = "odd" if i % 2 == 0 else "even"
            action_icon = "📤  BORROW" if entry["action"] == "BORROW" else "📥  RETURN"
            tree.insert("", "end", values=(
                action_icon, entry["book_id"],
                entry["title"], entry["person"], entry["date"]
            ), tags=(row_tag, tag))

        if not borrow_log:
            tk.Label(card,
                     text="No transactions recorded yet.",
                     font=FONT_BODY, bg=C["panel"],
                     fg=C["text3"], pady=30).pack()

        self._set_status(f"{len(borrow_log)} transaction(s) in log.")


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = LibraryApp(root)
    root.mainloop()