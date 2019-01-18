with open('activeplayers.txt', 'r') as f:
    lines = f.readlines()
lines = ['id, '+line for line in lines]
with open('activeplayers.txt', 'w') as f:
    f.writelines(lines)
