import random  # Import the random library to simulate dice rolls

NUM_SIDES = 6

def roll_dice():
    """Simulates rolling two dice and prints their results and total"""
    die1 = random.randint(1, NUM_SIDES)  # Roll the first die
    die2 = random.randint(1, NUM_SIDES)  # Roll the second die
    
    total = die1 + die2  # Calculate the total of both dice
    print(f"Rolled: Die 1 = {die1}, Die 2 = {die2}, Total = {total}")  # Print the result

def main():
    roll_dice()  

if __name__ == '__main__':
    main()
