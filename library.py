from typing import Optional, List

class Book:
    def __init__(self, book_id: int, title: str, author: str):
        self.book_id = book_id
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book({self.book_id}, '{self.title}', '{self.author}')"

# --- Binary Search Tree for catalog ---
class BSTNode:
    def __init__(self, book: Book):
        self.book = book
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BookCatalogBST:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, book: Book):
        self.root = self._insert(self.root, book)

    def _insert(self, node: Optional[BSTNode], book: Book) -> BSTNode:
        if node is None:
            return BSTNode(book)
        if book.book_id < node.book.book_id:
            node.left = self._insert(node.left, book)
        elif book.book_id > node.book.book_id:
            node.right = self._insert(node.right, book)
        else:
            node.book = book  # update if same id
        return node

    def search_by_id(self, book_id: int) -> Optional[Book]:
        node = self.root
        while node:
            if book_id == node.book.book_id:
                return node.book
            elif book_id < node.book.book_id:
                node = node.left
            else:
                node = node.right
        return None

    def inorder(self) -> List[Book]:
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node: Optional[BSTNode], res: List[Book]):
        if node is None:
            return
        self._inorder(node.left, res)
        res.append(node.book)
        self._inorder(node.right, res)

# --- Singly Linked List for issued books ---
class IssuedNode:
    def __init__(self, book: Book, issued_to: str):
        self.book = book
        self.issued_to = issued_to
        self.next: Optional['IssuedNode'] = None

class IssuedList:
    def __init__(self):
        self.head: Optional[IssuedNode] = None

    def issue(self, book: Book, issued_to: str):
        node = IssuedNode(book, issued_to)
        node.next = self.head
        self.head = node
        print(f"Issued {book.title} to {issued_to}")

    def return_book(self, book_id: int) -> bool:
        prev = None
        cur = self.head
        while cur:
            if cur.book.book_id == book_id:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                print(f"Returned {cur.book.title}")
                return True
            prev = cur
            cur = cur.next
        print('Book not found in issued list')
        return False

    def list_issued(self):
        cur = self.head
        res = []
        while cur:
            res.append((cur.book, cur.issued_to))
            cur = cur.next
        return res

# --- Merge Sort (for lists of Book by title) ---
def merge_sort_books(books: List[Book]) -> List[Book]:
    if len(books) <= 1:
        return books
    mid = len(books) // 2
    left = merge_sort_books(books[:mid])
    right = merge_sort_books(books[mid:])
    return merge(left, right)

def merge(left: List[Book], right: List[Book]) -> List[Book]:
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i].title.lower() <= right[j].title.lower():
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# --- Library Manager (CLI) ---
class LibraryManager:
    def __init__(self):
        self.catalog = BookCatalogBST()
        self.issued = IssuedList()
        self._next_id = 1

    def add_book(self, title: str, author: str):
        book = Book(self._next_id, title, author)
        self.catalog.insert(book)
        self._next_id += 1
        print(f"Added book: {book}")

    def remove_book(self, book_id: int):
        books = [b for b in self.catalog.inorder() if b.book_id != book_id]
        self.catalog = BookCatalogBST()
        for b in books:
            self.catalog.insert(b)
        print(f"Removed book id {book_id}")

    def search_book(self, book_id: int):
        b = self.catalog.search_by_id(book_id)
        if b:
            print('Found:', b)
        else:
            print('Not found')
        return b

    def list_books(self, sorted_by_title=False):
        books = self.catalog.inorder()
        if sorted_by_title:
            books = merge_sort_books(books)
        for b in books:
            print(b)

    def issue_book(self, book_id: int, issued_to: str):
        b = self.catalog.search_by_id(book_id)
        if b:
            self.issued.issue(b, issued_to)
        else:
            print('Book not in catalog')

    def return_book(self, book_id: int):
        return self.issued.return_book(book_id)

def main():
    lm = LibraryManager()
    # Seed sample books (optional)
    lm.add_book('The Alchemist', 'Paulo Coelho')
    lm.add_book('Introduction to Algorithms', 'Cormen')
    lm.add_book('Clean Code', 'Robert C. Martin')

    while True:
        print('\n--- LIBRARY MANAGEMENT ---')
        print('1. Add Book')
        print('2. Remove Book')
        print('3. Search Book by ID')
        print('4. List Books (inorder)')
        print('5. List Books (sorted by title)')
        print('6. Issue Book')
        print('7. Return Book')
        print('8. List Issued Books')
        print('9. Exit')
        ch = input('Choose: ').strip()
        try:
            if ch == '1':
                t = input('Title: ').strip()
                a = input('Author: ').strip()
                lm.add_book(t, a)
            elif ch == '2':
                bid = int(input('Book ID: ').strip())
                lm.remove_book(bid)
            elif ch == '3':
                bid = int(input('Book ID: ').strip())
                lm.search_book(bid)
            elif ch == '4':
                lm.list_books(sorted_by_title=False)
            elif ch == '5':
                lm.list_books(sorted_by_title=True)
            elif ch == '6':
                bid = int(input('Book ID: ').strip())
                person = input('Issued to (name): ').strip()
                lm.issue_book(bid, person)
            elif ch == '7':
                bid = int(input('Book ID: ').strip())
                lm.return_book(bid)
            elif ch == '8':
                lst = lm.issued.list_issued()
                for book, who in lst:
                    print(book, '->', who)
            elif ch == '9':
                break
            else:
                print('Invalid')
        except ValueError:
            print('Invalid input: please enter correct numeric values where required.')

if __name__ == '__main__':
    main()
