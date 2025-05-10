import time
import sys
import msvcrt
from datetime import datetime, timedelta
import winsound
import threading
import json
import os

class SuperCountdownTimer:
    def __init__(self):
        self.reset_state()
        self.load_settings()
        
    def reset_state(self):
        self.paused = False
        self.stopped = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.start_time = None
        self.end_time = None
        self.alarm_sound = True
        self.alarm_volume = 2 
        self.theme = 'default'
        self.saved_timers = []
        self.dark_mode = False
        
        self.themes = {
            'default': {'fill': '█', 'empty': ' ', 'color': ''},
            'star': {'fill': '★', 'empty': '☆', 'color': '\033[93m'},
            'heart': {'fill': '♥', 'empty': '♡', 'color': '\033[91m'},
            'tech': {'fill': '■', 'empty': '□', 'color': '\033[96m'},
            'nature': {'fill': '🌱', 'empty': '  ', 'color': '\033[92m'},
            'money': {'fill': '💰', 'empty': '  ', 'color': '\033[33m'},
        }
        
    def save_settings(self):
        settings = {
            'theme': self.theme,
            'alarm_sound': self.alarm_sound,
            'alarm_volume': self.alarm_volume,
            'dark_mode': self.dark_mode,
            'saved_timers': self.saved_timers
        }
        with open('timer_settings.json', 'w') as f:
            json.dump(settings, f)
    
    def load_settings(self):
        try:
            if os.path.exists('timer_settings.json'):
                with open('timer_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.theme = settings.get('theme', 'default')
                    self.alarm_sound = settings.get('alarm_sound', True)
                    self.alarm_volume = settings.get('alarm_volume', 2)
                    self.dark_mode = settings.get('dark_mode', False)
                    self.saved_timers = settings.get('saved_timers', [])
        except Exception:
            pass
    
    def play_alarm(self, duration=3):
        """Play alarm sound with configurable volume"""
        def _play():
            frequencies = [800, 1000, 1200] 
            duration_ms = [300, 500, 700]  
            
            freq = frequencies[self.alarm_volume - 1]
            dur = duration_ms[self.alarm_volume - 1]
            
            for _ in range(duration):
                if self.stopped:
                    break
                winsound.Beep(freq, dur)
                time.sleep(0.5)
        threading.Thread(target=_play, daemon=True).start()
    
    def display_time(self, seconds):
        sys.stdout.write('\033[2K') 
        
        theme = self.themes[self.theme]
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        
        progress = 30 * (self.total_seconds - seconds) // self.total_seconds
        progress_bar = theme['color'] + theme['fill'] * progress + theme['empty'] * (30 - progress)
        
        time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
        percent = 100 * (self.total_seconds - seconds) // self.total_seconds
        
        now = datetime.now()
        if self.end_time:
            time_left = self.end_time - now
            if time_left.total_seconds() > 0:
                end_str = f"Ends at: {self.end_time.strftime('%H:%M:%S')}"
            else:
                end_str = "Time's up!"
        else:
            end_str = ""
        
        display_lines = [
            f"{theme['color']}⏳ {time_str} | {progress_bar} | {percent:3d}%",
            f"Controls: [P]ause [R]esume [+/-]Adjust [S]top [T]heme [H]elp",
            f"Alarm: {'ON' if self.alarm_sound else 'OFF'} (Vol: {'🔈' * self.alarm_volume}) | {end_str}"
        ]
        
        sys.stdout.write('\033[3A' if seconds != self.total_seconds else '')
        sys.stdout.write('\n'.join(display_lines) + '\033[0m\n')
        sys.stdout.flush()
    
    def get_user_input(self):
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8').strip().lower()
            if char == '\x00' or char == '\xe0':
                char = msvcrt.getch().decode('utf-8').strip().lower()
                return f"special_{char}"
            return char
        return None
    
    def change_theme(self):
        themes = list(self.themes.keys())
        current_index = themes.index(self.theme)
        new_index = (current_index + 1) % len(themes)
        self.theme = themes[new_index]
        
        theme = self.themes[self.theme]
        preview = theme['color'] + (theme['fill'] * 5 + theme['empty'] * 5) * 3 + '\033[0m'
        print(f"\nTheme changed to: {self.theme} {preview}")
        self.save_settings()
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            print("\nDark mode activated")
            sys.stdout.write('\033[40m')  
            sys.stdout.write('\033[37m')  
        else:
            print("\nLight mode activated")
            sys.stdout.write('\033[0m')   
        self.save_settings()
    
    def adjust_volume(self):
        self.alarm_volume = self.alarm_volume % 3 + 1
        vol_icons = ['🔈', '🔉', '🔊']
        print(f"\nAlarm volume set to: {self.alarm_volume} {vol_icons[self.alarm_volume-1]}")
        self.save_settings()
    
    def save_current_timer(self):
        if self.total_seconds > 0:
            timer_name = input("Enter a name for this timer: ").strip() or f"Timer {len(self.saved_timers)+1}"
            self.saved_timers.append({
                'name': timer_name,
                'duration': self.total_seconds,
                'alarm': self.alarm_sound,
                'volume': self.alarm_volume,
                'theme': self.theme
            })
            self.save_settings()
            print(f"\nSaved timer: {timer_name}")
        else:
            print("\nNo active timer to save")
    
    def show_help(self):
        help_text = """
        \n=== SUPER COUNTDOWN TIMER CONTROLS ===
        
        BASIC CONTROLS:
        p - Pause timer
        r - Resume timer
        + - Add 1 minute
        - - Subtract 1 minute
        s - Stop timer
        h - Show this help
        
        APPEARANCE:
        t - Change theme
        d - Toggle dark/light mode
        
        ALARM:
        a - Toggle alarm sound
        v - Adjust alarm volume
        
        TIMER MANAGEMENT:
        n - Save current timer to favorites
        l - Load saved timer
        
        SPECIAL:
        q - Quit to main menu
        """
        print(help_text)
    
    def countdown(self, seconds):
        self.reset_state()
        self.total_seconds = self.remaining_seconds = seconds
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=seconds)
        self.stopped = False
        
        print("\n" * 3)  
        print("Starting countdown... Press 'h' for help")
        
        while self.remaining_seconds > 0 and not self.stopped:
            if not self.paused:
                self.display_time(self.remaining_seconds)
                time.sleep(1)
                self.remaining_seconds -= 1
            
            user_input = self.get_user_input()
            if user_input:
                if user_input == 'p' and not self.paused:
                    self.paused = True
                    print("\nTimer paused. Press 'r' to resume")
                elif user_input == 'r' and self.paused:
                    self.paused = False
                    self.end_time = datetime.now() + timedelta(seconds=self.remaining_seconds)
                    print("\nTimer resumed...")
                elif user_input == 's':
                    self.stopped = True
                    print("\nTimer stopped by user")
                elif user_input == '+' and not self.paused:
                    self.remaining_seconds += 60
                    self.total_seconds += 60
                    self.end_time += timedelta(seconds=60)
                    print("\nAdded 1 minute")
                elif user_input == '-' and not self.paused:
                    if self.remaining_seconds > 60:
                        self.remaining_seconds -= 60
                        self.total_seconds -= 60
                        self.end_time -= timedelta(seconds=60)
                        print("\nSubtracted 1 minute")
                    else:
                        print("\nCannot subtract - time would be negative")
                elif user_input == 't':
                    self.change_theme()
                elif user_input == 'a':
                    self.alarm_sound = not self.alarm_sound
                    status = "ON" if self.alarm_sound else "OFF"
                    print(f"\nAlarm sound turned {status}")
                    self.save_settings()
                elif user_input == 'v':
                    self.adjust_volume()
                elif user_input == 'd':
                    self.toggle_dark_mode()
                elif user_input == 'n':
                    self.save_current_timer()
                elif user_input == 'h':
                    self.show_help()
                elif user_input == 'q':
                    self.stopped = True
                    print("\nReturning to main menu...")
                    return
        
        if not self.stopped:
            self.display_time(0)
            print("\n\nTime's up! 🔔🔔🔔")
            if self.alarm_sound:
                self.play_alarm()
        
        if not self.stopped:
            input("\nPress Enter to continue...")

def main():
    timer = SuperCountdownTimer()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n=== SUPER COUNTDOWN TIMER ===")
        print("1. Start New Countdown")
        print("2. Saved Timers")
        print("3. Settings")
        print("4. Help")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            try:
                duration = input("Enter duration (e.g., '5m', '2h30m', '90s'): ").lower()
                
                seconds = 0
                current_val = ''
                for char in duration:
                    if char.isdigit():
                        current_val += char
                    elif char in ['h', 'm', 's'] and current_val:
                        val = int(current_val)
                        if char == 'h':
                            seconds += val * 3600
                        elif char == 'm':
                            seconds += val * 60
                        elif char == 's':
                            seconds += val
                        current_val = ''
                
                if current_val and not any(u in duration for u in ['h', 'm', 's']):
                    seconds = int(current_val) * 60
                elif current_val:
                    print("Invalid duration format")
                    continue
                
                if seconds <= 0:
                    print("Please enter a positive duration")
                    continue
                
                timer.countdown(seconds)
            except ValueError:
                print("Please enter a valid duration")
                input("Press Enter to continue...")
        
        elif choice == '2':
            if not timer.saved_timers:
                print("\nNo saved timers yet!")
                input("Press Enter to continue...")
                continue
                
            print("\nSaved Timers:")
            for i, saved in enumerate(timer.saved_timers, 1):
                mins, secs = divmod(saved['duration'], 60)
                hours, mins = divmod(mins, 60)
                print(f"{i}. {saved['name']} - {hours:02d}:{mins:02d}:{secs:02d}")
            
            try:
                selection = input("\nSelect timer to load (number) or 'd' to delete: ").strip().lower()
                if selection == 'd':
                    to_delete = input("Enter number of timer to delete: ").strip()
                    idx = int(to_delete) - 1
                    if 0 <= idx < len(timer.saved_timers):
                        deleted = timer.saved_timers.pop(idx)
                        timer.save_settings()
                        print(f"Deleted timer: {deleted['name']}")
                    else:
                        print("Invalid selection")
                else:
                    idx = int(selection) - 1
                    if 0 <= idx < len(timer.saved_timers):
                        saved = timer.saved_timers[idx]
                        timer.theme = saved.get('theme', 'default')
                        timer.alarm_sound = saved.get('alarm', True)
                        timer.alarm_volume = saved.get('volume', 2)
                        timer.countdown(saved['duration'])
                    else:
                        print("Invalid selection")
            except (ValueError, IndexError):
                print("Invalid input")
            input("Press Enter to continue...")
        
        elif choice == '3':
            print("\n=== SETTINGS ===")
            print(f"1. Theme: {timer.theme}")
            print(f"2. Alarm Sound: {'ON' if timer.alarm_sound else 'OFF'}")
            print(f"3. Alarm Volume: {'🔈' * timer.alarm_volume}")
            print(f"4. Color Mode: {'Dark' if timer.dark_mode else 'Light'}")
            print("5. Back")
            
            setting = input("\nSelect setting to change (1-5): ").strip()
            if setting == '1':
                timer.change_theme()
            elif setting == '2':
                timer.alarm_sound = not timer.alarm_sound
                status = "ON" if timer.alarm_sound else "OFF"
                print(f"\nAlarm sound turned {status}")
                timer.save_settings()
            elif setting == '3':
                timer.adjust_volume()
            elif setting == '4':
                timer.toggle_dark_mode()
            elif setting == '5':
                continue
            else:
                print("Invalid selection")
            input("Press Enter to continue...")
        
        elif choice == '4':
            timer.show_help()
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            print("\nExiting Super Countdown Timer. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-5")
            time.sleep(1)

if __name__ == "__main__":
    main()