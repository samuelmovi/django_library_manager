# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- add logging functionality
- make the info pages show the created and modified fields (display only)
- check for translation error and non-translations in translated interface
- refactor with semantic elements
- implement table sorting with jquery
- add media_url settings
- implement testing for new views

## 2019-09-03
### Fixed
- better container styles for template's layouts

### Added
- new view for books `/books/<path:book_id>/` to show info
- in book info view add buttons to modify or delete entry
- add hover-over colors to table heads and rows to indicate interactivity
- implemented new scheme for locations

## 2019-08-28
### Changed
- div tags in templates for semantic tags

## 2019-08-21
### Added
- try/except code

## 2019-08-08
### Added
- django.middleware.locale.LocaleMiddleware to MIDDLESWARE in settings.py and it works

## 2019-08-06
### Changed
- moved app domain from `'/library/'` to `''` in my_library_manager/urls.py

### Added 
- Testing for signup view

### Fixed
- Wrong path for virtual environment in `init.sh`

## 2019-08-05
### Added
- Translation file for spanish (es)
- Basic testing for models

### Changed
- Rebuilt entire project under new name (my_library_manager) in new repository with postgresql backend
- Changed models a bit
- Created model fields list in view classes so as to not use the request's own fields, for robustness

## 2019-08-04
### Changed
- Making changed in templates and views to accommodate a proper site-wide translation


## 2019-08-03
### Added
- Signup page template
- signup view

### Changed
- Location model: removed modification date, added owner field
- improved login page
- improved signup page
- made nav bar and bottom bar dependent on user authentication for rendering
- improved home view styling
- all but 4 views moved to class-based views


## 2019-08-02 
### Changed
- font size in table-info now small
- leaving modification date null when creating new model instances
- radio buttons in choose views are no longer w3-radio class but simple radio types
- labels before input fields in info views
- home page shows info on user's book collection

### Added
- login test for all views with decorators and mixins
- user-name link on top-right corner to go to home
- check if user is authenticated before displaying the home link
- update modification_date when modifying book or location
- owner char-field to book model
- code to assign username to book.owner
- logout link to home page


## 2019-08-01
### Changed
- side bar for bottom bar in show views
- books in book view ordered by author
- in new book locations ordered by id
- deleting location works (if foreign key constraint allows it)
- removed holdover footer and replaced with permanent bottom bar

## Fixed
- model list in book view updating after moving the call into a function
- modifying book info works
- deleting books works
- location list now refreshes when reloaded
- modifying location works
- loaning books works
- loan books only shows books not loaned
- return books only shows loans with no return date

### Added
- modify book functionality
- delete book functionality
- returning books works


## 2019-07-31
### Added
- sidebar for navigation
- post data handling for add_book and add_location views


## 2019-07-30
### Added
- authentication system and login page