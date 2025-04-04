MINIMUM_HEIGHT : int = 50 # arbitrary units :)

def main():
    while True:  
        height = input("How tall are you? ")

        if height == "":  
            break
        
        height = float(height)  
        
        if height >= MINIMUM_HEIGHT:
            print("You're tall enough to ride!")
        else:
            print("You're not tall enough to ride, but maybe next year!")

if __name__ == '__main__':
    main()
