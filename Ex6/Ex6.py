def string_to_binary(s):
    """Convert a string to binary representation."""
    return ''.join(format(ord(i), '08b') for i in s)

def hamming_encode(data):
    """Encode binary data using Hamming(7, 4) code."""
    data = [int(bit) for bit in data]
    encoded = []
    data_len = len(data)
   
    # Number of parity bits needed
    parity_bits = 0
    while (2 ** parity_bits) < (data_len + parity_bits + 1):
        parity_bits += 1

    # Initialize the encoded data with 0s
    encoded_len = data_len + parity_bits
    encoded = [0] * encoded_len
    data_index = 0

    # Place data bits in their correct positions
    for i in range(1, encoded_len + 1):
        if (i & (i - 1)) == 0:  # Position is a power of 2 (parity bit position)
            continue
        encoded[i - 1] = data[data_index]
        data_index += 1

    # Calculate and insert parity bits
    for i in range(parity_bits):
        parity_position = (2 ** i) - 1
        parity = 0
        for j in range(parity_position, encoded_len, 2 * (parity_position + 1)):
            for k in range(j, min(j + parity_position + 1, encoded_len)):
                parity ^= encoded[k]
        encoded[parity_position] = parity

    return ''.join(map(str, encoded))

def hamming_decode(encoded):
    """Decode and correct binary data using Hamming(7, 4) code."""
    encoded = [int(bit) for bit in encoded]
    parity_bits = 0
    while (2 ** parity_bits) < len(encoded):
        parity_bits += 1

    # Calculate error position
    error_position = 0
    for i in range(parity_bits):
        parity_position = (2 ** i) - 1
        parity = 0
        for j in range(parity_position, len(encoded), 2 * (parity_position + 1)):
            for k in range(j, min(j + parity_position + 1, len(encoded))):
                parity ^= encoded[k]
        if parity != 0:
            error_position += (2 ** i)

    if error_position:
        print(f"Error detected at position: {error_position}")
        encoded[error_position - 1] ^= 1  # Correct the error

    # Extract original data bits
    decoded = []
    for i in range(len(encoded)):
        if (i & (i - 1)) != 0:  # Skip parity bits
            decoded.append(encoded[i])

    return ''.join(map(str, decoded))

def main():
    input_string = input("Enter a string: ")
    binary_data = string_to_binary(input_string)
    print(f"Original binary data: {binary_data}")

    encoded_data = hamming_encode(binary_data)
    print(f"Encoded data: {encoded_data}")

    error_bit_position = int(input("Enter the position to introduce an error: "))
    encoded_list = list(encoded_data)
    if 1 <= error_bit_position <= len(encoded_list):
        encoded_list[error_bit_position - 1] = '1' if encoded_list[error_bit_position - 1] == '0' else '0'
        erroneous_encoded_data = ''.join(encoded_list)
        print(f"Data with introduced error: {erroneous_encoded_data}")
       
        corrected_data = hamming_decode(erroneous_encoded_data)
        print(f"Corrected data: {corrected_data}")
    else:
        print("Invalid position. Error bit position must be within the range of encoded data length.")
    print("Decoded String:", input_string)

if __name__ == "__main__":
    main()
