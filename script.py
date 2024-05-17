from flask import Flask, render_template, request, send_file, after_this_request
from PIL import Image
import io
import os
import uuid

app = Flask(__name__)

END_OF_MESSAGE = "\n"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "encrypt":
            return render_template("encrypt.html")
        elif action == "decrypt":
            return render_template("decrypt.html")
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    text_file = request.files["text_file"]
    image_file = request.files["image_file"]

    message = text_file.read().decode("utf-8") + END_OF_MESSAGE

    img = Image.open(io.BytesIO(image_file.read()))
    width, height = img.size

    if len(message) * 8 > width * height:
        return "El mensaje es demasiado grande para ocultarlo en esta imagen."

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

    temp_filename = str(uuid.uuid4()) + ".png"
    img.save(temp_filename)

    @after_this_request
    def remove_temp(response):
        try:
            os.remove(temp_filename)
        except:
            pass
        return response

    return send_file(
        temp_filename,
        mimetype="image/png",
        as_attachment=True,
        download_name="encrypted_image.png",
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():
    image_file = request.files["image_file"]

    img = Image.open(io.BytesIO(image_file.read()))
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

    return message


if __name__ == "__main__":
    app.run(debug=True)
