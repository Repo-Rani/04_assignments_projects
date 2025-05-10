from PIL import Image, ImageFilter, ImageOps
import os
import copy

def show_menu():
    print("\n📷 CLI Photo Editor")
    print("==========================")
    print("1. Resize Image")
    print("2. Convert to Grayscale")
    print("3. Rotate Image")
    print("4. Apply Blur")
    print("5. Sharpen Image")
    print("6. Flip Image (Horizontal/Vertical)")
    print("7. Crop Image")
    print("8. Undo Last Operation")
    print("9. Show Image")
    print("10. Save As New File")
    print("11. Exit")

def load_image(path):
    try:
        image = Image.open(path)
        print("✅ Image loaded successfully!")
        return image
    except FileNotFoundError:
        print("❌ File not found. Please check the path.")
        return None

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❗ Please enter a valid number.")

def main():
    path = input("Enter the path to the image: ").strip()
    img = load_image(path)
    if img is None:
        return

    original = copy.deepcopy(img)
    history = [img.copy()] 
    while True:
        show_menu()
        choice = input("Choose an option (1-11): ").strip()

        if choice == '1':
            w = get_int_input("Enter new width: ")
            h = get_int_input("Enter new height: ")
            history.append(img.copy())
            img = img.resize((w, h))
            print("✅ Image resized.")

        elif choice == '2':
            history.append(img.copy())
            img = img.convert("L")
            print("✅ Converted to grayscale.")

        elif choice == '3':
            angle = get_int_input("Enter angle to rotate (in degrees): ")
            history.append(img.copy())
            img = img.rotate(angle, expand=True)
            print(f"✅ Rotated {angle} degrees.")

        elif choice == '4':
            history.append(img.copy())
            img = img.filter(ImageFilter.BLUR)
            print("✅ Blur applied.")

        elif choice == '5':
            history.append(img.copy())
            img = img.filter(ImageFilter.SHARPEN)
            print("✅ Sharpen applied.")

        elif choice == '6':
            direction = input("Flip (H)orizontal or (V)ertical? ").strip().lower()
            history.append(img.copy())
            if direction == 'h':
                img = ImageOps.mirror(img)
                print("✅ Flipped horizontally.")
            elif direction == 'v':
                img = ImageOps.flip(img)
                print("✅ Flipped vertically.")
            else:
                print("❌ Invalid input. Choose 'H' or 'V'.")

        elif choice == '7':
            print("Enter crop coordinates (left, upper, right, lower):")
            left = get_int_input("Left: ")
            upper = get_int_input("Upper: ")
            right = get_int_input("Right: ")
            lower = get_int_input("Lower: ")
            history.append(img.copy())
            try:
                img = img.crop((left, upper, right, lower))
                print("✅ Image cropped.")
            except Exception as e:
                print(f"❌ Error cropping image: {e}")

        elif choice == '8':
            if len(history) > 1:
                history.pop()
                img = history[-1].copy()
                print("↩️ Undo successful.")
            else:
                print("⚠️ No more steps to undo.")

        elif choice == '9':
            try:
                img.show()
                print("🖼️ Showing image in default viewer.")
            except Exception as e:
                print(f"❌ Error displaying image: {e}")

        elif choice == '10':
            new_name = input("Enter new file name (with extension like new_img.jpg): ").strip()
            try:
                img.save(new_name)
                print(f"✅ Image saved as {new_name}.")
            except Exception as e:
                print(f"❌ Error saving file: {e}")

        elif choice == '11':
            print("👋 Exiting... Thank you!")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()