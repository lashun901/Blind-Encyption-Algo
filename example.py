from src.single_string_enc import SingleStringEC, Key

sse: SingleStringEC = SingleStringEC("Lovers & Friendssss") # Initialize encryption object.

key: Key = sse.GENERATE_KEY() # Generate a key from your encryption object.

print(f"Encrypted Value: {sse.perform_encryption(key)}") # Encrypt value with key.
print(f"True Value: {sse.perform_decryption(key)}") # Decrypt value with key.