def double_numbers(numbers):
    for i in range(len(numbers)):
        numbers[i] *= 2  
    return numbers

def main():
    numbers = [1, 2, 3, 4]
    
    # Call the function to double each number
    doubled_numbers = double_numbers(numbers)
    
    print("Doubled numbers:", doubled_numbers)

if __name__ == '__main__':
    main()
