from uuid import uuid4


database = {
    "books": [
        {
            "id": str(uuid4()),
            "name": "Animagus",
            "Author": "Alice",
            "Editor": "John Doe"
        },
        {
            "id": str(uuid4()),
            "name": "Les misérables",
            "Author": "Victor Hugo",
            "Editor": "Marc Doe"
        },
        {
            "id": str(uuid4()),
            "name": "The Hobbit",
            "Author": "J.R.R. Tolkien",
            "Editor": "Bob Doe"
       
        },
    ],
    "users" : [

        {
            "id": str(uuid4()),
            "username": "admin",
            "name": "admin",
            "surname": "admin",
            "password": "Admin!123",
            "email": "admin@juice-sh.op",
            "group": "admin",
            "whitelist": True
        },
        {
            "id": str(uuid4()),
            "username": "User2",
            "name": "John",
            "surname": "Doe",
            "password": "Test123!",
            "email": "test@gmail.com",
            "group": "client",
            "whitelist": True
        }

    ]

}
