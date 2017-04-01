from .api_adapter import API_adapter
# from app.crawler.crawler import crawler
from flask import render_template, request
from random import randint
from . import app
import json
# index view function suppressed for brevity


# index page
@app.route("/")
def show_index_page():
    return render_template('index.html')

# index page
@app.route("/login.html")
def show_login_page():
    return render_template('login.html')

# result page
@app.route("/result", methods=['GET'])
def show_random():
    location = request.args.get('location')
    cata = request.args.get('cata')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    adapter = API_adapter()
    if location is None:
        locations,loc_latlon = adapter.get_place(address=None, category_filter=cata,lat=lat,lon=lon)
    else:
        locations,loc_latlon = adapter.get_place(address=location, category_filter=cata)
            #flickr.photos.geo.getLocation(photo_id=28237538626_b1240b244f_c)

    print locations
    return render_template('result.html', locations=locations,lat=loc_latlon['lat'],lon=loc_latlon['lng'])


# # save my favorite
# @app.route("/save/favorite", methods=['post'])
# def test_post():
#     '''
#     To be implemented with DB connection
#     '''
#     print(request.json)
#     return("Success!")