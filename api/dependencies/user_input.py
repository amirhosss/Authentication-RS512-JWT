from fastapi import Form


class UserInput:
    def __init__(
        self,
        first_name: str = Form(..., max_length=50),
        last_name: str = Form(..., max_length=50),
        username: str = Form(..., max_length=50),
        password: str = Form(
            ...,
            regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,50}$'
        ),
        email: str = Form(
            ...,
            max_length=64,
            regex=r'^([a-zA-Z0-9]+(?:[.-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:[.-]?[a-zA-Z0-9]+)*\.[a-zA-Z]{2,7})$'
        )
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email