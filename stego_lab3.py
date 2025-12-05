from PIL import Image

END_MARKER = "<END>"
DEFAULT_MESSAGE = "Your Name, 01.01.2000"  # change to your real data


def text_to_bits(text: str) -> list[int]:
    data = text.encode("utf-8")
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits


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


def hide_message(input_image_path: str, output_image_path: str, message: str) -> None:
    img = Image.open(input_image_path)
    img = img.convert("RGB")
    pixels = img.load()

    full_message = message + END_MARKER
    bits = text_to_bits(full_message)

    width, height = img.size
    capacity = width * height  # using one channel (blue)

    if len(bits) > capacity:
        raise ValueError(
            f"Message too long. Bits: {len(bits)}, capacity: {capacity}"
        )

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bits):
                break

            r, g, b = pixels[x, y]
            new_b = (b & 0b11111110) | bits[bit_index]
            pixels[x, y] = (r, g, new_b)

            bit_index += 1
        if bit_index >= len(bits):
            break

    img.save(output_image_path)
    print(f"[+] Message hidden in {output_image_path}")


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

    if end_index == -1:
        print("[!] END marker not found.")
        return text

    return text[:end_index]


def main():
    print("=== Lab 3: LSB Steganography ===")
    print("1) Hide message")
    print("2) Extract message")
    choice = input("Choose option (1/2): ").strip()

    if choice == "1":
        input_img = input("Path to original image (e.g. input.png): ").strip()
        output_img = input("Path to stego image (e.g. output.png): ").strip()
        msg = input("Message to hide (leave empty to use default): ").strip()
        if not msg:
            msg = DEFAULT_MESSAGE
        hide_message(input_img, output_img, msg)

    elif choice == "2":
        stego_img = input("Path to stego image: ").strip()
        message = extract_message(stego_img)
        print("\n[+] Extracted message:")
        print(message)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
