# Issue Tracker Application
## 4th Milestone Project - Full Stack Frameworks with Django - Code Institute

### Table of contents
- [Overview](#overview)
- [UX](#ux)
- [User stories](#user-stories)
- [Features](#features)
- [Technologies used](#technologies-used)
- [Testing](#testing)
- [Installation](#installation)
- [Deployment](#deployment)
- [Acknowledgements](#acknowledgements)


## Overview
Issue Tracker is a ticketing system that can be used to manage queries related to other application and to keep track of progress done. The primary entity in the Issue Tracker is a ticket describing a user's issue. The application allows users to create tickets, comment on tickets and shows the status of the ticket. Issues come in two varieties - 'bugs' that will be fixed for free and 'features' that will be developed for money. To help prioritize the work, users will be able to upvote bugs (signifying 'I have this too') and upvote feature requests (signifying 'I want to have this too'). While upvoting bugs is free, to upvote a feature request, users would need to pay some money. The highest paid feature will be developed as first.

## UX
The applcation can serve users to report the bugs they encounter or to share ideas for new features that can be implemented. The purpose of Issue tracker application is to facilitate this process to them. Tickets can be raised very quickly and users get an instant response regarding the progress via email notifications or a user profile tab.

I wanted the user interface to be simple and consistent throughout the whole application. The data is presented in a clean and organized way. User has easy access to all the functions from the navigation bar on larger screens or a mobile menu that is triggered by the 'hamburger' button.

There are four models in the application: Ticket, Comment, Vote and Payment that inherit from Django models. 

Ticket model consists of the following fields: title, author, description, ticket type and ticket status. By default ticket status is set to 'To do' and can be changed by the administrator only. User can edit his/her own tickets but they cannot be deleted. 

Comment model has comment text and created date fields. Two foreign keys are user and ticket.

Vote model has user, ticket and created date fields. It also has a unique together option, to prevent voting more than once by one person on the same ticket.

Payment model has two foreign keys: ticket and user. Other fields that are also included in the model are: date, payment value and charge id, which is a transaction id obtained from Stripe after payment completion.

## User Stories
### Guest
As a guest user:
* I want to be able to browse the list of tickets,
* I want to be able to see the details of a specific ticket,
* I want to bo able to filter tickets by their status,
* I want to be able to search tickets by their title or a word from ticket's description,
* I want to be able to sort the tickets based on different criterias,
* I want to be able to see the comments placed by users,

### Logged in User
As a logged in user:
* I want to be able to perform all the operations that a guest user can do,
* I want to be able to set up an account,
* I want to be able to raise a new ticket,
* I want to be able to vote on a bug type ticket
* I want to be able to make a payment for a feature type ticket,
* I want to be able to add a comment to a ticket,
* I want to be able to view my profile, whre I can check statuses of my tickets,
* I want to get updates by email whenever there has been a status change made on any of my tickets,

### Administrator / Developer
As an administrator / developer:
* I want to be able to perform all the operations that user can do,
* I want to be able to update the ticket status, to give user a feedback on a progress

## Features
Application allows users to create two type of tickets: bugs and features. Bugs should be used to report any issues related to the application and features should be raised whenever a user comes up with a new functionality idea that could be implemented. Users can upvote bugs, if they have the same issue to prioritise fixing it. Features will be developed based on the total amount contributed towards a specific feature.

The application has following functionalities:

Available to everyone:

- [x] browsing tickets

- [x] filtering and sorting tickets

- [x] searching tickets

- [x] viewing details of a specific ticket

Available to registered users:

- [x] create a new ticket

- [x] edit a ticket

- [x] comment a ticket

- [x] vote bug ticket

- [x] make payment for feature ticket

- [x] view user's profile

- [x] receive a notification email, once the ticket status has changed

Available to administrator/developer:
- [x] changing tickets' statuses

Functionalities left to implement:

- [ ] - pagination

## Technologies Used
- [Python](https://www.python.org/) - used for general-purpose programming and writing the logic of the application,
- [Django 3.0](https://www.djangoproject.com/) - used for serving templates, performing CRUD operations and administrative functions,
- [Allauth library] - used for signup and login functions, forgotten password and email verification flows,
- [PostgreSQL](https://www.postgresql.org/) - used for storing the application data,
- [Jinja templating language](https://jinja.palletsprojects.com/en/2.10.x/) - used for incorporating Python code into HTML templates,
- [HTML](https://html.spec.whatwg.org/) - used for building the structure of the interface,
- [CSS](https://docs.ckan.org/en/ckan-2.7.3/contributing/css.html) - used for custom styling of some elements,
- [JavaScript / jQuery](https://jquery.com/) - used for triggering certain functions that set timeout on Django messages or disable buttons, preventing them from being double clicked,
- [Bootstrap](https://getbootstrap.com/) - used for building the visual side of the application,
- [Stripe API](https://stripe.com/en-ie) - used for processing card payments from the application (please use test card number: 4242 4242 4242 4242). Please do NOT enter your valid card details.

## Testing

Application has been tested across different devices:

- desktop,
- laptop,
- smartphone,

as well as different browsers:

- Google Chrome (desktop & mobile),
- Mozilla Firefox (desktop),
- Microsoft Edge (desktop),
- Brave (mobile).

Application works correctly across different screen and resolutions, as well as the orientations.

Aplication functions have been tested to ensure they work correctly:

- browsing tickets - Tickets can be browsed by clicking 'Bugs' or 'Features' link from the menu, which open list views. All tickets are available in these views. By default all tickets are sorted by votes total (bugs) and payments total (features) in descending order.

- filtering and sorting tickets - Filtering and sorting can be done through the forms that are available in 'Bugs' and 'Features' lists. Tickets can be sorted by creation date and votes total (bugs) or payments total (features).

- searching tickets - Search functionality is also done through the forms available in 'Bugs and 'Features'. Tickets can be looked up be the word from either ticket's title or its description.

- viewing details of a specific ticket - this is done by clicking 'Show details' button in list views

- creating a new ticket - To create a new ticket, user needs to click 'New Ticket' option from the menu and fulfill the form specifying ticket's subject, type (bug or feature) and providing a description of an issue or a new functionality suggestion and clicking 'Submit' button,

- editing a ticket - Tickets can be edited by author and administrator. This can be done by clicking 'Edit' button in ticket detailed view. This opens an instance of a form, where the data can be amended.

- commenting a ticket - To add a comment, user needs to click 'Comment' button in ticket detailed view. This opens a form where the comment can be entered and submitted by clicking 'Add comment' button

- vote bug ticket - To vote for a bug, user needs to click 'I have this too' button in ticket detailed view. Then, vote is being added to the total votes amount. In case the user has already voted for the ticket, 'You can't vote twice' message will display

- make payment for feature ticket - To make a payment, user needs to click 'Pay' button in a specific feature detailed view, which opens payment template, where user can enter credit card details (please use test card number: 4242 4242 4242 4242 and do NOT enter your valid card details), select an amount that he/she wishes to contribute and submit the payment. Once the button has been clicked, it gets disabled to prevent from clicking it more than once. Also, payment will not be accepted if ticket status had been changed to 'Completed'.

- view user's profile - User can view his/her profile page by clicking 'User profile' link from the menu. 

- receive a notification email, once the ticket status has changed - Ticket author will receive an email informing of the ticket status change, once the status has been updated by administrator, so he/she will stay up-to-date with the work progress on their tickets.

Available to administrator/developer:
- changing tickets' statuses - This functionality can be accessed by clicking 'Tickets management' link from the menu and 'Bug Tickets' or 'Feature tickets' subsequently. The tickets are sorted by votes total (bugs) and payments total (features). Beside this Administrator can see who is the author of the ticket, what is the ticket's current status and when it was created. Tickets can also be filtered based on their status.Administrator is able to change statuses of the tickets that are being currently worked on. 

Tickets can be administered by a user with admin privileges and the panel can be accessed from the menu by clicking 'Tickets Management' from the menu (this option will not appear for guest or logged in users that do not have superuser rights). Once the admin panel is open, the tickets can be accessed by clicking 'Bug Tickets' or 'Feature Tickets' links. The tickets are sorted by votes (bugs) or payments total (features). There is also a filter available, that allows to filter the tickets based on their status. This is to help developer to determine which bug / feature should be worked on as first.

Few unit tests were written and they are located in tickets app. The purpose of these test is to prove that the templates display correctly and that signup function works with no issues. They can be run by typing `python3 manage.py tests.py`. The tests ran successfully and results can be found here.

## Installation

To run the appliaction on your local machine please follow the instructions below:

1. Clone the repository to your local drive by `git clone https://github.com/r-andy79/issue-tracker-project.git`
2. Create a virtual environment within the project folder (to create a virtual environment please follow the instructions specific to your operating system)
3. Run virtual environment
4. Install project dependencies using `pip install -r requirements.txt` command
5. Apply the migrations using `python manage.py migrate` command
6. Create a superuser using `python manage.py createsuperuser` command and provide the details as required
7. Run the project locally by typing `python manage.py runserver`

## Deployment

Application has been deployed to Heroku platform and is available under this [link](https://github.com/r-andy79/issue-tracker-project). In order to deploy the application to Heroku, the following steps were followed:

1. Installation of psycopg2
2. Installation of gunicorn
3. Installation of whitenoise
4. Export of all requirements to requirements.txt file
5. Creating a Procfile
6. Creating an application in Heroku
7. Linking PostgreSQL database to Heroku application
8. Setting environment variables in Heroku
9. Creating a Heroku remote
10. Pushing the application to Heroku
11. Creating a superuser on Heroku server

There are no differences between deployed and development version of the application.
