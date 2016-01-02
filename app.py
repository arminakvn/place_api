# install pip if you dont have it: https://pypi.python.org/pypi/pip
# intall dependencies: pip install simplejson, cartodb, pymonfo
## excelent guide here: http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import sys, getopt
import json, simplejson, urllib
from read_csv_to_dict import read_csv, write_csv
from write_to_mongo import getMongoColl, writeMongoDoc, writeMongoColl
from cartodb import CartoDBException
from place_results import cleanData
from place_details import getPlaceDetails
from credentials import cartoCred, gKey

gKey = gKey()
cl = cartoCred()
try:
#    print(cl.sql('select * from msapoint'))
   points = cl.sql('select * from msapoint')
except CartoDBException as e:
   print("some error ocurred", e)


def main(argv):
    inputfile = ''
    outputfile = ''
    radius = ''
    qrtr = ''
    
    try:
        opts, args = getopt.getopt(argv,"hr:t:k:",[ "radius=", "types=", "keyword="])

    except getopt.GetoptError:
        print 'app.py -r <radius> -t <types> -k <keyword>'
        sys.exit(2)
    
    RADARSHEARCH_BASE_URL = 'https://maps.googleapis.com/maps/api/place/radarsearch/json'
    print "RADARSHEARCH_BASE_URL", RADARSHEARCH_BASE_URL
    def placeRadar(location, radius, types, keyword, key, **geo_args):
        geo_args.update({
            'location': location,
            'radius': radius,
            'types': types,
#             'keyword': keyword,
            'key': key
        })
        url = RADARSHEARCH_BASE_URL + '?' + urllib.urlencode(geo_args)
        print "url", url
        result = simplejson.load(urllib.urlopen(url))
        return result
   
    for opt, arg in opts:
        if opt == '-h':
            print 'app.py -r <radius> -t <types> -k <keyword>' 
            sys.exit()
        elif opt in ("-r", "--radius"):
            radius = arg
        elif opt in ("-t", "--types"):
            types = arg
        elif opt in ("-k", "--keyword"):
            keyword = arg
        else:
            keyword = ""
    
    raw_matrix = points['rows']
    sresults = []
    sresults_dict = {}
    for each_line in raw_matrix:
        locations = str(each_line['lng']) + ',' + str(each_line['lat'])
        each_line['placeRadar'] = placeRadar(locations, radius=radius, types=types, keyword="", key=gKey)
        point_places=[]
        for each in each_line["placeRadar"]["results"]:
            point_places.append(each["place_id"])
        point_place_dict = {
            "point_id": each_line["id"],
            "places": point_places
            }
        sresults.append(point_place_dict)
        # this is saving a collection for the results of the radar search and is optional!!!
#         mongoCollection = getMongoColl('place_db', 'chicago')
#         written = writeMongoDoc(mongoCollection, point_place_dict)
    # it is possible that there are overlapping between each radar search area, so just getting the uniq place_ids
    uniqs = cleanData(sresults)
    # making the call to the place details api
    details_results = getPlaceDetails(uniqs)
    # saving the cleaned and selected fields of the results
    print "types", types
    mongoCollection = getMongoColl('place_db', types)
    written = writeMongoColl(mongoCollection, details_results)
if __name__ == '__main__':
    main(sys.argv[1:])