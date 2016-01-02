from cartodb import CartoDBAPIKey


# cartodb credentials:
API_KEY =''
cartodb_domain = ''

# google api key
google_key = ''

def cartoCred():
    cl = CartoDBAPIKey(API_KEY, cartodb_domain)
    return cl

def gKey():
    return google_key