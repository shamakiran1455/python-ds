import pandas as pd
import numpy as np

def ans_one():
    """
    After instructions to merge all data, This function should return a DataFrame with 20 columns and 15 entries.
    """

    #Starting with energy data, exclude the header and footer
    energy = pd.read_excel("./data/Energy_Indicators.xls", skiprows=18, skip_footer=38, header=None)
    # Exclude the two first columns
    energy.drop([0, 1], axis=1, inplace=True)
    # Make your header
    energy_col = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.columns = energy_col
    # Treat your missing values
    energy.replace("...", np.NaN, inplace=True)
    # Convert "Energy Supply" to gigajoules
    energy["Energy Supply"] = energy["Energy Supply"].apply(lambda x: x*1000000)
    # Replace the numbers in countries names
    energy["Country"] = energy["Country"].replace(to_replace=["0","1","2","3","4","5","6","7","8","9"], value="", regex=True)
    # Cleaning data
    energy["Country"].replace(to_replace={
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Republic of Korea": "South Korea",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
    }, inplace=True)
    # Cleaning strings with "()"
    energy["Country"] = energy["Country"][energy["Country"].notnull()].apply(
    lambda x: x.split(" (")[0] if x.endswith(")") else x)

    # Now, GDP data, skip the header
    GDP = pd.read_csv("./data/world_bank.csv", skiprows=4)
    # Cleaning data
    GDP["Country Name"].replace(to_replace={
    "Korea, Rep.": "South Korea",
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
    }, inplace=True)
    # Using the last 10 years of data
    GDP_use = pd.concat([GDP.ix[:, 0], GDP.ix[:, -10:]], axis=1)
    # Change the column name for the merge
    GDP_use.rename(columns={"Country Name": "Country"}, inplace=True)

    # Finally, ScimEn data
    ScimEn = pd.read_excel("./data/scimagojr-3.xlsx")
    # Using just the 15 first countries
    ScimEn_use = ScimEn.ix[:14,:]

    # Merging data
    df_use = ScimEn_use.merge(energy, how="inner", on="Country").merge(GDP_use, how="inner", on="Country").set_index("Country")
    # Organize your data
    df_use = df_use[df_use["Rank"].notnull()]
    df_use[["Rank", "Documents", "Citable documents", "Citations", "Self-citations", "H index"]] = df_use[["Rank", "Documents", "Citable documents", "Citations", "Self-citations", "H index"]].astype(int)
    df_use[["Energy Supply", "Energy Supply per Capita", "% Renewable"]] = df_use[["Energy Supply", "Energy Supply per Capita", "% Renewable"]].astype(float)
    return df_use

def ans_two():
    """
    The previous question joined three datasets then reduced this to just the top 15 entries.
    When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
    This function should return a single number.
    """

    #Starting with energy data, exclude the header and footer
    energy = pd.read_excel("./data/Energy_Indicators.xls", skiprows=18, skip_footer=38, header=None)
    # Exclude the two first columns
    energy.drop([0, 1], axis=1, inplace=True)
    # Make your header
    energy_col = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.columns = energy_col
    # Treat your missing values
    energy.replace("...", np.NaN, inplace=True)
    # Convert "Energy Supply" to gigajoules
    energy["Energy Supply"] = energy["Energy Supply"].apply(lambda x: x*1000000)
    # Replace the numbers presente in the strings
    energy["Country"] = energy["Country"].replace(to_replace=["0","1","2","3","4","5","6","7","8","9"], value="", regex=True)
    # Cleaning data
    energy["Country"].replace(to_replace={
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Republic of Korea": "South Korea",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
    }, inplace=True)
    # Cleaning strings with "()"
    energy["Country"] = energy["Country"][energy["Country"].notnull()].apply(
    lambda x: x.split(" (")[0] if x.endswith(")") else x)

    # Now, GDP data, skip the header
    GDP = pd.read_csv("./data/world_bank.csv", skiprows=4)
    # Cleaning data
    GDP["Country Name"].replace(to_replace={
    "Korea, Rep.": "South Korea",
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
    }, inplace=True)
    # Change the column name for the merge
    GDP.rename(columns={"Country Name": "Country"}, inplace=True)

    # Finally, ScimEn data
    ScimEn = pd.read_excel("./data/scimagojr-3.xlsx")
    # Using just the 15 first countries

    # Merging data to take the intersection (inner)
    df_i = pd.merge(pd.merge(energy, GDP, on="Country"), ScimEn, on="Country")
    # Merging data to take the union (outer)
    df_u = pd.merge(pd.merge(energy, GDP, on="Country", how="outer"), ScimEn, on="Country", how="outer")
    return df_u.shape[0] - df_i.shape[0]

def ans_three():
    """
    This function should return a Series named avgGDP with 15 countries and their average GDP
    sorted in descending order.
    """
    Top15 = ans_one()
    avgGDP = Top15.ix[:,-10:].mean(axis=1).sort_values(ascending=False)
    return avgGDP

def ans_four():
    """
    By how much had the GDP changed over the 10 year span for the country with the
    6th largest average GDP?
    This function should return a single number.
    """
    Top15 = ans_one()
    Top15["avgGDP"] = Top15.ix[:,-10:].mean(axis=1)
    Top15.sort_values(by="avgGDP", ascending=False, inplace=True)
    Top15.reset_index(inplace=True)
    country = Top15["Country"][5]
    Top15["varGDP"] = Top15["2015"] - Top15["2006"]
    return Top15.iloc[5,-1]

def ans_five():
    """
    What is the mean energy supply per capita?
    """
    Top15 = ans_one()
    return Top15["Energy Supply per Capita"].mean()

def ans_six():
    """
    What country has the maximum % Renewable and what is the percentage?
    """
    Top15 = ans_one()
    max_country = tuple(Top15[Top15["% Renewable"] == Top15["% Renewable"].max()][\
    "% Renewable"].reset_index(level=0).iloc[0])
    return max_country

def ans_seven():
    """
    Create a new column that is the ratio of Self-Citations to Total Citations.
    What is the maximum value for this new column, and what country has the highest ratio?
    """
    Top15 = ans_one()
    Top15["Ratio-citations"] = Top15['Self-citations'] / Top15['Citations']
    return tuple(Top15[Top15["Ratio-citations"] == Top15["Ratio-citations"].max()][\
    "Ratio-citations"].reset_index(level=0).iloc[0])

def ans_eight():
    """
    Create a column that estimates the population using Energy Supply and
    Energy Supply per capita. What is the third most populous country according
    to this estimate?
    """
    Top15 = ans_one()
    df = Top15[["Energy Supply", "Energy Supply per Capita"]]
    df["Population_est"] = df["Energy Supply"] / df["Energy Supply per Capita"]
    return tuple(df.sort_values(["Population_est"], ascending=False)["Population_est"\
    ].reset_index(level=0).iloc[2])[0]

def ans_nine():
    """
    Create a column that estimates the number of citable documents per person.
    What is the correlation between the number of citable documents per capita and
    the energy supply per capita? Use the .corr() method, (Pearson's correlation).
    This function should return a single number.
    """
    Top15 = ans_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    return Top15["Citable docs per Capita"].corr(Top15["Energy Supply per Capita"])

def ans_ten():
    """
    Create a new column with a 1 if the country's % Renewable value is at or above
    the median for all countries in the top 15, and a 0 if the country's % Renewable
    value is below the median.
    This function should return a series named HighRenew whose index is the country
    name sorted in ascending order of rank.
    """
    Top15 = ans_one()
    mean = Top15["% Renewable"].median()
    Top15.loc[Top15["% Renewable"] < mean, "HighRenew"] = 0
    Top15.loc[Top15["% Renewable"] >= mean, "HighRenew"] = 1
    Top15["HighRenew"] = Top15["HighRenew"].astype(int)
    print(mean)
    return Top15[["% Renewable", "HighRenew"]]

def ans_eleven():
    """
    Use the following dictionary to group the Countries by Continent, then create
    a dateframe that displays the sample size (the number of countries in each
    continent bin), and the sum, mean, and std deviation for the estimated
    population of each country. This function should return a DataFrame with index
    named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America']
    and columns ['size', 'sum', 'mean', 'std']
    """
    Top15 = ans_one()
    ContinentDict = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}
    # Create a new column with the continents
    Top15["Continent"] = Top15.index.to_series().map(ContinentDict)
    # Create a column with the estimated population
    Top15["EstPop"] = Top15["Energy Supply"] / Top15["Energy Supply per Capita"]
    # Group your DataFrame by Continent and select yout estimated population to use agg
    Top15 = Top15.groupby("Continent")["EstPop"].agg(["size", "sum", "mean", "std"])
    Top15["size"] = Top15["size"].astype(float)
    return Top15["size"]

def ans_twelve():
    """
    Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these
    new % Renewable bins. How many countries are in each of these groups?
    This function should return a Series with a MultiIndex of Continent, then
    the bins for % Renewable. Do not include groups with no countries.
    """
    Top15 = ans_one()
    ContinentDict = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}
    # Reset my index
    Top15 = Top15.reset_index()
    # Create a new column with the continents
    Top15["Continent"] = Top15["Country"].map(ContinentDict)
    # Cut % Renewable into 5 bins
    # Group the DataFrame by Continent and Renewable bins
    # How many countries for each group?
    res = Top15.groupby(["Continent", pd.cut(Top15["% Renewable"], 5)])["Country"].count().dropna()
    return res

def ans_thirteen():
    """
    Convert the Population Estimate series to a string with thousands separator
    (using commas). Do not round the results.
    e.g. 317615384.61538464 -> 317,615,384.61538464
    This function should return a Series PopEst whose index is the country name
    and whose values are the population estimate string.
    """
    Top15 = ans_one()
    # Create a column with the estimated population
    Top15["PopEst"] = Top15["Energy Supply"] / Top15["Energy Supply per Capita"]
    return Top15["PopEst"].map('{:,}'.format)

def main():
    data = ans_four()
    print(data)

if __name__ == "__main__":
    main()
