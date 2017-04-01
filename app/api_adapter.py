from flickrapi import FlickrAPI
import json, os, sys,urllib
import io

class API_adapter(object):

    def __init__(self):
        '''
        Load Oauth keys
        '''

        FLICKR_PUBLIC = '73a0bbb73ee9d6d1cd8b6a03ae56b20b'
        FLICKR_SECRET = '318ac4fa3350b331'
        self.GoogleAPIkey = 'AIzaSyD6RtWqUNMQvRwPFyVlwH_WsGvTyHzm5NI'
        self.flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        # self.extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
        self.extras='url_m,geo'
        
    def GoogPlac(self,address,key):
        #making the url
        AUTH_KEY = key
        MyUrl = ('https://maps.googleapis.com/maps/api/geocode/json'
                   '?address=%s'
                   '&key=%s') % (address.replace(" ","+"), AUTH_KEY)
        #grabbing the JSON result
        response = urllib.urlopen(MyUrl)
        jsonRaw = response.read()
        jsonData = json.loads(jsonRaw)
        return jsonData['results'][0]['geometry']['location']

    def get_place(self, address, category_filter=None,lat=0,lon=0):
        if address is None:
            params = {
                'lat': lat,
                'lon':lon,
                'per_page':10,
                'extras':self.extras,
            }
            location={'lat':lat,'lng':lon}
        else:
            location = self.GoogPlac(address,self.GoogleAPIkey)
            params = {
                'lat': location['lat'],
                'lon':location['lng'],
                'per_page':10,
                'extras':self.extras,
            }
        if category_filter:
            params['text'] = category_filter
        
        cats=self.flickr.photos.search(**params)
        photos = cats['photos']['photo']
        # loc=self.flickr.photos.geo.getLocation(photo_id='28060447005')
        photo_info=[]
        for i in xrange(len(photos)):
            # loc=self.flickr.photos.geo.getLocation(photo_id=photos[i]['id'])['photo']['location']
            photo_info.append({'id':i,'name':photos[i]['id'],'lat':photos[i]['latitude'],'lng':photos[i]['longitude'],'img':photos[i]['url_m'],'url':'www.flickr.com/photos/' + photos[i]['owner'] +'/' + photos[i]['id']})
        # photo_info = [{'id':photos['photo'][i]['id'],'img':photos['photo'][i]['url_m'],'url':'www.flickr.com/photos/' + photos['photo'][0]['owner'] +'/' + photos['photo'][i]['id']} for i in range(len(photos))]
        # photo_info = [[photos[i]['id'],self.flickr.photos.geo.getLocation(photo_id=photos[i]['id'])['photo']['location']['latitude'],self.flickr.photos.geo.getLocation(photo_id=photos[i]['id'])['photo']['location']['longitude'],photos[i]['url_m'],i,'www.flickr.com/photos/' + photos[i]['owner'] +'/' + photos[i]['id']] for i in range(len(photos))]
        return [photo_info,location]
