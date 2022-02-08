from stack import Stack
from dynamodb import Book


with open('template.yaml', 'r') as cf_file:
    cft_template = cf_file.read()
stack_obj = Stack("myfirstdynamodbtable",cft_template,"ap-south-1")
stack_obj.create_stack()
stack_obj.update_stack()

book = Book()
book_resp = book.put_item("Fantasy","The Fifth season","English")
print("Insert in to DynamoDB succeeded............")
get_response= book.get_item("Fantasy","The Fifth season")
print("Get an item from DynamoDB succeeded............")
update_book=book.update_book("Fantasy","The Fifth season","German","2015","5")
print("Update item in Dynamodb is succeeded......")
update_resp = book.increase_rating("Fantasy","The Fifth season","6")
print("Increment an Atomic Counter in DynamoDB succeeded............")
delete_book = book.delete_underratedbook("Fantasy", "The Fifth season", "12")
print("Delete item in Dynamodb succeeded.....")
batch_write = book.batch_write_item("Fiction","Harry Potter","2015","Greek")
print("Batched operation in dynamodb is succeeded.............")