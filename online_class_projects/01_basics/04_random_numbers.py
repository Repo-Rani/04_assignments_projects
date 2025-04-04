import random

# Constants
N_NUMBERS = 10
MIN_VALUE = 1
MAX_VALUE = 100

def main():
    # Generate N_NUMBERS unique random numbers
    unique_numbers = random.sample(range(MIN_VALUE, MAX_VALUE + 1), N_NUMBERS)
    print(*unique_numbers)

if __name__ == '__main__':
    main()
