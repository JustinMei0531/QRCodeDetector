from generator.QRCodeGenerator import QRCodeGenerator

def main():
    generator = QRCodeGenerator(32)
    generator.generate(10, (123, 234, 96), (123, 123, 123))



if __name__ == "__main__":
    main()