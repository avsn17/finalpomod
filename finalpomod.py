import time, random, os, json, webbrowser, shutil
from colorama import Fore, Style, init
from blessed import Terminal 

try:
    from playsound import playsound
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False

init(autoreset=True)
term = Terminal()
STATS_FILE = "voyage_logs.json"

# DIMENSIONS & BREAK THEMES
THEMES = {
    "1": {"name": "DEEP NEBULA", "c": Fore.MAGENTA, "s": "🦋", "unit": "LY", "music": "https://www.youtube.com/watch?v=egxyRSb_XtI"},
    "2": {"name": "NIGHT CITY", "c": Fore.RED, "s": "🏮", "unit": "Cred", "music": "https://www.youtube.com/watch?v=f02mOEt11OQ"},
    "3": {"name": "MINECRAFT", "c": Fore.GREEN, "s": "🧱", "unit": "Blocks", "music": "https://www.youtube.com/watch?v=Dg0IjOzxpzM"},
    "7": {"name": "THE MATRIX", "c": Fore.CYAN, "s": "🍃", "unit": "Data", "music": "https://www.youtube.com/watch?v=u36th-a8zMM"}
}

BREAK_THEME = {"name": "COOLDOWN", "c": Fore.BLUE, "s": "☕", "music": "https://www.youtube.com/watch?v=jfKfPfyJRdk"}

# PHILOSOPHY SETS
WORK_QUOTES = [
    {"a": "Marcus Aurelius", "m": "The soul becomes dyed with the color of its thoughts."},
    {"a": "Musashi", "m": "Do nothing which is of no use."},
    {"a": "Seneca", "m": "Luck is what happens when preparation meets opportunity."}
]

BREAK_QUOTES = [
    {"a": "Lao Tzu", "m": "Nature does not hurry, yet everything is accomplished."},
    {"a": "Pascal", "m": "All of humanity's problems stem from man's inability to sit quietly in a room alone."},
    {"a": "Epicurus", "m": "Be moderate in order to taste the joys of life in abundance."}
]

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f: return json.load(f)
        except: pass
    return {"sessions": 0, "total_score": 0, "mentor_history": {}, "sessions_today": 0}

def play_alert():
    if SOUND_ENABLED: print('\a') 
    else: print('\a')

def draw_buttons(cols, mode="work"):
    btns = [("[M] MEME", Fore.YELLOW), ("[H] MANUAL", Fore.BLUE), ("[C] QUOTE", Fore.WHITE), ("[X] EXIT", Fore.RED)]
    if mode == "work": btns.insert(0, ("[S] SYNC", Fore.GREEN))
    button_row = " ".join([f"{c}【 {t} 】{Style.RESET_ALL}" for t, c in btns])
    print(f"\n{button_row.center(cols + 40)}")

def run_timer(minutes, label, theme, stats, daily_target, is_break=False):
    total_seconds = minutes * 60
    seconds = total_seconds
    quote_list = BREAK_QUOTES if is_break else WORK_QUOTES
    quote = random.choice(quote_list)
    
    # Auto-open music for the mode
    webbrowser.open(theme['music'])
    
    with term.cbreak():
        while seconds >= 0:
            cols, _ = shutil.get_terminal_size()
            print(term.clear + term.home)
            
            # --- DAILY GOAL PROGRESS ---
            completed = stats.get("sessions_today", 0)
            goal_bar = "⦿" * completed + "○" * max(0, daily_target - completed)
            print(f"{Fore.YELLOW}{f'GOAL: {goal_bar}'.center(cols)}")
            
            # --- MENTOR PANEL ---
            print(f"{theme['c']}╔{'═'*(cols-2)}╗")
            print(f"{theme['c']}║ {Fore.CYAN}{'REFLECTING' if is_break else 'FOCUSING'}: {quote['a']}".ljust(cols-2) + f"{theme['c']}║")
            print(f"{theme['c']}║ {Fore.WHITE}\"{quote['m']}\"".ljust(cols-2) + f"{theme['c']}║")
            print(f"{theme['c']}╚{'═'*(cols-2)}╝")
            
            # --- TIMER ---
            mins, secs = divmod(seconds, 60)
            print(f"\n{theme['c']}{f'⚡ {label} ⚡'.center(cols)}")
            print(f"{Fore.WHITE + Style.BRIGHT}{f'{mins:02d}:{secs:02d}'.center(cols)}")
            
            draw_buttons(cols, mode="break" if is_break else "work")
            
            val = term.inkey(timeout=1)
            if val.lower() == 's' and not is_break: os.system("bash ~/.local/bin/sync_grind")
            elif val.lower() == 'm': webbrowser.open("https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3.../giphy.gif")
            elif val.lower() == 'c': quote = random.choice(quote_list)
            elif val.lower() == 'x': return False
            seconds -= 1
            
    play_alert()
    if not is_break:
        stats["sessions"] += 1
        stats["sessions_today"] = stats.get("sessions_today", 0) + 1
        stats["total_score"] += minutes
        stats["mentor_history"][quote['a']] = stats["mentor_history"].get(quote['a'], 0) + 1
        with open(STATS_FILE, "w") as f: json.dump(stats, f)
    return True

def main():
    stats = load_stats()
    cols, _ = shutil.get_terminal_size()
    
    print(term.clear + term.home)
    print(f"{Fore.CYAN}🛸 MISSION CONTROL INITIALIZED".center(cols))
    target_input = input(f"{'DAILY GOAL: '.rjust(cols//2)}")
    daily_target = int(target_input) if target_input.isdigit() else 4
    
    print(f"\n{Fore.WHITE}SELECT DIMENSION:".center(cols))
    for k, v in THEMES.items():
        print(f"{k} > {v['c']}{v['name']} {v['s']}".center(cols + 10))
    
    choice = input(f"\n{'ENTRY > '.rjust(cols//2)}")
    active_key = choice if choice in THEMES else "1"
    active_theme = THEMES[active_key]

    # --- MAIN LOOP ---
    while True:
        # WORK SESSION (45 MIN)
        if not run_timer(45, "THE GRIND", active_theme, stats, daily_target): break
        
        # BREAK SESSION (5 MIN)
        print(term.clear + term.home)
        print(f"{Fore.BLUE}MISSION COMPLETE. ENTERING COOLDOWN...".center(cols))
        time.sleep(2)
        if not run_timer(5, "COOLDOWN", BREAK_THEME, stats, daily_target, is_break=True): break

if __name__ == "__main__":
    main()

def save_to_cloud():
    print(Fore.GREEN + "\n☁️  INITIATING QUANTUM SYNC...")
    # This calls the bash script we just created
    result = os.system("bash ~/.local/bin/sync_grind")
    if result == 0:
        print(Fore.CYAN + "✅ GITHUB SYNC COMPLETE. AURA SECURED.")
    else:
        print(Fore.RED + "❌ SYNC FAILED. CHECK YOUR GIT CONFIG.")
    time.sleep(2)