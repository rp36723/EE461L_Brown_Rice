#encrypt and decrypt functions for the server

def encrypt(inputText, N, D):
    reversed_string = inputText[::-1]
    listed_string = list(reversed_string)
    for i in range(len(listed_string)):
        char = ord(listed_string[i])
        if 34 <= char <= 126:
            if D == 1: 
                char = (char + N - 34) % 93 + 34
            elif D == -1:
                char = (char - N - 34) % 93 + 34
        listed_string[i] = chr(char) 
    return ''.join(listed_string)

def decrypt(inputText, N, D):
    reversed_string = inputText[::-1]
    listed_string = list(reversed_string)
    for i in range(len(listed_string)):
        char = ord(listed_string[i])
        if 34 <= char <= 126: 
            if D == 1: 
                char = (char - N - 34) % 93 + 34
            elif D == -1:
                char = (char + N - 34) % 93 + 34
        listed_string[i] = chr(char) 
    return ''.join(listed_string) 