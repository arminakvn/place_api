If you don't have it already, install `pip`,if you are on mac, use `homebrew` (install it from [here](http://brew.sh/)), on linux use `apt-get`:

```
brew install pip
``` 
or for a linux machine:
```
sudo apt-get install pip
```

put in your credentials in the `credentials.py` file.    
make sure to install the requirements through either:
```
pip install -r requirements.txt
``` 
or
```
pip install cartodb, pymongo, simplejson
```

in command-line, `cd` to the project folder and run `python app.py -h` to see the available options.
run the application for searching with 10,000 meters radius around each [point-grid](https://arminavn.cartodb.com/viz/f5c5484e-b011-11e5-b2db-0ecfd53eb7d3/public_map) for the type of food with:
```
python app.py -r 10000 -t food
```

This will use radarsearch endpoint to search the google places api for up to 200 places in the set type of food, then makes them into a unique list and uses the details endpoint to get the information for open and close times from the google's place api,sums the total open hours for each place and saves them into a `mongodb` database running on bitnami+google compute instances. Each type makes it's own collection, which could exported to csv using the following:

```
mongoexport --host 146.148.61.119 --authenticationDatabase admin --username root --password 67yX8Fuw --collection food --csv --fields place_id,name,type,lat,lng,week_total_open --db place_db --out placedb_food.csv
```


