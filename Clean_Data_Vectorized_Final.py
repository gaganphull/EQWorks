import pandas as pd
import numpy as np


# Making the Dataframes Print on One Line
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.get_option('display.width')
pd.set_option('expand_frame_repr', False)

# Reading the csv files of interest
# Number of Initial Records: 22024
df = pd.read_csv('/Users/gagan/Desktop/PycharmProjects/LeoLi Interview/ws-data-pandas-main/data/DataSample.csv')
dfPOI = pd.read_csv('/Users/gagan/Desktop/PycharmProjects/LeoLi Interview/ws-data-pandas-main/data/POIList.csv')


# Leaving the Option to Run the File in "Debug Mode"
# In "Debug Mode" Only the File is Run Against Only m Records Thus Saving Time
# m=15
# df2 = df.head(m)


# Finding The TimeSt's That Are Duplicates
series = df[df.columns[1]].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_TimeSt_Values = series[series].index
# Dropping The Duplicates
df = df.drop(Drop_TimeSt_Values)


# Finding the Geoinfo's That are Duplicates
series2 = df.iloc[:,2:7].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_GeoInfo_Values = series2[series2].index
# Dropping The Duplicates
df = df.drop(Drop_GeoInfo_Values)
# Final Number of Records: 5543



# Finding the POIs That are Duplicates
seriesPOI = dfPOI.iloc[:,1:3].duplicated()
# Creating a Boolean Array to Identify Duplicates
Drop_POI_Values = seriesPOI[seriesPOI].index
# Dropping The Duplicates
dfPOI = dfPOI.drop(Drop_POI_Values)
# Final Number of POIs: 3


def Distance_From_POI(df, dfPOI):
    # Creating Dataframe to Hold Distance Values
    dfKM = pd.DataFrame(data=None)
    # Iterating Over The Number of POIs of Interest
    for n in range(0, len(dfPOI.iloc[:, 1])):
        # Extracting Longitude and Latitude Data From DataSample
        df2 = df.iloc[:, 5:7]
        # Extracting Longitude and Latitude Data From POIList
        df2['POI Latitude'] = dfPOI.iloc[n, 1]
        df2['POI Longitude'] = dfPOI.iloc[n, 2]
        # Converting to Longitude and Latitude Values to Radians
        df2 = np.radians(df2)
        # Calculating Distance Based on the Haverside Formula
        df2['dLat'] = df2['POI Latitude'] - df2['Latitude']
        df2['dLon'] = df2['POI Longitude'] - df2['Longitude']
        df2['a'] = np.sin(df2['dLat'] / 2) ** 2 + np.cos(df2['Latitude']) * np.cos(df2['POI Latitude']) * np.sin(df2['dLon'] / 2) ** 2
        df2['c'] = 2 * np.arcsin(np.sqrt(df2['a']))
        df2['km'] = 6367 * df2['c']
        # Appending Result to dfKM
        dfKM['{}'.format(dfPOI.iloc[n, 0])] = df2['km']
    # Assigning POI to DataSample Request
    df['POI_Min_Dist'] = dfKM.idxmin(axis=1)
    return
   
# Calling the POI Distance Function
POI_index = Distance_From_POI(df,dfPOI)
print(df)


