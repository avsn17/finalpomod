import time, random, os, json, webbrowser, shutil
from colorama import Fore, Style, init
from blessed import Terminal 

init(autoreset=True)
term = Terminal()
STATS_FILE = "voyage_logs.json"

THEMES = {
    "1": {"name": "DEEP NEBULA", "c": Fore.MAGENTA, "s": "🦋", "unit": "Light-years"},
    "2": {"name": "NIGHT CITY", "c": Fore.RED, "s": "🏮", "unit": "Street Cred"},
    "3": {"name": "MINECRAFT", "c": Fore.GREEN, "s": "🧱", "unit": "Diamonds"},
    "7": {"name": "THE MATRIX", "c": Fore.CYAN, "s": "🍃", "unit": "Data Fragments"}
}

PHILOSOPHY_QUOTES = [
    {"a": "Marcus Aurelius", "m": "The soul becomes dyed with the color of its thoughts."},
    {"a": "Seneca", "m": "Luck is what happens when preparation meets opportunity."},
    {"a": "Nietzsche", "m": "He who has a why to live can bear almost any how."},
    {"a": "Musashi", "m": "Do nothing which is of no use."},
    {"a": "Epictetus", "m": "First learn the meaning of what you say, and then speak."},
    {"a": "Lao Tzu", "m": "Nature does not hurry, yet everything is accomplished."},
    {"a": "Sun Tzu", "m": "Victory comes from finding opportunities in problems."},
    {"a": "Socrates", "m": "An unexamined life is not worth living."}
]

# Genz Meme Rewards (Brainrot / High Aura)
MEME_REWARDS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2ZpYmdmNDByYjIycG80eXN6eHExZTViYjZqYm0zcHd4amZtZmthYiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/PqXrajrUkwX06qrUz0/giphy.gif",
    "https://media.tenor.com/8m-Y9_x180UAAAAM/low-taper-fade.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bm93Ynk3OXBsemY0bm5pZzZ0ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3/3o7TKMGpxx8G3kgv6M/giphy.gif"
]

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f: return json.load(f)
        except: pass
    return {"sessions": 0, "total_score": 0, "mentor_history": {}}

def save_stats(stats):
    with open(STATS_FILE, "w") as f: json.dump(stats, f, indent=4)

def run_timer(minutes, label, theme_key, stats):
    total_seconds = minutes * 60
    seconds = total_seconds
    theme = THEMES[theme_key]
    quote = random.choice(PHILOSOPHY_QUOTES)
    
    with term.cbreak():
        while seconds >= 0:
            cols, _ = shutil.get_terminal_size()
            print(term.clear + term.home)
            
            # --- MENTOR INTERFACE ---
            header = f" 🏛️  {quote['a'].upper()} IS WATCHING "
            print(f"{theme['c']}┌──{header}──{'─' * (cols - len(header) - 6)}")
            print(f"{theme['c']}│ {Fore.WHITE}\"{quote['m']}\"")
            print(f"{theme['c']}└{'─' * (cols-2)}")
            
            # --- CLOCK ---
            mins, secs = divmod(seconds, 60)
            print(f"\n{Style.BRIGHT}{theme['c']}{f'{label}'.center(cols)}")
            print(f"{Fore.WHITE + Style.BRIGHT}{f'{mins:02d}:{secs:02d}'.center(cols)}")
            
            # --- PROGRESS BAR ---
            progress = (total_seconds - seconds) / total_seconds
            filled = int(progress * 35)
            bar = "█" * filled + "░" * (35 - filled)
            print(f"{theme['c']}{f'[{bar}]'.center(cols)}")
            
            # --- HOTKEYS ---
            print(f"\n{Fore.BLACK + Style.BRIGHT}{'[M] MEME   [C] CHANGE MENTOR   [X] EXIT'.center(cols)}")
            
            val = term.inkey(timeout=1)
            if val.lower() == 'm': webbrowser.open(random.choice(MEME_REWARDS))
            elif val.lower() == 'c': quote = random.choice(PHILOSOPHY_QUOTES)
            elif val.lower() == 'x': return False
            seconds -= 1
            
    # Update Stats
    stats["sessions"] += 1
    stats["total_score"] += minutes
    stats["mentor_history"][quote['a']] = stats["mentor_history"].get(quote['a'], 0) + 1
    save_stats(stats)
    return True

def main():
    stats = load_stats()
    cols, _ = shutil.get_terminal_size()
    print(term.clear + term.home)
    
    # Dashboard
    print(f"{Fore.YELLOW}{'📜 CURRENT STANDING'.center(cols)}")
    if stats["mentor_history"]:
        top_mentor = max(stats["mentor_history"], key=stats["mentor_history"].get)
        print(f"{Fore.WHITE}Aligned School: {top_mentor}ism".center(cols))
        print(f"{Fore.WHITE}Total Grind: {stats['total_score']} Units".center(cols))
    
    print(f"\n{Fore.CYAN}{'🌌 CHOOSE YOUR DIMENSION'.center(cols)}")
    for k, v in THEMES.items():
        print(f"{k}) {v['name']} {v['s']}".center(cols))
    
    choice = input(f"\n{'Select: '.rjust(cols//2)}")
    active = choice if choice in THEMES else "1"
    
    if run_timer(45, "THE GRIND", active, stats):
        print(term.clear + term.home)
        print(f"{Fore.GREEN}{'MISSION SUCCESS'.center(cols)}")
        print(f"{Fore.WHITE}{f'+45 {THEMES[active]['unit']} gained.'.center(cols)}")
        webbrowser.open(random.choice(MEME_REWARDS))
        time.sleep(3)

if __name__ == "__main__":
    main()
