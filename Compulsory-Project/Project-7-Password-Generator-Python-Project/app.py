import random
import string
import pyperclip
import secrets
import os
from datetime import datetime
import json
import sys

CONFIG_FILE = "password_generator_config.json"
DEFAULT_CONFIG = {
    "default_length": 12,
    "default_special_chars": True,
    "default_avoid_ambiguous": True,
    "save_to_file": True,
    "auto_copy": True,
    "history_size": 50
}

def load_config():
    """Load or create configuration file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def generate_password(length=12, use_special_chars=True, avoid_ambiguous=False, exclude_chars=""):
    """
    Generate a secure password using cryptographically strong random generator
    """
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    ambiguous_chars = "lI10Oo|{}[]()\/'\"`~,;:.<>"

    characters = letters + digits
    if use_special_chars:
        characters += special_chars
    if avoid_ambiguous:
        characters = ''.join(c for c in characters if c not in ambiguous_chars)
    if exclude_chars:
        characters = ''.join(c for c in characters if c not in exclude_chars)

    # Ensure we have at least one character from each selected category
    password = []
    if letters:
        password.append(secrets.choice(letters))
    if digits:
        password.append(secrets.choice(digits))
    if use_special_chars and special_chars:
        password.append(secrets.choice(special_chars))

    # Fill the rest of the password
    remaining_length = length - len(password)
    password.extend(secrets.choice(characters) for _ in range(remaining_length))

    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    return ''.join(password)

def save_password_to_file(password, filename="passwords.txt"):
    """Save password to file with timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as file:
            file.write(f"{timestamp}: {password}\n")
        return True
    except:
        return False

def get_user_choice(prompt, default=None, yes_no=False):
    """Helper function to get user input with default values"""
    while True:
        user_input = input(prompt).strip().lower()
        
        if not user_input and default is not None:
            return default
        
        if yes_no:
            if user_input in ('y', 'yes'):
                return True
            elif user_input in ('n', 'no'):
                return False
            else:
                print("Please enter 'yes' or 'no'")
        else:
            return user_input

def display_password_strength(password):
    """Display a simple strength indicator for the password"""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if has_upper and has_lower: score += 1
    if has_digit: score += 1
    if has_special: score += 1
    
    strength = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong", "Excellent"]
    return strength[min(score, len(strength)-1)]

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_passwords(config):
    """Generate passwords based on user preferences"""
    clear_screen()
    print("🔐 Password Generation 🔐\n")
    
    # Password length selection
    print("Choose Password Length:")
    print("1. Short (8 characters)")
    print("2. Medium (12 characters)")
    print("3. Long (16 characters)")
    print("4. Custom length")
    
    length_choice = get_user_choice("Enter choice (1-4): ", "2")
    
    if length_choice == "1":
        length = 8
    elif length_choice == "2":
        length = config.get("default_length", 12)
    elif length_choice == "3":
        length = 16
    else:
        while True:
            custom_length = input("Enter custom length (8-64): ").strip()
            if custom_length.isdigit() and 8 <= int(custom_length) <= 64:
                length = int(custom_length)
                break
            print("Please enter a number between 8 and 64")
    
    # Other options
    use_special_chars = get_user_choice(
        f"Include special characters? (yes/no) [default: {'yes' if config['default_special_chars'] else 'no'}]: ",
        "yes" if config["default_special_chars"] else "no",
        yes_no=True
    )
    
    avoid_ambiguous = get_user_choice(
        f"Avoid ambiguous characters? (yes/no) [default: {'yes' if config['default_avoid_ambiguous'] else 'no'}]: ",
        "yes" if config["default_avoid_ambiguous"] else "no",
        yes_no=True
    )
    
    exclude_chars = input("Enter any characters to exclude (leave empty for none): ").strip()
    
    num_passwords = 1
    if get_user_choice("Generate multiple passwords? (yes/no): ", "no", yes_no=True):
        while True:
            num_input = input("How many passwords to generate? (2-20): ").strip()
            if num_input.isdigit() and 2 <= int(num_input) <= 20:
                num_passwords = int(num_input)
                break
            print("Please enter a number between 2 and 20")
    
    # Generate and display passwords
    print("\nGenerated Passwords:")
    print("=" * 50)
    
    passwords = []
    for _ in range(num_passwords):
        password = generate_password(
            length=length,
            use_special_chars=use_special_chars,
            avoid_ambiguous=avoid_ambiguous,
            exclude_chars=exclude_chars
        )
        strength = display_password_strength(password)
        print(f"{password} \t[Strength: {strength}]")
        passwords.append(password)
    
    print("=" * 50)
    
    # Post-generation options
    if config["auto_copy"] and num_passwords == 1:
        pyperclip.copy(passwords[0])
        print("\n✅ Password copied to clipboard!")
    
    if config["save_to_file"]:
        if save_password_to_file("\n".join(passwords)):
            print("✅ Passwords saved to file")
        else:
            print("❌ Could not save passwords to file")
    
    if num_passwords > 1:
        print("\nOptions:")
        print("1. Copy all passwords to clipboard")
        print("2. Save all passwords to file")
        print("3. Continue")
        
        option = get_user_choice("\nEnter option (1-3): ", "3")
        if option == "1":
            pyperclip.copy("\n".join(passwords))
            print("✅ All passwords copied to clipboard!")
        elif option == "2":
            if save_password_to_file("\n".join(passwords)):
                print("✅ Passwords saved to file")
            else:
                print("❌ Could not save passwords to file")
    
    input("\nPress Enter to continue...")

def configure_settings(config):
    """Configure application settings"""
    while True:
        clear_screen()
        print("⚙️ Settings ⚙️\n")
        
        print(f"1. Default password length: {config['default_length']}")
        print(f"2. Include special chars by default: {'yes' if config['default_special_chars'] else 'no'}")
        print(f"3. Avoid ambiguous chars by default: {'yes' if config['default_avoid_ambiguous'] else 'no'}")
        print(f"4. Auto-save to file: {'yes' if config['save_to_file'] else 'no'}")
        print(f"5. Auto-copy single password: {'yes' if config['auto_copy'] else 'no'}")
        print(f"6. Password history size: {config['history_size']}")
        print("7. Back to main menu")
        
        choice = get_user_choice("\nEnter setting to change (1-7): ")
        
        if choice == "1":
            while True:
                new_length = input("Enter new default length (8-64): ").strip()
                if new_length.isdigit() and 8 <= int(new_length) <= 64:
                    config['default_length'] = int(new_length)
                    break
                print("Please enter a number between 8 and 64")
        elif choice == "2":
            config['default_special_chars'] = not config['default_special_chars']
        elif choice == "3":
            config['default_avoid_ambiguous'] = not config['default_avoid_ambiguous']
        elif choice == "4":
            config['save_to_file'] = not config['save_to_file']
        elif choice == "5":
            config['auto_copy'] = not config['auto_copy']
        elif choice == "6":
            while True:
                new_size = input("Enter history size (10-1000): ").strip()
                if new_size.isdigit() and 10 <= int(new_size) <= 1000:
                    config['history_size'] = int(new_size)
                    break
                print("Please enter a number between 10 and 1000")
        elif choice == "7":
            save_config(config)
            return

def main():
    config = load_config()
    
    while True:
        clear_screen()
        print("🔐 Advanced Password Generator 🔐\n")
        print("1. Generate Password")
        print("2. Settings")
        print("3. Exit")
        
        choice = get_user_choice("\nEnter your choice (1-3): ", "1")
        
        if choice == "1":
            generate_passwords(config)
        elif choice == "2":
            configure_settings(config)
        elif choice == "3":
            save_config(config)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)