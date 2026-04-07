######################################################################
# Author: Joyce Nimely
# Username: Nimely_J
#
# FinalProject: FitPro App
# Purpose: A python based fitness tracking application that allows user to log workouts,
# set fitness goal, and track progress
#This project uses the Tkinter module to build a user-friendly graphical
# interface (GUI).

# A GUI widget is a graphical component such as a button, text label as shown below.
# GUI widgets also exist to make drop-down menus and scroll bars, display images, etc...
# Tkinter gives you the ability to create GUI Windows containing widgets.
# This program is a simple exploration.
##########################################################################
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime
import os

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

DB_FILE = "fitpro.db"

# ── Database setup ────────────────────────────────────────────────────────────

def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            age     INTEGER,
            height  REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            workout_type TEXT NOT NULL,
            duration     INTEGER NOT NULL,
            calories     INTEGER NOT NULL,
            date         TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            weekly_workouts INTEGER DEFAULT 3,
            weekly_calories INTEGER DEFAULT 1500,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    con.commit()
    con.close()


# ── Domain classes ────────────────────────────────────────────────────────────

class User:
    def __init__(self, db_id, name, age, height):
        self.db_id = db_id
        self.name = name
        self.age = age
        self.height = height

    def __str__(self):
        return f"User(name={self.name}, age={self.age}, height={self.height})"

    def get_workouts(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute(
            "SELECT workout_type, duration, calories, date FROM workouts "
            "WHERE user_id=? ORDER BY date DESC",
            (self.db_id,)
        )
        rows = cur.fetchall()
        con.close()
        return rows  # list of (type, duration, calories, date)

    def log_workout(self, workout_type, duration, calories):
        today = datetime.date.today().isoformat()
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO workouts (user_id, workout_type, duration, calories, date) "
            "VALUES (?, ?, ?, ?, ?)",
            (self.db_id, workout_type, duration, calories, today)
        )
        con.commit()
        con.close()

    def get_goals(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute("SELECT weekly_workouts, weekly_calories FROM goals WHERE user_id=?", (self.db_id,))
        row = cur.fetchone()
        con.close()
        return row if row else (3, 1500)

    def set_goals(self, weekly_workouts, weekly_calories):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute("SELECT id FROM goals WHERE user_id=?", (self.db_id,))
        if cur.fetchone():
            cur.execute(
                "UPDATE goals SET weekly_workouts=?, weekly_calories=? WHERE user_id=?",
                (weekly_workouts, weekly_calories, self.db_id)
            )
        else:
            cur.execute(
                "INSERT INTO goals (user_id, weekly_workouts, weekly_calories) VALUES (?,?,?)",
                (self.db_id, weekly_workouts, weekly_calories)
            )
        con.commit()
        con.close()

    def get_streak(self):
        workouts = self.get_workouts()
        if not workouts:
            return 0
        dates = sorted({w[3] for w in workouts}, reverse=True)
        streak = 1
        for i in range(1, len(dates)):
            d1 = datetime.date.fromisoformat(dates[i - 1])
            d2 = datetime.date.fromisoformat(dates[i])
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return streak


# ── App ───────────────────────────────────────────────────────────────────────

COLORS = {
    "bg":       "#0f0f0f",
    "surface":  "#1a1a1a",
    "card":     "#242424",
    "accent":   "#00e5a0",
    "accent2":  "#00b8d4",
    "text":     "#f0f0f0",
    "subtext":  "#888888",
    "danger":   "#ff4d6d",
    "border":   "#333333",
}

FONT_TITLE  = ("Helvetica Neue", 22, "bold")
FONT_LABEL  = ("Helvetica Neue", 11)
FONT_SMALL  = ("Helvetica Neue", 9)
FONT_BUTTON = ("Helvetica Neue", 11, "bold")
FONT_STAT   = ("Helvetica Neue", 28, "bold")


def styled_button(parent, text, command, color=None, width=18):
    c = color or COLORS["accent"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=c, fg=COLORS["bg"],
        font=FONT_BUTTON,
        relief="flat", bd=0, cursor="hand2",
        padx=14, pady=8, width=width,
        activebackground=c, activeforeground=COLORS["bg"]
    )
    return btn


def styled_entry(parent, width=22):
    e = tk.Entry(
        parent,
        bg=COLORS["card"], fg=COLORS["text"],
        insertbackground=COLORS["accent"],
        relief="flat", bd=0,
        font=FONT_LABEL, width=width
    )
    # bottom border via frame trick handled in layout
    return e


class FitPro:
    def __init__(self, window):
        self.window = window
        self.window.title("FitPro")
        self.window.configure(bg=COLORS["bg"])
        self.window.resizable(True, True)
        self.user = None

        init_db()
        self._build_ui()

    # ── UI skeleton ───────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.window, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=30, pady=(24, 0))
        tk.Label(hdr, text="FitPro", font=("Helvetica Neue", 32, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(side="left")
        tk.Label(hdr, text="Workout Tracker", font=("Helvetica Neue", 14),
                 bg=COLORS["bg"], fg=COLORS["subtext"]).pack(side="left", padx=(8, 0), pady=(12, 0))

        sep = tk.Frame(self.window, bg=COLORS["border"], height=1)
        sep.pack(fill="x", padx=30, pady=12)

        # Notebook
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=COLORS["surface"],
                        foreground=COLORS["subtext"],
                        font=FONT_LABEL, padding=[16, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", COLORS["card"])],
                  foreground=[("selected", COLORS["accent"])])

        self.nb = ttk.Notebook(self.window)
        self.nb.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        self.tab_login    = tk.Frame(self.nb, bg=COLORS["bg"])
        self.tab_log      = tk.Frame(self.nb, bg=COLORS["bg"])
        self.tab_progress = tk.Frame(self.nb, bg=COLORS["bg"])
        self.tab_goals    = tk.Frame(self.nb, bg=COLORS["bg"])
        self.tab_history  = tk.Frame(self.nb, bg=COLORS["bg"])

        self.nb.add(self.tab_login,    text="  Profile  ")
        self.nb.add(self.tab_log,      text="  Log Workout  ")
        self.nb.add(self.tab_progress, text="  Progress  ")
        self.nb.add(self.tab_goals,    text="  Goals  ")
        self.nb.add(self.tab_history,  text="  History  ")

        self._build_login_tab()
        self._build_log_tab()
        self._build_progress_tab()
        self._build_goals_tab()
        self._build_history_tab()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _card(self, parent, title=None):
        outer = tk.Frame(parent, bg=COLORS["card"], bd=0)
        outer.pack(fill="x", padx=0, pady=8)
        if title:
            tk.Label(outer, text=title, font=FONT_SMALL,
                     bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w", padx=16, pady=(12, 2))
        return outer

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, font=FONT_LABEL,
                 bg=COLORS["card"], fg=COLORS["subtext"]).grid(
            row=row, column=0, sticky="w", padx=16, pady=6)
        e = tk.Entry(parent, bg=COLORS["surface"], fg=COLORS["text"],
                     insertbackground=COLORS["accent"],
                     relief="flat", bd=4, font=FONT_LABEL, width=22)
        e.grid(row=row, column=1, padx=(8, 16), pady=6)
        return e

    # ── Login tab ─────────────────────────────────────────────────────────────

    def _build_login_tab(self):
        p = self.tab_login
        tk.Label(p, text="Your Profile", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(20, 4))
        tk.Label(p, text="Create a new profile or log in to an existing one.",
                 font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["subtext"]).pack(anchor="w")

        card = self._card(p)
        grid = tk.Frame(card, bg=COLORS["card"])
        grid.pack(padx=8, pady=8)

        self.name_entry   = self._field(grid, "Name",        0)
        self.age_entry    = self._field(grid, "Age",         1)
        self.height_entry = self._field(grid, "Height (cm)", 2)

        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(pady=(4, 16))
        styled_button(btn_row, "Create / Login", self.log_in).pack(side="left", padx=8)
        styled_button(btn_row, "Load Existing", self._load_user_dialog,
                      color=COLORS["accent2"]).pack(side="left", padx=8)

        self.status_label = tk.Label(p, text="", font=FONT_LABEL,
                                     bg=COLORS["bg"], fg=COLORS["accent"])
        self.status_label.pack(pady=8)

    def log_in(self):
        try:
            name   = self.name_entry.get().strip()
            age    = int(self.age_entry.get())
            height = float(self.height_entry.get())
            if not name:                          raise ValueError("Name required.")
            if not (1 <= age <= 120):             raise ValueError("Age must be 1–120.")
            if not (30 <= height <= 300):         raise ValueError("Height must be 30–300 cm.")

            con = sqlite3.connect(DB_FILE)
            cur = con.cursor()
            cur.execute("SELECT id FROM users WHERE name=?", (name,))
            row = cur.fetchone()
            if row:
                uid = row[0]
                cur.execute("UPDATE users SET age=?, height=? WHERE id=?", (age, height, uid))
            else:
                cur.execute("INSERT INTO users (name, age, height) VALUES (?,?,?)", (name, age, height))
                uid = cur.lastrowid
            con.commit()
            con.close()

            self.user = User(uid, name, age, height)
            self.status_label.config(text=f"✓  Logged in as {name}")
            for e in (self.name_entry, self.age_entry, self.height_entry):
                e.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _load_user_dialog(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute("SELECT id, name, age, height FROM users ORDER BY name")
        users = cur.fetchall()
        con.close()
        if not users:
            messagebox.showinfo("No Users", "No saved profiles found.")
            return

        dlg = tk.Toplevel(self.window)
        dlg.title("Select Profile")
        dlg.configure(bg=COLORS["bg"])
        dlg.resizable(False, False)
        tk.Label(dlg, text="Select a profile:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(padx=24, pady=(16, 8))

        lb = tk.Listbox(dlg, bg=COLORS["card"], fg=COLORS["text"],
                        selectbackground=COLORS["accent"], selectforeground=COLORS["bg"],
                        font=FONT_LABEL, relief="flat", bd=0, width=30)
        for u in users:
            lb.insert(tk.END, f"{u[1]}  (age {u[2]}, {u[3]} cm)")
        lb.pack(padx=24, pady=4)

        def select():
            idx = lb.curselection()
            if not idx:
                return
            uid, name, age, height = users[idx[0]]
            self.user = User(uid, name, age, height)
            self.status_label.config(text=f"✓  Logged in as {name}")
            dlg.destroy()

        styled_button(dlg, "Select", select).pack(pady=12)

    # ── Log Workout tab ───────────────────────────────────────────────────────

    def _build_log_tab(self):
        p = self.tab_log
        tk.Label(p, text="Log a Workout", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(20, 4))

        card = self._card(p)
        grid = tk.Frame(card, bg=COLORS["card"])
        grid.pack(padx=8, pady=8)

        tk.Label(grid, text="Workout Type", font=FONT_LABEL,
                 bg=COLORS["card"], fg=COLORS["subtext"]).grid(row=0, column=0, sticky="w", padx=16, pady=6)
        self.wtype_var = tk.StringVar(value="Running")
        types = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "Walking", "Other"]
        om = tk.OptionMenu(grid, self.wtype_var, *types)
        om.config(bg=COLORS["surface"], fg=COLORS["text"], font=FONT_LABEL,
                  relief="flat", bd=0, activebackground=COLORS["card"],
                  activeforeground=COLORS["accent"], highlightthickness=0)
        om["menu"].config(bg=COLORS["surface"], fg=COLORS["text"])
        om.grid(row=0, column=1, padx=(8, 16), pady=6, sticky="w")

        self.duration_entry = self._field(grid, "Duration (min)", 1)
        self.calories_entry = self._field(grid, "Calories Burned", 2)

        styled_button(card, "Log Workout", self.log_workout).pack(pady=(4, 16))

    def log_workout(self):
        if not self.user:
            messagebox.showwarning("No Profile", "Please log in first (Profile tab).")
            return
        try:
            wtype    = self.wtype_var.get()
            duration = int(self.duration_entry.get())
            calories = int(self.calories_entry.get())
            if duration <= 0 or calories <= 0:
                raise ValueError("Duration and calories must be positive.")
            self.user.log_workout(wtype, duration, calories)
            for e in (self.duration_entry, self.calories_entry):
                e.delete(0, tk.END)
            messagebox.showinfo("Logged!", f"{wtype} workout saved ✓")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ── Progress tab ──────────────────────────────────────────────────────────

    def _build_progress_tab(self):
        p = self.tab_progress
        tk.Label(p, text="Your Progress", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(20, 4))

        styled_button(p, "Refresh Charts", self._refresh_progress,
                      color=COLORS["accent2"], width=16).pack(anchor="w", pady=(0, 12))

        self.progress_inner = tk.Frame(p, bg=COLORS["bg"])
        self.progress_inner.pack(fill="both", expand=True)

    def _refresh_progress(self):
        if not self.user:
            messagebox.showwarning("No Profile", "Please log in first.")
            return

        for w in self.progress_inner.winfo_children():
            w.destroy()

        workouts = self.user.get_workouts()
        streak   = self.user.get_streak()
        goals    = self.user.get_goals()

        # ── Stat cards ───────────────────────────────────────────────────────
        total_workouts = len(workouts)
        total_duration = sum(w[1] for w in workouts)
        total_calories = sum(w[2] for w in workouts)

        # This week
        today = datetime.date.today()
        week_start = today - datetime.timedelta(days=today.weekday())
        week_workouts = [w for w in workouts if w[3] >= week_start.isoformat()]
        week_cal = sum(w[2] for w in week_workouts)

        stat_row = tk.Frame(self.progress_inner, bg=COLORS["bg"])
        stat_row.pack(fill="x", pady=(0, 12))

        def stat_card(parent, label, value, unit="", color=COLORS["accent"]):
            f = tk.Frame(parent, bg=COLORS["card"], padx=16, pady=12)
            f.pack(side="left", expand=True, fill="both", padx=4)
            tk.Label(f, text=label, font=FONT_SMALL, bg=COLORS["card"], fg=COLORS["subtext"]).pack()
            tk.Label(f, text=str(value), font=FONT_STAT, bg=COLORS["card"], fg=color).pack()
            if unit:
                tk.Label(f, text=unit, font=FONT_SMALL, bg=COLORS["card"], fg=COLORS["subtext"]).pack()

        stat_card(stat_row, "Total Workouts",   total_workouts)
        stat_card(stat_row, "Total Duration",   total_duration, "min")
        stat_card(stat_row, "Total Calories",   total_calories, "kcal",  COLORS["accent2"])
        stat_card(stat_row, "Day Streak 🔥",    streak,         "days",  "#ff9800")

        # Goal progress bars
        gf = tk.Frame(self.progress_inner, bg=COLORS["card"], padx=16, pady=12)
        gf.pack(fill="x", padx=0, pady=(0, 12))
        tk.Label(gf, text="THIS WEEK'S GOALS", font=FONT_SMALL,
                 bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w")

        def progress_bar(parent, label, current, goal, color):
            row = tk.Frame(parent, bg=COLORS["card"])
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}: {current}/{goal}", font=FONT_LABEL,
                     bg=COLORS["card"], fg=COLORS["text"], width=28, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=COLORS["surface"], height=10, width=200)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            pct = min(current / goal, 1.0) if goal else 0
            bar_fg = tk.Frame(bar_bg, bg=color, height=10, width=int(200 * pct))
            bar_fg.place(x=0, y=0)

        progress_bar(gf, "Workouts", len(week_workouts), goals[0], COLORS["accent"])
        progress_bar(gf, "Calories",  week_cal,           goals[1], COLORS["accent2"])

        # ── Charts ───────────────────────────────────────────────────────────
        if not HAS_MATPLOTLIB:
            tk.Label(self.progress_inner,
                     text="Install matplotlib for charts:  pip install matplotlib",
                     font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["subtext"]).pack(pady=20)
            return

        if not workouts:
            tk.Label(self.progress_inner, text="No workouts logged yet.",
                     font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["subtext"]).pack(pady=20)
            return

        # Aggregate by date
        from collections import defaultdict
        cal_by_date = defaultdict(int)
        dur_by_date = defaultdict(int)
        type_count  = defaultdict(int)
        for wt, dur, cal, date in workouts:
            cal_by_date[date] += cal
            dur_by_date[date] += dur
            type_count[wt]    += 1

        dates       = sorted(cal_by_date.keys())
        date_objs   = [datetime.date.fromisoformat(d) for d in dates]
        cals        = [cal_by_date[d] for d in dates]
        durs        = [dur_by_date[d] for d in dates]

        fig, axes = plt.subplots(1, 3, figsize=(13, 3.2))
        fig.patch.set_facecolor("#1a1a1a")

        def style_ax(ax, title):
            ax.set_facecolor("#242424")
            ax.set_title(title, color="#888888", fontsize=9, pad=8)
            ax.tick_params(colors="#888888", labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor("#333333")

        # Calories over time
        ax1 = axes[0]
        ax1.plot(date_objs, cals, color=COLORS["accent"], linewidth=2, marker="o", markersize=4)
        ax1.fill_between(date_objs, cals, alpha=0.15, color=COLORS["accent"])
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        fig.autofmt_xdate(ax=ax1, rotation=30)
        style_ax(ax1, "Calories Burned Over Time")
        ax1.yaxis.label.set_color("#888888")

        # Duration over time
        ax2 = axes[1]
        ax2.bar(date_objs, durs, color=COLORS["accent2"], alpha=0.8, width=0.6)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        fig.autofmt_xdate(ax=ax2, rotation=30)
        style_ax(ax2, "Duration per Day (min)")

        # Workout type pie
        ax3 = axes[2]
        palette = ["#00e5a0", "#00b8d4", "#ff9800", "#ff4d6d", "#a78bfa", "#f472b6"]
        wedges, texts, autotexts = ax3.pie(
            list(type_count.values()),
            labels=list(type_count.keys()),
            autopct="%1.0f%%",
            colors=palette[:len(type_count)],
            textprops={"color": "#888888", "fontsize": 8},
            pctdistance=0.75
        )
        for at in autotexts:
            at.set_color("#f0f0f0")
        ax3.set_facecolor("#1a1a1a")
        style_ax(ax3, "Workout Types")

        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=self.progress_inner)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ── Goals tab ─────────────────────────────────────────────────────────────

    def _build_goals_tab(self):
        p = self.tab_goals
        tk.Label(p, text="Weekly Goals", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(20, 4))
        tk.Label(p, text="Set targets for workouts and calories each week.",
                 font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["subtext"]).pack(anchor="w")

        card = self._card(p)
        grid = tk.Frame(card, bg=COLORS["card"])
        grid.pack(padx=8, pady=8)

        self.goal_workouts_entry = self._field(grid, "Workouts per week", 0)
        self.goal_calories_entry = self._field(grid, "Calories per week",  1)

        styled_button(card, "Save Goals", self._save_goals).pack(pady=(4, 16))

        self.goals_status = tk.Label(p, text="", font=FONT_LABEL,
                                     bg=COLORS["bg"], fg=COLORS["accent"])
        self.goals_status.pack()

        styled_button(p, "Load My Goals", self._load_goals,
                      color=COLORS["accent2"], width=14).pack(pady=4)

    def _save_goals(self):
        if not self.user:
            messagebox.showwarning("No Profile", "Please log in first.")
            return
        try:
            wg = int(self.goal_workouts_entry.get())
            cg = int(self.goal_calories_entry.get())
            if wg <= 0 or cg <= 0:
                raise ValueError("Goals must be positive.")
            self.user.set_goals(wg, cg)
            self.goals_status.config(text=f"✓  Goals saved: {wg} workouts, {cg} kcal/week")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _load_goals(self):
        if not self.user:
            messagebox.showwarning("No Profile", "Please log in first.")
            return
        wg, cg = self.user.get_goals()
        self.goal_workouts_entry.delete(0, tk.END)
        self.goal_workouts_entry.insert(0, str(wg))
        self.goal_calories_entry.delete(0, tk.END)
        self.goal_calories_entry.insert(0, str(cg))
        self.goals_status.config(text="Goals loaded.")

    # ── History tab ───────────────────────────────────────────────────────────

    def _build_history_tab(self):
        p = self.tab_history
        tk.Label(p, text="Workout History", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(20, 4))

        styled_button(p, "Load History", self._load_history,
                      color=COLORS["accent2"], width=14).pack(anchor="w", pady=(0, 8))

        cols = ("Date", "Type", "Duration", "Calories")
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=COLORS["card"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["card"],
                        rowheight=28,
                        font=FONT_LABEL)
        style.configure("Custom.Treeview.Heading",
                        background=COLORS["surface"],
                        foreground=COLORS["subtext"],
                        font=FONT_SMALL,
                        relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", COLORS["bg"])])

        self.tree = ttk.Treeview(p, columns=cols, show="headings",
                                  style="Custom.Treeview", height=14)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def _load_history(self):
        if not self.user:
            messagebox.showwarning("No Profile", "Please log in first.")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for wt, dur, cal, date in self.user.get_workouts():
            self.tree.insert("", tk.END, values=(date, wt, f"{dur} min", f"{cal} kcal"))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("820x680")
    app = FitPro(root)
    root.mainloop()