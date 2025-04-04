import random

DONE_LIKELIHOOD = 0.3  # 30% chance to stop counting

def done():
    """ Returns True with a probability of DONE_LIKELIHOOD """
    if random.random() < DONE_LIKELIHOOD:
        return True
    return False

def chaotic_counting():
    for i in range(1, 11):  # Change range to start at 1 and end at 10
        if done():
            return  # Ends the function execution, so we get back to main()
        print(i, end=" ")  # Print the current number with a space

def main():
    print("I'm going to count until 10 or until I feel like stopping, whichever comes first.")
    chaotic_counting()
    print("I'm done")

if __name__ == "__main__":
    main()
