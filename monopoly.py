import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
import threading

# ── Board definition ──────────────────────────────────────────────────────────
BOARD = [
    {"name": "START",         "type": "go",        "pos": 0,  "price": 0,   "color": None,       "group": None},
    {"name": "Slum St",       "type": "property",  "pos": 1,  "price": 60,  "color": "#8B4513",  "group": "brown"},
    {"name": "Vault",         "type": "chest",     "pos": 2,  "price": 0,   "color": None,       "group": None},
    {"name": "Alleyway",      "type": "property",  "pos": 3,  "price": 60,  "color": "#8B4513",  "group": "brown"},
    {"name": "Income Tax",    "type": "tax",       "pos": 4,  "price": 200, "color": None,       "group": None},
    {"name": "North RR",      "type": "railroad",  "pos": 5,  "price": 200, "color": "#555555",  "group": "railroad"},
    {"name": "Brick Ave",     "type": "property",  "pos": 6,  "price": 100, "color": "#87CEEB",  "group": "light-blue"},
    {"name": "Fate",          "type": "chance",    "pos": 7,  "price": 0,   "color": None,       "group": None},
    {"name": "Stone Ave",     "type": "property",  "pos": 8,  "price": 100, "color": "#87CEEB",  "group": "light-blue"},
    {"name": "Wood Ave",      "type": "property",  "pos": 9,  "price": 120, "color": "#87CEEB",  "group": "light-blue"},
    {"name": "Jail",          "type": "jail",      "pos": 10, "price": 0,   "color": None,       "group": None},
    {"name": "Neon Blvd",     "type": "property",  "pos": 11, "price": 140, "color": "#DA70D6",  "group": "pink"},
    {"name": "Power Co.",     "type": "utility",   "pos": 12, "price": 150, "color": "#FFD700",  "group": "utility"},
    {"name": "Holo St",       "type": "property",  "pos": 13, "price": 140, "color": "#DA70D6",  "group": "pink"},
    {"name": "Cyber St",      "type": "property",  "pos": 14, "price": 160, "color": "#DA70D6",  "group": "pink"},
    {"name": "East RR",       "type": "railroad",  "pos": 15, "price": 200, "color": "#555555",  "group": "railroad"},
    {"name": "Bronze Wy",     "type": "property",  "pos": 16, "price": 180, "color": "#FF8C00",  "group": "orange"},
    {"name": "Vault",         "type": "chest",     "pos": 17, "price": 0,   "color": None,       "group": None},
    {"name": "Silver Wy",     "type": "property",  "pos": 18, "price": 180, "color": "#FF8C00",  "group": "orange"},
    {"name": "Gold Wy",       "type": "property",  "pos": 19, "price": 200, "color": "#FF8C00",  "group": "orange"},
    {"name": "Free Parking",  "type": "freeparking","pos": 20,"price": 0,   "color": None,       "group": None},
    {"name": "Ruby Rd",       "type": "property",  "pos": 21, "price": 220, "color": "#e74c3c",  "group": "red"},
    {"name": "Fate",          "type": "chance",    "pos": 22, "price": 0,   "color": None,       "group": None},
    {"name": "Garnet Rd",     "type": "property",  "pos": 23, "price": 220, "color": "#e74c3c",  "group": "red"},
    {"name": "Onyx Rd",       "type": "property",  "pos": 24, "price": 240, "color": "#e74c3c",  "group": "red"},
    {"name": "South RR",      "type": "railroad",  "pos": 25, "price": 200, "color": "#555555",  "group": "railroad"},
    {"name": "Sapphire",      "type": "property",  "pos": 26, "price": 260, "color": "#FFD700",  "group": "yellow-prop"},
    {"name": "Emerald",       "type": "property",  "pos": 27, "price": 260, "color": "#FFD700",  "group": "yellow-prop"},
    {"name": "Water Co.",     "type": "utility",   "pos": 28, "price": 150, "color": "#4fc3f7",  "group": "utility"},
    {"name": "Diamond",       "type": "property",  "pos": 29, "price": 280, "color": "#FFD700",  "group": "yellow-prop"},
    {"name": "Go to Jail",    "type": "gotojail",  "pos": 30, "price": 0,   "color": None,       "group": None},
    {"name": "Plaza Blvd",    "type": "property",  "pos": 31, "price": 300, "color": "#228B22",  "group": "green"},
    {"name": "Metro Blvd",    "type": "property",  "pos": 32, "price": 300, "color": "#228B22",  "group": "green"},
    {"name": "Vault",         "type": "chest",     "pos": 33, "price": 0,   "color": None,       "group": None},
    {"name": "Uptown Ave",    "type": "property",  "pos": 34, "price": 320, "color": "#228B22",  "group": "green"},
    {"name": "West RR",       "type": "railroad",  "pos": 35, "price": 200, "color": "#555555",  "group": "railroad"},
    {"name": "Fate",          "type": "chance",    "pos": 36, "price": 0,   "color": None,       "group": None},
    {"name": "Billion Row",   "type": "property",  "pos": 37, "price": 350, "color": "#00008B",  "group": "dark-blue"},
    {"name": "Luxury Tax",    "type": "tax",       "pos": 38, "price": 100, "color": None,       "group": None},
    {"name": "Tycoon Twr",    "type": "property",  "pos": 39, "price": 400, "color": "#00008B",  "group": "dark-blue"},
]

GROUP_SIZES = {
    "brown": 2, "light-blue": 3, "pink": 3, "orange": 3,
    "red": 3, "yellow-prop": 3, "green": 3, "dark-blue": 2,
    "railroad": 4, "utility": 2,
}

HOUSE_COSTS = {
    "brown": 50, "light-blue": 50,
    "pink": 100, "orange": 100,
    "red": 150, "yellow-prop": 150,
    "green": 200, "dark-blue": 200,
}

RENT_MULTIPLIERS = [0.10, 0.20, 0.40, 0.80, 1.25, 1.75]

TOKENS = ["🎩", "🚗", "🐶", "🚢"]
TOKEN_COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]

CARD_DECK = [
    {"desc": "Bank pays you $200 dividend!", "action": "money", "amount": 200},
    {"desc": "Pay school fees $150.", "action": "money", "amount": -150},
    {"desc": "Go to Jail!", "action": "gotojail"},
    {"desc": "Advance to START — collect $200.", "action": "advance", "dest": 0},
    {"desc": "Back 3 spaces.", "action": "back3"},
    {"desc": "Nearest Railroad — pay double rent.", "action": "nearest_rr"},
    {"desc": "Collect $50 from each player!", "action": "collect_all", "amount": 50},
    {"desc": "Pay $40 per house, $115 per hotel.", "action": "house_repairs"},
    {"desc": "You won a beauty contest — collect $10!", "action": "money", "amount": 10},
    {"desc": "Bank error in your favor — collect $75!", "action": "money", "amount": 75},
    {"desc": "Doctor's bill — pay $50.", "action": "money", "amount": -50},
    {"desc": "Pay each player $20.", "action": "pay_all", "amount": 20},
    {"desc": "Tax refund — collect $20!", "action": "money", "amount": 20},
    {"desc": "Get Out of Jail Free card.", "action": "jailfree"},
    {"desc": "Speeding fine — pay $100.", "action": "money", "amount": -100},
    {"desc": "Inheritance — collect $100!", "action": "money", "amount": 100},
    {"desc": "Street repairs — pay $40/house, $115/hotel.", "action": "house_repairs"},
    {"desc": "Advance to START — collect $200.", "action": "advance", "dest": 0},
    {"desc": "Life insurance matures — collect $100!", "action": "money", "amount": 100},
    {"desc": "Luxury tax — pay $75.", "action": "money", "amount": -75},
]


# ── Player class ──────────────────────────────────────────────────────────────
class Player:
    def __init__(self, name, token, color, is_human):
        self.name = name
        self.token = token
        self.color = color
        self.is_human = is_human
        self.money = 1500
        self.pos = 0
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = 0
        self.doubles_count = 0
        self.properties = []
        self.bankrupt = False

    def status_text(self):
        if self.bankrupt:
            return "Bankrupt"
        if self.in_jail:
            return f"In Jail ({self.jail_turns} turns)"
        return "Active"


# ── Main Game Class ───────────────────────────────────────────────────────────
class MonopolyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Property Tycoon")
        self.root.geometry("1400x900")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.players = [
            Player("You",      TOKENS[0], TOKEN_COLORS[0], True),
            Player("AI Alice", TOKENS[1], TOKEN_COLORS[1], False),
            Player("AI Bob",   TOKENS[2], TOKEN_COLORS[2], False),
            Player("AI Carol", TOKENS[3], TOKEN_COLORS[3], False),
        ]
        self.current = 0
        self.free_parking_pot = 0
        self.card_deck = CARD_DECK[:]
        random.shuffle(self.card_deck)
        self.card_index = 0
        # ownership: pos -> player index
        self.ownership = {}
        # buildings: pos -> 0-5 (5 = hotel)
        self.buildings = {}
        # mortgaged: pos -> bool
        self.mortgaged = {}
        self.nearest_rr_double = False
        self.dice_result = (0, 0)
        self.turn_phase = "start"  # start | extra_roll | rolled
        self.animation_id = None
        self.turn_number = 1
        self.speed_var = None
        self.toast_count = 0
        self.last_purchase = None
        self.sound_enabled = True
        self._log_filter = "all"

        self._token_selection()
        self._build_ui()
        self._draw_board()
        self.refresh_panel()
        self.log("Welcome to Property Tycoon! You go first.", "system")
        self._update_buttons()

    def _token_selection(self):
        """Show a startup dialog for the human to pick their token and name."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Choose Your Token")
        dlg.geometry("360x280")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, False)
        # Center on screen
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() - 360) // 2
        y = (dlg.winfo_screenheight() - 280) // 2
        dlg.geometry(f"360x280+{x}+{y}")

        tk.Label(dlg, text="PROPERTY TYCOON", font=("Georgia", 16, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack(pady=(15, 5))
        tk.Label(dlg, text="Enter your name and pick a token:",
                 font=("Helvetica", 10), fg="#bdc3c7", bg="#1a1a2e").pack()

        name_var = tk.StringVar(value="You")
        name_frame = tk.Frame(dlg, bg="#1a1a2e")
        name_frame.pack(pady=6)
        tk.Label(name_frame, text="Name:", font=("Helvetica", 10), fg="white", bg="#1a1a2e").pack(side=tk.LEFT, padx=4)
        tk.Entry(name_frame, textvariable=name_var, font=("Helvetica", 10),
                 bg="#16213e", fg="white", insertbackground="white", width=16).pack(side=tk.LEFT)

        chosen = [0]  # default: first token
        token_frame = tk.Frame(dlg, bg="#1a1a2e")
        token_frame.pack(pady=8)
        token_btns = []
        tokens_available = TOKENS[:]
        colors_available = TOKEN_COLORS[:]

        def pick(idx):
            chosen[0] = idx
            for j, b in enumerate(token_btns):
                b.config(relief=tk.SUNKEN if j == idx else tk.RAISED,
                         bg="#f39c12" if j == idx else "#16213e")

        for i, tok in enumerate(tokens_available):
            b = tk.Button(token_frame, text=tok, font=("Helvetica", 22),
                          bg="#16213e", fg="white", width=3, relief=tk.RAISED,
                          command=lambda i=i: pick(i))
            b.pack(side=tk.LEFT, padx=6)
            token_btns.append(b)
        pick(0)

        def confirm():
            idx = chosen[0]
            # Assign chosen token to human player (index 0)
            self.players[0].token = tokens_available[idx]
            self.players[0].color = colors_available[idx]
            self.players[0].name = name_var.get().strip() or "You"
            # Reassign remaining tokens to AI players
            remaining_tokens = [t for j, t in enumerate(tokens_available) if j != idx]
            remaining_colors = [c for j, c in enumerate(colors_available) if j != idx]
            for ai_i, ai_player in enumerate([p for p in self.players if not p.is_human]):
                ai_player.token = remaining_tokens[ai_i]
                ai_player.color = remaining_colors[ai_i]
            dlg.destroy()

        tk.Button(dlg, text="▶  START GAME", font=("Helvetica", 12, "bold"),
                  bg="#27ae60", fg="white", command=confirm, padx=20, pady=6).pack(pady=12)
        self.root.wait_window(dlg)

    # ─────────────────────────────────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Left: board canvas
        self.canvas = tk.Canvas(self.root, width=770, height=770,
                                bg="#0d1b2a", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=15)
        self.canvas.bind("<Button-1>", self._canvas_click)

        # Right panel
        right = tk.Frame(self.root, bg="#1a1a2e", width=580)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        right.pack_propagate(False)

        # Title
        title_row = tk.Frame(right, bg="#1a1a2e")
        title_row.pack(fill=tk.X, padx=5, pady=(5, 2))
        tk.Label(title_row, text="PROPERTY TYCOON",
                 font=("Helvetica", 18, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack(side=tk.LEFT)
        self.turn_label = tk.Label(title_row, text="Turn #1",
                                   font=("Helvetica", 10), fg="#95a5a6", bg="#1a1a2e")
        self.turn_label.pack(side=tk.RIGHT, padx=4)

        # Status label (full width)
        self.status_var = tk.StringVar(value="Game starting...")
        self.status_label = tk.Label(right, textvariable=self.status_var,
                                     font=("Helvetica", 11, "bold"), fg="#f39c12",
                                     bg="#1a1a2e", wraplength=550, justify=tk.CENTER)
        self.status_label.pack(fill=tk.X, padx=5, pady=(2, 0))

        # Dice canvas — real drawn dice
        self.dice_canvas = tk.Canvas(right, width=130, height=65,
                                     bg="#1a1a2e", highlightthickness=0)
        self.dice_canvas.pack(pady=3)

        # Free Parking pot
        self.fp_var = tk.StringVar(value="Free Parking Pot: $0")
        tk.Label(right, textvariable=self.fp_var,
                 font=("Helvetica", 10, "bold"),
                 fg="#2ecc71", bg="#1a1a2e").pack(pady=2)

        # Player cards
        cards_frame = tk.Frame(right, bg="#1a1a2e")
        cards_frame.pack(fill=tk.X, padx=5, pady=3)
        self.player_cards = []
        for i in range(4):
            card = tk.Frame(cards_frame, bg="#16213e", relief=tk.RIDGE, bd=2,
                            padx=4, pady=3)
            card.grid(row=0, column=i, padx=2, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)
            name_lbl   = tk.Label(card, text="", font=("Helvetica", 8, "bold"),
                                  fg="white", bg="#16213e")
            name_lbl.pack()
            money_lbl  = tk.Label(card, text="", font=("Helvetica", 9),
                                  fg="#2ecc71", bg="#16213e")
            money_lbl.pack()
            status_lbl = tk.Label(card, text="", font=("Helvetica", 7),
                                  fg="#bdc3c7", bg="#16213e")
            status_lbl.pack()
            props_lbl  = tk.Label(card, text="", font=("Helvetica", 7),
                                  fg="#95a5a6", bg="#16213e")
            props_lbl.pack()
            dots_lbl   = tk.Label(card, text="", font=("Helvetica", 8),
                                  fg="white", bg="#16213e")
            dots_lbl.pack()
            net_lbl = tk.Label(card, text="", font=("Helvetica", 7),
                               fg="#74b9ff", bg="#16213e")
            net_lbl.pack()
            bar = tk.Frame(card, bg=TOKEN_COLORS[i], height=3)
            bar.pack(fill=tk.X, side=tk.BOTTOM)
            self.player_cards.append({
                "frame": card, "name": name_lbl, "money": money_lbl,
                "status": status_lbl, "props": props_lbl, "dots": dots_lbl,
                "net": net_lbl,
            })

        # Button row 1
        btn_frame1 = tk.Frame(right, bg="#1a1a2e")
        btn_frame1.pack(fill=tk.X, padx=5, pady=3)
        self.roll_btn = tk.Button(btn_frame1, text="🎲 ROLL DICE",
                                  command=self.roll_dice,
                                  bg="#e74c3c", fg="white",
                                  font=("Helvetica", 11, "bold"), padx=10)
        self.roll_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.manage_btn = tk.Button(btn_frame1, text="🏠 MANAGE PROPS",
                                    command=self.open_manage_dialog,
                                    bg="#2980b9", fg="white",
                                    font=("Helvetica", 11, "bold"), padx=10)
        self.manage_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Button row 2
        btn_frame2 = tk.Frame(right, bg="#1a1a2e")
        btn_frame2.pack(fill=tk.X, padx=5, pady=2)
        self.end_btn = tk.Button(btn_frame2, text="⏳ END TURN",
                                 command=self.end_turn,
                                 bg="#27ae60", fg="white",
                                 font=("Helvetica", 11, "bold"), padx=10)
        self.end_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.jail_btn = tk.Button(btn_frame2, text="🔓 GET OUT OF JAIL",
                                  command=self.get_out_of_jail_btn,
                                  bg="#8e44ad", fg="white",
                                  font=("Helvetica", 11, "bold"), padx=10)
        self.jail_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Button row 3
        btn_frame3 = tk.Frame(right, bg="#1a1a2e")
        btn_frame3.pack(fill=tk.X, padx=5, pady=2)
        self.trade_btn = tk.Button(btn_frame3, text="🤝 TRADE",
                                   command=self.open_trade_dialog,
                                   bg="#8e44ad", fg="white",
                                   font=("Helvetica", 10, "bold"), padx=6)
        self.trade_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.undo_btn = tk.Button(btn_frame3, text="↩ UNDO BUY",
                                  command=self.undo_purchase,
                                  bg="#7f8c8d", fg="white",
                                  font=("Helvetica", 10, "bold"), padx=6)
        self.undo_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.props_btn = tk.Button(btn_frame3, text="📋 ALL PROPS",
                                   command=self.open_props_list_dialog,
                                   bg="#16213e", fg="white",
                                   font=("Helvetica", 10, "bold"), padx=6)
        self.props_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Button row 4
        btn_frame4 = tk.Frame(right, bg="#1a1a2e")
        btn_frame4.pack(fill=tk.X, padx=5, pady=2)
        tk.Button(btn_frame4, text="💾 SAVE",
                  command=self.save_game,
                  bg="#2c3e50", fg="white",
                  font=("Helvetica", 10, "bold"), padx=6).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(btn_frame4, text="📂 LOAD",
                  command=self.load_game,
                  bg="#2c3e50", fg="white",
                  font=("Helvetica", 10, "bold"), padx=6).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(btn_frame4, text="🔊 Sound",
                       variable=self.sound_var, bg="#1a1a2e", fg="white",
                       selectcolor="#16213e", activebackground="#1a1a2e",
                       font=("Helvetica", 9),
                       command=lambda: setattr(self, "sound_enabled", self.sound_var.get())
                       ).pack(side=tk.LEFT, padx=6)

        # AI Speed slider
        speed_frame = tk.Frame(right, bg="#1a1a2e")
        speed_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(speed_frame, text="⚡ AI Speed:",
                 font=("Helvetica", 9), fg="#95a5a6", bg="#1a1a2e").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=6)
        speed_slider = tk.Scale(speed_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                variable=self.speed_var, bg="#1a1a2e", fg="white",
                                troughcolor="#16213e", highlightthickness=0,
                                showvalue=False, length=140)
        speed_slider.pack(side=tk.LEFT, padx=4)
        tk.Label(speed_frame, text="Fast ← → Slow",
                 font=("Helvetica", 7), fg="#6c7086", bg="#1a1a2e").pack(side=tk.LEFT)

        # Event log
        log_frame = tk.Frame(right, bg="#1a1a2e")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
        log_header = tk.Frame(log_frame, bg="#1a1a2e")
        log_header.pack(fill=tk.X)
        tk.Label(log_header, text="Event Log",
                 font=("Helvetica", 9, "bold"),
                 fg="#95a5a6", bg="#1a1a2e").pack(side=tk.LEFT)
        filter_data = [("All","all","#95a5a6"), ("✓","good","#2ecc71"),
                       ("✗","bad","#e74c3c"), ("🃏","card","#a29bfe"), ("⚙","system","#fdcb6e")]
        self._filter_btns = {}
        for label, key, color in filter_data:
            def _set_filter(k=key):
                self._log_filter = k
                self._apply_log_filter()
                for fk, fb in self._filter_btns.items():
                    fb.config(relief=tk.SUNKEN if fk == k else tk.RAISED)
            btn = tk.Button(log_header, text=label, font=("Helvetica", 7),
                            bg="#16213e", fg=color, relief=tk.SUNKEN if key == "all" else tk.RAISED,
                            padx=3, pady=0, command=_set_filter)
            btn.pack(side=tk.LEFT, padx=1)
            self._filter_btns[key] = btn
        self.log_text = tk.Text(log_frame, state=tk.DISABLED,
                                bg="#0d1b2a", fg="white",
                                font=("Courier", 8), wrap=tk.WORD,
                                relief=tk.SUNKEN, bd=1)
        scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Log colour tags
        self.log_text.tag_config("good",    foreground="#2ecc71")
        self.log_text.tag_config("bad",     foreground="#e74c3c")
        self.log_text.tag_config("neutral", foreground="#74b9ff")
        self.log_text.tag_config("card",    foreground="#a29bfe")
        self.log_text.tag_config("system",  foreground="#fdcb6e")

    @property
    def ai_delay(self):
        if self.speed_var is None:
            return 600
        return 100 + (self.speed_var.get() - 1) * 150  # 100ms to 1450ms

    # ─────────────────────────────────────────────────────────────────────
    # Board drawing helpers
    # ─────────────────────────────────────────────────────────────────────
    # Board layout constants
    _MARGIN  = 10
    _CORNER  = 90
    _TILE_W  = 52      # narrow dimension of edge tiles
    _TILE_H  = 90      # long dimension of edge tiles
    _SIZE    = 770

    def _tile_rect(self, pos):
        """Return (x1, y1, x2, y2) pixel rectangle for a board position."""
        M = self._MARGIN
        C = self._CORNER
        W = self._TILE_W
        H = self._TILE_H
        S = self._SIZE

        # Corners
        if pos == 0:  return (S - M - C, S - M - C, S - M,     S - M)
        if pos == 10: return (M,          S - M - C, M + C,     S - M)
        if pos == 20: return (M,          M,          M + C,     M + C)
        if pos == 30: return (S - M - C, M,          S - M,     M + C)

        # Bottom row: pos 1-9 (right to left)
        if 1 <= pos <= 9:
            idx = 9 - pos          # 0..8 left-to-right offset from jail corner
            x1 = M + C + idx * W
            return (x1, S - M - H, x1 + W, S - M)

        # Left column: pos 11-19 (bottom to top)
        if 11 <= pos <= 19:
            idx = pos - 10         # 1..9
            y1 = S - M - C - idx * W
            return (M, y1, M + H, y1 + W)

        # Top row: pos 21-29 (left to right)
        if 21 <= pos <= 29:
            idx = pos - 20         # 1..9
            x1 = M + C + (idx - 1) * W
            return (x1, M, x1 + W, M + H)

        # Right column: pos 31-39 (top to bottom)
        if 31 <= pos <= 39:
            idx = 40 - pos         # 9..1 (39->1, 31->9)
            y1 = M + C + (idx - 1) * W
            return (S - M - H, y1, S - M, y1 + W)

        return (0, 0, 0, 0)

    def _draw_board(self):
        self.canvas.delete("all")
        S = self._SIZE
        M = self._MARGIN
        C = self._CORNER

        # Outer border — cream
        self.canvas.create_rectangle(0, 0, S, S, fill="#F5E6C8", outline="")
        # Board area background — cream/ivory
        self.canvas.create_rectangle(M, M, S - M, S - M, fill="#FFFDE7", outline="#c8a96e", width=2)
        # Inner center area — muted green felt
        self.canvas.create_rectangle(M + C, M + C, S - M - C, S - M - C,
                                     fill="#B8D4B8", outline="#8aab8a", width=2)

        # Center title box
        cx = S / 2
        cy = S / 2
        box_w = 160
        box_h = 80
        self.canvas.create_rectangle(cx - box_w / 2, cy - box_h / 2,
                                     cx + box_w / 2, cy + box_h / 2,
                                     fill="#1B5E20", outline="#F9A825", width=3)
        self.canvas.create_text(cx, cy - 18, text="PROPERTY",
                                font=("Georgia", 16, "bold"), fill="#F9A825",
                                justify=tk.CENTER)
        self.canvas.create_text(cx, cy + 10, text="TYCOON",
                                font=("Georgia", 16, "bold"), fill="#F9A825",
                                justify=tk.CENTER)
        self.canvas.create_text(cx, cy + 32, text="🏦",
                                font=("Helvetica", 20), fill="#F9A825")

        for tile in BOARD:
            self._draw_tile(tile)
        self._draw_possible_moves()
        self._draw_tokens()

    def _draw_possible_moves(self):
        """Highlight tiles the current human player can reach this roll."""
        player = self.players[self.current]
        if not player.is_human or self.turn_phase != "start" or player.in_jail:
            return
        highlight_color = "#F9A825"
        for total in range(2, 13):
            target = (player.pos + total) % 40
            x1, y1, x2, y2 = self._tile_rect(target)
            self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2,
                                         outline=highlight_color, width=2,
                                         fill="", tags="possible_move")

    def _draw_tile(self, pos_or_tile):
        if isinstance(pos_or_tile, dict):
            tile = pos_or_tile
        else:
            tile = BOARD[pos_or_tile]

        pos = tile["pos"]
        x1, y1, x2, y2 = self._tile_rect(pos)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        w  = x2 - x1
        h  = y2 - y1

        BAND = 16

        # Choose background colour
        bg_map = {
            "go":          "#E8F5E9",
            "jail":        "#FFF8E1",
            "freeparking": "#F3E5F5",
            "gotojail":    "#FFEBEE",
            "tax":         "#ECEFF1",
            "chance":      "#FFF9C4",
            "chest":       "#EDE7F6",
        }
        bg = bg_map.get(tile["type"], "#FFFDE7")
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                     fill=bg, outline="#2c3e50", width=1)

        # Thick ownership border
        if pos in self.ownership:
            oc = TOKEN_COLORS[self.ownership[pos]]
            self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                         outline=oc, width=3)

        # Colour band for purchasable tiles (16px thick)
        band_color = None
        if tile["type"] == "property" and tile["color"]:
            band_color = tile["color"]
        elif tile["type"] == "railroad":
            band_color = "#555555"

        if band_color:
            if 1 <= pos <= 9:   # bottom row: band at bottom
                self.canvas.create_rectangle(x1, y2 - BAND, x2, y2,
                                             fill=band_color, outline="")
            elif 11 <= pos <= 19:  # left col: band on left
                self.canvas.create_rectangle(x1, y1, x1 + BAND, y2,
                                             fill=band_color, outline="")
            elif 21 <= pos <= 29:  # top row: band at top
                self.canvas.create_rectangle(x1, y1, x2, y1 + BAND,
                                             fill=band_color, outline="")
            elif 31 <= pos <= 39:  # right col: band on right
                self.canvas.create_rectangle(x2 - BAND, y1, x2, y2,
                                             fill=band_color, outline="")

        # Corner tiles — special rendering
        if pos in (0, 10, 20, 30):
            if pos == 0:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#43A047", outline="#2c3e50", width=1)
                self.canvas.create_text(cx, cy - 12, text="GO",
                                        font=("Helvetica", 16, "bold"),
                                        fill="white", justify=tk.CENTER)
                self.canvas.create_text(cx, cy + 14, text="→ Collect $200",
                                        font=("Helvetica", 7, "bold"),
                                        fill="white", justify=tk.CENTER)

            elif pos == 10:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFF8E1", outline="#2c3e50", width=1)
                mid_y = (y1 + y2) / 2
                self.canvas.create_rectangle(x1, mid_y, x2, y2, fill="#FB8C00", outline="")
                self.canvas.create_text(cx, mid_y + (y2 - mid_y) / 2,
                                        text="JUST VISITING",
                                        font=("Helvetica", 6, "bold"),
                                        fill="#1a1a2e", justify=tk.CENTER)
                self.canvas.create_line(x1, y2, x2, y1, fill="#888888", width=1)
                self.canvas.create_text(cx + 15, cy - 15, text="IN JAIL ⛓",
                                        font=("Helvetica", 6, "bold"),
                                        fill="#1a1a2e", justify=tk.CENTER)

            elif pos == 20:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#8E44AD", outline="#2c3e50", width=1)
                self.canvas.create_text(cx, cy - 10, text="FREE PARKING 🅿",
                                        font=("Helvetica", 7, "bold"),
                                        fill="white", justify=tk.CENTER)
                self.canvas.create_text(cx, cy + 14,
                                        text=f"${self.free_parking_pot}",
                                        font=("Helvetica", 10, "bold"),
                                        fill="#F9A825")

            elif pos == 30:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#E53935", outline="#2c3e50", width=1)
                self.canvas.create_text(cx, cy, text="GO TO JAIL 👮",
                                        font=("Helvetica", 8, "bold"),
                                        fill="white", justify=tk.CENTER)
            return

        # Determine text rotation angle based on position
        if 1 <= pos <= 9:
            angle = 0
            wrap_w = w - 6
        elif 11 <= pos <= 19:
            angle = 90
            wrap_w = h - 6
        elif 21 <= pos <= 29:
            angle = 180
            wrap_w = w - 6
        elif 31 <= pos <= 39:
            angle = 270
            wrap_w = h - 6
        else:
            angle = 0
            wrap_w = w - 6

        # Tile name
        name_lines = self._split_name(tile["name"])
        name_text = "\n".join(name_lines)
        self.canvas.create_text(cx, cy - 8, text=name_text,
                                font=("Arial", 6, "bold"),
                                fill="#1a1a2e", justify=tk.CENTER,
                                angle=angle, width=wrap_w)

        # Icon
        icon = ""
        if tile["type"] == "railroad":
            icon = "🚂"
        elif tile["type"] == "utility":
            icon = "⚡" if "Power" in tile["name"] else "💧"
        elif tile["type"] == "chance":
            icon = "?"
        elif tile["type"] == "chest":
            icon = "📦"
        if icon:
            self.canvas.create_text(cx, cy + 10, text=icon,
                                    font=("Helvetica", 10), fill="#2c3e50",
                                    angle=angle)

        # Price
        if tile["price"] > 0:
            price_color = "#c0392b" if self.mortgaged.get(pos) else "#2c3e50"
            if tile["type"] not in ("tax",):
                self.canvas.create_text(cx, cy + 22, text=f"${tile['price']}",
                                        font=("Helvetica", 6), fill=price_color,
                                        angle=angle)

        # Mortgage indicator
        if self.mortgaged.get(pos):
            self.canvas.create_text(x1 + 7, y1 + 7, text="M",
                                    font=("Helvetica", 7, "bold"), fill="#c0392b")

        # Buildings
        bcount = self.buildings.get(pos, 0)
        if bcount > 0 and tile["type"] == "property":
            self._draw_buildings_on_tile(pos, x1, y1, x2, y2, bcount)

        # Ownership dot — small colored oval in corner
        if pos in self.ownership:
            oc = TOKEN_COLORS[self.ownership[pos]]
            self.canvas.create_oval(x2 - 10, y1 + 2, x2 - 2, y1 + 10,
                                    fill=oc, outline="white")

    def _split_name(self, name):
        words = name.split()
        if len(words) <= 2:
            return words
        mid = len(words) // 2
        return [" ".join(words[:mid]), " ".join(words[mid:])]

    def _draw_buildings_on_tile(self, pos, x1, y1, x2, y2, count):
        BAND = 16
        if 1 <= pos <= 9:
            # Bottom row: buildings near bottom of tile, inside the band
            bx1 = x1
            bby2 = y2 - BAND
            bby1 = y2 - BAND - 12
            if count == 5:  # Hotel
                self.canvas.create_rectangle(bx1 + 2, bby1, bx1 + 18, bby2,
                                             fill="#e74c3c", outline="white")
                self.canvas.create_text(bx1 + 10, (bby1 + bby2) / 2, text="H",
                                        font=("Helvetica", 6, "bold"), fill="white")
            else:
                for i in range(count):
                    self.canvas.create_rectangle(bx1 + 2 + i * 9, bby1,
                                                 bx1 + 9 + i * 9, bby2,
                                                 fill="#27ae60", outline="white")
        elif 11 <= pos <= 19:
            # Left col: buildings near the band (left side)
            bbx1 = x1 + BAND
            bbx2 = x1 + BAND + 12
            if count == 5:
                self.canvas.create_rectangle(bbx1, y1 + 2, bbx2, y1 + 18,
                                             fill="#e74c3c", outline="white")
                self.canvas.create_text((bbx1 + bbx2) / 2, y1 + 10, text="H",
                                        font=("Helvetica", 6, "bold"), fill="white")
            else:
                for i in range(count):
                    self.canvas.create_rectangle(bbx1, y1 + 2 + i * 9,
                                                 bbx2, y1 + 9 + i * 9,
                                                 fill="#27ae60", outline="white")
        elif 21 <= pos <= 29:
            # Top row: buildings near the top band
            bby1 = y1 + BAND
            bby2 = y1 + BAND + 12
            if count == 5:
                self.canvas.create_rectangle(x1 + 2, bby1, x1 + 18, bby2,
                                             fill="#e74c3c", outline="white")
                self.canvas.create_text(x1 + 10, (bby1 + bby2) / 2, text="H",
                                        font=("Helvetica", 6, "bold"), fill="white")
            else:
                for i in range(count):
                    self.canvas.create_rectangle(x1 + 2 + i * 9, bby1,
                                                 x1 + 9 + i * 9, bby2,
                                                 fill="#27ae60", outline="white")
        elif 31 <= pos <= 39:
            # Right col: buildings near the right band
            bbx2 = x2 - BAND
            bbx1 = x2 - BAND - 12
            if count == 5:
                self.canvas.create_rectangle(bbx1, y1 + 2, bbx2, y1 + 18,
                                             fill="#e74c3c", outline="white")
                self.canvas.create_text((bbx1 + bbx2) / 2, y1 + 10, text="H",
                                        font=("Helvetica", 6, "bold"), fill="white")
            else:
                for i in range(count):
                    self.canvas.create_rectangle(bbx1, y1 + 2 + i * 9,
                                                 bbx2, y1 + 9 + i * 9,
                                                 fill="#27ae60", outline="white")
        else:
            # Fallback (corners etc.)
            if count == 5:
                self.canvas.create_rectangle(x1 + 2, y1 + 2, x1 + 18, y1 + 12,
                                             fill="#e74c3c", outline="white")
                self.canvas.create_text(x1 + 10, y1 + 7, text="H",
                                        font=("Helvetica", 6, "bold"), fill="white")
            else:
                for i in range(count):
                    self.canvas.create_rectangle(x1 + 2 + i * 9, y1 + 2,
                                                 x1 + 9 + i * 9, y1 + 10,
                                                 fill="#27ae60", outline="white")

    def _draw_tokens(self):
        positions = {}
        for idx, player in enumerate(self.players):
            if not player.bankrupt:
                positions.setdefault(player.pos, []).append(idx)

        offsets = [(-11, -11), (11, -11), (-11, 11), (11, 11)]
        for pos, idxs in positions.items():
            x1, y1, x2, y2 = self._tile_rect(pos)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            for i, pidx in enumerate(idxs):
                ox, oy = (offsets[i] if len(idxs) > 1 else (0, 0))
                px, py = cx + ox, cy + oy
                r = 10
                col = TOKEN_COLORS[pidx]
                # Drop shadow
                self.canvas.create_oval(px-r+2, py-r+2, px+r+2, py+r+2,
                                        fill="#333333", outline="")
                # Filled circle
                self.canvas.create_oval(px-r, py-r, px+r, py+r,
                                        fill=col, outline="white", width=2)
                # Token emoji
                self.canvas.create_text(px, py-1, text=self.players[pidx].token,
                                        font=("Segoe UI Emoji", 8))

    def _draw_dice_on_canvas(self):
        self.dice_canvas.delete("all")
        d1, d2 = self.dice_result if self.dice_result[0] > 0 else (1, 1)
        self._draw_single_die(8, 7, 58, 57, d1)
        self._draw_single_die(72, 7, 122, 57, d2)

    def _draw_single_die(self, x1, y1, x2, y2, value):
        # Shadow
        self.dice_canvas.create_rectangle(x1+3, y1+3, x2+3, y2+3,
                                          fill="#333333", outline="")
        # Die face
        self.dice_canvas.create_rectangle(x1, y1, x2, y2,
                                          fill="#FAFAFA", outline="#333333", width=2)
        # Inner highlight
        self.dice_canvas.create_rectangle(x1+3, y1+3, x2-3, y1+12,
                                          fill="#FFFFFF", outline="")
        # Pip positions for each face value
        pip_layouts = {
            1: [(0.5, 0.5)],
            2: [(0.28, 0.28), (0.72, 0.72)],
            3: [(0.28, 0.28), (0.5, 0.5), (0.72, 0.72)],
            4: [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)],
            5: [(0.28, 0.28), (0.72, 0.28), (0.5, 0.5), (0.28, 0.72), (0.72, 0.72)],
            6: [(0.28, 0.2), (0.72, 0.2), (0.28, 0.5), (0.72, 0.5), (0.28, 0.8), (0.72, 0.8)],
        }
        w = x2 - x1
        h = y2 - y1
        pr = min(w, h) * 0.095
        for fx, fy in pip_layouts.get(value, [(0.5, 0.5)]):
            cx = x1 + fx * w
            cy = y1 + fy * h
            self.dice_canvas.create_oval(cx-pr, cy-pr, cx+pr, cy+pr,
                                         fill="#1a1a2e", outline="")

    # ─────────────────────────────────────────────────────────────────────
    # Panel refresh & logging
    # ─────────────────────────────────────────────────────────────────────
    def refresh_panel(self):
        self.turn_label.config(text=f"Turn #{self.turn_number}")
        self.fp_var.set(f"Free Parking Pot: ${self.free_parking_pot}")

        for i, player in enumerate(self.players):
            card = self.player_cards[i]
            is_current = (i == self.current and not player.bankrupt)
            bg = "#1e3a5f" if is_current else "#16213e"
            card["frame"].config(bg=bg)
            for key in ("name", "money", "status", "props", "dots", "net"):
                card[key].config(bg=bg)

            card["name"].config(text=f"{player.token} {player.name}",
                                fg=TOKEN_COLORS[i])
            card["money"].config(text=f"${player.money}")
            st = "CURRENT TURN" if is_current else player.status_text()
            card["status"].config(text=st)
            card["props"].config(text=f"{len(player.properties)} props")
            card["dots"].config(text=self._group_dots(i))
            net = self._calc_net_worth(i)
            card["net"].config(text=f"Net: ${net}")

        self._draw_dice_on_canvas()

    def _group_dots(self, player_idx):
        player = self.players[player_idx]
        owned_count = {}
        for pos in player.properties:
            g = BOARD[pos].get("group")
            if g:
                owned_count[g] = owned_count.get(g, 0) + 1

        group_symbols = [
            ("brown",       "🟤"),
            ("light-blue",  "🔵"),
            ("pink",        "🟣"),
            ("orange",      "🟠"),
            ("red",         "🔴"),
            ("yellow-prop", "🟡"),
            ("green",       "🟢"),
            ("dark-blue",   "🔵"),
        ]
        result = ""
        for g, sym in group_symbols:
            cnt = owned_count.get(g, 0)
            if cnt == 0:
                continue
            total = GROUP_SIZES.get(g, 0)
            result += sym if cnt >= total else "○"
        return result or "—"

    def _calc_net_worth(self, player_idx):
        player = self.players[player_idx]
        worth = player.money
        for pos in player.properties:
            tile = BOARD[pos]
            worth += tile["price"]
            b = self.buildings.get(pos, 0)
            if b > 0:
                g = tile.get("group", "")
                hcost = HOUSE_COSTS.get(g, 50)
                worth += b * hcost
        return worth

    def _update_buttons(self):
        player = self.players[self.current]
        is_human = player.is_human and not player.bankrupt
        phase = self.turn_phase

        self.roll_btn.config(
            state=tk.NORMAL if (is_human and phase in ("start", "extra_roll")) else tk.DISABLED)
        self.end_btn.config(
            state=tk.NORMAL if (is_human and phase == "rolled") else tk.DISABLED)
        self.manage_btn.config(
            state=tk.NORMAL if is_human else tk.DISABLED)
        self.trade_btn.config(
            state=tk.NORMAL if is_human else tk.DISABLED)
        self.undo_btn.config(
            state=tk.NORMAL if (is_human and self.last_purchase is not None) else tk.DISABLED)

        if is_human and player.in_jail and phase == "start":
            self.jail_btn.config(state=tk.NORMAL)
            if player.jail_free_cards > 0:
                self.jail_btn.config(text="🎴 USE JAIL FREE")
            else:
                self.jail_btn.config(text="🔓 PAY $50 BAIL")
        else:
            self.jail_btn.config(state=tk.DISABLED, text="🔓 GET OUT OF JAIL")

    def log(self, msg, tag="neutral"):
        if not hasattr(self, "_log_entries"):
            self._log_entries = []
        self._log_entries.append((msg, tag))
        if self._log_filter in ("all", tag):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, msg + "\n", tag)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

    def _apply_log_filter(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        for msg, tag in getattr(self, "_log_entries", []):
            if self._log_filter in ("all", tag):
                self.log_text.insert(tk.END, msg + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    # ─────────────────────────────────────────────────────────────────────
    # Dice rolling
    # ─────────────────────────────────────────────────────────────────────
    def roll_dice(self):
        player = self.players[self.current]
        if not player.is_human:
            return
        self.roll_btn.config(state=tk.DISABLED)
        self._animate_dice(0, self._after_human_roll)

    def _animate_dice(self, frame, callback):
        if frame >= 8:
            callback()
            return
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.dice_result = (d1, d2)
        self._draw_dice_on_canvas()
        self.animation_id = self.root.after(
            80, lambda: self._animate_dice(frame + 1, callback))

    def _after_human_roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self._process_roll(self.players[self.current], d1, d2, is_human=True)

    def _process_roll(self, player, d1, d2, is_human=False):
        self.dice_result = (d1, d2)
        self._draw_dice_on_canvas()
        self._play_sound("roll")
        is_doubles = (d1 == d2)
        self.log(f"{player.name} rolled {d1}+{d2}={'doubles!' if is_doubles else d1+d2}", "neutral")

        if player.in_jail:
            self._handle_jail_roll(player, d1, d2, is_doubles, is_human)
            return

        if is_doubles:
            player.doubles_count += 1
            if player.doubles_count >= 3:
                self.log(f"{player.name} rolled 3 doubles — Go to Jail!", "bad")
                self._send_to_jail(player)
                self.turn_phase = "rolled"
                self.refresh_panel()
                self._draw_board()
                self._update_buttons()
                return
        else:
            player.doubles_count = 0

        self._move_player(player, d1 + d2)

        if is_doubles:
            self.turn_phase = "extra_roll"
        else:
            self.turn_phase = "rolled"

        self.refresh_panel()
        self._draw_board()
        self._update_buttons()

        if not is_human:
            if is_doubles and not player.in_jail:
                self.root.after(self.ai_delay, self._ai_turn)
            else:
                self.root.after(self.ai_delay, self._ai_manage_and_end)

    def _handle_jail_roll(self, player, d1, d2, is_doubles, is_human):
        if is_doubles:
            player.in_jail = False
            player.jail_turns = 0
            player.doubles_count = 0
            self.log(f"{player.name} rolled doubles — escaped Jail!", "good")
            self._move_player(player, d1 + d2)
            self.turn_phase = "rolled"  # no bonus turn for jail escape
        else:
            player.jail_turns += 1
            if player.jail_turns >= 3:
                self.log(f"{player.name} forced to pay $50 bail after 3 turns.", "bad")
                self._pay(player, 50, to_parking=False)
                player.in_jail = False
                player.jail_turns = 0
                self._move_player(player, d1 + d2)
                self.turn_phase = "rolled"
            else:
                self.log(f"{player.name} failed to escape Jail (turn {player.jail_turns}/3).", "bad")
                self.turn_phase = "rolled"

        self.refresh_panel()
        self._draw_board()
        self._update_buttons()

        if not is_human:
            self.root.after(self.ai_delay, self._ai_manage_and_end)

    # ─────────────────────────────────────────────────────────────────────
    # Movement & landing
    # ─────────────────────────────────────────────────────────────────────
    def _move_player(self, player, steps):
        old_pos = player.pos
        new_pos = (old_pos + steps) % 40
        if new_pos < old_pos and not player.in_jail:
            player.money += 200
            self.log(f"{player.name} passed GO — collect $200!", "good")
        player.pos = new_pos
        self._land_on(player, new_pos)

    def _land_on(self, player, pos):
        tile = BOARD[pos]
        ttype = tile["type"]
        self.log(f"{player.name} landed on {tile['name']}.", "neutral")

        if ttype == "go":
            player.money += 200
            self.log(f"{player.name} landed on START — +$200!", "good")
        elif ttype == "gotojail":
            self._send_to_jail(player)
        elif ttype == "jail":
            self.log(f"{player.name} is just visiting.", "neutral")
        elif ttype == "freeparking":
            if self.free_parking_pot > 0:
                won = self.free_parking_pot
                player.money += won
                self._play_sound("good")
                self.log(f"{player.name} wins Free Parking pot: ${won}!", "good")
                self.free_parking_pot = 0
            else:
                self.log(f"{player.name} — Free Parking is empty.", "neutral")
        elif ttype == "tax":
            amount = tile["price"]
            self._pay(player, amount, to_parking=True)
            self.log(f"{player.name} paid ${amount} tax (goes to Free Parking).", "bad")
        elif ttype in ("chance", "chest"):
            self._play_sound("card")
            self._draw_card(player)
        elif ttype in ("property", "railroad", "utility"):
            self._handle_property_landing(player, pos, tile)

        self.refresh_panel()
        self._draw_board()

    def _send_to_jail(self, player):
        player.pos = 10
        player.in_jail = True
        player.jail_turns = 0
        player.doubles_count = 0
        self._play_sound("jail")
        self.log(f"{player.name} was sent to Jail!", "bad")

    # ─────────────────────────────────────────────────────────────────────
    # Money helpers
    # ─────────────────────────────────────────────────────────────────────
    def _pay(self, player, amount, to_parking=False, to_player=None):
        """Deduct amount from player; route to parking or another player."""
        player.money -= amount
        if to_parking:
            self.free_parking_pot += amount
        elif to_player is not None:
            to_player.money += amount
        if player.money < 0:
            self._handle_bankruptcy(player, to_player if to_player else None)

    def _show_toast(self, pos, text, color):
        """Show a floating toast message near a board tile for 1.5 seconds."""
        x1, y1, x2, y2 = self._tile_rect(pos)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        tag = f"toast_{self.toast_count}"
        self.toast_count += 1
        # Background pill
        tw = max(len(text) * 6 + 10, 60)
        self.canvas.create_rectangle(cx - tw//2, cy - 12, cx + tw//2, cy + 12,
                                     fill="#1a1a2e", outline=color, width=2, tags=tag)
        self.canvas.create_text(cx, cy, text=text,
                                font=("Helvetica", 8, "bold"), fill=color, tags=tag)
        self.root.after(1500, lambda t=tag: self.canvas.delete(t))

    # ─────────────────────────────────────────────────────────────────────
    # Property landing
    # ─────────────────────────────────────────────────────────────────────
    def _handle_property_landing(self, player, pos, tile):
        pidx = self.players.index(player)

        if pos in self.ownership:
            owner_idx = self.ownership[pos]
            if owner_idx == pidx:
                return  # own property
            owner = self.players[owner_idx]
            if owner.bankrupt:
                return
            if self.mortgaged.get(pos):
                self.log(f"{tile['name']} is mortgaged — no rent.", "neutral")
                return
            rent = self._calc_rent(pos, tile)
            if self.nearest_rr_double and tile["type"] == "railroad":
                rent *= 2
                self.nearest_rr_double = False
            self.log(f"{player.name} pays ${rent} rent to {owner.name}.", "bad")
            self._play_sound("rent")
            self._pay(player, rent, to_player=owner)
            self._show_toast(pos, f"-${rent} rent", "#e74c3c")
        else:
            # Unowned
            if player.is_human:
                self._offer_buy_human(player, pos, tile)
            else:
                self._ai_buy_decision(player, pos, tile)

    def _calc_rent(self, pos, tile):
        ttype = tile["type"]
        if ttype == "railroad":
            owner_idx = self.ownership[pos]
            count = sum(1 for t in BOARD
                        if t["type"] == "railroad"
                        and self.ownership.get(t["pos"]) == owner_idx)
            return [0, 25, 50, 100, 200][min(count, 4)]

        elif ttype == "utility":
            owner_idx = self.ownership[pos]
            count = sum(1 for t in BOARD
                        if t["type"] == "utility"
                        and self.ownership.get(t["pos"]) == owner_idx)
            d1, d2 = self.dice_result
            multiplier = 10 if count >= 2 else 4
            return multiplier * (d1 + d2)

        else:  # property
            bcount = self.buildings.get(pos, 0)
            rent = tile["price"] * RENT_MULTIPLIERS[bcount]
            # Monopoly doubles base rent when no buildings
            if bcount == 0 and self._has_monopoly(self.ownership[pos], tile["group"]):
                rent *= 2
            return int(rent)

    def _has_monopoly(self, player_idx, group):
        if not group or group in ("railroad", "utility"):
            return False
        size = GROUP_SIZES.get(group, 0)
        count = sum(1 for t in BOARD
                    if t.get("group") == group
                    and self.ownership.get(t["pos"]) == player_idx)
        return count >= size

    # ─────────────────────────────────────────────────────────────────────
    # Buying & auctioning
    # ─────────────────────────────────────────────────────────────────────
    def _offer_buy_human(self, player, pos, tile):
        answer = messagebox.askyesno(
            "Buy Property?",
            f"Buy {tile['name']} for ${tile['price']}?\n"
            f"Your balance: ${player.money}  →  ${player.money - tile['price']}",
            parent=self.root,
        )
        if answer and player.money >= tile["price"]:
            self._buy_property(player, pos, tile)
            self.log(f"You bought {tile['name']} for ${tile['price']}.", "good")
        else:
            reason = "declined" if answer or player.money < tile["price"] else "declined"
            self.log(f"You {reason} {tile['name']} — going to auction.", "neutral")
            self._start_auction(pos, tile, skip_idx=self.players.index(player))

    def _ai_buy_decision(self, player, pos, tile):
        pidx = self.players.index(player)
        group = tile.get("group")
        owned_in_group = sum(1 for t in BOARD if t.get("group") == group
                             and self.ownership.get(t["pos"]) == pidx) if group else 0
        group_size = GROUP_SIZES.get(group, 0) if group else 0
        # Lower buffer when close to completing a monopoly
        if group_size > 0 and owned_in_group >= group_size - 1:
            buffer = 100
        elif tile["type"] in ("railroad", "utility"):
            buffer = 150
        else:
            buffer = 200
        if player.money >= tile["price"] + buffer:
            self._buy_property(player, pos, tile)
            self.log(f"{player.name} bought {tile['name']} for ${tile['price']}.", "good")
        else:
            self.log(f"{player.name} declined {tile['name']}.", "neutral")
            self._start_auction(pos, tile, skip_idx=pidx)

    def _buy_property(self, player, pos, tile):
        player.money -= tile["price"]
        player.properties.append(pos)
        pidx = self.players.index(player)
        self.ownership[pos] = pidx
        if player.is_human:
            self.last_purchase = {"pos": pos, "price": tile["price"], "pidx": pidx}
        self._play_sound("buy")

    def _start_auction(self, pos, tile, skip_idx=None):
        self.log(f"Auction: {tile['name']} (list price ${tile['price']}).", "system")
        bids = {}

        # AI bids
        for idx, player in enumerate(self.players):
            if player.bankrupt or idx == skip_idx:
                continue
            if not player.is_human:
                max_bid = int(tile["price"] * 0.80)
                bid = min(max_bid, player.money)
                if bid >= 10:
                    bids[idx] = bid

        # Human bid
        human_idx = next((i for i, p in enumerate(self.players)
                          if p.is_human and not p.bankrupt and i != skip_idx), None)
        if human_idx is not None:
            human = self.players[human_idx]
            current_high = max(bids.values()) if bids else 0
            raw = simpledialog.askstring(
                "Auction",
                f"Auction: {tile['name']}\nHighest AI bid: ${current_high}\n"
                f"Your cash: ${human.money}\nYour bid (0 = pass):",
                parent=self.root,
            )
            try:
                hbid = int(raw) if raw else 0
            except ValueError:
                hbid = 0
            if 0 < hbid <= human.money:
                bids[human_idx] = hbid

        if not bids:
            self.log(f"No bids — {tile['name']} stays with bank.", "system")
            return

        winner_idx = max(bids, key=lambda k: bids[k])
        winning_bid = bids[winner_idx]
        winner = self.players[winner_idx]
        winner.money -= winning_bid
        winner.properties.append(pos)
        self.ownership[pos] = winner_idx
        self.log(f"{winner.name} won auction for {tile['name']} at ${winning_bid}!", "system")

    def _show_card_overlay(self, desc):
        """Show a card text overlay on the board center for 2 seconds."""
        S = self._SIZE
        cx, cy = S / 2, S / 2
        tag = "card_overlay"
        self.canvas.delete(tag)
        # Backdrop
        self.canvas.create_rectangle(cx - 200, cy - 70, cx + 200, cy + 70,
                                     fill="#1a1a2e", outline="#f39c12", width=3, tags=tag)
        self.canvas.create_text(cx, cy - 20, text="📋 FATE CARD",
                                font=("Helvetica", 10, "bold"), fill="#f39c12", tags=tag)
        self.canvas.create_text(cx, cy + 10, text=desc,
                                font=("Helvetica", 9), fill="white",
                                width=370, justify=tk.CENTER, tags=tag)
        self.root.after(2000, lambda: self.canvas.delete(tag))

    # ─────────────────────────────────────────────────────────────────────
    # Card mechanics
    # ─────────────────────────────────────────────────────────────────────
    def _draw_card(self, player):
        card = self.card_deck[self.card_index % len(self.card_deck)]
        self.card_index += 1
        self.log(f"Card: {card['desc']}", "card")
        self._show_card_overlay(card["desc"])

        action = card["action"]

        if action == "money":
            amt = card["amount"]
            if amt > 0:
                player.money += amt
                self.log(f"{player.name} received ${amt}.", "good")
            else:
                self._pay(player, -amt, to_parking=True)
                self.log(f"{player.name} paid ${-amt}.", "bad")

        elif action == "gotojail":
            self._send_to_jail(player)

        elif action == "advance":
            dest = card["dest"]
            if dest <= player.pos:
                player.money += 200
                self.log(f"{player.name} passed GO — +$200!", "good")
            player.pos = dest
            self._land_on(player, dest)

        elif action == "back3":
            player.pos = (player.pos - 3) % 40
            self._land_on(player, player.pos)

        elif action == "nearest_rr":
            rr_positions = [t["pos"] for t in BOARD if t["type"] == "railroad"]
            dist = [(rp - player.pos) % 40 for rp in rr_positions]
            nearest = rr_positions[dist.index(min(dist))]
            if nearest <= player.pos:
                player.money += 200
                self.log(f"{player.name} passed GO — +$200!", "good")
            player.pos = nearest
            self.nearest_rr_double = True
            self._land_on(player, nearest)

        elif action == "collect_all":
            amt = card["amount"]
            pidx = self.players.index(player)
            for idx, other in enumerate(self.players):
                if idx != pidx and not other.bankrupt:
                    self._pay(other, amt, to_player=player)
            self.log(f"{player.name} collected ${amt} from each player.", "good")

        elif action == "pay_all":
            amt = card["amount"]
            pidx = self.players.index(player)
            for idx, other in enumerate(self.players):
                if idx != pidx and not other.bankrupt:
                    self._pay(player, amt, to_player=other)
            self.log(f"{player.name} paid ${amt} to each player.", "bad")

        elif action == "jailfree":
            player.jail_free_cards += 1
            self.log(f"{player.name} got a Get Out of Jail Free card!", "good")

        elif action == "house_repairs":
            houses = sum(1 for p in player.properties
                         if 0 < self.buildings.get(p, 0) < 5)
            hotels = sum(1 for p in player.properties
                         if self.buildings.get(p, 0) == 5)
            cost = houses * 40 + hotels * 115
            if cost > 0:
                self._pay(player, cost, to_parking=True)
                self.log(f"{player.name} paid ${cost} for repairs "
                         f"({houses}h/{hotels}H).", "bad")

    # ─────────────────────────────────────────────────────────────────────
    # Jail button
    # ─────────────────────────────────────────────────────────────────────
    def get_out_of_jail_btn(self):
        player = self.players[self.current]
        if not player.in_jail:
            return
        if player.jail_free_cards > 0:
            player.jail_free_cards -= 1
            player.in_jail = False
            player.jail_turns = 0
            self.log(f"{player.name} used Get Out of Jail Free card!", "good")
        else:
            if player.money < 50:
                self.log("Not enough money for $50 bail!", "bad")
                return
            player.money -= 50
            player.in_jail = False
            player.jail_turns = 0
            self.log(f"{player.name} paid $50 bail.", "bad")
        self.refresh_panel()
        self._draw_board()
        self._update_buttons()

    # ─────────────────────────────────────────────────────────────────────
    # Turn flow
    # ─────────────────────────────────────────────────────────────────────
    def end_turn(self):
        player = self.players[self.current]
        if not player.is_human:
            return
        player.doubles_count = 0
        self.nearest_rr_double = False
        self.next_turn()

    def next_turn(self):
        self.turn_number += 1
        active = [i for i, p in enumerate(self.players) if not p.bankrupt]
        if len(active) <= 1:
            winner = self.players[active[0]] if active else None
            if winner:
                self.log(f"{winner.name} wins!", "system")
                self._show_win_screen(winner)
            return

        # Advance current — loop (not recursion) to skip bankrupt
        self.current = (self.current + 1) % 4
        while self.players[self.current].bankrupt:
            self.current = (self.current + 1) % 4

        self.turn_phase = "start"
        self.dice_result = (0, 0)
        self.players[self.current].doubles_count = 0

        self.refresh_panel()
        self._draw_board()
        self._update_buttons()

        cp = self.players[self.current]
        self.log(f"--- {cp.name}'s turn ---", "system")
        self.status_var.set(f"{cp.name}'s turn")

        if not cp.is_human:
            self.root.after(self.ai_delay, self._ai_turn)

    def _ai_turn(self):
        player = self.players[self.current]
        if player.bankrupt or player.is_human:
            return

        # Jail logic
        if player.in_jail:
            if player.jail_free_cards > 0:
                player.jail_free_cards -= 1
                player.in_jail = False
                player.jail_turns = 0
                self.log(f"{player.name} used Jail Free card.", "good")
            elif player.jail_turns >= 2:
                if player.money >= 50:
                    player.money -= 50
                    player.in_jail = False
                    player.jail_turns = 0
                    self.log(f"{player.name} paid $50 bail.", "bad")

        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self._process_roll(player, d1, d2, is_human=False)

    def _ai_manage_and_end(self):
        player = self.players[self.current]
        pidx = self.current

        # Auto-unmortgage if cash is healthy
        for pos in list(player.properties):
            if self.mortgaged.get(pos) and self.buildings.get(pos, 0) == 0:
                tile = BOARD[pos]
                cost = int(tile["price"] * 0.55)
                if player.money >= cost + 400:
                    player.money -= cost
                    self.mortgaged[pos] = False
                    self.log(f"{player.name} unmortgaged {tile['name']}.", "good")
                    break

        # Auto-build when monopoly is held — up to 2 builds per turn
        builds_this_turn = 0
        for group in HOUSE_COSTS:
            if builds_this_turn >= 2:
                break
            if not self._has_monopoly(pidx, group):
                continue
            house_cost = HOUSE_COSTS[group]
            group_props = sorted(
                [t["pos"] for t in BOARD if t.get("group") == group],
                key=lambda p: self.buildings.get(p, 0),
            )
            for prop_pos in group_props:
                if self.buildings.get(prop_pos, 0) >= 5:
                    continue
                if self.mortgaged.get(prop_pos):
                    continue
                if not self._can_build_here(pidx, prop_pos, group):
                    continue
                if player.money >= house_cost + 150:
                    self.buildings[prop_pos] = self.buildings.get(prop_pos, 0) + 1
                    player.money -= house_cost
                    self.log(f"{player.name} built on {BOARD[prop_pos]['name']}.", "good")
                    builds_this_turn += 1
                break

        self.refresh_panel()
        self._draw_board()
        self.root.after(self.ai_delay, self.next_turn)

    # ─────────────────────────────────────────────────────────────────────
    # Bankruptcy
    # ─────────────────────────────────────────────────────────────────────
    def _handle_bankruptcy(self, player, creditor=None):
        if player.money >= 0:
            return

        # Try to liquidate buildings
        for pos in list(player.properties):
            while self.buildings.get(pos, 0) > 0:
                tile = BOARD[pos]
                refund = HOUSE_COSTS.get(tile.get("group", ""), 50) // 2
                self.buildings[pos] -= 1
                player.money += refund
                if player.money >= 0:
                    return

        # Try to mortgage properties
        for pos in list(player.properties):
            if not self.mortgaged.get(pos, False) and self.buildings.get(pos, 0) == 0:
                tile = BOARD[pos]
                mv = tile["price"] // 2
                self.mortgaged[pos] = True
                player.money += mv
                if player.money >= 0:
                    return

        # Truly bankrupt
        player.bankrupt = True
        self.log(f"{player.name} is bankrupt!", "bad")

        pidx = self.players.index(player)
        if creditor is not None:
            cidx = self.players.index(creditor)
            for pos in list(player.properties):
                self.ownership[pos] = cidx
                creditor.properties.append(pos)
            self.log(f"{player.name}'s assets transferred to {creditor.name}.", "bad")
        else:
            for pos in list(player.properties):
                del self.ownership[pos]
                self.buildings.pop(pos, None)
                self.mortgaged.pop(pos, None)
            self.log(f"{player.name}'s assets returned to bank.", "bad")

        player.properties.clear()

        # Check game over
        active = [p for p in self.players if not p.bankrupt]
        if len(active) == 1:
            self.log(f"{active[0].name} WINS!", "system")
            self._show_win_screen(active[0])

    # ─────────────────────────────────────────────────────────────────────
    # Canvas click → tile info popup
    # ─────────────────────────────────────────────────────────────────────
    def _canvas_click(self, event):
        x, y = event.x, event.y
        for tile in BOARD:
            x1, y1, x2, y2 = self._tile_rect(tile["pos"])
            if x1 <= x <= x2 and y1 <= y <= y2:
                self._show_tile_info(tile)
                return

    def _show_tile_info(self, tile):
        pos = tile["pos"]
        dlg = tk.Toplevel(self.root)
        dlg.title(tile["name"])
        dlg.geometry("300x400")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, False)
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() - 300) // 2
        y = (dlg.winfo_screenheight() - 400) // 2
        dlg.geometry(f"300x400+{x}+{y}")

        # Color band header
        band_color = tile.get("color") or "#555555"
        if tile["type"] not in ("property", "railroad", "utility"):
            band_color = "#1B5E20"
        header = tk.Frame(dlg, bg=band_color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text=tile["name"].upper(),
                 font=("Georgia", 13, "bold"), fg="white", bg=band_color).pack(expand=True)

        body = tk.Frame(dlg, bg="#16213e", padx=12, pady=8)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        def row(label, value, vc="#bdc3c7"):
            f = tk.Frame(body, bg="#16213e")
            f.pack(fill=tk.X, pady=1)
            tk.Label(f, text=label, font=("Helvetica", 9),
                     fg="#95a5a6", bg="#16213e", anchor="w", width=14).pack(side=tk.LEFT)
            tk.Label(f, text=value, font=("Helvetica", 9, "bold"),
                     fg=vc, bg="#16213e", anchor="w").pack(side=tk.LEFT)

        row("Type:", tile["type"].capitalize())
        if tile["price"] > 0:
            row("Price:", f"${tile['price']}", "#f39c12")
        if pos in self.ownership:
            owner = self.players[self.ownership[pos]]
            row("Owner:", f"{owner.token} {owner.name}", owner.color)
            if tile["type"] == "property":
                b = self.buildings.get(pos, 0)
                row("Buildings:", "Hotel" if b == 5 else str(b))
                for lvl in range(6):
                    base_rent = int(tile["price"] * RENT_MULTIPLIERS[lvl])
                    if lvl == 0 and self._has_monopoly(self.ownership[pos], tile.get("group")):
                        base_rent *= 2
                    lbl = ["Base", "1H", "2H", "3H", "4H", "Hotel"][lvl]
                    current = (b == lvl)
                    row(f"Rent {lbl}:", f"${base_rent}",
                        "#2ecc71" if current else "#bdc3c7")
            elif tile["type"] == "railroad":
                rent = self._calc_rent(pos, tile)
                row("Current Rent:", f"${rent}", "#2ecc71")
            elif tile["type"] == "utility":
                own_cnt = sum(1 for t in BOARD if t["type"] == "utility"
                              and self.ownership.get(t["pos"]) == self.ownership[pos])
                mult = 10 if own_cnt >= 2 else 4
                row("Rent Multiplier:", f"×{mult} dice", "#2ecc71")
        else:
            row("Owner:", "Bank (for sale)")
        if self.mortgaged.get(pos):
            row("Status:", "MORTGAGED", "#e74c3c")

        tk.Button(dlg, text="Close", command=dlg.destroy,
                  bg="#c0392b", fg="white",
                  font=("Helvetica", 10, "bold"), pady=4).pack(pady=8)

    # ─────────────────────────────────────────────────────────────────────
    # Property Management Dialog
    # ─────────────────────────────────────────────────────────────────────
    def open_manage_dialog(self):
        player = self.players[self.current]
        if not player.is_human:
            return
        pidx = self.current

        dlg = tk.Toplevel(self.root)
        dlg.title("Manage Properties")
        dlg.geometry("540x580")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, True)

        tk.Label(dlg,
                 text=f"Properties — {player.name}  (Cash: ${player.money})",
                 font=("Helvetica", 12, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack(pady=6)

        # Scrollable canvas
        outer = tk.Frame(dlg, bg="#1a1a2e")
        outer.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        scr_canvas = tk.Canvas(outer, bg="#1a1a2e", highlightthickness=0)
        vsb = tk.Scrollbar(outer, orient=tk.VERTICAL, command=scr_canvas.yview)
        scr_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        scr_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(scr_canvas, bg="#1a1a2e")
        cw = scr_canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner_configure(event):
            scr_canvas.configure(scrollregion=scr_canvas.bbox("all"))

        def _on_canvas_configure(event):
            scr_canvas.itemconfig(cw, width=event.width)

        inner.bind("<Configure>", _on_inner_configure)
        scr_canvas.bind("<Configure>", _on_canvas_configure)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()

            groups_order = [
                "brown", "light-blue", "pink", "orange",
                "red", "yellow-prop", "green", "dark-blue",
                "railroad", "utility",
            ]
            # Bucket player properties by group
            grouped = {g: [] for g in groups_order}
            for pos in sorted(player.properties):
                g = BOARD[pos].get("group")
                if g in grouped:
                    grouped[g].append(pos)

            for group in groups_order:
                props = grouped[group]
                if not props:
                    continue

                monopoly = self._has_monopoly(pidx, group)
                sample_tile = BOARD[props[0]]
                gcolor = sample_tile["color"] or "#888888"

                # Group header
                header_text = ("★  " if monopoly else "") + group.upper() + ("  ★" if monopoly else "")
                hf = tk.Frame(inner, bg=gcolor, pady=2)
                hf.pack(fill=tk.X, pady=(10, 1), padx=5)
                tk.Label(hf, text=header_text,
                         font=("Helvetica", 9, "bold"),
                         fg="white", bg=gcolor).pack()

                for prop_pos in props:
                    tile = BOARD[prop_pos]
                    is_mort = self.mortgaged.get(prop_pos, False)
                    bcount  = self.buildings.get(prop_pos, 0)
                    btext   = "Hotel" if bcount == 5 else (f"{bcount}H" if bcount > 0 else "no bldg")

                    row = tk.Frame(inner, bg="#16213e", pady=3)
                    row.pack(fill=tk.X, pady=1, padx=12)

                    info = f"{tile['name']}  [{btext}]"
                    if is_mort:
                        info += "  [MORTGAGED]"
                    tk.Label(row, text=info,
                             font=("Helvetica", 8),
                             fg="#e74c3c" if is_mort else "#bdc3c7",
                             bg="#16213e", anchor="w").pack(side=tk.LEFT, padx=5)

                    btns = tk.Frame(row, bg="#16213e")
                    btns.pack(side=tk.RIGHT, padx=3)

                    # Build button
                    if group not in ("railroad", "utility") and monopoly and not is_mort:
                        hcost = HOUSE_COSTS.get(group, 100)
                        can_build = (bcount < 5 and
                                     self._can_build_here(pidx, prop_pos, group))
                        if can_build:
                            def _do_build(p=prop_pos, g=group):
                                hc = HOUSE_COSTS.get(g, 100)
                                if player.money < hc:
                                    self.log("Not enough money to build.", "bad")
                                    return
                                player.money -= hc
                                self.buildings[p] = self.buildings.get(p, 0) + 1
                                self.log(f"Built on {BOARD[p]['name']}. Cost ${hc}.", "good")
                                self.refresh_panel()
                                self._draw_board()
                                refresh()
                            tk.Button(btns, text=f"Build ${hcost}",
                                      command=_do_build,
                                      bg="#27ae60", fg="white",
                                      font=("Helvetica", 7), padx=3).pack(side=tk.LEFT, padx=1)

                    # Sell building button
                    if bcount > 0 and self._can_sell_here(pidx, prop_pos, group):
                        refund = HOUSE_COSTS.get(group, 100) // 2
                        def _do_sell(p=prop_pos, g=group):
                            r = HOUSE_COSTS.get(g, 100) // 2
                            player.money += r
                            self.buildings[p] = max(0, self.buildings.get(p, 0) - 1)
                            self.log(f"Sold building on {BOARD[p]['name']}. +${r}.", "good")
                            self.refresh_panel()
                            self._draw_board()
                            refresh()
                        tk.Button(btns, text=f"Sell +${refund}",
                                  command=_do_sell,
                                  bg="#e67e22", fg="white",
                                  font=("Helvetica", 7), padx=3).pack(side=tk.LEFT, padx=1)

                    # Mortgage button
                    if not is_mort and bcount == 0:
                        mv = tile["price"] // 2
                        def _do_mortgage(p=prop_pos, t=tile):
                            val = t["price"] // 2
                            player.money += val
                            self.mortgaged[p] = True
                            self.log(f"Mortgaged {t['name']} for +${val}.", "neutral")
                            self.refresh_panel()
                            self._draw_board()
                            refresh()
                        tk.Button(btns, text=f"Mortgage +${mv}",
                                  command=_do_mortgage,
                                  bg="#7f8c8d", fg="white",
                                  font=("Helvetica", 7), padx=3).pack(side=tk.LEFT, padx=1)

                    # Unmortgage button
                    if is_mort:
                        cost = int(tile["price"] * 0.55)
                        def _do_unmortgage(p=prop_pos, t=tile):
                            uc = int(t["price"] * 0.55)
                            if player.money < uc:
                                self.log("Not enough money to unmortgage.", "bad")
                                return
                            player.money -= uc
                            self.mortgaged[p] = False
                            self.log(f"Unmortgaged {t['name']}. Cost ${uc}.", "good")
                            self.refresh_panel()
                            self._draw_board()
                            refresh()
                        tk.Button(btns, text=f"Unmortgage ${cost}",
                                  command=_do_unmortgage,
                                  bg="#2980b9", fg="white",
                                  font=("Helvetica", 7), padx=3).pack(side=tk.LEFT, padx=1)

        refresh()

        tk.Button(dlg, text="Close", command=dlg.destroy,
                  bg="#c0392b", fg="white",
                  font=("Helvetica", 10, "bold")).pack(pady=6)

    # ─────────────────────────────────────────────────────────────────────
    # Even building helpers
    # ─────────────────────────────────────────────────────────────────────
    def _can_build_here(self, pidx, prop_pos, group):
        """Can only build if this property has <= buildings of every other in group."""
        group_props = [t["pos"] for t in BOARD if t.get("group") == group]
        my_count = self.buildings.get(prop_pos, 0)
        for pp in group_props:
            if pp != prop_pos:
                if self.buildings.get(pp, 0) < my_count:
                    return False
        return True

    def _can_sell_here(self, pidx, prop_pos, group):
        """Can only sell if this property has >= buildings of every other in group."""
        group_props = [t["pos"] for t in BOARD if t.get("group") == group]
        my_count = self.buildings.get(prop_pos, 0)
        for pp in group_props:
            if pp != prop_pos:
                if self.buildings.get(pp, 0) > my_count:
                    return False
        return True

    # ─────────────────────────────────────────────────────────────────────
    # Sound Effects
    # ─────────────────────────────────────────────────────────────────────
    def _play_sound(self, sound_type):
        if not self.sound_enabled:
            return
        freqs = {"roll": (700, 60), "buy": (880, 120), "rent": (300, 180),
                 "jail": (200, 350), "good": (1000, 100), "card": (550, 140)}
        freq, dur = freqs.get(sound_type, (500, 80))
        def _do():
            try:
                import winsound
                winsound.Beep(freq, dur)
            except Exception:
                pass
        threading.Thread(target=_do, daemon=True).start()

    # ─────────────────────────────────────────────────────────────────────
    # Undo Last Purchase
    # ─────────────────────────────────────────────────────────────────────
    def undo_purchase(self):
        if not self.last_purchase:
            self.log("Nothing to undo.", "neutral")
            return
        lp = self.last_purchase
        player = self.players[lp["pidx"]]
        pos = lp["pos"]
        tile = BOARD[pos]
        player.money += lp["price"]
        if pos in player.properties:
            player.properties.remove(pos)
        self.ownership.pop(pos, None)
        self.buildings.pop(pos, None)
        self.mortgaged.pop(pos, None)
        self.last_purchase = None
        self.log(f"Undid purchase of {tile['name']} — refunded ${lp['price']}.", "good")
        self.refresh_panel()
        self._draw_board()
        self._update_buttons()

    # ─────────────────────────────────────────────────────────────────────
    # Save / Load Game
    # ─────────────────────────────────────────────────────────────────────
    def save_game(self):
        data = {
            "turn_number": self.turn_number,
            "current": self.current,
            "turn_phase": self.turn_phase,
            "free_parking_pot": self.free_parking_pot,
            "card_index": self.card_index,
            "ownership": {str(k): v for k, v in self.ownership.items()},
            "buildings": {str(k): v for k, v in self.buildings.items()},
            "mortgaged": {str(k): v for k, v in self.mortgaged.items()},
            "dice_result": list(self.dice_result),
            "players": [
                {
                    "name": p.name, "token": p.token, "color": p.color,
                    "is_human": p.is_human, "money": p.money, "pos": p.pos,
                    "in_jail": p.in_jail, "jail_turns": p.jail_turns,
                    "jail_free_cards": p.jail_free_cards,
                    "doubles_count": p.doubles_count,
                    "properties": p.properties, "bankrupt": p.bankrupt,
                }
                for p in self.players
            ],
        }
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monopoly_save.json")
        with open(save_path, "w") as f:
            json.dump(data, f, indent=2)
        self.log(f"Game saved.", "system")

    def load_game(self):
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monopoly_save.json")
        if not os.path.exists(save_path):
            self.log("No save file found.", "bad")
            return
        with open(save_path) as f:
            data = json.load(f)
        self.turn_number = data["turn_number"]
        self.current = data["current"]
        self.turn_phase = data["turn_phase"]
        self.free_parking_pot = data["free_parking_pot"]
        self.card_index = data["card_index"]
        self.ownership = {int(k): v for k, v in data["ownership"].items()}
        self.buildings = {int(k): v for k, v in data["buildings"].items()}
        self.mortgaged = {int(k): v for k, v in data["mortgaged"].items()}
        self.dice_result = tuple(data["dice_result"])
        for i, pd in enumerate(data["players"]):
            p = self.players[i]
            p.name = pd["name"]
            p.token = pd["token"]
            p.color = pd["color"]
            p.money = pd["money"]
            p.pos = pd["pos"]
            p.in_jail = pd["in_jail"]
            p.jail_turns = pd["jail_turns"]
            p.jail_free_cards = pd["jail_free_cards"]
            p.doubles_count = pd["doubles_count"]
            p.properties = pd["properties"]
            p.bankrupt = pd["bankrupt"]
        self.last_purchase = None
        self.refresh_panel()
        self._draw_board()
        self._update_buttons()
        self.log("Game loaded.", "system")

    # ─────────────────────────────────────────────────────────────────────
    # Trading Dialog
    # ─────────────────────────────────────────────────────────────────────
    def open_trade_dialog(self):
        player = self.players[self.current]
        if not player.is_human:
            return
        pidx = self.current
        # Find AI players to trade with
        ai_players = [(i, p) for i, p in enumerate(self.players)
                      if not p.is_human and not p.bankrupt and p.properties]
        if not ai_players:
            self.log("No AI players have properties to trade.", "neutral")
            return

        dlg = tk.Toplevel(self.root)
        dlg.title("Trade Properties")
        dlg.geometry("480x560")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, False)

        tk.Label(dlg, text="🤝 TRADE", font=("Georgia", 14, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack(pady=(10, 4))

        # Select trading partner
        tk.Label(dlg, text="Trade with:", font=("Helvetica", 9),
                 fg="#bdc3c7", bg="#1a1a2e").pack()
        partner_var = tk.IntVar(value=ai_players[0][0])
        pf = tk.Frame(dlg, bg="#1a1a2e")
        pf.pack()
        for ai_idx, ai_p in ai_players:
            tk.Radiobutton(pf, text=f"{ai_p.token} {ai_p.name}",
                           variable=partner_var, value=ai_idx,
                           bg="#1a1a2e", fg="white", selectcolor="#16213e",
                           activebackground="#1a1a2e",
                           font=("Helvetica", 9)).pack(side=tk.LEFT, padx=6)

        lists_frame = tk.Frame(dlg, bg="#1a1a2e")
        lists_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Your properties
        your_frame = tk.Frame(lists_frame, bg="#1a1a2e")
        your_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(your_frame, text="You offer:", font=("Helvetica", 9, "bold"),
                 fg="#2ecc71", bg="#1a1a2e").pack()
        your_listbox = tk.Listbox(your_frame, bg="#16213e", fg="white",
                                  selectbackground="#27ae60",
                                  font=("Courier", 8), height=12)
        your_listbox.pack(fill=tk.BOTH, expand=True)

        # Their properties
        their_frame = tk.Frame(lists_frame, bg="#1a1a2e")
        their_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(their_frame, text="You receive:", font=("Helvetica", 9, "bold"),
                 fg="#e74c3c", bg="#1a1a2e").pack()
        their_listbox = tk.Listbox(their_frame, bg="#16213e", fg="white",
                                   selectbackground="#e74c3c",
                                   font=("Courier", 8), height=12)
        their_listbox.pack(fill=tk.BOTH, expand=True)

        # Cash offer
        cash_frame = tk.Frame(dlg, bg="#1a1a2e")
        cash_frame.pack(fill=tk.X, padx=10, pady=4)
        tk.Label(cash_frame, text="Cash you add ($):", font=("Helvetica", 9),
                 fg="#bdc3c7", bg="#1a1a2e").pack(side=tk.LEFT)
        cash_var = tk.StringVar(value="0")
        tk.Entry(cash_frame, textvariable=cash_var, width=8,
                 bg="#16213e", fg="white", insertbackground="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT, padx=4)

        def populate_lists():
            your_listbox.delete(0, tk.END)
            their_listbox.delete(0, tk.END)
            for pos in sorted(player.properties):
                tile = BOARD[pos]
                your_listbox.insert(tk.END, f"${tile['price']:>3} {tile['name']}")
            ai_idx = partner_var.get()
            for pos in sorted(self.players[ai_idx].properties):
                tile = BOARD[pos]
                their_listbox.insert(tk.END, f"${tile['price']:>3} {tile['name']}")

        populate_lists()
        for rb_widget in pf.winfo_children():
            rb_widget.config(command=populate_lists)

        def do_trade():
            ai_idx = partner_var.get()
            ai_player = self.players[ai_idx]
            your_sel = your_listbox.curselection()
            their_sel = their_listbox.curselection()
            if not your_sel and not their_sel:
                self.log("Select at least one property for trade.", "neutral")
                return
            try:
                cash = int(cash_var.get())
            except ValueError:
                cash = 0

            your_props = [sorted(player.properties)[i] for i in your_sel]
            their_props = [sorted(ai_player.properties)[i] for i in their_sel]

            if cash > player.money:
                self.log("Not enough cash for this trade.", "bad")
                return

            # Execute trade
            for pos in your_props:
                player.properties.remove(pos)
                ai_player.properties.append(pos)
                self.ownership[pos] = ai_idx
            for pos in their_props:
                ai_player.properties.remove(pos)
                player.properties.append(pos)
                self.ownership[pos] = pidx
            if cash > 0:
                player.money -= cash
                ai_player.money += cash

            self.log(f"Trade complete: gave {len(your_props)} prop(s), got {len(their_props)} prop(s).", "good")
            self.refresh_panel()
            self._draw_board()
            dlg.destroy()

        tk.Button(dlg, text="✅ CONFIRM TRADE", command=do_trade,
                  bg="#27ae60", fg="white",
                  font=("Helvetica", 11, "bold"), pady=6).pack(pady=6)
        tk.Button(dlg, text="Cancel", command=dlg.destroy,
                  bg="#c0392b", fg="white",
                  font=("Helvetica", 9)).pack()

    # ─────────────────────────────────────────────────────────────────────
    # Property List View
    # ─────────────────────────────────────────────────────────────────────
    def open_props_list_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("All Properties")
        dlg.geometry("400x560")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, True)

        tk.Label(dlg, text="📋 ALL PROPERTIES", font=("Georgia", 13, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack(pady=(8, 4))

        outer = tk.Frame(dlg, bg="#1a1a2e")
        outer.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        scr = tk.Canvas(outer, bg="#1a1a2e", highlightthickness=0)
        vsb = tk.Scrollbar(outer, orient=tk.VERTICAL, command=scr.yview)
        scr.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        scr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inner = tk.Frame(scr, bg="#1a1a2e")
        cw = scr.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: scr.configure(scrollregion=scr.bbox("all")))
        scr.bind("<Configure>", lambda e: scr.itemconfig(cw, width=e.width))

        groups_order = ["brown", "light-blue", "pink", "orange",
                        "red", "yellow-prop", "green", "dark-blue",
                        "railroad", "utility"]
        for group in groups_order:
            tiles = [t for t in BOARD if t.get("group") == group]
            if not tiles:
                continue
            gcolor = tiles[0].get("color") or "#555555"
            hf = tk.Frame(inner, bg=gcolor, pady=1)
            hf.pack(fill=tk.X, pady=(6, 1), padx=4)
            tk.Label(hf, text=group.upper(), font=("Helvetica", 8, "bold"),
                     fg="white", bg=gcolor).pack(side=tk.LEFT, padx=4)
            for tile in tiles:
                pos = tile["pos"]
                owner_idx = self.ownership.get(pos)
                if owner_idx is not None:
                    owner = self.players[owner_idx]
                    owner_text = f"{owner.token} {owner.name}"
                    fg = owner.color
                else:
                    owner_text = "Bank"
                    fg = "#666666"
                b = self.buildings.get(pos, 0)
                btext = " 🏨" if b == 5 else ("🏠" * b if b else "")
                mort = " [M]" if self.mortgaged.get(pos) else ""
                row = tk.Frame(inner, bg="#16213e")
                row.pack(fill=tk.X, pady=1, padx=8)
                tk.Label(row, text=f"{tile['name']}{btext}{mort}",
                         font=("Helvetica", 8), fg="#bdc3c7", bg="#16213e",
                         anchor="w", width=18).pack(side=tk.LEFT, padx=3)
                tk.Label(row, text=owner_text, font=("Helvetica", 8, "bold"),
                         fg=fg, bg="#16213e", anchor="w").pack(side=tk.LEFT)

        tk.Button(dlg, text="Close", command=dlg.destroy,
                  bg="#c0392b", fg="white", font=("Helvetica", 9, "bold")).pack(pady=6)

    # ─────────────────────────────────────────────────────────────────────
    # Win Screen
    # ─────────────────────────────────────────────────────────────────────
    def _show_win_screen(self, winner):
        dlg = tk.Toplevel(self.root)
        dlg.title("Game Over!")
        dlg.geometry("420x480")
        dlg.configure(bg="#1a1a2e")
        dlg.grab_set()
        dlg.resizable(False, False)
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() - 420) // 2
        y = (dlg.winfo_screenheight() - 480) // 2
        dlg.geometry(f"420x480+{x}+{y}")

        tk.Label(dlg, text="🏆", font=("Helvetica", 56), bg="#1a1a2e").pack(pady=(18, 2))
        tk.Label(dlg, text="WINNER!", font=("Georgia", 22, "bold"),
                 fg="#f39c12", bg="#1a1a2e").pack()
        tk.Label(dlg, text=f"{winner.token}  {winner.name}",
                 font=("Georgia", 16, "bold"), fg=winner.color, bg="#1a1a2e").pack(pady=4)

        stats_frame = tk.Frame(dlg, bg="#16213e", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, padx=24, pady=8)
        tk.Label(stats_frame, text="Final Standings",
                 font=("Helvetica", 10, "bold"), fg="#f39c12", bg="#16213e").pack()
        sorted_players = sorted(
            range(len(self.players)),
            key=lambda i: self._calc_net_worth(i), reverse=True
        )
        for rank, pidx in enumerate(sorted_players, 1):
            p = self.players[pidx]
            net = self._calc_net_worth(pidx)
            status = "BANKRUPT" if p.bankrupt else f"Net: ${net}"
            row = tk.Frame(stats_frame, bg="#16213e")
            row.pack(fill=tk.X, pady=1)
            fg = p.color if not p.bankrupt else "#555555"
            tk.Label(row, text=f"#{rank}  {p.token} {p.name}  —  {status}",
                     font=("Helvetica", 9), fg=fg, bg="#16213e", anchor="w").pack(fill=tk.X, padx=4)

        tk.Label(dlg, text=f"Turns played: {self.turn_number}",
                 font=("Helvetica", 9), fg="#95a5a6", bg="#1a1a2e").pack()

        def quit_game():
            dlg.destroy()
            self.root.quit()

        def new_game():
            dlg.destroy()
            self.root.destroy()
            import subprocess, sys
            subprocess.Popen([sys.executable, __file__])

        btn_row = tk.Frame(dlg, bg="#1a1a2e")
        btn_row.pack(pady=12)
        tk.Button(btn_row, text="🔄 NEW GAME", command=new_game,
                  bg="#27ae60", fg="white",
                  font=("Helvetica", 11, "bold"), padx=14, pady=6).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_row, text="🚪 QUIT", command=quit_game,
                  bg="#c0392b", fg="white",
                  font=("Helvetica", 11, "bold"), padx=14, pady=6).pack(side=tk.LEFT, padx=6)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    game = MonopolyGame(root)
    root.mainloop()
