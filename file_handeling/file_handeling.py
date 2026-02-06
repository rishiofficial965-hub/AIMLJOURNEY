from pathlib import Path
import shutil

def create_folder():
    try:
        name = input("please provide your folder name:- ")
        p = Path(name)
        p.mkdir(exist_ok=True)
        print("folder created....")
    except Exception as err:
        print(f"error cause because of {err}")

def read_folder():
    p = Path(".")
    items = list(p.rglob('*'))
    for i, item in enumerate(items):
        print(f"{i+1}. {item}")

def update_folder():
    try:
        read_folder()
        name = input("please tell your folder name for updation:- ")
        p = Path(name)
        if p.exists() and p.is_dir():
            new_name = input("new name:- ")
            new_p = Path(new_name)
            p.rename(new_p)
            print("donee...")
        else:
            print("no such folder exist")
    except Exception as err:
        print(f"error cause because of {err}")

def delete_folder():
    try:
        read_folder()
        name = input("please provide your folder name:- ")
        p = Path(name)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)
            print("deleted")
        else:
            print("no such folder exists")
    except Exception as err:
        print(f"error cause because of {err}")

def create_file():
    try:
        read_folder()
        name = input("please provide your file name:- ")
        p = Path(name)
        if not p.exists():
            with p.open('w') as fs:
                data = input("what u want in this file:- ")
                fs.write(data)
            print("created a file")
        else:
            print("file name already exists try different name")
    except Exception as err:
        print(f"error cause because of {err}")

def read_file():
    try:
        read_folder()
        name = input("please provide your file name:- ")
        p = Path(name)
        if p.exists() and p.is_file():
            print("file content....")
            print(p.read_text())
        else:
            print("no file exists")
    except Exception as err:
        print(f"error cause because of {err}")

def delete_file():
    try:
        read_folder()
        name = input("please provide your file name:- ")
        p = Path(name)
        if p.exists() and p.is_file():
            p.unlink()
            print("file deleted....")
        else:
            print("no file exists")
    except Exception as err:
        print(f"error cause because of {err}")

def update_file():
    try:
        read_folder()
        name = input("please provide your file name:- ")
        p = Path(name)
        if p.exists() and p.is_file():
            print("options..") 
            print("1. rename the file") 
            print("2. append content") 
            print("3. overwrite content") 

            choice = int(input("please choose your option:- "))

            if choice == 1:
                n_name = input("tell new name with extension:- ")
                n_path = Path(n_name)
                if not n_path.exists():
                    p.rename(n_path)
                    print("name changed..")
                else:
                    print("suggest new name")

            elif choice == 2:
                data = input("input the data u want to append:- ")
                p.write_text(p.read_text() + " " + data)
                print("done")

            elif choice == 3:
                data = input("input the data u want to overwrite:- ")
                p.write_text(data)
                print("done")
    except Exception as err:
        print(f"error cause because of {err}")

while True:
    print("\nOption:- ")
    print("1. Create a folder")
    print("2. Read files and folder")
    print("3. Update the folder")
    print("4. Delete the folder")
    print("5. Create a file")
    print("6. Read a file")
    print("7. Update a file")
    print("8. Delete a file")
    print("0. Exit")

    choice = int(input("please choose your option:- "))

    if choice == 1:
        create_folder()
    elif choice == 2:
        read_folder()
    elif choice == 3:
        update_folder()
    elif choice == 4:
        delete_folder()
    elif choice == 5:
        create_file()
    elif choice == 6:
        read_file()
    elif choice == 7:
        update_file()
    elif choice == 8:
        delete_file()
    elif choice == 0:
        break
    else:
        print("Invalid input")
