import sys
import os
import argparse

from xml.dom.minidom import parse

#############################################
# CLASSES
#############################################

class Book:

    def __init__(self, author, title, genre, price, publish_date, description):

        self.author = author
        self.title = title
        self.genre = genre
        self.price = price
        self.publish_date = publish_date
        self.description = description

class Book_Factory():

    def create_book_from_book_xml(self, book_xml):

        book_dict = parse_book_xml(book_xml)

        new_book = Book(book_dict["author"],
                        book_dict["title"],
                        book_dict["genre"],
                        book_dict["price"],
                        book_dict["publish_date"],
                        book_dict["description"])

        return new_book

#############################################
# FUNCTIONS
#############################################

def existing_file(input_file):

    if input_file != None:

        if os.path.exists(input_file):

            return input_file

    raise argparse.ArgumentTypeError("File '%s' does not exist" % input_file)

def get_commandline_parser():

    parser = argparse.ArgumentParser(description='Process library.')
    parser.add_argument('--library-file', nargs='?', type=existing_file, required=True,\
                       help='library file to be processed')

    return parser

def get_library_file(input_arguments):

    library_file = input_arguments.library_file

    return library_file

def get_books(library_file):

    books = [] # output array for Book objects

    books_xml = library_file.getElementsByTagName("book")

    book_factory = Book_Factory()

    for book in books_xml:

        books.append(book_factory.create_book_from_book_xml(book))

    return books

def parse_book_xml(book_xml):
    """extract data from 'book_xml' object and return it as dictionary"""

    output_dict = {}

    output_dict["author"] = get_value_of_book_xml_attribute(book_xml, "author")
    output_dict["title"] = get_value_of_book_xml_attribute(book_xml, "title")
    output_dict["genre"] = get_value_of_book_xml_attribute(book_xml, "genre")
    output_dict["price"] = get_value_of_book_xml_attribute(book_xml, "price")
    output_dict["publish_date"] = get_value_of_book_xml_attribute(book_xml, "publish_date")
    output_dict["description"] = get_value_of_book_xml_attribute(book_xml, "description")

    return output_dict

def get_value_of_book_xml_attribute(book_xml, attribute):

    parent = book_xml.getElementsByTagName(attribute).item(0)

    return parent.childNodes[0].data

def create_tuples_from_books(books):

    book_tuples = []

    for book in books:

        book_tuples.append((book.author, book.title, book.genre, book.price, book.publish_date, book.description))

    return book_tuples

#############################################
# MAIN PROGRAM
#############################################

parser = get_commandline_parser()

input_arguments = parser.parse_args()

library_file_content = parse(get_library_file(input_arguments))

books = get_books(library_file_content)

book_tuples = create_tuples_from_books(books)

for book_tuple in book_tuples:

    print book_tuple

