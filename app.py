################################################################################
# STAR WARS SWAPI ROUTE
################################################################################
from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('form.html')



@app.route('/results')
def results():
    apiUrl = 'https://swapi.py4e.com/api/'
    character_id = request.args.get('character_id')
    response_people = requests.get(apiUrl + 'people/' + character_id)
    character = json.loads(response_people.content)

    try:
        films = character['films']
        response_films = list()
        for film in films:
            response_films.append(json.loads(requests.get(film).content))
    except KeyError:
        response_films = ''

    try:
        response_homeworld = requests.get(character['homeworld'])
        homeworld = json.loads(response_homeworld.content)
    except KeyError:
        homeworld = ''

    context = {
        'character': character, 
        'films': response_films,
        'homeworld': homeworld,
        }
    return render_template('results.html', **context)

 

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True, port=3000)
