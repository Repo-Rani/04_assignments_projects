import random  

# Number of sides on each die
NUM_SIDES = 6  

def roll_dice():
    """Simulates rolling two dice and prints their total"""
    die1 = random.randint(1, NUM_SIDES)  # Generates a number between 1 and 6
    die2 = random.randint(1, NUM_SIDES)  # Generates a number between 1 and 6
    total = die1 + die2
    print(f"Total of two dice: {total}")  # Matches original output

def main():
    die1 = 10  # Local variable in main() to demonstrate scope
    print(f"die1 in main() starts as: {die1}")

    roll_dice()
    roll_dice()
    roll_dice()

    print(f"die1 in main() is: {die1}")  # Matches original output

if __name__ == '__main__':
    main()
