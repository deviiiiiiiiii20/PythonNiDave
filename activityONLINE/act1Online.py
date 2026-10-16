class Book:

    discount_rate = 0.10
    total_books = 0


    def  __init__(self, title, author, price):
        self.title = str(title)
        self.author = str(author)
        self.price = float(price)


        Book.total_books += 1

        if self.price >= 1000:
            self.apply_discount()

    def get_summary(self):
        # summary = self.title + ' by ' + self.author + ' - ${}'.format(self.price)
        summary = "'{}' by {} - {}".format(self.title, self.author, self.price)
        return summary


    def apply_discount(self):
        self.price = self.price - (self.price * self.discount_rate)
        return self.price


while True:
    print("=" * 50)
    author = input("Enter your name: ")
    title = input("Enter your book title: ")
    price = float(input("Enter your book price: "))
    print("=" * 50)

    user = Book(title, author, price)
    print("=" * 50)
    print(user.get_summary())
    print("=" * 50)

    '''
    print("=" * 50)
    print(Book.total_books)
    print("=" * 50)
    
    book1.discount_rate = 0.20
    print(book1.apply_discount())
    print(book2.apply_discount())
    
    print("=" * 50)
    print(book1.get_summary())
    print(book2.get_summary())
    print("=" * 50)
    print(book1.__dict__)
    print(book2.__dict__)
    
    '''