<a href="https://skyhop.org"><img src="https://app.skyhop.org/assets/images/skyhop.svg" width=200 alt="skyhop logo" /></a>

----

This project is just a quick 'n dirty wrapper around the XCSoar python library.

You can upload an IGC file through the web interface, and you'll get a JSON blob with some data back.

## Running the app

For development purposes you can use the flask development server:

```
export FLASK_APP=main.py
python -m flask run
```

For production (through Docker) you can do the following (in the root of the project):

```
docker build .
docker run [with the tag you get]
```

