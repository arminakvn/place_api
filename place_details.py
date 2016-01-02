import time
from datetime import datetime
import sys, getopt
import json, simplejson, urllib
from data_products import produceOpenPerWeek
detail_results = []
DETAILS_BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"
key='AIzaSyAmOSpEfX9QrGlbZXOJsS1T_phh5ox9LrE'

def placeDetails(place_id, key, **geo_args):
        geo_args.update({
            'placeid': place_id,
             'key': key
        })
        url = DETAILS_BASE_URL + '?' + urllib.urlencode(geo_args)
        result = simplejson.load(urllib.urlopen(url))
        return result
def getPlaceDetails(uniqs):
    count = 1
    places_details = []
    for each_placeid in uniqs:
        detail = placeDetails(each_placeid, key)
#         deltawk_dt = datetime.strptime('0000-1', "%H%M-%d") - datetime.strptime('0000-1', "%H%M-%d")
#         deltawk = deltawk_dt.total_seconds()
        deltawk = 0
        
        # check if there is any openning hours data
        try:
            opening_hours = detail['result']["opening_hours"]
       
            for each_period in opening_hours["periods"]:
                try:
                    if (each_period["close"]["day"] == 0) and (each_period["open"]["day"] == 6):
                        time_str_c = datetime.strptime('%s-%s'%(each_period["close"]["time"], str(8)), "%H%M-%d")
                        time_str_o = datetime.strptime('%s-%s'%(each_period["open"]["time"], str(int(each_period["open"]["day"])+1)), "%H%M-%d")
                    else:
                        time_str_c = datetime.strptime('%s-%s'%(each_period["close"]["time"], str(int(each_period["close"]["day"])+1)), "%H%M-%d")
                        time_str_o = datetime.strptime('%s-%s'%(each_period["open"]["time"], str(int(each_period["open"]["day"])+1)), "%H%M-%d")                
                except:
                    print "except opening_hours", opening_hours
                    if opening_hours['periods'] == [{'open': {'day': 0, 'time': '0000'}}]:
                        time_str_c = datetime.strptime('1900-01-08 00:00:00', '%Y-%m-%d %H:%M:%S')
                        time_str_o = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                # calculate delta between close and open
                deltime = time_str_c - time_str_o
                # add they delta for the day to the delta for a week
                deltawk += deltime.total_seconds()
                if deltawk < 0:
                    print each_period
#                 print deltawk
        except:
            print "no openning hours data"
            pass
        try:
            cur = produceOpenPerWeek(detail, deltawk)
            detail_results.append(cur)
        except:
            print 'cur object could not created'#, detail['result']
            pass
#         if count == 8:
#             break
#         else:
#             count +=1
    return detail_results
    