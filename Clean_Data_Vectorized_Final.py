import pandas as pd
import numpy as np
import numba as nb
from geopy.distance import geodesic


# Making the Dataframes Print on One Line
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.get_option('display.width')
pd.set_option('expand_frame_repr', False)

# Reading the csv files of interest
# Number of Initial Records: 22024
df = pd.read_csv('/Users/gagan/Desktop/PycharmProjects/LeoLi Interview/ws-data-pandas-main/data/DataSample.csv')
dfPOI = pd.read_csv('/Users/gagan/Desktop/PycharmProjects/LeoLi Interview/ws-data-pandas-main/data/POIList.csv')

# Creating a Copy of The Above Dataframe
df2 = df


# Leaving the Option to Run the File in "Debug Mode"
# In "Debug Mode" Only the File is Run Against Only m Records Thus Saving Time
# m=15
# df2 = df.head(m)


# Finding The TimeSt's That Are Duplicates
series = df2[df2.columns[1]].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_TimeSt_Values = series[series].index
# Dropping The Duplicates
df2 = df2.drop(Drop_TimeSt_Values)


# Creating a Copy of The Working Dataframe
df3 = df2
# Finding the Geoinfo's That are Duplicates
series2 = df3.iloc[:,2:7].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_GeoInfo_Values = series2[series2].index
# Dropping The Duplicates
df2 = df2.drop(Drop_GeoInfo_Values)
# Final Number of Records: 5543


# Creating a Copy of The Second Dataframe of Interest
dfPOI2 = dfPOI
# Finding the POIs That are Duplicates
seriesPOI = dfPOI2.iloc[:,1:3].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_POI_Values = seriesPOI[seriesPOI].index
# Dropping The Duplicates
dfPOI2 = dfPOI2.drop(Drop_POI_Values)
# Final Number of POIs: 3


# Creating Numpy Arrays for the POI Distance Function
# The POI Distance Function was Created for the Common Problems
# Longitude and Latitude Data From The Data Sample
np_requests = np.array(df2.iloc[:,5:7])
# Longitude and Latitude Data From The POI List
np_POIs = np.array(dfPOI2.iloc[:,1:3])
# Names of the POIs From the POI List Minus Duplicates
np_POI_map = np.array(dfPOI2.iloc[:,0])

# POI Distance Function
def Distance_From_POI (np_requests, np_POIs,np_POI_map):

    # Container Array for the POIs
    POI_index = np.array

    # Counts Number of Records Inserted Into POI_Index
    Count2 = 0

    # Iterating Over the Number of Requests in the Data Sample
    for n in np_requests:

        # Container Array for the Distances Values
        Dist_Values = np.array([])

        # Counts Number of Records Inserted Into Dist_Values
        Count = 0

        # Iterating Over the Number of POIs in the POI List
        for m in np_POIs:

            # Calculating All the Distances Between the Data Sample and the POIs:

            # Method found at :
            # https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas
            # Assigning Variables for the Latitudes and Longitudes
            lat1 = n[0]
            lon1 = n[1]
            lat2 = m[0]
            lon2 = m[1]

            # Converting Latitude and Longitude Values to Radians
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

            # Calculating Distance Using the Haverside Formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
            c = 2 * np.arcsin(np.sqrt(a))
            km = 6367 * c

            # Storing the Distance Values in Kilometers
            Dist_Values = np.insert(Dist_Values,Count,km)

            # Adding 1 to the Count to Ensure Proper Indexing
            Count = Count + 1

        # Finding the Index of the POI that has the Shortest Distance to this Data Sample
        values_index = np.argmin(Dist_Values)

        # Assigning the Data Sample to the Closest POI
        POI_index = np.insert(POI_index,Count2,np_POI_map[values_index])

        # Adding 1 to the Count to Ensure Proper Indexing
        Count2 = Count2 + 1

    # Returning the Data Sample - POI Pairs
    return POI_index


# Calling the POI Distance Function
POI_index = Distance_From_POI(np_requests,np_POIs,np_POI_map)

# Adding a Column to the Original DataFrame
# This Column Associates the Data Samples to Their Closest POI
df2['POI_Min_Dist'] = POI_index[0:-1]

# Printing the Result
print(df2)


