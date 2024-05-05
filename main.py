from generator.QRCodeGenerator import QRCodeGenerator
from detector.QRCodeDetector import QRCodeDetector
from utils.util import showImage

def main() -> None:
    '''
    An example on how to use the QRCodeGenerator and QRCodeDetector

    Parameters:
    None

    Returns:
    None
    '''
    # Declare a QRCodeGenerator object.
    generator = QRCodeGenerator(32)
    # Generate ten QR codes. The images will be saved to "images" folder.
    generator.generate(3, (123, 234, 96), (123, 123, 123))

    # Image path. Replace this path as you needed.
    image_path = "./images/qrcode1.png"
    # Declare a QRCodeDetector object
    detector = QRCodeDetector(image_path)

    # Detect the QR code.
    image = detector.markQRCode(line_color=(253, 51, 36))
    
    # Show the image
    showImage(image)
    
    return

if __name__ == "__main__":
    main()