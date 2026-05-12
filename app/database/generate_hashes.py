from werkzeug.security import generate_password_hash

users = {
    "admin": "Admin123!",
    "resp_equipe": "RespEq123!",
    "resp_projet": "RespPr123!",
    "guest1": "Guest1!",
    "guest2": "Guest2!"
}

for username, password in users.items():
    hash_value = generate_password_hash(password, method = "scrypt")

    print(f"{username}:")
    print(hash_value)
    print()