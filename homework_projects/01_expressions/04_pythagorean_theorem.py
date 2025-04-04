import math  # Import the math module to use sqrt()

def main():
    AB = float(input("Enter the length of AB: "))  # Length of one side
    AC = float(input("Enter the length of AC: "))  # Length of the other side
    
    # Calculate the length of the hypotenuse using the Pythagorean theorem
    BC = math.sqrt(AB**2 + AC**2)  # Applying the theorem to find BC
    
    print(f"The length of BC (the hypotenuse) is: {BC}")

if __name__ == '__main__':
    main()
