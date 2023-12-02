def beaufort_cipher(plaintext, key):
    """Encrypts or decrypts plaintext using the Beaufort Cipher with the given key."""
    ciphertext = ""
    for i in range(len(plaintext)):
        # Convert the characters to uppercase and subtract 'A' to get a value between 0 and 25
        char_value = (ord(plaintext[i].upper()) - ord('A')) % 26
        key_value = (ord(key[i % len(key)].upper())-ord('A')) % 26
        # Apply the Beaufort Cipher algorithm to obtain the encrypted or decrypted character
        encrypted_char = chr(((key_value - char_value) % 26) + ord('A'))
        ciphertext += encrypted_char

    return ciphertext


def main():
    # Prompt the user for the message to be encrypted or decrypted
    plaintext = input("Enter the message to be encrypted or decrypted: ")
    # Prompt the user for the key to be used for encryption or decryption
    key = input("Enter the key to be used for encryption or decryption: ")
    # Validate the key to ensure it only contains letters
    while not key.isalpha():
        print("Key must only contain letters.")
        key = input("Enter the key to be used for encryption or decryption: ")

    # Prompt the user to choose whether to encrypt or decrypt the message
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ")

    # Encrypt or decrypt the message based on the user's choice
    if choice == 'e':
        ciphertext = beaufort_cipher(plaintext, key)
        print("Encrypted message:", ciphertext)
    elif choice == 'd':
        decryptedtext = beaufort_cipher(plaintext, key)
        print("Decrypted message:", decryptedtext)
    else:
        print("Invalid choice. Please enter 'e' or 'd'.")


if __name__ == '__main__':
    main()
