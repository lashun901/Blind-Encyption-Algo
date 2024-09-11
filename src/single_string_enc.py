from random import choice as rnd_choice
from string import (printable as printable_characters,
                    ascii_letters,
                    punctuation)
from src.key_generator import KeyGenerator, Key
encryption_profile_characters = ascii_letters + punctuation

class SingleStringEC:
    def __init__(self, unsafe_string: str, complexity: int = 1) -> None:
        self.complexity_length: int = complexity + 2 # Mainly determines the length of a character's encryption profile.
        self.unencrypted_string: str = unsafe_string # Stores the string
        self.encrypted_string: str = None
        self.enc_prof_memory: dict = {0: "Null"} # Memorizes the used encryption profiles in order to ensure no duplicates are created.
        self._enc_prof_progression_number: int = 1 # Used as a the "key" for the self.enc_prof_memory dictionary. Will (should/might) make generating encryptions for larger messages faster.
        self.enc_prof_key: dict = self._generate_enc_prof_key()
        self.enc_prof_reverse_key: dict = {v: k for k, v in self.enc_prof_key.items()} # A reversed version of the key is needed in order to reverse engineer encryptions.
        self.enc_prof_memory: None = None
        self._enc_prof_progression_number: None = None
        
        self.key_created: bool = False
        self.expected_key: int = 0
    
    def GENERATE_KEY(self, seed: int = None):
        if self.key_created:
            return "Key already generated."
        else:
            self.key_created: bool = True
            if seed:
                key_gen: KeyGenerator = KeyGenerator(seed=seed)
                new_key: Key = key_gen.get_key()
                self.expected_key: int = new_key.get_value()
                return new_key
            else:
                key_gen: KeyGenerator = KeyGenerator()
                new_key: Key = key_gen.get_key()
                self.expected_key: int = new_key.get_value()
                return new_key
    
    def _check_key(self, key_obj: Key):
        if key_obj.value != self.expected_key:
            print("INVALID KEY!")
            return False
        else:
            return True

    def _split_string(self, encrypted_string, complexity_length) -> list:
        broken_encrypted_string: list = []
        for i in range(0, len(encrypted_string), complexity_length):
            broken_encrypted_string.append(encrypted_string[i:i+complexity_length])
        return broken_encrypted_string
    
    # Randomly changes the encryption profile of a character.
    def _change_encryption_profile(self):
        new_encryption_profile: list = []
        for i in range(self.complexity_length): # (Complexity influencing the length of encryption profile.)
            new_encryption_profile.append(rnd_choice(encryption_profile_characters)) # (Randomly creating encryption profiles.)
        new_encryption_profile: str = "".join(new_encryption_profile)
        return new_encryption_profile
        
    # Checks for & handles any duplicate encryption profiles.
    def _check_encryption_profile(self, enc_prof: str) -> None:
        okay_encryption_profile: bool = False
        while okay_encryption_profile == False:
            for i, encryption_profile in enumerate(self.enc_prof_memory):
                if encryption_profile == enc_prof: enc_prof: str = self._change_encryption_profile() # If theres a duplicate encryption profile, generate another one instead.
                else: 
                    okay_encryption_profile = True

    # This will generate the encryption profile for an unsafe character from the unsafe string. Includes checking for no duplicate profiles.
    def _generate_encryption_profile(self) -> str:
        encryption_profile: str = self._change_encryption_profile()
        self._check_encryption_profile(enc_prof=encryption_profile) # Checks for duplicate encryption profiles
        
        self.enc_prof_memory[self._enc_prof_progression_number] = encryption_profile
        self._enc_prof_progression_number += 1
        return encryption_profile

    # This will generate a new encryption profile key. This holds logic for what the encrypted equivalent of each printable character.
    def _generate_enc_prof_key(self) -> dict:
        key = {" ": (self._generate_encryption_profile(), # Six total possible profiles.
                     self._generate_encryption_profile(),
                     self._generate_encryption_profile(),
                     self._generate_encryption_profile(),
                     self._generate_encryption_profile(),
                     self._generate_encryption_profile())}
        for char in printable_characters:
            try:
                key[char]
            except KeyError:
                key[char] = (self._generate_encryption_profile(), # Six total possible profiles.
                             self._generate_encryption_profile(),
                             self._generate_encryption_profile(),
                             self._generate_encryption_profile(),
                             self._generate_encryption_profile(),
                             self._generate_encryption_profile())
        return key

    # Performs encryption. Comments throughout the function further describe its inner workings.
    def perform_encryption(self, KEY: Key) -> str:
        if self._check_key(key_obj=KEY):
            pass
        else:
            return AssertionError
        incrementing_index: int = 0 # This index value is used to cycle over the encryption profile of a character.
        broken_safe_str: list = []
        for char in self.unencrypted_string: # Loops over every character in the string the user provided.
            broken_safe_str.append(self.enc_prof_key[char][incrementing_index]) # Selects an encryption profile based on the incrementing index.
            incrementing_index += 1 # Increment by 1 happens
            if incrementing_index == 6: incrementing_index: int = 0 # Ensures an IndexError never happens.
        self.encrypted_string: str = "".join(broken_safe_str)
        return self.encrypted_string
    
    # Performs decryption. Comments throughout the function further describe its inner workings.
    def perform_decryption(self, KEY: Key) -> str:
        if self._check_key(key_obj=KEY):
            pass
        else:
            return AssertionError
        broken_encrypted_string: list = self._split_string(self.encrypted_string, self.complexity_length) # Splits the encrypted string by it's complexity-length.

        broken_decrypted_string: list = []
        for encrypted_profile in broken_encrypted_string: # Iterates over each encryption profile of the encrypted message.
            for i, key_profiles in enumerate(self.enc_prof_reverse_key): # Iterates over the encrypted-profile-reverse-key in order to reverse engineer the original message.
                #print(key_profiles)
                if encrypted_profile == key_profiles[0] or encrypted_profile == key_profiles[1] or encrypted_profile == key_profiles[2] or encrypted_profile == key_profiles[3] or encrypted_profile == key_profiles[4] or encrypted_profile == key_profiles[5]: 
                    broken_decrypted_string.append(self.enc_prof_reverse_key[key_profiles]) # Assigns the correct character based on a matching encryption profile.
        decrypted_string: str = "".join(broken_decrypted_string)
        return decrypted_string


