def print_multiple(message, repeats):
    # Loop to print the message the specified number of times
    for _ in range(repeats):
        print(message)

def main():
    # Asking the user for input
    message = input("Please type a message: ")
    repeats = int(input("Enter a number of times to repeat your message: "))
    
    print_multiple(message, repeats)

if __name__ == "__main__":
    main()
