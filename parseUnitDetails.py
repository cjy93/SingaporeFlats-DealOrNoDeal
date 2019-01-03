import numpy as np
import os

# list of all HDB towns with SBF (Chinese, Nov18) 
# (Town naming according to HDB SBF format)
allTowns = ['Ang Mo Kio','Bedok','Bukit Batok','Bukit Merah','Bukit Panjang',
            'Choa Chu Kang', 'Clementi','Geylang','Hougang','Jurong East',
            'Jurong West','Kallang / Whampoa','Pasir Ris','Punggol','Queenstown',
            'Sembawang','Sengkang','Serangoon','Tampines','Toa Payoh', 
            'Woodlands','Yishun']

def getUnitDetails(fn='Merged_unitsDetails_DistToMrt.csv'):
    unitDetails = np.genfromtxt(fn, delimiter=",",skip_header=1,
                dtype=[('town','U24'),('rmType','U7'),('blk','U6'),
                    ('unitNum','U10'),('level','i4'),('sqm','i8'),
                    ('sellingPrice','i8'),('color','U12') ,
                    ('repurchasedFlat','U30'),('leaseLessThan60Yrs','U10'),
                    ('street','U30'),('probableCompletionDate','U10'),
                    ('deliveryPossessionDate','U30'),
                    ('leaseCommencementDate','U15'),
                    ('availableEthnicQuotaMl','U20'),
                    ('availableEthnicQuotaCh','U25'),
                    ('availableEthnicQuotaIn','U20'),('lastUpdate','U60'),
                    ('NearestMrt','U30'),('DistToMrt','f8'),
                    ('blkX','i8'),('blkY','i8')],
                missing_values=['na','-',''],filling_values=0, comments='!')
    return(unitDetails)

def getUnitDetails_subset_town_rmType(unitDetails, town, rmType):
    '''subset of unitDetails by town and room type
       rmType is either 4-Room or 5-Room
    '''
    subsetRmType = unitDetails[unitDetails['rmType'] == rmType]
    subsetRmTypeTown = subsetRmType[subsetRmType['town'] == town]
    return(subsetRmTypeTown)


def getEstatesMaturity(fn = 'Number of Applications Received for 3-room and bigger flats as at 19 Nov 2018.csv'):
    ''' Returns a dict of town:maturity states
        Where town is HDB/URA town name
    '''
    estatesMaturity  = np.genfromtxt(fn, delimiter=",",skip_header=1,
                dtype=[('town','U24'),('FlatType','U50'),('No_of_Units','i8'),
                    ('Number_of_applicants','i8'),
                    ('Rate_Non_Elderly_First_timers','f8'),
                    ('Rate_Non_Elderly_Second_timers','f8'),
                    ('Rate_Non_Elderly_Overall','f8'),('Mature_Estates','U8')],
                missing_values=['na','-','','NA'],filling_values=0)

    estatesMaturityTown= estatesMaturity['town']
    estatesMaturityMature= estatesMaturity['Mature_Estates']
    
    estatesMaturityCon= zip(estatesMaturityTown,estatesMaturityMature)
    
    # make unique sets of 'towns' and 'Mature Estates'
    estatesMaturityCon =dict(set(estatesMaturityCon))
    
    # this dataset combines both JE/JW as 1 item
    # to split it manually
    estatesMaturityCon['Jurong East'] = estatesMaturityCon['Jurong East / West'] 
    estatesMaturityCon['Jurong West'] = estatesMaturityCon['Jurong East / West'] 
    del(estatesMaturityCon['Jurong East / West'])
    
        
    # This dataset also combines Kallang/Whampoa into 1. 
    # URA planning area only has Kallang, so copy Kallang/Whampoa to Kallang
    estatesMaturityCon['Kallang'] = estatesMaturityCon['Kallang / Whampoa']
    del(estatesMaturityCon['Kallang / Whampoa'])

    return(estatesMaturityCon)


def getMaturityColour():
    ## Mature and Non Mature estates
    estatesMaturity  = np.genfromtxt("Number of Applications Received for 3-room and bigger flats as at 19 Nov 2018.csv",     delimiter=",",skip_header=1,
                    dtype=[('town','U24'),('FlatType','U50'),('No_of_Units','i8'),('Number_of_applicants','i8'),
                          ('Rate_Non_Elderly_First_timers','f8'),('Rate_Non_Elderly_Second_timers','f8'),
                          ('Rate_Non_Elderly_Overall','f8'),('Mature_Estates','U8')],
                    missing_values=['na','-','','NA'],filling_values=0)

    estatesMaturityTown= estatesMaturity['town']
    estatesMaturityMature= estatesMaturity['Mature_Estates']
    estatesMaturityCon= zip(estatesMaturityTown,estatesMaturityMature)

    # make unique sets of 'towns' and 'Mature Estates'
    estatesMaturityCon =set(estatesMaturityCon)

    nMature = []
    yMature = []


    for town in estatesMaturityCon:
        if town[1]=='N':
            nMature.append(town[0])
        elif town[1]=='Y':
            yMature.append(town[0])
    nMature.append('Jurong East')
    nMature.append('Jurong West')
    nMature.remove('Jurong East / West')
    print("Mature estates : \n{}".format(yMature))
    print("Non Mature estates : \n{}".format(nMature))

    Mature = []
    for repeatMature in range(len(yMature)):
        Mature.append('Mature')


    NonMature = []
    for repeatMature in range(len(yMature)):
        NonMature.append('Non Mature')

    ## Making labels in order
    label = yMature + nMature
    print(label)

    # Make different colour for Mature and Non Mature estates  
    values= Mature + NonMature
    keys = label
    
    return(yMature,nMature,keys,values)


def genPopupTxtDictByTown():
    unitDetails = getUnitDetails()
    estatesMaturity = getEstatesMaturity()
    
    #friendly display for Y/N mature/nonMature
    ynMaturityMapping = {'Y': 'Mature Estate', 'N': 'Non Mature Estate'}
    
    # get all the URA planning area town name. 
    # estate maturity has already been process to the URA format
    allTownsUra = estatesMaturity.keys()
    
    # loop thru town and rmType to gen the popup text
    allTownsPopupDict = {}
    rmTypesList = ['4-Room', '5-Room']
    for townUra in allTownsUra:
        # map URA/HDB towns
        if townUra == 'Kallang':
            town = 'Kallang / Whampoa'
        else:
            town = townUra
        thisTownMaturity = estatesMaturity[townUra]
        thisTownMaturityStr = ynMaturityMapping[thisTownMaturity]
        thisTownPopupHtml = '<b><u>%s</u></b><br /><i>%s</i><br />' % (
                            town, thisTownMaturityStr)
        #print('townUra: ', townUra, ' townHdb: ', town, 
        #      ' maturity: ',thisTownMaturityStr)
        for rmType in rmTypesList:
            #print('    rmType:', rmType)
            unitDetailsSubset = getUnitDetails_subset_town_rmType(
                                                    unitDetails, town, rmType)

            qtyThisTown = len(unitDetailsSubset)
            if qtyThisTown > 0:
                minPrice = np.min(unitDetailsSubset['sellingPrice'])
                maxPrice = np.max(unitDetailsSubset['sellingPrice'])
                medianPrice = np.median(unitDetailsSubset['sellingPrice'])
                minPriceStr = '$%.1fk' % (minPrice/1000.0,)
                maxPriceStr = '$%.1fk' % (maxPrice/1000.0,)
                medianPriceStr = '$%.1fk' % (medianPrice/1000.0,)
            else:
                minPriceStr = '<i>NA</i>'
                maxPriceStr = '<i>NA</i>'
                medianPriceStr = '<i>NA</i>'

            #thisTownRmTypeHtml = """<b>%s</b><br />
            #                     No of units: %i<br />
            #                     MinPrice: %s<br />
            #                     MedianPrice: %s<br />
            #                     MaxPrice: %s<br />""" % (
            #                        rmType, qtyThisTown, minPriceStr, 
            #                        medianPriceStr, maxPriceStr)
            thisTownRmTypeHtml = """<b>%s</b><br />
                                 No of units: %i<br />
                                 MedianPrice: %s<br />""" % (
                                    rmType, qtyThisTown, medianPriceStr)

            #print(thisTownRmTypeStr)
            thisTownPopupHtml = thisTownPopupHtml + thisTownRmTypeHtml
        #print(thisTownPopupHtml)
        allTownsPopupDict[townUra] = thisTownPopupHtml

    #print(allTownsPopupDict)
    return(allTownsPopupDict)







