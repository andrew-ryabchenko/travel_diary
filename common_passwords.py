COMMON_PASSWORDS = []

with open("CommonPassword.txt") as infile:
    for line in infile:
        COMMON_PASSWORDS.append(line.rstrip("\n"))

