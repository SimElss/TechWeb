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
    ]
}
