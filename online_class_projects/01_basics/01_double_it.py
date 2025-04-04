def main():
    # Step 1: Prompt the user to enter a number
    user_input = input("Enter a number: ")
    
    # Step 2: Convert the input to a float and initialize curr_value
    curr_value = float(user_input)
    
    # Step 3: Use a while loop to double the value until it reaches or exceeds 100
    while curr_value < 100:
        curr_value *= 2
        print(curr_value)

if __name__ == "__main__":
    main()
