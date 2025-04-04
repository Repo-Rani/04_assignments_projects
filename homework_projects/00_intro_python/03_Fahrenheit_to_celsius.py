
def main():
    temp_f = float(input("Enter temperature in Fahrenheit: " )) # Get temprature in  Fahrenheit
    temp_c = (temp_f - 32) * 5.0/9.0
    print(f"Temperature: {temp_f}F = {temp_c}C")  # Print result
if __name__ == '__main__':
 main()