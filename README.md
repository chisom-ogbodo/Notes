# Notes api app

A  basic note keeping app built with fastapi and postgresql. This project is intended to demonstrate how to build applications with modern python.

## Features

- Supports create, read, update and delete notes, the good old  crud operations.
- Multi user support, Logged in user only performs crud operations on notes they own. 
- User registration
- Authentication and authorisation with jwt tokens
- Users' password are stored in postgres database with good hashing algorithms

## How to use

1) clone the repo and navigate to the Notes directory
```bash
git clone https://github.com/chisom-ogbodo/Notes.git
cd Notes
```

2) Create a virtual environment
   
```bash
python3 -m venv venv
```

3) Install the dependencies
   ```bash
   pip install -r requirements.txt
   ```
4) With everything set up, we can now run the app by
```bash
uvicorn main:app --reload
```
## To do

- [ ] Add roles: Admin and User
- [ ] Write test coverage for the application
- [ ] Add database migration
- [ ] Implement offline usage with sqlite when there's no internet 

## Contributions

Contibutions are welcome to this project. If you find any issues or have an idea for improvement, feel free to open an issue or submit a pull request.

## License

This project is licenced under the terms of MIT. See https://opensource.org/license/MIT  for more information
