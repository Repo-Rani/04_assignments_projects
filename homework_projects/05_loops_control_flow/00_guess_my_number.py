import random

def main():
    secret_number = random.randint(1, 99)

    print("I am thinking of a number between 1 and 99...")

    # Get user's guess
    guess = int(input("Enter a guess: "))

    # Keep looping until the correct guess
    while guess != secret_number:
        if guess < secret_number:
            print("Your guess is too low")
        else:
            print("Your guess is too high")

        print()  # Print an empty line for better readability
        guess = int(input("Enter a new guess: "))  # Get a new guess from the user

    print("Congrats! The number was:", secret_number)

if __name__ == '__main__':
    main()
