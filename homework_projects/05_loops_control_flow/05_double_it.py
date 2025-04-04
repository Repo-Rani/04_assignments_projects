def main():
    # Ask the user to enter a number
    curr_value = int(input("Enter a number: "))
    
    # Repeat doubling the number until it reaches 100 or greater
    while curr_value < 100:
        curr_value *= 2  # Double the current value
        print(curr_value)  # Print the current doubled value

# Call the main function to run the program
if __name__ == "__main__":
    main()
