from libs import (random as rnd,
                  re as regex,
                  printable as printable_characters,
                  key_values)

class SingleStringEC:
    def __init__(self, unsafe_string: str, complexity: int = 1) -> None:
        self.complexity: int = complexity + 2
        self.unsafe_string: str = unsafe_string
        self.safe_str: str = None
        self.key_memory: dict = {0: "Null"}
        self.key_progression_number: int = 1
        self.key: dict = self.generate_key()
        self.reverse_key: dict = {v: k for k, v in self.key.items()}
        self.key_memory: None = None
    
    # This will generate the encryption for a value. Includes checking for no duplicates.
    def generate_key_value(self) -> str:
        # This nested function generates the encyption for a single character.
        def change_key_value():
            new_key_value: list = []
            for i in range(self.complexity):
                new_key_value.append(rnd.choice(key_values))
            new_key_value: str = "".join(new_key_value)
            return new_key_value
        
        key_value: str = change_key_value()
        
        okay_key_value: bool = False
        while okay_key_value == False:
            for i, key in enumerate(self.key_memory):
                if key == key_value: key_value: str = change_key_value()
                else: 
                    okay_key_value = True
        self.key_memory[self.key_progression_number] = key_value
        self.key_progression_number += 1
        return key_value

    # This will generate the entire key for one messsage.
    def generate_key(self) -> dict:
        key = {" ": self.generate_key_value()}
        for char in printable_characters:
            try:
                key[char]
            except KeyError:
                key[char] = self.generate_key_value()
        return key

    # Will do exactly what the function is named.
    def perform_encryption(self) -> str:
        safe_str_list: list = []
        for char in self.unsafe_string:
            safe_str_list.append(self.key[char])
        self.safe_str: str = "".join(safe_str_list)
    
    # Will do exactly what the function is named.
    def perform_decryption(self) -> str:
        def split_string(safe_string, chunk_size) -> list:
            listed_safe_str: list = []
            for i in range(0, len(safe_string), chunk_size):
                listed_safe_str.append(safe_string[i:i+chunk_size])
            return listed_safe_str
        listed_safe_str = split_string(self.safe_str, self.complexity)

        decrypted_str: list = []
        for encrypted_piece in listed_safe_str:
            for i, key_piece in enumerate(self.reverse_key):
                if encrypted_piece == key_piece: 
                    decrypted_str.append(self.reverse_key[key_piece])
        decrypted_str: str = "".join(decrypted_str)
        return decrypted_str

