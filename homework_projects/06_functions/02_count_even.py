def count_even(lst):
    """
    Returns the number of even numbers in the list.
    """
    count = 0  # Even numbers ka count store karega
    for num in lst:  # Har number ko check karega
        if num % 2 == 0:  # Agar number even hai
            count += 1  # Count badha do
    print(count)  # Even numbers ka count print karo

def get_list_of_ints():
    """
    User se integers input lene ka function.
    """
    lst = []  # Empty list banayi jisme numbers store honge
    while True:
        user_input = input("Enter an integer or press enter to stop: ")  
        if user_input == "":  # Agar user ne enter press kiya bina koi number diye
            break  # Loop se bahar nikal jao
        lst.append(int(user_input))  # Number ko list me add karo
    return lst  # List return karo

def main():
    lst = get_list_of_ints()  # User se numbers le kar list banaye
    count_even(lst)  # Even numbers count kare aur print kare

# Program yahan se execute hoga
if __name__ == "__main__":
    main()
