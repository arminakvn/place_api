from sets import Set
holder_list = []
holder_dict = {}
def cleanData(sresults):
    for each in sresults:
        eachplaces = each["places"]
        for pl in eachplaces:
            holder_list.append(pl)
    uniq_places = Set(holder_list)
    return uniq_places