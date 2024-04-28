def decode_numbers_from_file(file_path):
    decoded_numbers = []
    with open(file_path, 'r') as file:
        encoded_numbers = file.readlines()
        for encoded_number in encoded_numbers:
            encoded_number = encoded_number.strip()  # Remove newline characters
            decoded_numbers.append(decode_number(encoded_number))
    return decoded_numbers

def decode_number(encoded_str):
    digits = [encoded_str[i:i+2] for i in range(0, len(encoded_str), 2)]
    reversed_str = ''.join(chr(int(digit)) for digit in digits)
    number = int(''.join(filter(str.isdigit, reversed_str))[::-1])
    return number

# Example usage
file_path = 'enbarcodedata.txt'
decoded_numbers = decode_numbers_from_file(file_path)

# Write decoded numbers to a new file
with open('debarcodedata.txt', 'w') as file:
    for number in decoded_numbers:
        file.write(str(number) + '\n')
