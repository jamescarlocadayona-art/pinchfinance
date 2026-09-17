import tkinter as tk
import calendar
import ctypes
import hashlib
import hmac
import locale
import os
import secrets
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter import font as tkfont


BG = "#edf1f5"
INK = "#1f3448"
MUTED = "#667787"
LINE = "#c4d0da"
CARD = "#ffffff"
GREEN = "#2d638d"
MINT = "#dcebf3"
CORAL = "#b85f4e"
YELLOW = "#e4b847"
NAVY = "#174d78"
APP_DIR = (Path(os.environ.get("LOCALAPPDATA", Path.home())) / "PinchFinance" if getattr(sys, "frozen", False) else Path(__file__).parent)
DATABASE_PATH = APP_DIR / "pinch_finance.db"
CURRENCIES = [
    ("AED", "UAE dirham"), ("AFN", "Afghani"), ("ALL", "Lek"), ("AMD", "Armenian dram"),
    ("ANG", "Netherlands Antillean guilder"), ("AOA", "Kwanza"), ("ARS", "Argentine peso"),
    ("AUD", "Australian dollar"), ("AWG", "Aruban florin"), ("AZN", "Azerbaijan manat"),
    ("BAM", "Convertible mark"), ("BBD", "Barbados dollar"), ("BDT", "Taka"), ("BGN", "Bulgarian lev"),
    ("BHD", "Bahraini dinar"), ("BIF", "Burundi franc"), ("BMD", "Bermudian dollar"),
    ("BND", "Brunei dollar"), ("BOB", "Boliviano"), ("BOV", "Mvdol"), ("BRL", "Brazilian real"),
    ("BSD", "Bahamian dollar"), ("BTN", "Ngultrum"), ("BWP", "Pula"), ("BYN", "Belarusian ruble"),
    ("BZD", "Belize dollar"), ("CAD", "Canadian dollar"), ("CDF", "Congolese franc"),
    ("CHE", "WIR euro"), ("CHF", "Swiss franc"), ("CHW", "WIR franc"), ("CLF", "Unidad de Fomento"),
    ("CLP", "Chilean peso"), ("CNY", "Yuan renminbi"), ("COP", "Colombian peso"), ("COU", "Unidad de Valor Real"),
    ("CRC", "Costa Rican colon"), ("CUC", "Peso convertible"), ("CUP", "Cuban peso"), ("CVE", "Cabo Verde escudo"),
    ("CZK", "Czech koruna"), ("DJF", "Djibouti franc"), ("DKK", "Danish krone"), ("DOP", "Dominican peso"),
    ("DZD", "Algerian dinar"), ("EGP", "Egyptian pound"), ("ERN", "Nakfa"), ("ETB", "Ethiopian birr"),
    ("EUR", "Euro"), ("FJD", "Fiji dollar"), ("FKP", "Falkland Islands pound"), ("GBP", "Pound sterling"),
    ("GEL", "Lari"), ("GHS", "Ghana cedi"), ("GIP", "Gibraltar pound"), ("GMD", "Dalasi"),
    ("GNF", "Guinean franc"), ("GTQ", "Quetzal"), ("GYD", "Guyana dollar"), ("HKD", "Hong Kong dollar"),
    ("HNL", "Lempira"), ("HTG", "Gourde"), ("HUF", "Forint"), ("IDR", "Rupiah"), ("ILS", "New Israeli shekel"),
    ("INR", "Indian rupee"), ("IQD", "Iraqi dinar"), ("IRR", "Iranian rial"), ("ISK", "Iceland krona"),
    ("JMD", "Jamaican dollar"), ("JOD", "Jordanian dinar"), ("JPY", "Yen"), ("KES", "Kenyan shilling"),
    ("KGS", "Som"), ("KHR", "Riel"), ("KMF", "Comorian franc"), ("KPW", "North Korean won"),
    ("KRW", "Won"), ("KWD", "Kuwaiti dinar"), ("KYD", "Cayman Islands dollar"), ("KZT", "Tenge"),
    ("LAK", "Lao kip"), ("LBP", "Lebanese pound"), ("LKR", "Sri Lanka rupee"), ("LRD", "Liberian dollar"),
    ("LSL", "Loti"), ("LYD", "Libyan dinar"), ("MAD", "Moroccan dirham"), ("MDL", "Moldovan leu"),
    ("MGA", "Malagasy ariary"), ("MKD", "Denar"), ("MMK", "Kyat"), ("MNT", "Tugrik"), ("MOP", "Pataca"),
    ("MRU", "Ouguiya"), ("MUR", "Mauritius rupee"), ("MVR", "Rufiyaa"), ("MWK", "Malawi kwacha"),
    ("MXN", "Mexican peso"), ("MXV", "Unidad de Inversion"), ("MYR", "Malaysian ringgit"), ("MZN", "Mozambique metical"),
    ("NAD", "Namibia dollar"), ("NGN", "Naira"), ("NIO", "Cordoba oro"), ("NOK", "Norwegian krone"),
    ("NPR", "Nepalese rupee"), ("NZD", "New Zealand dollar"), ("OMR", "Rial Omani"), ("PAB", "Balboa"),
    ("PEN", "Sol"), ("PGK", "Kina"), ("PHP", "Philippine peso"), ("PKR", "Pakistan rupee"),
    ("PLN", "Zloty"), ("PYG", "Guarani"), ("QAR", "Qatari rial"), ("RON", "Romanian leu"),
    ("RSD", "Serbian dinar"), ("RUB", "Russian ruble"), ("RWF", "Rwanda franc"), ("SAR", "Saudi riyal"),
    ("SBD", "Solomon Islands dollar"), ("SCR", "Seychelles rupee"), ("SDG", "Sudanese pound"),
    ("SEK", "Swedish krona"), ("SGD", "Singapore dollar"), ("SHP", "Saint Helena pound"),
    ("SLE", "Leone"), ("SOS", "Somali shilling"), ("SRD", "Surinamese dollar"), ("SSP", "South Sudanese pound"),
    ("STN", "Dobra"), ("SVC", "El Salvador colon"), ("SYP", "Syrian pound"), ("SZL", "Lilangeni"),
    ("THB", "Baht"), ("TJS", "Somoni"), ("TMT", "Turkmenistan manat"), ("TND", "Tunisian dinar"),
    ("TOP", "Pa'anga"), ("TRY", "Turkish lira"), ("TTD", "Trinidad and Tobago dollar"), ("TWD", "New Taiwan dollar"),
    ("TZS", "Tanzanian shilling"), ("UAH", "Hryvnia"), ("UGX", "Uganda shilling"), ("USD", "US dollar"),
    ("USN", "US dollar next day"), ("UYU", "Peso Uruguayo"), ("UYW", "Unidad Previsional"), ("UZS", "Uzbekistan sum"),
    ("VED", "Digital bolivar"), ("VES", "Bolivar soberano"), ("VND", "Dong"), ("VUV", "Vatu"),
    ("WST", "Tala"), ("XAF", "CFA franc BEAC"), ("XAG", "Silver"), ("XAU", "Gold"), ("XCD", "East Caribbean dollar"),
    ("XOF", "CFA franc BCEAO"), ("XPF", "CFP franc"), ("YER", "Yemeni rial"), ("ZAR", "Rand"),
    ("ZMW", "Zambian kwacha"), ("ZWL", "Zimbabwe dollar"),
]
CURRENCY_SYMBOLS = {
    "AED": "د.إ", "ARS": "$", "AUD": "$", "BRL": "R$", "CAD": "$", "CHF": "Fr",
    "CLP": "$", "CNY": "¥", "COP": "$", "CZK": "Kč", "DKK": "kr", "EGP": "£",
    "EUR": "€", "GBP": "£", "HKD": "$", "HUF": "Ft", "IDR": "Rp", "ILS": "₪",
    "INR": "₹", "ISK": "kr", "JPY": "¥", "KES": "KSh", "KRW": "₩", "MAD": "د.م.",
    "MXN": "$", "MYR": "RM", "NOK": "kr", "NZD": "$", "PHP": "₱", "PKR": "₨",
    "PLN": "zł", "RUB": "₽", "SAR": "﷼", "SEK": "kr", "SGD": "$", "THB": "฿",
    "TRY": "₺", "TWD": "NT$", "UAH": "₴", "USD": "$", "VND": "₫", "ZAR": "R",
}


def currency_symbol(code: str) -> str:
    return CURRENCY_SYMBOLS.get(code, "¤")


ICON_CODES = {
    "home": "\uf015", "transactions": "\uf53a", "accounts": "\uf555", "savings": "\uf4d3",
    "shopping": "\uf07a", "bills": "\uf571", "goals": "\uf140", "insights": "\uf200",
    "settings": "\uf013", "refresh": "\uf2f1", "logout": "\uf2f5", "add": "\uf067",
    "calendar": "\uf133",
}


@dataclass
class Transaction:
    name: str
    category: str
    amount: float
    kind: str
    day: str
    account: str = ""


class PinchFinance(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Pinch Finance - 0.1 beta")
        self.geometry("1180x760")
        self.minsize(980, 650)
        self.configure(bg=BG)
        self.withdraw()

        self.transactions = []
        self.accounts = []
        self.savings = []
        self.goal_records = []
        self.bills = []
        self.shopping = []
        self.notified_bills = set()
        self.current_user_id = None
        self.insight_history = []
        self.theme_name = "Classic Blue"
        self.default_currency = self._detect_currency()
        self.icon_font_family = "Font Awesome 6 Free"
        self._load_icon_font()
        self.active_filter = "All activity"
        self.account_filter = None
        self.current_username = ""
        self.active_page = "Home"
        self.nav_buttons = {}
        self.fonts = {
            "display": ("Georgia", 32, "bold"),
            "title": ("Georgia", 19, "bold"),
            "body": ("Segoe UI", 10),
            "body_bold": ("Segoe UI", 10, "bold"),
            "small": ("Segoe UI", 9),
            "number": ("Segoe UI", 22, "bold"),
        }
        self._initialize_database()
        self._setup_styles()
        self._show_splash()

    def _load_icon_font(self) -> None:
        try:
            import fontawesomefree
            font_path = Path(fontawesomefree.__file__).parent / "static" / "fontawesomefree" / "webfonts" / "fa-solid-900.ttf"
            ctypes.windll.gdi32.AddFontResourceExW(str(font_path), 0x10, 0)
        except (ImportError, AttributeError, OSError):
            self.icon_font_family = "Segoe UI Symbol"

    def _icon(self, name: str) -> str:
        return ICON_CODES.get(name, "")

    def _initialize_database(self) -> None:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, kind TEXT NOT NULL, balance REAL NOT NULL, currency TEXT NOT NULL DEFAULT 'USD')")
            account_columns = {row[1] for row in connection.execute("PRAGMA table_info(accounts)")}
            if "currency" not in account_columns:
                connection.execute("ALTER TABLE accounts ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD'")
            connection.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL, kind TEXT NOT NULL, day TEXT NOT NULL, account TEXT NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS savings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, amount REAL NOT NULL, day TEXT NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, target REAL NOT NULL, saved REAL NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS bills (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, amount REAL NOT NULL, due TEXT NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS insights (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, title TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            connection.execute("CREATE TABLE IF NOT EXISTS shopping (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, item TEXT NOT NULL, amount REAL NOT NULL, store TEXT NOT NULL, purchased_at TEXT NOT NULL, account TEXT NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY CHECK (id = 1), user_id INTEGER, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            connection.execute("CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            connection.execute("DELETE FROM users WHERE username = ?", ("demo",))

    def _load_user_data(self) -> None:
        if self.current_user_id is None:
            return
        with sqlite3.connect(DATABASE_PATH) as connection:
            self.accounts = [{"id": row[0], "name": row[1], "kind": row[2], "balance": row[3], "currency": row[4]} for row in connection.execute("SELECT id, name, kind, balance, currency FROM accounts WHERE user_id = ? ORDER BY name", (self.current_user_id,))]
            self.transactions = [Transaction(row[0], row[1], row[2], row[3], row[4], row[5]) for row in connection.execute("SELECT name, category, amount, kind, day, account FROM transactions WHERE user_id = ? ORDER BY day DESC, id DESC", (self.current_user_id,))]
            self.savings = [{"id": row[0], "name": row[1], "amount": row[2], "day": row[3]} for row in connection.execute("SELECT id, name, amount, day FROM savings WHERE user_id = ? ORDER BY day DESC, id DESC", (self.current_user_id,))]
            self.goal_records = [{"id": row[0], "name": row[1], "target": row[2], "saved": row[3]} for row in connection.execute("SELECT id, name, target, saved FROM goals WHERE user_id = ? ORDER BY id DESC", (self.current_user_id,))]
            self.bills = [{"id": row[0], "name": row[1], "amount": row[2], "due": row[3]} for row in connection.execute("SELECT id, name, amount, due FROM bills WHERE user_id = ? ORDER BY due", (self.current_user_id,))]
            self.insight_history = [{"title": row[0], "detail": row[1], "created_at": row[2]} for row in connection.execute("SELECT title, detail, created_at FROM insights WHERE user_id = ? ORDER BY created_at DESC", (self.current_user_id,))]
            self.shopping = [{"id": row[0], "item": row[1], "amount": row[2], "store": row[3], "purchased_at": row[4], "account": row[5]} for row in connection.execute("SELECT id, item, amount, store, purchased_at, account FROM shopping WHERE user_id = ? ORDER BY purchased_at DESC", (self.current_user_id,))]

    def _restore_session(self) -> bool:
        with sqlite3.connect(DATABASE_PATH) as connection:
            record = connection.execute("SELECT users.id, users.username FROM sessions JOIN users ON users.id = sessions.user_id WHERE sessions.id = 1").fetchone()
        if record is None:
            return False
        self.current_user_id, self.current_username = record
        self._load_user_data()
        return True

    def _remember_session(self) -> None:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("INSERT INTO sessions (id, user_id) VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET user_id = excluded.user_id, updated_at = CURRENT_TIMESTAMP", (self.current_user_id,))

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 120_000
        ).hex()

    def _check_login(self, username: str, password: str) -> bool:
        username = username.strip()
        if not username or not password:
            return False
        with sqlite3.connect(DATABASE_PATH) as connection:
            record = connection.execute(
                "SELECT id, password_hash, password_salt FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if record is None:
            return False
        user_id, stored_hash, stored_salt = record
        candidate_hash = self._hash_password(password, bytes.fromhex(stored_salt))
        authenticated = hmac.compare_digest(candidate_hash, stored_hash)
        if authenticated:
            self.current_username = username
            self.current_user_id = user_id
            self._load_user_data()
            self._remember_session()
        return authenticated

    def _create_user(self, username: str, password: str) -> bool:
        username = username.strip()
        if not username or not password:
            return False
        salt = secrets.token_bytes(16)
        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute(
                    "INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)",
                    (username, self._hash_password(password, salt), salt.hex()),
                )
                self.current_user_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError:
            return False
        self.current_username = username
        self._load_user_data()
        self._remember_session()
        return True

    def _show_splash(self) -> None:
        self.deiconify()
        self.geometry("620x420")
        self.minsize(620, 420)
        for child in self.winfo_children():
            child.destroy()
        splash = tk.Frame(self, bg=NAVY)
        splash.pack(fill="both", expand=True)
        tk.Label(splash, text="pinch", bg=NAVY, fg="#f8f4e9", font=("Georgia", 54, "bold")).pack(pady=(105, 2))
        tk.Label(splash, text="finance / 0.1 beta", bg=NAVY, fg="#a9c8bf", font=self.fonts["body"]).pack()
        self.splash_status = tk.Label(splash, text="Preparing your money view", bg=NAVY, fg="#d6e1de", font=self.fonts["small"])
        self.splash_status.pack(pady=(56, 13))
        progress = ttk.Progressbar(splash, style="Pinch.Horizontal.TProgressbar", mode="indeterminate", length=190)
        progress.pack()
        progress.start(12)
        self.after(1500, lambda: self._finish_startup(progress))

    def _finish_startup(self, progress: ttk.Progressbar) -> None:
        progress.stop()
        if self._restore_session():
            self._open_dashboard()
        elif not self._oobe_completed():
            self._show_oobe()
        else:
            self._show_login(None)

    def _oobe_completed(self) -> bool:
        with sqlite3.connect(DATABASE_PATH) as connection:
            return connection.execute("SELECT 1 FROM app_settings WHERE key = ?", ("oobe_completed",)).fetchone() is not None

    def _show_oobe(self) -> None:
        self.geometry("700x560")
        self.minsize(700, 560)
        self.unbind("<Return>")
        for child in self.winfo_children():
            child.destroy()
        panel = tk.Frame(self, bg=BG, padx=72, pady=48)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="pinch", bg=BG, fg=GREEN, font=("Georgia", 38, "bold")).pack(anchor="w")
        tk.Label(panel, text="Let's set up your money workspace.", bg=BG, fg=INK, font=self.fonts["title"]).pack(anchor="w", pady=(8, 4))
        tk.Label(panel, text="A few choices now make the rest of Pinch feel like yours.", bg=BG, fg=MUTED, font=self.fonts["body"]).pack(anchor="w", pady=(0, 28))

        tk.Label(panel, text="1  DISPLAY", bg=BG, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        theme = tk.StringVar(value=self.theme_name)
        ttk.Combobox(panel, textvariable=theme, values=["Classic Blue", "Light"], state="readonly", width=38).pack(anchor="w", pady=(7, 22), ipady=5)
        tk.Label(panel, text="2  CURRENCY", bg=BG, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        currency_options = {f"{currency_symbol(code)} - {name}": code for code, name in CURRENCIES}
        suggested = self.default_currency
        currency_value = next((label for label, code in currency_options.items() if code == suggested), "$ - US dollar")
        currency = tk.StringVar(value=currency_value)
        ttk.Combobox(panel, textvariable=currency, values=list(currency_options), state="readonly", width=38).pack(anchor="w", pady=(7, 8), ipady=5)
        tk.Label(panel, text=f"Suggested from your computer locale: {currency_symbol(suggested)} {self._currency_name(suggested)}", bg=BG, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")

        def finish() -> None:
            self.theme_name = theme.get()
            self.default_currency = currency_options[currency.get()]
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)", ("oobe_completed", "1"))
                connection.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)", ("theme", self.theme_name))
                connection.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)", ("currency", self.default_currency))
            self._show_login(None)

        tk.Button(panel, text=f"{self._icon('add')}  Finish setup", command=finish, bg=GREEN, fg="white", activebackground="#245576", relief="flat", bd=0, font=self.fonts["body_bold"], padx=18, pady=11, cursor="hand2").pack(anchor="w", pady=(32, 0))

    def _show_login(self, progress: ttk.Progressbar | None) -> None:
        if progress is not None:
            progress.stop()
        self.unbind("<Return>")
        self.geometry("620x520")
        self.minsize(620, 520)
        for child in self.winfo_children():
            child.destroy()
        panel = tk.Frame(self, bg=BG, padx=78, pady=48)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="pinch", bg=BG, fg=GREEN, font=("Georgia", 34, "bold")).pack(anchor="w")
        tk.Label(panel, text="Your money, held lightly.", bg=BG, fg=MUTED, font=self.fonts["body"]).pack(anchor="w", pady=(0, 33))
        tk.Label(panel, text="Welcome to your workspace", bg=BG, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        tk.Label(panel, text="Sign in to continue, or create a new account.", bg=BG, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(4, 18))
        mode = tk.StringVar(value="login")
        switch = tk.Frame(panel, bg=BG)
        switch.pack(fill="x", pady=(0, 18))
        form = tk.Frame(panel, bg=BG)
        form.pack(fill="x")
        self.login_status = tk.Label(panel, text="", bg=BG, fg=CORAL, font=self.fonts["small"])
        self.login_status.pack(anchor="w", pady=(10, 0))
        fields: dict[str, tk.Entry] = {}

        def submit(event: object = None) -> None:
            username = fields["username"].get()
            password = fields["password"].get()
            if mode.get() == "login":
                success = self._check_login(username, password)
                message = "Username or password is incorrect."
            else:
                success = self._create_user(username, password)
                message = "That username already exists, or the fields are empty."
            if success:
                self._open_dashboard()
            else:
                self.login_status.config(text=message)
                fields["password"].delete(0, tk.END)
                fields["password"].focus_set()

        def render_form() -> None:
            for child in form.winfo_children():
                child.destroy()
            fields.clear()
            fields["username"] = self._login_field(form, "Username")
            fields["password"] = self._login_field(form, "Password", show="*")
            label = "Sign in" if mode.get() == "login" else "Create account"
            tk.Button(form, text=label, command=submit, bg=GREEN, fg="white", activebackground="#0b5949", activeforeground="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=20, pady=11, cursor="hand2").pack(anchor="w", pady=(3, 10))
            fields["username"].focus_set()
            self.login_status.config(text="")
            self.bind("<Return>", submit)

        def set_mode(value: str) -> None:
            mode.set(value)
            render_form()

        tk.Button(switch, text="Sign in", command=lambda: set_mode("login"), bg="#c5dce9", fg=NAVY, activebackground="#c5dce9", relief="flat", bd=0, font=self.fonts["body_bold"], padx=16, pady=7, cursor="hand2").pack(side="left")
        tk.Button(switch, text="Create account", command=lambda: set_mode("create"), bg=BG, fg=MUTED, activebackground="#c5dce9", relief="flat", bd=0, font=self.fonts["body_bold"], padx=16, pady=7, cursor="hand2").pack(side="left", padx=5)
        render_form()

    def _login_field(self, parent: tk.Frame, label: str, show: str = "") -> tk.Entry:
        tk.Label(parent, text=label, bg=BG, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(0, 5))
        field = tk.Entry(parent, relief="flat", bg="white", fg=INK, show=show, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
        field.pack(fill="x", ipady=8, pady=(0, 14))
        return field

    def _open_dashboard(self) -> None:
        self.unbind("<Return>")
        self.geometry("1180x760")
        self.minsize(980, 650)
        for child in self.winfo_children():
            child.destroy()
        self._build_shell()
        self._refresh()

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Pinch.Horizontal.TProgressbar",
            troughcolor="#d7e1e8",
            background=GREEN,
            bordercolor="#d7e1e8",
            lightcolor=GREEN,
            darkcolor=GREEN,
            thickness=8,
        )

    def _build_shell(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        topbar = tk.Frame(self, bg=NAVY, height=74)
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        topbar.grid_propagate(False)
        tk.Label(topbar, text="pinch", bg=NAVY, fg="#ffffff", font=("Georgia", 25, "bold")).pack(side="left", padx=(22, 25))
        menus = {
            "File": [("Refresh", self._refresh_current_page), ("Log out", self._logout), ("Exit", self.destroy)],
            "Edit": [("Add transaction", self._open_add_dialog), ("Add account", self._account_notice), ("Add savings", self._savings_notice), ("Create goal", self._goal_notice), ("Add bill", self._bill_notice), ("Record shopping", self._shopping_notice)],
            "View": [("Home", lambda: self._show_screen("Home")), ("Transactions", lambda: self._show_screen("Transactions")), ("Accounts", lambda: self._show_screen("Accounts")), ("Savings", lambda: self._show_screen("Savings")), ("Shopping", lambda: self._show_screen("Shopping")), ("Settings", lambda: self._show_screen("Settings"))],
            "Reports": [("Insights", lambda: self._show_screen("Insights")), ("Spending details", lambda: self._show_total_details("spent"))],
            "Planning": [("Goals", lambda: self._show_screen("Goals")), ("Bills", lambda: self._show_screen("Bills")), ("Savings", lambda: self._show_screen("Savings"))],
            "Help": [("About Pinch Finance", self._show_about), ("Settings", lambda: self._show_screen("Settings")), ("Refresh data", self._refresh_current_page)],
        }
        for label, items in menus.items():
            menu = tk.Menu(topbar, tearoff=False, bg=CARD, fg=INK, activebackground="#c5dce9", activeforeground=NAVY)
            for item_label, command in items:
                menu.add_command(label=item_label, command=command)
            tk.Menubutton(topbar, text=label, menu=menu, bg=NAVY, fg="#d9e6f0", activebackground="#28628e", activeforeground="white", relief="flat", bd=0, font=self.fonts["small"], padx=10, pady=7, cursor="hand2").pack(side="left", padx=2)
        tk.Label(topbar, text="Personal Financial Information", bg=NAVY, fg="#a9c8d9", font=self.fonts["small"]).pack(side="right", padx=24)
        tk.Button(topbar, text=f"{self._icon('refresh')} Refresh", command=self._refresh_current_page, bg="#28628e", fg="white", activebackground="#34749f", activeforeground="white", relief="flat", bd=0, font=self.fonts["small"], padx=12, pady=5, cursor="hand2").pack(side="right", padx=(0, 8))
        tk.Button(topbar, text=f"{self._icon('logout')} Log out", command=self._logout, bg="#28628e", fg="white", activebackground="#34749f", activeforeground="white", relief="flat", bd=0, font=self.fonts["small"], padx=12, pady=5, cursor="hand2").pack(side="right", padx=(0, 10))

        sidebar = tk.Frame(self, bg="#e3eaf0", width=235)
        sidebar.grid(row=1, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        tk.Label(sidebar, text="MY PERSONAL FINANCES", bg="#d6e1e9", fg=NAVY, font=("Segoe UI", 9, "bold"), anchor="w", padx=18, pady=10).pack(fill="x")
        tk.Label(sidebar, text="Account List", bg="#e3eaf0", fg=INK, font=self.fonts["small"], anchor="w", padx=18, pady=13).pack(fill="x")
        nav = tk.Frame(sidebar, bg="#e3eaf0")
        nav.pack(fill="x", padx=12, pady=8)
        nav_icons = {"Home": "home", "Transactions": "transactions", "Accounts": "accounts", "Savings": "savings", "Shopping": "shopping", "Bills": "bills", "Goals": "goals", "Insights": "insights", "Settings": "settings"}
        for label in nav_icons:
            row = tk.Frame(nav, bg="#e3eaf0")
            row.pack(fill="x", pady=2)
            icon_label = tk.Label(row, text=self._icon(nav_icons[label]), bg="#e3eaf0", fg="#4d6577", font=(self.icon_font_family, 10), width=3)
            icon_label.pack(side="left", padx=(8, 0))
            button = tk.Button(
                row, text=label, anchor="w", relief="flat", bd=0,
                bg="#e3eaf0", fg="#4d6577",
                activebackground="#c5dce9", activeforeground=NAVY, font=self.fonts["body_bold"],
                padx=4, pady=9, cursor="hand2", command=lambda page=label: self._show_screen(page),
            )
            button.pack(side="left", fill="x", expand=True)
            self.nav_buttons[label] = button
        self._set_active_nav("Home")
        tk.Label(sidebar, text="TASKS", bg="#e3eaf0", fg=MUTED, font=("Segoe UI", 8, "bold"), anchor="w", padx=18, pady=14).pack(fill="x")
        tk.Label(sidebar, text="Click a section to open it", bg="#e3eaf0", fg="#4d6577", font=self.fonts["small"], anchor="w", padx=18, pady=5).pack(fill="x")
        bottom = tk.Frame(sidebar, bg="#e3eaf0")
        bottom.pack(side="bottom", fill="x", padx=26, pady=27)
        self._avatar(bottom, self.current_username or "User").pack(side="left")
        display_name = self.current_username or "Your workspace"
        tk.Label(bottom, text=f"  {display_name}", bg="#e3eaf0", fg="#4d6577", font=self.fonts["small"]).pack(side="left")

        main = tk.Frame(self, bg=BG)
        main.grid(row=1, column=1, sticky="nsew", padx=24, pady=20)
        self.main = main
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)

        header = tk.Frame(main, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 23))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="September 17, 2026", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="My Personal Finances", bg=BG, fg=INK, font=("Georgia", 25, "bold")).grid(row=1, column=0, sticky="w", pady=(2, 0))
        add = tk.Button(header, text=f"{self._icon('add')}  Add transaction", command=self._open_add_dialog, bg=GREEN, fg="white", activebackground="#245576", activeforeground="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=15, pady=8, cursor="hand2")
        add.grid(row=1, column=1, sticky="e")

        self.cards = tk.Frame(main, bg=BG)
        self.cards.grid(row=1, column=0, sticky="ew", pady=(0, 25))
        for i in range(3):
            self.cards.grid_columnconfigure(i, weight=1)
        self.balance_card = self._metric_card(self.cards, "Available to spend", "$0.00", "Accounts + transaction activity", GREEN, 0, lambda: self._show_total_details("available"))
        self.spent_card = self._metric_card(self.cards, "Spent this month", "$0.00", "Click for category detail", CORAL, 1, lambda: self._show_total_details("spent"))
        self.saved_card = self._metric_card(self.cards, "Saved this month", "$0.00", "Click for savings detail", NAVY, 2, lambda: self._show_total_details("saved"))
        self._update_metrics()

        insight = tk.Frame(main, bg=MINT, padx=20, pady=15)
        insight.grid(row=2, column=0, sticky="ew", pady=(0, 24))
        tk.Label(insight, text="✦", bg=MINT, fg=GREEN, font=("Segoe UI", 17, "bold")).pack(side="left", padx=(0, 13))
        tk.Label(insight, text="Your spending is quieter this week.", bg=MINT, fg=INK, font=self.fonts["body_bold"]).pack(side="left")
        tk.Label(insight, text=" You have $184 more breathing room than usual.", bg=MINT, fg="#42675d", font=self.fonts["body"]).pack(side="left")

        content = tk.Frame(main, bg=BG)
        content.grid(row=3, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)
        self.activity = tk.Frame(content, bg=CARD, padx=22, pady=20)
        self.activity.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        self.goals = tk.Frame(content, bg=CARD, padx=22, pady=20)
        self.goals.grid(row=0, column=1, sticky="nsew")
        self._build_goals()

    def _show_screen(self, page: str) -> None:
        self.active_page = page
        self._set_active_nav(page)
        if page == "Home":
            self._open_dashboard()
            return
        for child in self.main.winfo_children():
            child.destroy()
        self.main.grid_rowconfigure(1, weight=1)
        header = tk.Frame(self.main, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 23))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="September 17, 2026", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=0, column=0, sticky="w")
        tk.Label(header, text=page, bg=BG, fg=INK, font=("Georgia", 25, "bold")).grid(row=1, column=0, sticky="w", pady=(2, 0))
        action = {
            "Transactions": (f"{self._icon('add')}  Add transaction", self._open_add_dialog),
            "Accounts": (f"{self._icon('add')}  Add account", self._account_notice),
            "Savings": (f"{self._icon('add')}  Add savings", self._savings_notice),
            "Shopping": (f"{self._icon('add')}  Record purchase", self._shopping_notice),
            "Bills": (f"{self._icon('add')}  Add bill", self._bill_notice),
            "Goals": (f"{self._icon('add')}  Create goal", self._goal_notice),
            "Insights": (f"{self._icon('refresh')}  Refresh insights", self._insight_notice),
            "Settings": (f"{self._icon('settings')}  Detect currency", self._detect_currency_notice),
        }[page]
        tk.Button(header, text=action[0], command=action[1], bg=GREEN, fg="white", activebackground="#245576", activeforeground="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=15, pady=8, cursor="hand2").grid(row=1, column=1, sticky="e")

        body = tk.Frame(self.main, bg=BG)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        if page == "Transactions":
            self._build_transactions_screen(body)
        elif page == "Accounts":
            self._build_accounts_screen(body)
        elif page == "Savings":
            self._build_savings_screen(body)
        elif page == "Bills":
            self._build_bills_screen(body)
        elif page == "Goals":
            self._build_goals_screen(body)
        elif page == "Shopping":
            self._build_shopping_screen(body)
        elif page == "Settings":
            self._build_settings_screen(body)
        else:
            self._build_insights_screen(body)
        if page == "Bills":
            self.after(100, self._notify_due_bills)

    def _set_active_nav(self, page: str) -> None:
        for label, button in self.nav_buttons.items():
            selected = label == page
            button.configure(
                bg="#c5dce9" if selected else "#e3eaf0",
                fg=NAVY if selected else "#4d6577",
            )

    @staticmethod
    def _avatar_color(value: str) -> str:
        palette = [
            "#2d638d", "#7a5a9e", "#b85f4e", "#2f806b", "#a8792d", "#4b6f8f",
            "#9b536d", "#437c8b", "#8a6d3b", "#5d709d", "#9a634f", "#4d8062",
            "#8a5f91", "#577b9b", "#ad6b3f", "#3c8779", "#866b9f", "#b15c61",
            "#527d67", "#706b9b", "#9d704a", "#477d93", "#925d79", "#658050",
            "#765e89", "#a05d45",
        ]
        first = value.strip().upper()[:1] or "?"
        return palette[(ord(first) - ord("A")) % len(palette)]

    def _avatar(self, parent: tk.Widget, value: str, size: int = 3) -> tk.Label:
        first = value.strip().upper()[:1] or "?"
        return tk.Label(parent, text=first, bg=self._avatar_color(first), fg="white", font=("Segoe UI", 9, "bold"), width=size, height=1)

    def _screen_panel(self, parent: tk.Frame, title: str, subtitle: str, column: int = 0) -> tk.Frame:
        panel = tk.Frame(parent, bg=CARD, padx=22, pady=20, highlightbackground=LINE, highlightthickness=1)
        panel.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0))
        tk.Label(panel, text=title, bg=CARD, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        tk.Label(panel, text=subtitle, bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(4, 19))
        return panel

    def _build_transactions_screen(self, parent: tk.Frame) -> None:
        title = f"Transactions · {self.account_filter}" if self.account_filter else "All transactions"
        subtitle = "History for the selected account" if self.account_filter else "Your latest money movements"
        panel = self._screen_panel(parent, title, subtitle)
        table = ttk.Treeview(panel, columns=("name", "account", "category", "date", "amount"), show="headings", height=12)
        for column, heading, width in [("name", "Transaction", 135), ("account", "Account", 110), ("category", "Category", 85), ("date", "Date", 90), ("amount", "Amount", 95)]:
            table.heading(column, text=heading)
            table.column(column, width=width, anchor="e" if column == "amount" else "w")
        visible = [item for item in self.transactions if not self.account_filter or item.account == self.account_filter]
        for item in visible:
            account_currency = next((account.get("currency", "USD") for account in self.accounts if account["name"] == item.account), "USD")
            table.insert("", "end", values=(f"{item.name[:1].upper()}  {item.name}", item.account or "Unassigned", item.category, item.day, f"{'+' if item.kind == 'income' else '-'}{currency_symbol(account_currency)}{item.amount:,.2f}"))
        table.pack(fill="both", expand=True, pady=(0, 10))
        if not visible:
            message = "No transactions for this account." if self.account_filter else "No transactions yet. Use Add transaction to create your first entry."
            tk.Label(panel, text=message, bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=8)
        if self.account_filter:
            tk.Button(panel, text="← Show all transactions", command=lambda: self._show_all_transactions(), bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, font=self.fonts["body_bold"], padx=12, pady=7, cursor="hand2").pack(anchor="w")
        summary = self._screen_panel(parent, "This month", "A quick read of your activity", 1)
        income = sum(item.amount for item in visible if item.kind == "income")
        expenses = sum(item.amount for item in visible if item.kind == "expense")
        self._summary_line(summary, "Income", f"${income:,.2f}", GREEN)
        self._summary_line(summary, "Expenses", f"${expenses:,.2f}", CORAL)
        self._summary_line(summary, "Net change", f"${income - expenses:,.2f}", NAVY)

    def _show_all_transactions(self) -> None:
        self.account_filter = None
        self._show_screen("Transactions")

    def _transaction_row_in(self, item: Transaction, parent: tk.Frame) -> None:
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", pady=8)
        self._avatar(row, item.name).pack(side="left", padx=(0, 10))
        account_label = item.account or "Unassigned"
        tk.Label(row, text=f"{item.name}\n{account_label}  ·  {item.category}  ·  {item.day}", justify="left", bg=CARD, fg=INK, font=self.fonts["small"]).pack(side="left", fill="x", expand=True)
        item_currency = next((account.get("currency", "USD") for account in self.accounts if account["name"] == item.account), "USD")
        tk.Label(row, text=f"{'+' if item.kind == 'income' else '-'}{currency_symbol(item_currency)}{item.amount:,.2f}", bg=CARD, fg=GREEN if item.kind == "income" else INK, font=self.fonts["body_bold"]).pack(side="right")

    def _summary_line(self, parent: tk.Frame, label: str, value: str, color: str) -> None:
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", pady=12)
        tk.Label(row, text=label, bg=CARD, fg=MUTED, font=self.fonts["body"]).pack(side="left")
        tk.Label(row, text=value, bg=CARD, fg=color, font=self.fonts["body_bold"]).pack(side="right")

    def _build_accounts_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Accounts", "Accounts connected to your workspace")
        table = ttk.Treeview(panel, columns=("account", "type", "currency", "balance"), show="headings", height=12)
        for column, heading, width in [("account", "Account", 170), ("type", "Type", 95), ("currency", "Symbol", 80), ("balance", "Balance", 110)]:
            table.heading(column, text=heading)
            table.column(column, width=width, anchor="e" if column == "balance" else "w")
        for account in self.accounts:
            currency = account.get("currency", "USD")
            symbol = currency_symbol(currency)
            row_id = table.insert("", "end", values=(f"{account['name'][:1].upper()}  {account['name']}", account["kind"], symbol, f"{symbol}{account['balance']:,.2f}"))
            table.item(row_id, tags=(account["name"],))
        table.bind("<<TreeviewSelect>>", lambda event: self._open_account_history(table))
        table.pack(fill="both", expand=True, pady=(0, 10))
        if not self.accounts:
            tk.Label(panel, text="No accounts connected yet. Add your first account to see it here.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=8)
        note = self._screen_panel(parent, "Account health", "Keep your balances easy to understand", 1)
        tk.Label(note, text=str(len(self.accounts)), bg=CARD, fg=INK, font=self.fonts["number"]).pack(anchor="w")
        tk.Label(note, text="active accounts", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")
        tk.Button(note, text=f"{self._icon('add')}  Add account", command=self._account_notice, bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, font=self.fonts["body_bold"], padx=12, pady=8, cursor="hand2").pack(anchor="w", pady=(22, 0))

    def _open_account_history(self, table: ttk.Treeview) -> None:
        selection = table.selection()
        if not selection:
            return
        values = table.item(selection[0], "values")
        self.account_filter = values[0].split("  ", 1)[-1]
        self._show_screen("Transactions")

    def _build_savings_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Savings", "Money set aside for what comes next")
        if not self.savings:
            tk.Label(panel, text="No savings recorded yet. Add your first contribution.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=24)
        else:
            for saving in self.savings:
                self._summary_line(panel, f"{saving['name']}\n{saving['day']}", f"${saving['amount']:,.2f}", GREEN)
        note = self._screen_panel(parent, "Savings rhythm", "Your current pace", 1)
        total_saved = sum(item["amount"] for item in self.savings)
        tk.Label(note, text=f"${total_saved:,.2f}", bg=CARD, fg=INK, font=self.fonts["number"]).pack(anchor="w")
        tk.Label(note, text="saved this month", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")

    def _goal_row_in(self, parent: tk.Frame, name: str, amount: str, progress: int, color: str) -> None:
        tk.Label(parent, text=name, bg=CARD, fg=INK, font=self.fonts["body_bold"]).pack(anchor="w", pady=(5, 2))
        tk.Label(parent, text=amount, bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")
        ttk.Progressbar(parent, style="Pinch.Horizontal.TProgressbar", maximum=100, value=progress).pack(fill="x", pady=(8, 18))

    def _build_bills_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Bills & deposits", "Upcoming commitments")
        if not self.bills:
            tk.Label(panel, text="No bills scheduled yet. Add a due date to receive notifications.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=24)
        else:
            for bill in self.bills:
                due = self._bill_due_label(bill["due"])
                self._summary_line(panel, f"{bill['name']}\nDue {due}", f"${bill['amount']:,.2f}", CORAL)
        note = self._screen_panel(parent, "Bill planning", "Stay ahead of fixed costs", 1)
        upcoming = sum(item["amount"] for item in self.bills if item["due"] >= date.today().isoformat())
        tk.Label(note, text=f"${upcoming:,.2f}", bg=CARD, fg=INK, font=self.fonts["number"]).pack(anchor="w")
        tk.Label(note, text="upcoming bills", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")

    def _build_shopping_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Shopping history", "Purchases with store, account, date, and time")
        table = ttk.Treeview(panel, columns=("item", "store", "when", "account", "amount"), show="headings", height=12)
        for column, heading, width in [("item", "Item", 120), ("store", "Store / mall", 120), ("when", "Purchased", 125), ("account", "Account", 105), ("amount", "Amount", 90)]:
            table.heading(column, text=heading)
            table.column(column, width=width, anchor="e" if column == "amount" else "w")
        for purchase in self.shopping:
            table.insert("", "end", values=(purchase["item"], purchase["store"], purchase["purchased_at"], purchase["account"], f"{currency_symbol('USD')}{purchase['amount']:,.2f}"))
        table.pack(fill="both", expand=True, pady=(0, 10))
        if not self.shopping:
            tk.Label(panel, text="No purchases recorded yet. Record your first shopping trip.", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=8)
        summary = self._screen_panel(parent, "Shopping total", "All recorded purchases", 1)
        total = sum(item["amount"] for item in self.shopping)
        tk.Label(summary, text=f"${total:,.2f}", bg=CARD, fg=INK, font=self.fonts["number"]).pack(anchor="w")
        tk.Label(summary, text=f"{len(self.shopping)} purchase(s)", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")

    def _build_settings_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Settings", "Personalize your Pinch workspace")
        tk.Label(panel, text="Theme", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(4, 5))
        theme = tk.StringVar(value=self.theme_name)
        ttk.Combobox(panel, textvariable=theme, values=["Classic Blue", "Light"], state="readonly", width=28).pack(anchor="w", ipady=4)
        tk.Button(panel, text="Save theme", command=lambda: self._save_theme(theme.get()), bg=GREEN, fg="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=14, pady=8, cursor="hand2").pack(anchor="w", pady=(12, 25))
        tk.Label(panel, text="Automatic currency", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")
        detected = self._detect_currency()
        tk.Label(panel, text=f"{currency_symbol(detected)}  {self._currency_name(detected)}", bg=CARD, fg=INK, font=self.fonts["title"]).pack(anchor="w", pady=(6, 3))
        tk.Label(panel, text="Detected from your computer locale. Account currency remains selectable when creating an account.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=340, justify="left").pack(anchor="w")
        details = self._screen_panel(parent, "Session", "Your current workspace", 1)
        tk.Label(details, text=self.current_username or "Not signed in", bg=CARD, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        tk.Label(details, text="Session stays active until you choose Log out.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=260, justify="left").pack(anchor="w", pady=(6, 0))

    def _save_theme(self, theme: str) -> None:
        self.theme_name = theme
        messagebox.showinfo("Settings", f"Theme set to {theme}.")

    def _detect_currency_notice(self) -> None:
        detected = self._detect_currency()
        messagebox.showinfo("Automatic currency", f"Detected currency: {currency_symbol(detected)} {self._currency_name(detected)}")

    @staticmethod
    def _currency_name(code: str) -> str:
        return dict(CURRENCIES).get(code, "Local currency")

    @staticmethod
    def _detect_currency() -> str:
        locale_name = locale.getlocale()[0] or ""
        country = locale_name.split("_")[-1].upper()
        country_map = {"US": "USD", "CA": "CAD", "GB": "GBP", "AU": "AUD", "NZ": "NZD", "IN": "INR", "JP": "JPY", "CN": "CNY", "KR": "KRW", "BR": "BRL", "MX": "MXN", "CH": "CHF", "NO": "NOK", "SE": "SEK", "DK": "DKK", "PL": "PLN", "TR": "TRY", "ZA": "ZAR", "SG": "SGD", "HK": "HKD"}
        return country_map.get(country, "USD")

    def _build_goals_screen(self, parent: tk.Frame) -> None:
        panel = self._screen_panel(parent, "Goals", "Give your next milestones a place to live")
        if not self.goal_records:
            tk.Label(panel, text="No goals yet. Create your first goal to see progress here.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=24)
        else:
            for goal in self.goal_records:
                progress = min(100, int(goal["saved"] / goal["target"] * 100)) if goal["target"] else 0
                self._goal_row_in(panel, goal["name"], f"${goal['saved']:,.2f} / ${goal['target']:,.2f}", progress, GREEN)
        note = self._screen_panel(parent, "Next move", "Small and specific wins add up", 1)
        tk.Label(note, text=str(len(self.goal_records)), bg=CARD, fg=INK, font=self.fonts["number"]).pack(anchor="w")
        tk.Label(note, text="active goals", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w")

    def _build_insights_screen(self, parent: tk.Frame) -> None:
        parent.grid_rowconfigure(1, weight=1)
        panel = self._screen_panel(parent, "Insights", "Patterns from your recent activity")
        expenses = sum(item.amount for item in self.transactions if item.kind == "expense")
        income = sum(item.amount for item in self.transactions if item.kind == "income")
        net = income - expenses
        entries = [("Current net change", f"${net:,.2f} from recorded income and expenses.")]
        if self.savings:
            entries.append(("Savings momentum", f"${sum(item['amount'] for item in self.savings):,.2f} recorded in savings."))
        if self.bills:
            entries.append(("Upcoming commitments", f"{len(self.bills)} bill(s) have due dates on your calendar."))
        if not self.transactions and not self.savings and not self.bills:
            entries.append(("Start with an entry", "Add a transaction, saving, or bill to generate personal insights."))
        self._persist_insights(entries)
        for title, detail in entries:
            tk.Label(panel, text=title, bg=CARD, fg=INK, font=self.fonts["body_bold"]).pack(anchor="w", pady=(3, 2))
            tk.Label(panel, text=detail, bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=(0, 16))
        chart = self._screen_panel(parent, "Spending by category", "This month's mix", 1)
        categories = {}
        for item in self.transactions:
            if item.kind == "expense":
                categories[item.category] = categories.get(item.category, 0) + item.amount
        if not categories:
            tk.Label(chart, text="Category insights will appear after you add expenses.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=320, justify="left").pack(anchor="w", pady=24)
        else:
            graph = tk.Canvas(chart, bg=CARD, height=220, highlightthickness=0)
            graph.pack(fill="x", expand=True, pady=(4, 0))
            colors = [GREEN, CORAL, NAVY, YELLOW, "#7a5a9e"]
            ordered = sorted(categories.items(), key=lambda pair: pair[1], reverse=True)
            maximum = max(amount for _, amount in ordered)
            for index, (category, amount) in enumerate(ordered):
                x = 28 + index * 70
                bar_height = max(12, (amount / maximum) * 140)
                y = 178 - bar_height
                color = colors[index % len(colors)]
                graph.create_rectangle(x, y, x + 38, 178, fill=color, outline="")
                graph.create_text(x + 19, y - 9, text=f"${amount:,.0f}", fill=INK, font=("Segoe UI", 8, "bold"))
                graph.create_text(x + 19, 194, text=category[:9], fill=MUTED, font=("Segoe UI", 8))
            graph.create_line(20, 178, 340, 178, fill=LINE)
        pie_panel = tk.Frame(parent, bg=CARD, padx=22, pady=20, highlightbackground=LINE, highlightthickness=1)
        pie_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(16, 0))
        tk.Label(pie_panel, text="Spending share", bg=CARD, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        tk.Label(pie_panel, text="Category distribution", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(4, 8))
        if categories:
            pie = tk.Canvas(pie_panel, bg=CARD, width=300, height=190, highlightthickness=0)
            pie.pack(fill="both", expand=True)
            colors = [GREEN, CORAL, NAVY, YELLOW, "#7a5a9e"]
            total = sum(categories.values())
            start = 0.0
            for index, (category, amount) in enumerate(sorted(categories.items(), key=lambda pair: pair[1], reverse=True)):
                extent = amount / total * 360
                pie.create_arc(22, 18, 162, 158, start=start, extent=extent, fill=colors[index % len(colors)], outline=CARD, width=2)
                legend_y = 28 + index * 25
                pie.create_rectangle(190, legend_y, 202, legend_y + 12, fill=colors[index % len(colors)], outline="")
                pie.create_text(210, legend_y + 6, text=f"{category}  {amount / total:.0%}", anchor="w", fill=INK, font=("Segoe UI", 8))
                start += extent
        else:
            tk.Label(pie_panel, text="The pie chart will appear after you add expenses.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=260, justify="left").pack(anchor="w", pady=24)

    def _persist_insights(self, entries: list[tuple[str, str]]) -> None:
        if self.current_user_id is None:
            return
        with sqlite3.connect(DATABASE_PATH) as connection:
            for title, detail in entries:
                exists = connection.execute("SELECT id FROM insights WHERE user_id = ? AND title = ? AND detail = ?", (self.current_user_id, title, detail)).fetchone()
                if exists is None:
                    connection.execute("INSERT INTO insights (user_id, title, detail) VALUES (?, ?, ?)", (self.current_user_id, title, detail))

    def _account_notice(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Add account")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack()
        tk.Label(box, text="Create an account", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        fields = {}
        for row, label in enumerate(["Account name", "Opening balance"], start=1):
            tk.Label(box, text=label, bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(box, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
            entry.grid(row=row, column=1, padx=(20, 0), pady=6, ipady=6)
            fields[label] = entry
        tk.Label(box, text="Type", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=3, column=0, sticky="w", pady=6)
        kind = tk.StringVar(value="Checking")
        ttk.Combobox(box, textvariable=kind, values=["Checking", "Savings", "Credit", "Cash"], state="readonly", width=24).grid(row=3, column=1, padx=(20, 0), pady=6, ipady=4)
        tk.Label(box, text="Currency", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=4, column=0, sticky="w", pady=6)
        currency_options = {f"{currency_symbol(code)} - {name}": code for code, name in CURRENCIES}
        currency = tk.StringVar(value="$ - US dollar")
        currency_values = list(currency_options)
        ttk.Combobox(box, textvariable=currency, values=currency_values, state="readonly", width=24).grid(row=4, column=1, padx=(20, 0), pady=6, ipady=4)

        def save() -> None:
            name = fields["Account name"].get().strip()
            try:
                balance = float(fields["Opening balance"].get().replace(",", "").replace("$", "") or 0)
            except ValueError:
                balance = -1
            if not name or balance < 0:
                messagebox.showwarning("Check the details", "Enter an account name and a valid opening balance.", parent=dialog)
                return
            currency_code = currency_options[currency.get()]
            self.accounts.append({"name": name, "kind": kind.get(), "balance": balance, "currency": currency_code})
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO accounts (user_id, name, kind, balance, currency) VALUES (?, ?, ?, ?, ?)", (self.current_user_id, name, kind.get(), balance, currency_code))
            dialog.destroy()
            self._show_screen("Accounts")

        tk.Button(box, text="Create account", command=save, bg=GREEN, fg="white", activebackground="#245576", relief="flat", bd=0, font=self.fonts["body_bold"], padx=16, pady=10, cursor="hand2").grid(row=5, column=1, sticky="e", pady=(18, 0))
        fields["Account name"].focus_set()

    def _savings_notice(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Add savings")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack()
        tk.Label(box, text="Record savings", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        fields = self._record_fields(box, ["Description", "Amount"])

        def save() -> None:
            name = fields["Description"].get().strip()
            amount = self._read_amount(fields["Amount"].get())
            if not name or amount <= 0:
                messagebox.showwarning("Check the details", "Enter a description and an amount greater than zero.", parent=dialog)
                return
            self.savings.append({"name": name, "amount": amount, "day": date.today().isoformat()})
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO savings (user_id, name, amount, day) VALUES (?, ?, ?, ?)", (self.current_user_id, name, amount, date.today().isoformat()))
            dialog.destroy()
            self._show_screen("Savings")

        self._dialog_button(box, "Save savings", save, 3)
        fields["Description"].focus_set()

    def _bill_notice(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Add bill")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack()
        tk.Label(box, text="Schedule a bill", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        fields = self._record_fields(box, ["Bill name", "Amount"])
        tk.Label(box, text="Due date", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=3, column=0, sticky="w", pady=6)
        due = tk.Entry(box, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
        due.insert(0, date.today().isoformat())
        due.grid(row=3, column=1, padx=(20, 0), pady=6, ipady=6)

        def save() -> None:
            name = fields["Bill name"].get().strip()
            amount = self._read_amount(fields["Amount"].get())
            try:
                due_date = datetime.strptime(due.get().strip(), "%Y-%m-%d").date()
            except ValueError:
                due_date = None
            if not name or amount <= 0 or due_date is None:
                messagebox.showwarning("Check the details", "Use a name, a positive amount, and a date in YYYY-MM-DD format.", parent=dialog)
                return
            self.bills.append({"name": name, "amount": amount, "due": due_date.isoformat()})
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO bills (user_id, name, amount, due) VALUES (?, ?, ?, ?)", (self.current_user_id, name, amount, due_date.isoformat()))
            dialog.destroy()
            self._show_screen("Bills")

        self._dialog_button(box, "Schedule bill", save, 4)
        fields["Bill name"].focus_set()

    def _shopping_notice(self) -> None:
        if not self.accounts:
            messagebox.showwarning("Shopping", "Create an account before recording a purchase.")
            return
        dialog = tk.Toplevel(self)
        dialog.title("Shopping calculator")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack()
        tk.Label(box, text="Shopping calculator", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        fields = self._record_fields(box, ["Grocery items / combination", "Store / mall"])
        tk.Label(box, text="Amount", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=3, column=0, sticky="w", pady=6)
        amount = tk.StringVar()
        amount_entry = tk.Entry(box, textvariable=amount, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["number"], justify="right", highlightthickness=1, highlightbackground=LINE)
        amount_entry.grid(row=3, column=1, padx=(20, 0), pady=6, ipady=5)
        keypad = tk.Frame(box, bg=BG)
        keypad.grid(row=4, column=1, sticky="e", pady=(4, 6))
        def press(value: str) -> None:
            if value == "C":
                amount.set("")
            elif value == "⌫":
                amount.set(amount.get()[:-1])
            elif value == "." and "." in amount.get():
                return
            else:
                amount.set(amount.get() + value)
        for index, value in enumerate(["7", "8", "9", "4", "5", "6", "1", "2", "3", "C", "0", "."]):
            tk.Button(keypad, text=value, command=lambda item=value: press(item), bg=CARD, fg=INK, relief="flat", bd=0, width=4, pady=5, cursor="hand2").grid(row=index // 3, column=index % 3, padx=2, pady=2)
        tk.Button(keypad, text="⌫", command=lambda: press("⌫"), bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, width=4, pady=5, cursor="hand2").grid(row=3, column=2, padx=2, pady=2)
        tk.Label(box, text="Account", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=5, column=0, sticky="w", pady=6)
        account = tk.StringVar(value=self.accounts[0]["name"])
        ttk.Combobox(box, textvariable=account, values=[item["name"] for item in self.accounts], state="readonly", width=24).grid(row=5, column=1, padx=(20, 0), pady=6, ipady=4)
        tk.Label(box, text="Purchase date", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=6, column=0, sticky="w", pady=6)
        purchased_date = tk.StringVar(value=date.today().isoformat())
        date_row = tk.Frame(box, bg=BG)
        date_row.grid(row=6, column=1, padx=(20, 0), pady=6, sticky="e")
        tk.Entry(date_row, textvariable=purchased_date, width=17, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE).pack(side="left", ipady=6)
        tk.Button(date_row, text=self._icon("calendar"), command=lambda: self._open_date_picker(purchased_date), bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, font=(self.icon_font_family, 10), padx=8, pady=6, cursor="hand2").pack(side="left", padx=(5, 0))
        tk.Label(box, text="Purchase time", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=7, column=0, sticky="w", pady=6)
        purchased_time = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        tk.Entry(box, textvariable=purchased_time, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE).grid(row=7, column=1, padx=(20, 0), pady=6, ipady=6)

        def save() -> None:
            item = fields["Grocery items / combination"].get().strip()
            store = fields["Store / mall"].get().strip()
            total = self._read_amount(amount.get())
            try:
                purchased_at = datetime.strptime(f"{purchased_date.get().strip()} {purchased_time.get().strip()}", "%Y-%m-%d %H:%M")
            except ValueError:
                purchased_at = None
            if not item or not store or total <= 0 or purchased_at is None:
                messagebox.showwarning("Check the details", "Enter item, store, positive amount, date YYYY-MM-DD, and time HH:MM.", parent=dialog)
                return
            record = {"item": item, "amount": total, "store": store, "purchased_at": purchased_at.strftime("%Y-%m-%d %H:%M"), "account": account.get()}
            self.shopping.insert(0, record)
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO shopping (user_id, item, amount, store, purchased_at, account) VALUES (?, ?, ?, ?, ?, ?)", (self.current_user_id, item, total, store, record["purchased_at"], account.get()))
            dialog.destroy()
            self._show_screen("Shopping")

        self._dialog_button(box, "Save purchase", save, 8)
        fields["Grocery items / combination"].focus_set()

    def _insight_notice(self) -> None:
        self._show_screen("Insights")

    def _record_fields(self, parent: tk.Frame, labels: list[str]) -> dict[str, tk.Entry]:
        fields = {}
        for row, label in enumerate(labels, start=1):
            tk.Label(parent, text=label, bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(parent, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
            entry.grid(row=row, column=1, padx=(20, 0), pady=6, ipady=6)
            fields[label] = entry
        return fields

    def _dialog_button(self, parent: tk.Frame, label: str, command: object, row: int) -> None:
        tk.Button(parent, text=label, command=command, bg=GREEN, fg="white", activebackground="#245576", relief="flat", bd=0, font=self.fonts["body_bold"], padx=16, pady=10, cursor="hand2").grid(row=row, column=1, sticky="e", pady=(18, 0))

    @staticmethod
    def _read_amount(value: str) -> float:
        try:
            return float(value.replace(",", "").replace("$", "").strip())
        except ValueError:
            return -1

    @staticmethod
    def _bill_due_label(value: str) -> str:
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%b %d, %Y")
        except ValueError:
            return value

    def _notify_due_bills(self) -> None:
        today = date.today()
        due_soon = []
        for bill in self.bills:
            if bill["name"] in self.notified_bills:
                continue
            due_date = datetime.strptime(bill["due"], "%Y-%m-%d").date()
            days_left = (due_date - today).days
            if days_left <= 3:
                due_soon.append(f"{bill['name']} - ${bill['amount']:,.2f} ({self._bill_due_label(bill['due'])})")
                self.notified_bills.add(bill["name"])
        if due_soon:
            messagebox.showwarning("Bills due soon", "Review these bills:\n\n" + "\n".join(due_soon), parent=self)

    def _logout(self) -> None:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("DELETE FROM sessions WHERE id = 1")
        self.current_username = ""
        self.current_user_id = None
        self._show_login(None)

    def _refresh_current_page(self) -> None:
        self._load_user_data()
        if self.active_page == "Home":
            self._open_dashboard()
        else:
            self._show_screen(self.active_page)

    def _metric_card(self, parent: tk.Widget, label: str, value: str, detail: str, accent: str, column: int, command: object = None) -> tk.Frame:
        card = tk.Frame(parent, bg=CARD, padx=20, pady=17, highlightbackground=LINE, highlightthickness=1)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 7, 7 if column < 2 else 0))
        tk.Label(card, text=label.upper(), bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        value_label = tk.Label(card, text=value, bg=CARD, fg=INK, font=self.fonts["number"])
        value_label.pack(anchor="w", pady=(11, 4))
        tk.Label(card, text=detail, bg=CARD, fg=accent, font=self.fonts["small"]).pack(anchor="w")
        card.value_label = value_label
        if command is not None:
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda event: command())
            card.bind("<Button-1>", lambda event: command())
            card.configure(cursor="hand2")
        return card

    def _build_goals(self) -> None:
        tk.Label(self.goals, text="Your goals", bg=CARD, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        tk.Label(self.goals, text="Small moves, visible progress.", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(3, 22))
        if not self.goal_records:
            tk.Label(self.goals, text="No goals yet. Create one from Goals.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=240, justify="left").pack(anchor="w", pady=15)
        else:
            for goal in self.goal_records[:3]:
                progress = min(100, int(goal["saved"] / goal["target"] * 100)) if goal["target"] else 0
                self._goal_row(goal["name"], f"${goal['saved']:,.2f} / ${goal['target']:,.2f}", progress, GREEN)
        tk.Button(self.goals, text=f"{self._icon('add')}  Create a goal", command=self._goal_notice, bg="#eef1e8", fg=GREEN, activebackground="#e2e9dd", relief="flat", bd=0, font=self.fonts["body_bold"], padx=14, pady=9, cursor="hand2").pack(anchor="w", pady=(21, 0))

    def _goal_row(self, name: str, amount: str, progress: int, color: str) -> None:
        row = tk.Frame(self.goals, bg=CARD)
        row.pack(fill="x", pady=(0, 19))
        top = tk.Frame(row, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=name, bg=CARD, fg=INK, font=self.fonts["body_bold"]).pack(side="left")
        tk.Label(top, text=amount, bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(side="right")
        bar = ttk.Progressbar(row, style="Pinch.Horizontal.TProgressbar", maximum=100, value=progress)
        bar.pack(fill="x", pady=(9, 0))

    def _refresh(self) -> None:
        for child in self.activity.winfo_children():
            child.destroy()
        header = tk.Frame(self.activity, bg=CARD)
        header.pack(fill="x", pady=(0, 17))
        tk.Label(header, text="Recent activity", bg=CARD, fg=INK, font=self.fonts["title"]).pack(side="left")
        tk.Button(header, text="View all  →", command=lambda: self._set_filter("All activity"), bg=CARD, fg=GREEN, activebackground=CARD, relief="flat", bd=0, font=self.fonts["small"], cursor="hand2").pack(side="right")
        filters = tk.Frame(self.activity, bg=CARD)
        filters.pack(fill="x", pady=(0, 10))
        for label in ["All activity", "Income", "Expenses"]:
            active = label == self.active_filter
            tk.Button(filters, text=label, command=lambda value=label: self._set_filter(value), bg=GREEN if active else CARD, fg="white" if active else MUTED, activebackground=GREEN, activeforeground="white", relief="flat", bd=0, font=self.fonts["small"], padx=10, pady=5, cursor="hand2").pack(side="left", padx=(0, 5))
        visible = self.transactions if self.active_filter == "All activity" else [item for item in self.transactions if (item.kind == "income") == (self.active_filter == "Income")]
        if not visible:
            tk.Label(self.activity, text="No transactions yet. Add your first one to start building your view.", bg=CARD, fg=MUTED, font=self.fonts["small"], wraplength=420, justify="left").pack(anchor="w", pady=24)
        else:
            for item in visible:
                self._transaction_row(item)

    def _transaction_row(self, item: Transaction) -> None:
        row = tk.Frame(self.activity, bg=CARD)
        row.pack(fill="x", pady=9)
        color = MINT if item.kind == "income" else "#f4e4df"
        symbol = "＋" if item.kind == "income" else "−"
        badge = tk.Label(row, text=symbol, bg=color, fg=GREEN if item.kind == "income" else CORAL, font=("Segoe UI", 12, "bold"), width=3, height=1)
        badge.pack(side="left", padx=(0, 12))
        info = tk.Frame(row, bg=CARD)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=item.name, bg=CARD, fg=INK, font=self.fonts["body_bold"]).pack(anchor="w")
        tk.Label(info, text=f"{item.category}  ·  {item.day}", bg=CARD, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=(2, 0))
        amount = f"{'+' if item.kind == 'income' else '-'}${item.amount:,.2f}"
        tk.Label(row, text=amount, bg=CARD, fg=GREEN if item.kind == "income" else INK, font=self.fonts["body_bold"]).pack(side="right")

    def _set_filter(self, value: str) -> None:
        self.active_filter = value
        self._refresh()

    def _goal_notice(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Create goal")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack()
        tk.Label(box, text="Create a goal", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        fields = self._record_fields(box, ["Goal name", "Target amount", "Already saved"])

        def save() -> None:
            name = fields["Goal name"].get().strip()
            target = self._read_amount(fields["Target amount"].get())
            saved = self._read_amount(fields["Already saved"].get() or "0")
            if not name or target <= 0 or saved < 0 or saved > target:
                messagebox.showwarning("Check the details", "Enter a name, a positive target, and saved amount up to the target.", parent=dialog)
                return
            self.goal_records.append({"name": name, "target": target, "saved": saved})
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO goals (user_id, name, target, saved) VALUES (?, ?, ?, ?)", (self.current_user_id, name, target, saved))
            dialog.destroy()
            self._show_screen("Goals")

        self._dialog_button(box, "Create goal", save, 4)
        fields["Goal name"].focus_set()

    def _open_add_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Add transaction")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=BG, padx=28, pady=25)
        box.pack()
        tk.Label(box, text="Add a transaction", bg=BG, fg=INK, font=self.fonts["title"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        if not self.accounts:
            tk.Label(box, text="Create an account before recording a transaction.", bg=BG, fg=CORAL, font=self.fonts["small"]).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
            tk.Button(box, text="Open Accounts", command=lambda: (dialog.destroy(), self._show_screen("Accounts")), bg=GREEN, fg="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=14, pady=9, cursor="hand2").grid(row=2, column=1, sticky="e")
            return
        fields = {}
        for row, (label, key) in enumerate([("Name", "name"), ("Amount", "amount")], start=1):
            tk.Label(box, text=label, bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(box, width=27, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
            entry.grid(row=row, column=1, padx=(20, 0), pady=6, ipady=6)
            fields[key] = entry
        tk.Label(box, text="Account", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=3, column=0, sticky="w", pady=6)
        account = tk.StringVar(value=self.accounts[0]["name"])
        ttk.Combobox(box, textvariable=account, values=[item["name"] for item in self.accounts], state="readonly", width=24).grid(row=3, column=1, padx=(20, 0), pady=6, ipady=4)
        tk.Label(box, text="Type", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=4, column=0, sticky="w", pady=6)
        kind = tk.StringVar(value="expense")
        ttk.Combobox(box, textvariable=kind, values=["expense", "income"], state="readonly", width=24).grid(row=4, column=1, padx=(20, 0), pady=6, ipady=4)
        tk.Label(box, text="Category", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=5, column=0, sticky="w", pady=6)
        category = tk.StringVar(value="General")
        ttk.Combobox(box, textvariable=category, values=["General", "Food", "Home", "Transport", "Groceries", "Fun", "Income"], state="readonly", width=24).grid(row=5, column=1, padx=(20, 0), pady=6, ipady=4)
        tk.Label(box, text="Date", bg=BG, fg=MUTED, font=self.fonts["small"]).grid(row=6, column=0, sticky="w", pady=6)
        day = tk.StringVar(value=date.today().isoformat())
        date_row = tk.Frame(box, bg=BG)
        date_row.grid(row=6, column=1, padx=(20, 0), pady=6, sticky="e")
        date_entry = tk.Entry(date_row, textvariable=day, width=17, relief="flat", bg="white", fg=INK, font=self.fonts["body"], highlightthickness=1, highlightbackground=LINE)
        date_entry.pack(side="left", ipady=6)
        tk.Button(date_row, text=self._icon("calendar"), command=lambda: self._open_date_picker(day), bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, font=(self.icon_font_family, 10), padx=8, pady=6, cursor="hand2").pack(side="left", padx=(5, 0))

        def save() -> None:
            name = fields["name"].get().strip()
            try:
                amount = float(fields["amount"].get().replace(",", "").replace("$", ""))
            except ValueError:
                amount = 0
            try:
                transaction_date = datetime.strptime(day.get().strip(), "%Y-%m-%d").date()
            except ValueError:
                transaction_date = None
            if not name or amount <= 0 or transaction_date is None:
                messagebox.showwarning("Check the details", "Enter a name, a positive amount, and a date in YYYY-MM-DD format.", parent=dialog)
                return
            self.transactions.insert(0, Transaction(name, category.get(), amount, kind.get(), transaction_date.isoformat(), account.get()))
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("INSERT INTO transactions (user_id, name, category, amount, kind, day, account) VALUES (?, ?, ?, ?, ?, ?, ?)", (self.current_user_id, name, category.get(), amount, kind.get(), transaction_date.isoformat(), account.get()))
            dialog.destroy()
            self._refresh_current_page()

        tk.Button(box, text="Save transaction", command=save, bg=GREEN, fg="white", activebackground="#0b5949", relief="flat", bd=0, font=self.fonts["body_bold"], padx=16, pady=10, cursor="hand2").grid(row=7, column=1, sticky="e", pady=(18, 0))
        fields["name"].focus_set()

    def _open_date_picker(self, target: tk.StringVar) -> None:
        try:
            selected = datetime.strptime(target.get(), "%Y-%m-%d").date()
        except ValueError:
            selected = date.today()
        picker = tk.Toplevel(self)
        picker.title("Choose date")
        picker.configure(bg=BG)
        picker.resizable(False, False)
        picker.transient(self)
        picker.grab_set()
        picker.geometry("390x410")
        month = [selected.year, selected.month]

        def render() -> None:
            for child in picker.winfo_children():
                child.destroy()
            heading = tk.Frame(picker, bg=NAVY, padx=18, pady=15)
            heading.pack(fill="x")
            tk.Label(heading, text="Choose transaction date", bg=NAVY, fg="#d9e6f0", font=self.fonts["small"]).pack(anchor="w")
            controls = tk.Frame(heading, bg=NAVY)
            controls.pack(fill="x", pady=(7, 0))
            tk.Button(controls, text="‹", command=lambda: change_month(-1), bg="#28628e", fg="white", relief="flat", bd=0, font=self.fonts["title"], width=3).pack(side="left")
            tk.Label(controls, text=f"{calendar.month_name[month[1]]} {month[0]}", bg=NAVY, fg="white", font=self.fonts["body_bold"]).pack(side="left", expand=True)
            tk.Button(controls, text="›", command=lambda: change_month(1), bg="#28628e", fg="white", relief="flat", bd=0, font=self.fonts["title"], width=3).pack(side="right")
            grid = tk.Frame(picker, bg=BG, padx=18, pady=15)
            grid.pack()
            for column, name in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
                tk.Label(grid, text=name, bg=BG, fg=MUTED, font=("Segoe UI", 8, "bold"), width=5).grid(row=0, column=column, pady=(0, 7))
            for row, week in enumerate(calendar.monthcalendar(month[0], month[1]), start=1):
                for column, day_number in enumerate(week):
                    if day_number:
                        day_value = date(month[0], month[1], day_number)
                        is_selected = day_value == selected
                        is_today = day_value == date.today()
                        button_bg = GREEN if is_selected else MINT if is_today else CARD
                        button_fg = "white" if is_selected else INK
                        tk.Button(grid, text=str(day_number), command=lambda value=day_number: choose(value), bg=button_bg, fg=button_fg, activebackground="#c5dce9", relief="flat", bd=0, width=5, pady=7, cursor="hand2").grid(row=row, column=column, padx=2, pady=2)
            footer = tk.Frame(picker, bg=BG, padx=18, pady=(0, 14))
            footer.pack(fill="x")
            tk.Button(footer, text="Today", command=lambda: choose(date.today().day) if month == [date.today().year, date.today().month] else set_today(), bg="#e8f0f5", fg=GREEN, relief="flat", bd=0, font=self.fonts["body_bold"], padx=12, pady=7, cursor="hand2").pack(side="left")
            tk.Button(footer, text="Cancel", command=picker.destroy, bg=BG, fg=MUTED, relief="flat", bd=0, font=self.fonts["body_bold"], padx=12, pady=7, cursor="hand2").pack(side="right")

        def choose(day_number: int) -> None:
            target.set(date(month[0], month[1], day_number).isoformat())
            picker.destroy()

        def change_month(offset: int) -> None:
            month[1] += offset
            if month[1] == 13:
                month[0] += 1
                month[1] = 1
            elif month[1] == 0:
                month[0] -= 1
                month[1] = 12
            render()

        def set_today() -> None:
            target.set(date.today().isoformat())
            picker.destroy()

        render()

    def _update_metrics(self) -> None:
        expenses = sum(item.amount for item in self.transactions if item.kind == "expense")
        income = sum(item.amount for item in self.transactions if item.kind == "income")
        account_total = sum(account["balance"] for account in self.accounts)
        saved = sum(item["amount"] for item in self.savings)
        currency = self.accounts[0].get("currency", "USD") if self.accounts else "USD"
        symbol = currency_symbol(currency)
        self.balance_card.value_label.config(text=f"{symbol}{account_total + income - expenses:,.2f}")
        self.spent_card.value_label.config(text=f"{symbol}{expenses:,.2f}")
        self.saved_card.value_label.config(text=f"{symbol}{saved:,.2f}")

    def _show_total_details(self, total_type: str) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Money detail")
        dialog.configure(bg=BG)
        dialog.transient(self)
        box = tk.Frame(dialog, bg=BG, padx=28, pady=24)
        box.pack(fill="both", expand=True)
        titles = {"available": "Where available money comes from", "spent": "Where spending belongs", "saved": "Where savings are held"}
        tk.Label(box, text=titles[total_type], bg=BG, fg=INK, font=self.fonts["title"]).pack(anchor="w")
        if total_type == "available":
            for account in self.accounts:
                self._summary_line(box, account["name"], f"{currency_symbol(account.get('currency', 'USD'))}{account['balance']:,.2f}", NAVY)
            income = sum(item.amount for item in self.transactions if item.kind == "income")
            expenses = sum(item.amount for item in self.transactions if item.kind == "expense")
            self._summary_line(box, "Transaction net", f"{currency_symbol('USD')}{income - expenses:,.2f}", GREEN)
        elif total_type == "spent":
            categories = {}
            for item in self.transactions:
                if item.kind == "expense":
                    categories[item.category] = categories.get(item.category, 0) + item.amount
            for category, amount in sorted(categories.items(), key=lambda item: item[1], reverse=True):
                self._summary_line(box, category, f"{currency_symbol('USD')}{amount:,.2f}", CORAL)
            if not categories:
                tk.Label(box, text="No spending recorded yet.", bg=BG, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=20)
        else:
            for item in self.savings:
                self._summary_line(box, item["name"], f"{currency_symbol('USD')}{item['amount']:,.2f}", GREEN)
            if not self.savings:
                tk.Label(box, text="No savings recorded yet.", bg=BG, fg=MUTED, font=self.fonts["small"]).pack(anchor="w", pady=20)
        tk.Button(box, text="Close", command=dialog.destroy, bg=GREEN, fg="white", relief="flat", bd=0, font=self.fonts["body_bold"], padx=14, pady=8, cursor="hand2").pack(anchor="e", pady=(18, 0))

    def _show_about(self) -> None:
        messagebox.showinfo("About Pinch Finance", "Pinch Finance 0.1 beta\nA personal finance workspace.")


if __name__ == "__main__":
    app = PinchFinance()
    app.mainloop()
