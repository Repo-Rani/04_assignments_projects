def main():
    for i in range(10, 20):  # 10 se 19 tak loop chalega
        if is_odd(i):
            print(f"{i} odd")
        else:
            print(f"{i} even")

def is_odd(value: int):
    """
    Checks to see if a value is odd. If it is, returns True.
    """
    return value % 2 == 1  # Agar remainder 1 hai to odd hai, warna even

# There is no need to edit code beyond this point
if __name__ == '__main__':
    main()
