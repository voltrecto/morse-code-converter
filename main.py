from flask import Flask, render_template, request
import re
from morse_dictionary import alphabet, morse

app = Flask(__name__)


def converter(input_text):
    """Converts input string into morse code."""
    output_morse = ""
    for char in input_text:
        if char in alphabet:
            output_morse += f"{alphabet[char]} "
        elif " " in char:
            output_morse += "/ "
        else:
            output_morse += "# "
    return output_morse


def decoder(input_morse):
    """Splits input morse code, decodes and returns text."""
    split_string = input_morse.split(" ")  # Create list based on sets of code, remove spaces.
    input_list = []
    for item in split_string:
        if "/" in item:  # If string has "/", split into list.
            start = 0
            for match in re.finditer(r"/", item):
                input_list.append(item[start:match.start()])
                input_list.append("/")
                start = match.end()
            input_list.append(item[start:])
        else:
            input_list.append(item)
    input_list = [item for item in input_list if item]  # Remove null items
    output_text = ""
    for char in input_list:
        if char in morse:
            output_text += morse[char]
        elif char == "/":
            output_text += " "
        else:
            output_text += "#"
    return output_text


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.form
        if data["choice"] == "convert":
            input_text = data["input_text"]
            converted_text = converter(input_text.lower())
        else:
            input_text = data["input_text"]
            converted_text = decoder(input_text)
        return render_template("index.html", choice=data["choice"], input_text=input_text,
                               converted_text=converted_text)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
