# StarWars Favorites' App

## Task Details

### Problem Statement

To Make a simple favourites app that lets us view/favourite Star Wars data.

The app:

1. MUST load planets and movies from the JSON API provided by https://swapi.co/
2. MUST support searching by planet by - Title
3. SHOULD list Movies/Planets showing - Title, Image (if present), Add Button
4. MUST allow saving of planets to a local store or service using the Add Button
5. MUST list SavedTitle showing Title/Image

### Documentaion of Solution

The application supports following routes :

`/`

`/planets/`

`/favourite/planets`

`/favourite/movies`

`/saved/planets`

`/search`


## Installing the Deps & Running the application (Tested using Python 3.5.2)

```
virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```









