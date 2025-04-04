def get_user_numbers():
    user_numbers = []
    while True:
        user_input = input("Enter a number: ")
        
        if user_input == "":  # Stop when the user presses Enter without input
            break
        
        num = int(user_input)  # Convert input to an integer
        user_numbers.append(num)
    
    return user_numbers

def main():
    user_numbers = get_user_numbers()

    # Use a dictionary to count the occurrences of each number
    num_dict = {}
    for num in user_numbers:
        if num in num_dict:
            num_dict[num] += 1  # If the number is already in the dictionary, increment the count
        else:
            num_dict[num] = 1  # Otherwise, add the number to the dictionary with count 1

    # Print the counts for each number
    for num, count in num_dict.items():
        print(f"{num} appears {count} times.")

if __name__ == '__main__':
    main()
