Hello! Thank you for reviewing my application.

The whole app is build basing on docker-compose, django REST framework, PosgreSQL database.

To build an app open a terminal in the main folder location and use:
docker-compose build .

To run unit tests and test to check for code convention run:
docker-compose run app sh -c "python manage.py test && flake8"

To run the application (Later go to localhost:8000 using your browser, remember to turn off ModHeader if you use one):
docker-compose up

Performance considerations:
    1. Since we're building a thumbnail hosting service, IMO it's much better to build all the available thumbnails
    at the start, instead of creating them when we receive a request. Usage of space is less important than usage
    of computer's resources.
    2. It could be improved by checking if thumbnail already exists, if not creating it and saving for future use.
    (Some thumbnail sizes might not be used even once).

Things to improve:
    1. Right now app doesn't support changing of plans for the user. It should be done by checking the difference
    between AccountSize.thumbnail_sizes of current plan and new plan. Then in update_or_create method (to be checked
    further) files for thumbnail sizes not in new plan should be removed, and new ones created.
    2. Token authentication should be added. The project uses only basic authentication, since I don't want you
    to have to authenticate yourself, then get token etc.


Time it took me to build an app:
    4 evenings, approx. 4 hrs/evening of coding. This does not include planning process, which was also a vital
    part of project construction.

