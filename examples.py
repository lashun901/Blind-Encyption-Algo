from src.single_string_enc import SingleStringEC

# Recieving the string the user wants to encrypt.
unsafe_string:str = input("\nEnter a string to encrypt: ")

# Creating a Single String Encryption object.
ssec: object = SingleStringEC(unsafe_string=unsafe_string)

# Performs encryption on the unsafe string.
ssec.perform_encryption()

# Prints the new, encrypted string.
print(f"\n\nThe encypted string is:  {ssec.safe_str}")

# Decrypts unsafe string.
decrypted_str: str = ssec.perform_decryption()

# Prints the original, decrypted string.
print(f"\n\nThis is the decrypted string:  {decrypted_str}")