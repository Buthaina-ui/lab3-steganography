Lab 3 – LSB Steganography
Hiding and extracting text inside images using Least Significant Bit (LSB) technique.
1.Overview:
This project demonstrates how to hide secret text messages inside an image and later extract them using LSB Steganography.
The method modifies only the least significant bit of pixel values, making the hidden data invisible to the human eye.
2.Features:
✔ Hide a message inside an image
✔ Extract a hidden message from a stego-image
✔ Simple command-line interface
✔ Uses only the blue channel to embed data
✔ Supports custom or default messages
3. Practical Part:
Step 1 — Hiding the Message
Input image: input.jpg
Output image: output.png
Message used: Your Name, 01.01.2000
Command Line Output:
=== Lab 3: LSB Steganography ===
1) Hide message
2) Extract message
Choose option (1/2): 1
Path to original image (e.g. input.png): input.jpg
Path to stego image (e.g. output.png): output.png
Message to hide (leave empty to use default):
[+] Message hidden in output.png
Step 2 — Extracting the Hidden Message
Command Line Output:
=== Lab 3: LSB Steganography ===
1) Hide message
2) Extract message
Choose option (1/2): 2
Path to stego image: output.png
[+] Extracted message:
Your Name, 01.01.2000
4. Technical Specification
LSB Method Summary
Converts text to binary (8 bits per character)
Inserts each bit inside the Least Significant Bit of the blue pixel channel
Adds an <END> marker to indicate end of message
Extract function reads LSB bits until it finds <END>
Libraries Used
from PIL import Image
5. Program Code
The full code is stored in: stego_lab3.py
Key functions:
Convert text to bits
def text_to_bits(text: str) -> list[int]:
    data = text.encode("utf-8")
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits
Convert bits back to text
def bits_to_text(bits: list[int]) -> str:
    if len(bits) % 8 != 0:
        bits = bits[: len(bits) - (len(bits) % 8)]
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i : i + 8]:
            byte = (byte << 1) | b
        bytes_out.append(byte)
    return bytes_out.decode("utf-8", errors="ignore")
Hide message in image
def hide_message(input_image_path: str, output_image_path: str, message: str) -> None:
    img = Image.open(input_image_path)
    img = img.convert("RGB")
    pixels = img.load()

    full_message = message + END_MARKER
    bits = text_to_bits(full_message)

    width, height = img.size
    capacity = width * height

    if len(bits) > capacity:
        raise ValueError(f"Message too long.")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            new_b = (b & 0b11111110) | bits[bit_index]
            pixels[x, y] = (r, g, new_b)

            bit_index += 1
            if bit_index >= len(bits):
                break
        if bit_index >= len(bits):
            break

    img.save(output_image_path)
Extract message from image
def extract_message(stego_image_path: str) -> str:
    img = Image.open(stego_image_path)
    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size
    bits = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits.append(b & 1)

    text = bits_to_text(bits)
    end_index = text.find(END_MARKER)
    return text[:end_index] if end_index != -1 else "END marker not found."
6. How to Run the Program
Hide a Message
python stego_lab3.py
Choose option: 1
Extract a Message
python stego_lab3.py
Choose option: 2
7. Files in Repository
File	                    Description
stego_lab3.py        	Main program source code
input.jpg	         Original image used for hiding
output.png	       Stego-image containing hidden data
Lab3_Steganography_Report.pdf	   Full assignment report
README.md                 	Documentation
 8. GitHub Repository Link
https://github.com/Buthaina-ui/lab3-steganography%C2%AE
