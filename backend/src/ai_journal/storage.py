from pathlib import Path


user_data_location = Path(__file__).resolve().parent.parent / "user_data"
print(user_data_location)
user_data_location.mkdir(exist_ok=True)

example_data_location = Path(__file__).resolve().parent.parent / "data"


def read_user_data() -> dict:
    user_data = {}
    for user_data_file in user_data_location.iterdir():
        print(user_data_file.stem)
        with open(user_data_file, "r") as file:
            user_data[user_data_file.stem] = file.read()
    return user_data


def write_to_new_file(content: str):
    # new timestamp for the file name
    import datetime

    new_file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".md"

    new_file_path = user_data_location / new_file_name
    with open(new_file_path, "w") as file:
        file.write(content)
    return new_file_name
