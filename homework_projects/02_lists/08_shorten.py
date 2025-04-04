MAX_LENGTH: int = 3

def shorten(lst):
    while len(lst) > MAX_LENGTH:
        last_elem = lst.pop()
        print("Removed:", last_elem)  

def get_lst():
    """
    Prompts the user to enter one element at a time and returns the list.
    """
    lst = []
    elem = input("Please enter an element of the list or press enter to stop: ")
    while elem != "":
        lst.append(elem)
        elem = input("Please enter an element of the list or press enter to stop: ")
    return lst

def main():
    lst = get_lst()
    print("Original list:", lst)  
    shorten(lst)
    print("Final list:", lst)  

if __name__ == '__main__':
    main()
