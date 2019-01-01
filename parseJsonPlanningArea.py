import json
import os
print(os.getcwd())

allTowns= ['Ang Mo Kio','Bedok','Bukit Batok','Bukit Merah','Bukit Panjang','Choa Chu Kang',
                'Clementi','Geylang','Hougang','Jurong East','Jurong West','Kallang / Whampoa','Pasir Ris','Punggol',
                'Queenstown','Sembawang','Sengkang','Serangoon','Tampines','Toa Payoh', 'Woodlands','Yishun']

# the planning area dataset calls 'Kallang', but hdb calls it 'Kallang / Whampoa'
# change manually
allTowns_URA_naming = allTowns.copy()
allTowns_URA_naming[11] = 'Kallang'




def getSubsetPlanningArea(jsonFn = 'MP14_PLNG_AREA_NO_SEA_PL.json'):
    ''' Get subset of the planning areas that is available for SBF  from planning area json'''
    # Load a local file
    # ori data src: data@gov
    # convert kml to geojson https://github.com/mrcagney/kml2geojson
        
    with open(jsonFn) as f:
        mapJsonData = json.load(f)
    # do a subset of all the planning area, clear out all areas first, add back 1by1
    mapJsonDataSubset = mapJsonData.copy()
    mapJsonDataSubset['features'] = []

    #print('jsondata: ', (mapJsonData['features'][0])['properties']['name'])
    #print('jsondata: ', (mapJsonata['features'][0].keys()))
    #print('jsondata: ', (mapJsonata['features'][0]['geometry']['coordinates']))
    
    
    
    for feature in mapJsonData['features']:
        mapTownName = feature['properties']['name']
        mapTownName = mapTownName.title() # cap 1st alpha of each word, to match allTowns caps
        if mapTownName in allTowns_URA_naming:
            #print(mapTownName)
            mapJsonDataSubset['features'].append(feature)
        else:
            #print('not in: ', mapTownName)
            pass
    return(mapJsonDataSubset)


#for i,features in enumerate(mapJsonData['features']):
#    print(i,features['properties']['name'])

#for i,features in enumerate(mapJsonDataSubset['features']):
#    print('subset ', i,features['properties']['name'])


def getMeanCoordByTown(mapJsonDataSubset):
    ''' Calc mean coord based on planning area polygon
        of course this is one of the many methods available to get 'center' of polygon'''
    meanCoordByTown = {}
    for feature in mapJsonDataSubset['features']:
        town = feature['properties']['name']
        #print(town)    
        try:
            coordinates = feature['geometry']['coordinates']
        except KeyError:
            # Jurong East has this werid 2 part geo.
            #print('KeyError. Town: ', town)
            # mapJsonDataSubset['features'][9]['properties']['name']
            #print(feature['geometry']['geometries'][0].keys()) #['coordinates'][0])
            coordinates = feature['geometry']['geometries'][0]['coordinates'] # pick the 1st part
            #coordinates = [[[1,2,3],[4,5,6]]] # dummy
    
        sumCoordX = 0
        sumCoordY = 0
        sumPoints = 0
        for coordList in coordinates[0:4]:
            #print(town, len(coordList)
            for coord in coordList:
                #print(town, len(coord))
                sumCoordX = sumCoordX + coord[0]
                sumCoordY = sumCoordY + coord[1]
                sumPoints = sumPoints + 1
    
        meanX = sumCoordX / sumPoints
        meanY = sumCoordY / sumPoints
        meanCoordByTown[town] = (meanY, meanX) # swap the order to suit the ipyleaflet format
    return(meanCoordByTown)

if __name__ == '__main__':
    subset = getSubsetPlanningArea()
    print('meanCoordByTown', getMeanCoordByTown(subset))

