def subtract_seven(num):
    """
    This function subtracts 7 from the given number.
    """
    return num - 7

def main():
    num = int(input("Enter a number to subtract 7 from: "))
    
    result = subtract_seven(num)
    
    # Display the result
    print(f"The result of subtracting 7 from {num} is: {result}")

if __name__ == '__main__':
    main()
