def produceOpenPerWeek(detail, deltawk):
     cur = {
            'place_id': detail['result']['place_id'],
            'name': detail['result']['name'],
    #                 'open_hrs': detail['result']["opening_hours"],
            'type': detail['result']["types"],
    #                 'location': detail['result']["geometry"],
            'lat': detail['result']["geometry"]['location']['lat'],
            'lng': detail['result']["geometry"]['location']['lng'],
            'week_total_open': deltawk/86400, # make it on a day - 60 * 60 * 24
     }
     return cur