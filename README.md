# Issue Tracker Application
## 4th Milestone Project - Full Stack Frameworks with Django - Code Institute

Issue Tracker is a ticketing system that can be used to manage queries related to other application and to keep track of progress done. The primary entity in the Issue Tracker is a ticket describing a user's issue. The application allows users to create tickets, comment on tickets, and show the status of the ticket. Issues come in two varieties - 'bugs' that will be fixed for free and, 'features' that will be developed for money. To help prioritize the work, users will be able to upvote bugs (signifying 'I have this too') and upvote feature requests (signifying 'I want to have this too'). While upvoting bugs is free, to upvote a feature request, users would need to pay some money. The highest paid feature will be developed as first.

## UX
The applcation can serve anyone ... 

I wanted the user interface to be simple and consistent throughout the whole application. The data is presented in a clean and organized way. User has easy access to all the functions from the navigation bar on larger screens or a mobile menu that is triggered by the 'hamburger' button.

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
As an administrator / developr:
* I want to be able to perform all the operations that user can do,
* I want to be able to update the ticket status, to give user a feedback on a progress

## Features
Application allows users to create two type of tickets: bugs and features. Bugs should be used to report any issues related to the application and features should be raised whenever a user comes up with a new functionality idea that could be implemented. Users can upvote bugs, if they have the same issue to prioritise fixing it. Features will be developed based on the total amount contributed towards a specific feature.
The application has following functionalities:

Available to everyone:

- [x] browsing tickets
- [x] filtering and sorting tickets
- [x] viewing details of a specific ticket

Available to registered users:

- [x] create a new ticket

To create a new ticket, user needs to click 'New Ticket' option from the menu and fulfill the form specifying ticket's subject, type (bug or feature) and providing a description of an issue or a new functionality suggestion,

- [x] comment a ticket
- [x] vote bug ticket
- [x] make payment for feature ticket
- [x] view a profile
- [x] receive a notification email, once the ticket status has changed

Available to administrator/developer:
- [x] changing tickets' statuses

Tickets can be administered by a user with admin privileges and the panel can be accessed from the menu by clicking 'Tickets Management' from the menu (this option will not appear for guest or logged in users that do not have superuser rights). Once the admin panel is open the tickets can be accessed by clicking 'Bug Tickets' or 'Feature Tickets' links. The tickets are sorted by votes (bugs) or payments total (features). This is to help developer to determine which bug / feature should be worked on as first.

## Technologies Used
- [Python](https://www.python.org/) - used for general-purpose programming and writing the logic of the application,
- [Django](https://www.djangoproject.com/) - used for serving templates, performing CRUD operations and administrative functions,
- [PostgreSQL](https://www.postgresql.org/) - used for storing the application data,
- [Jinja templating language](https://jinja.palletsprojects.com/en/2.10.x/) - used for incorporating Python code into HTML templates,
- [HTML](https://html.spec.whatwg.org/) - used for building the structure of the interface,
- [CSS](https://docs.ckan.org/en/ckan-2.7.3/contributing/css.html) - used for custom styling of some elements,
- [JavaScript / jQuery](https://jquery.com/) - used for triggering certain functions that set timeout on Django messages or disable buttons, preventing them from being double clicked,
- [Bootstrap](https://getbootstrap.com/) - used for building the visual side of the application,
- [Stripe API](https://stripe.com/en-ie) - used for processing card payments from the application (please use test card number: 4242 4242 4242 4242). Please do NOT enter your valid card details.

## Testing

## Installation
To run the appliaction on your local machine please please create a virtual environment using command python3 -m venv /path/to/new/virtual/environment. Once created you can clone the repo: git clone https://github.com/r-andy79/issue-tracker-project.git. 
Run pip3 install -r requirements.txt 
apply the migrations
## Deployment
## Acknowledgements