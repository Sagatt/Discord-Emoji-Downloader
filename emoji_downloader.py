#!/bin/python3
import os
import shutil
import requests

# Ensure the 'requests' module is installed
try:
    import requests
except ImportError:
    print("The 'requests' module is not installed. Install it by running 'pip install requests'.")
    exit(1)

if os.path.isfile("./token.txt"):
    token = open("token.txt").read().strip()
else:
    token = input("token: ")
    open("token.txt", "w").write(token)

def restrict(str_):
    if os.name == "nt":
        str_ = str_.translate({ord(i): None for i in r'\/:*?"<>|'})
    else:
        str_ = str_.replace("/", "")
    if len(str_) == 0:
        str_ = "no name"
    return str_

if __name__ == "__main__":
    response = requests.get("https://discord.com/api/v8/users/@me/guilds", headers={"authorization": token})
    if response.status_code != 200:
        print(f"Failed to retrieve guilds: {response.status_code}")
        exit(1)
    
    guilds = response.json()
    i = 0
    msg = ""
    server_ids = []
    server_names = []
    for guild in guilds:
        i += 1
        server_ids.append(guild["id"])
        server_names.append(guild["name"])
        msg += f"{i} | {guild['name']}\n"
    print(msg)
    
    a = input("Choose the guild: ")
    if a.isdigit() and 1 <= int(a) <= len(server_ids):
        server_id = server_ids[int(a) - 1]
        server_name = server_names[int(a) - 1]
    else:
        print("Invalid selection")
        exit(0)
    
    server_folder = restrict(server_name)
    if os.path.isdir("./" + server_folder):
        print("Removing the folder " + server_folder)
        shutil.rmtree("./" + server_folder)
    os.mkdir("./" + server_folder)
    
    print("Getting the emoji list of " + server_name)
    response = requests.get(f"https://discord.com/api/v8/guilds/{server_id}/emojis", headers={"authorization": token})
    if response.status_code != 200:
        print(f"Failed to retrieve emojis: {response.status_code}")
        exit(1)
    
    emojis = response.json()
    i = 0
    for emoji in emojis:
        i += 1
        file_extension = "gif" if emoji["animated"] else "png"
        with open(f"./{server_folder}/{emoji['name']}.{file_extension}", "wb") as f:
            print(f"Downloading {emoji['name']} ({'animated' if emoji['animated'] else 'static'}) ({i}/{len(emojis)})")
            f.write(requests.get(f"https://cdn.discordapp.com/emojis/{emoji['id']}.{file_extension}?v=1").content)
    
    print("Finished downloading all emojis")
