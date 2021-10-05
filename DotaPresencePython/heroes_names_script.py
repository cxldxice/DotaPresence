import os

list_of_files = os.listdir("../assets/icons")

result = ''

for file in list_of_files:
    file = file.split(".")[0].replace('-', '')
    hero = file[14:]
    hero = hero[0].capitalize() + hero[1:]
    result += "'" + file + "': '" + hero + "',\n"

print(result)
