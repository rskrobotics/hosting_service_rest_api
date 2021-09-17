To build an app open a terminal in the main folder location and use:
docker-compose build

To run unit tests and test to check for code convention run:
docker-compose run app sh -c "python manage.py test && flake8"

To run the application (Later go to localhost:8000 using your browser, remember to turn off ModHeader if you use one):
docker-compose up

User authentication:
localhost:8000/login to attain token
localhost:8000/logout to delete token

Performance considerations:
    1. Since we're building a thumbnail hosting service, IMO it's much better to build all the available thumbnails
    at the start, instead of creating them when we receive a request. Usage of space is less important than usage
    of server's resources.
    2. It could be improved by checking if thumbnail already exists, if not creating it and saving for future use.
    (Some thumbnail sizes might not be used even once).

Things to improve:
    1. Right now app doesn't support changing of plans for the user. It should be done by checking the difference
    between AccountSize.thumbnail_sizes of current plan and new plan. Then in update_or_create method (to be checked
    further) files for thumbnail sizes not in new plan should be removed, and new ones created.
    2. Application needs A LOT more unit tests.


