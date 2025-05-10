import random
import time

def computer_guesses_number():
    print("🎯 Welcome to the Enhanced Computer Guess the Number Game! 🎯")
    print("----------------------------------------------------------")
    
    games_played = 0
    total_attempts = 0
    best_score = float('inf')
    
    while True:
        games_played += 1
        print("\nSelect Difficulty Level:")
        print("1. Easy (1-50, I get unlimited guesses)")
        print("2. Medium (1-100, max 10 guesses)")
        print("3. Hard (1-200, max 7 guesses)")
        print("4. Expert (1-500, max 5 guesses)")
        
        difficulty = input("Enter choice (1-4): ").strip()
        
        if difficulty == "1":
            low, high = 1, 50
            max_attempts = None
        elif difficulty == "2":
            low, high = 1, 100
            max_attempts = 10
        elif difficulty == "3":
            low, high = 1, 200
            max_attempts = 7
        elif difficulty == "4":
            low, high = 1, 500
            max_attempts = 5
        else:
            print("❌ Invalid choice. Please enter 1-4.")
            continue
        
        print(f"\nThink of a number between {low} and {high}...")
        time.sleep(2)
        print("Got it? Great! Let me try to guess it.")
        time.sleep(1)
        
        attempts = 0
        guessed = False
        previous_guesses = []
        
        while not guessed:
            if random.random() > 0.3 and len(previous_guesses) > 0:
                computer_guess = (low + high) // 2
            else:
                computer_guess = random.randint(low, high)
                
            attempts += 1
            previous_guesses.append(computer_guess)
            
            print(f"\n🔍 Attempt #{attempts}")
            if max_attempts:
                print(f"Guesses left: {max_attempts - attempts + 1}")
            print(f"My guess: {computer_guess}")
            
            while True:
                user_feedback = input("Is this (1) Too High, (2) Too Low, or (3) Correct? ").strip()
                if user_feedback in ("1", "2", "3"):
                    break
                print("❌ Please enter 1, 2, or 3")
            
            if user_feedback == "1":
                high = computer_guess - 1
                print("📉 Okay, I'll go lower next time!")
            elif user_feedback == "2":
                low = computer_guess + 1
                print("📈 Alright, I'll aim higher!")
            elif user_feedback == "3":
                guessed = True
                total_attempts += attempts
                if attempts < best_score:
                    best_score = attempts
                print(f"\n🎉 Got it! Your number was {computer_guess}!")
                print(f"I found it in {attempts} guesses!")
                
                if max_attempts:
                    efficiency = attempts / max_attempts
                    if efficiency < 0.5:
                        print("🌟 Genius-level guessing!")
                    elif efficiency < 0.8:
                        print("👍 Solid performance!")
                    else:
                        print("😅 That was close!")
                break
            
            if low > high:
                print("\n🤨 Wait a minute... This doesn't add up!")
                print("You must have given me wrong hints!")
                print(f"I guessed: {previous_guesses}")
                guessed = True  
                break
            
            if max_attempts and attempts >= max_attempts:
                print(f"\n💀 Out of guesses! I couldn't find your number in {max_attempts} tries.")
                print("Did I make a mistake or did you change your number?")
                break
            
            if attempts % 3 == 0 and not guessed:
                hint = input("Should I give you a hint about my thinking? (y/n): ").lower()
                if hint == 'y':
                    print(f"🤖 Current search range: {low} to {high}")
                    print(f"Possible numbers remaining: {high - low + 1}")
        
        print("\n📊 Game Statistics:")
        print(f"Games played: {games_played}")
        print(f"Total guesses: {total_attempts}")
        if games_played > 1:
            print(f"Average guesses per game: {total_attempts/games_played:.1f}")
        if best_score != float('inf'):
            print(f"Best score: {best_score} guesses")
        
        play_again = input("\nWant to play again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing! Here's my final performance:")
            print(f"▶ Total games: {games_played}")
            print(f"▶ Total guesses: {total_attempts}")
            if games_played > 0:
                print(f"▶ Average guesses: {total_attempts/games_played:.1f}")
            print("\nGoodbye! 👋")
            break

if __name__ == "__main__":
    computer_guesses_number()