import qrcode
import os

def generate_qr(data, filename="qrcode.png", version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_L):
    try:
        qr = qrcode.QRCode(
            version=version, 
            error_correction=error_correction,  
            box_size=box_size,  
            border=border  
        )

        qr.add_data(data) 
        qr.make(fit=True) 

        img = qr.make_image(fill="black", back_color="white")
        
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        img.save(filename)
        print(f"\n✅ QR code generated successfully and saved as '{filename}'!\n")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")

def main():
    print("\n📌 QR Code Generator")
    print("=====================")
    
    data = input("\nEnter the text or URL to encode in the QR code: ").strip()
    
    if not data:
        print("❌ Error: Data cannot be empty. Please provide a valid text or URL.")
        return

    filename = input("Enter the filename to save (default: qrcode.png): ").strip()
    if not filename:
        filename = "qrcode.png" 
    try:
        version = int(input("\nEnter the QR code version (1-40, default: 1): ").strip() or 1)
        if not (1 <= version <= 40):
            raise ValueError("Version must be between 1 and 40.")
        
        box_size = int(input("Enter the box size (default: 10): ").strip() or 10)
        border = int(input("Enter the border size (default: 4): ").strip() or 4)
        
        error_correction_level = input("Enter error correction level (L, M, Q, H, default: L): ").strip().upper()
        error_correction_dict = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_dict.get(error_correction_level, qrcode.constants.ERROR_CORRECT_L)

    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    generate_qr(data, filename, version, box_size, border, error_correction)

if __name__ == "__main__":
    main()