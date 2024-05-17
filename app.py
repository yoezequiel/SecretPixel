from PIL import Image

END_OF_MESSAGE = "\f"


def encrypt():
    text_file = input(
        "Introduce el nombre del archivo de texto a encriptar (con extensión): "
    )
    image_file = input(
        "Introduce el nombre de la imagen donde quieres ocultar el texto (con extensión): "
    )
    output_image = input(
        "Introduce el nombre del archivo de imagen de salida (con extensión): "
    )

    with open(text_file, "r") as file:
        message = file.read() + END_OF_MESSAGE

    img = Image.open(image_file)
    width, height = img.size

    if len(message) * 8 > width * height:
        print("El mensaje es demasiado grande para ocultarlo en esta imagen.")
        return

    binary_message = "".join(format(ord(char), "08b") for char in message)

    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[index])
                    index += 1
            img.putpixel((x, y), tuple(pixel))

    img.save(output_image)
    print("¡Encriptación exitosa!")


def decrypt():
    image_file = input(
        "Introduce el nombre de la imagen a desencriptar (con extensión): "
    )
    output_text = input(
        "Introduce el nombre del archivo de texto de salida (con extensión): "
    )

    img = Image.open(image_file)
    width, height = img.size

    binary_message = ""
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    message = ""
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i : i + 8], 2))
        if char == END_OF_MESSAGE:
            break
        message += char

    with open(output_text, "w") as file:
        file.write(message)

    print("¡Desencriptación exitosa!")


def main():
    choice = input("¿Quieres encriptar (E) o desencriptar (D)? ").upper()
    if choice == "E":
        encrypt()
    elif choice == "D":
        decrypt()
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
