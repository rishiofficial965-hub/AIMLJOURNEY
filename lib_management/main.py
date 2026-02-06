import json 
import random
import string
from pathlib import Path
from datetime import datetime

class Library:

    database = "library.json"
    data = {"books":[],"members":[]}
    #load existing data to json

    def __init__(self):
        self.load_data()

    def load_data(self):
        if Path(Library.database).exists():
            with open(Library.database,"r") as fs:
                content = fs.read().strip()
                if content:
                    Library.data = json.loads(content)
        else:
            with open(Library.database,"w") as fs:
                json.dump(Library.data,fs,indent=4)

    @classmethod
    def save_data(cls):
        with open(cls.database,'w') as fs:
            json.dump(cls.data,fs,indent=4,default=str)

    @staticmethod
    def gen_id(Prefix = "B"):
        random_id = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return Prefix+"-"+random_id
        
    def add_book(self, title, author, copies):
        book = {
            "Id" : self.gen_id(),
            "Title" : title,
            "Author" : author,
            "Available_copies" : copies,
            "Total_copies" : copies,
            "Added_on" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        Library.data["books"].append(book)
        Library.save_data()
        return book

    def list_books(self):
        return Library.data['books']

    def add_member(self, name, email):
        member = {
            "Id":self.gen_id("M"),
            "name":name,
            "email":email,
            "borrowed":[],
        }
        Library.data["members"].append(member)
        Library.save_data()
        return member

    def list_members(self):
        return Library.data['members']

    def borrow_book(self, member_id, book_id):
        members = [m for m in Library.data['members'] if m['Id'] == member_id]
        if not members:
            return False, "Member ID does not exist"
        
        member = members[0]
        books = [b for b in Library.data['books'] if b['Id'] == book_id]
        if not books:
            return False, "Book ID does not exist"
            
        book = books[0]
        if book['Available_copies'] <= 0:
            return False, "No copies available"
            
        borrow_entry ={
            "book_id" : book['Id'],
            'title':book['Title'],
            "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        member['borrowed'].append(borrow_entry)
        book['Available_copies'] -= 1
        Library.save_data()
        return True, "Book borrowed successfully"

    def return_book(self, member_id, book_index):
        members = [m for m in Library.data['members'] if m['Id'] == member_id]
        if not members:
            return False, "Member ID does not exist"
            
        member = members[0]
        if not member['borrowed'] or book_index < 0 or book_index >= len(member['borrowed']):
            return False, "Invalid book selection"
            
        selected = member['borrowed'].pop(book_index)
        books = [bk for bk in Library.data['books'] if bk['Id'] == selected['book_id']]
        if books:
            books[0]['Available_copies'] += 1
            
        Library.save_data()
        return True, f"Returned: {selected['title']}"

def main():
    lib = Library()
    while True:
        print("="*50)
        print("Library Management System")
        print("="*50)
        print("1. Add Book")
        print("2. List Book")
        print("3. Add Member")
        print("4. List Member")
        print("5. Borrow Book")
        print("6. Return Book")
        print("0. Exit the portal")
        print("="*50)

        try:
            choice = int(input("What task you want to do :- "))
        except ValueError:
            continue

        if choice == 1:
            title = input("Enter book title : ")
            author = input("Enter book author : ")
            copies = int(input("How many copies : "))
            lib.add_book(title, author, copies)
            print("Book added!")
        elif choice == 2:
            books = lib.list_books()
            if not books:
                print("No books available")
            else:
                print(f"{'ID':12} {'Title':25} {'Author':20} Copies")
                print("-" * 70)
                for b in books:
                    print(f"{b['Id']:12} {b['Title'][:24]:25} {b['Author'][:19]:20} {b['Available_copies']}/{b['Total_copies']}")
        elif choice == 3:
            name = input("Enter name : ")
            email = input("Enter your email : ")
            lib.add_member(name, email)
            print("Member added!")
        elif choice == 4:
            members = lib.list_members()
            if not members:
                print("No members listed")
            else:
                print(f"{'Id':12} {'Name':25} {'Email':20} Borrowed")
                print("-" * 70)
                for m in members:
                    print(f"{m['Id']:12} {m['name'][:24]:20} {m['email'][:19]:20} {len(m['borrowed'])}")
        elif choice == 5:
            m_id = input("Enter member ID: ")
            b_id = input("Enter book ID: ")
            success, msg = lib.borrow_book(m_id, b_id)
            print(msg)
        elif choice == 6:
            m_id = input("Enter member ID: ")
            members = [m for m in Library.data['members'] if m['Id'] == m_id]
            if members:
                member = members[0]
                for i, v in enumerate(member['borrowed']):
                    print(f"{i}. {v['title']} ({v['book_id']})")
                try:
                    idx = int(input("Enter index to return: "))
                    success, msg = lib.return_book(m_id, idx)
                    print(msg)
                except ValueError:
                    print("Invalid input")
        elif choice == 0:
            break

if __name__ == "__main__":
    main()
