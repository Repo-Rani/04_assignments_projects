def read_phone_numbers():
    """
    Ask the user for names/numbers to store in a phonebook (dictionary).
    Returns the phonebook.
    """
    phonebook = {}  

    while True:
        name = input("Enter name (or press Enter to finish): ")
        if name == "":
            break
        number = input(f"Enter number for {name}: ")
        phonebook[name] = number

    return phonebook


def print_phonebook(phonebook):
    """
    Prints out all the names/numbers in the phonebook.
    """
    if phonebook:
        for name, number in phonebook.items():
            print(f"{name} -> {number}")
    else:
        print("Phonebook is empty.")


def lookup_numbers(phonebook):
    """
    Allow the user to look up phone numbers in the phonebook
    by looking up the number associated with a name.
    """
    while True:
        name = input("Enter name to lookup (or press Enter to exit): ")
        if name == "":
            print("Exiting lookup.")
            break
        if name not in phonebook:
            print(f"{name} is not in the phonebook.")
        else:
            print(f"{name}'s number is {phonebook[name]}.")


def main():
    phonebook = read_phone_numbers()
    print_phonebook(phonebook)
    lookup_numbers(phonebook)


# Python boilerplate.
if __name__ == '__main__':
    main()
