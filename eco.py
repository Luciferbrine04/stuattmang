def encode_number_from_file(file_path):
    encoded_numbers = []
    with open(file_path, 'r') as file:
        numbers = file.readlines()
        for number in numbers:
            number = number.strip()  # Remove newline characters
            encoded_numbers.append(encode_number(int(number)))
    return encoded_numbers

def encode_number(number):
    reversed_str = str(number)[::-1]
    encoded_str = ''.join(str(ord(digit)) for digit in reversed_str)
    return encoded_str

# Example usage
file_path = 'barcodedata.txt'
encoded_numbers = encode_number_from_file(file_path)
print("Encoded numbers:", encoded_numbers)