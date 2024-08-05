from dataclasses import dataclass


@dataclass
class UserTest:
    EMAIL: str = "test@mail.ru"
    NEW_EMAIL: str = "new_test@mail.ru"
    NICKNAME: str = "NewUser"
    PASSWORD: str = "Abc123!@#def456$"


login_credentials_schema = {
    "username": UserTest.EMAIL,
    "password": UserTest.PASSWORD,
}
