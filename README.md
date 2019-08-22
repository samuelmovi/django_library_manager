# Django Library Manager
This is a Django-based web application for the management of personal book collections.

It supports multiple users, keeping track of their book collection, the locations of these books, and any book loans.

It's also multilingual, currently with support for English(default) and Spanish.

## Installation
For use in development, it required the following:

- Python 3.x
- Django: `pip install django`
- Postgresql docker image: `docker pull postgres:alpine`
- Postgresql client: `sudo apt install postgresql-client`


## Usage
- Registration: can be done either through exposing the sign-up page or by the admin page
- Home page: users are redirected here after a succesful login, or by clicking on the upper right-hand corner of 
every page. It includes a summary of their book collection, and active loans.


## Page Descriptions

### Home
The home page (`/`) shows a summary of the user's book collection and their outstanding loans.

### Books
The main books page (`/books/`) shows a list of all books registered to that user in the database.

It exposes the following links at the bottom:

- `/books/new/`: shows a form to create a new book entry. No mandatory fields (for the time being).
- `/books/modify/`: shows a list of all the book entries for the user (with radio buttons). Choosing an entry and 
clicking the button below the list takes you to a filled-out book form, where info can be modified, and saved by 
clicking the `Modify Book` button.


### Locations
The main locations page (`/locations/`) shows a list of all locations registered by that user.

It exposes the following links at the bottom:

- `/locations/new/`: it shows a form to create a new location entry for that user
- `/locations/delete`: it shows a list of all location entries for that user in the database (with radio buttons) and
 a button to delete the entry from the database.


### Loans
The main loans page (`/loans/`) shows a list of all loans in the database for that user, whether they have been returned or not.

It exposes the following links at the bottom:

- `/loans/loan/`: shows a list of all non-loaned books for that user (with radio buttons), a field for the borrower's 
name and a `Loan This Book` button.
- `/loans/return/`: shows a list of the user's active loans (with radio buttons) and a button to set the book as 
returned (`Book.loaned = False`)

## Steps
The included `STEPS.md` file is a compendium of the steps necessary to bring this project to a working order.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
