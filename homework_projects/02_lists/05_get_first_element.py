def get_first_element(lst):
    if lst:  
        print(lst[0])

def get_lst():
    lst = []
    while True:
        elem = input("Enter an element (or press Enter to stop): ").strip()
        if not elem:
            break
        lst.append(elem)
    return lst

def main():
    lst = get_lst()
    get_first_element(lst)

if __name__ == "__main__":
    main()
