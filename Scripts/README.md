# epa_power_plants

# Title: 
### DECOMMISSIONING COAL PLANTS & THE HEALTH IMPACT ON ENVIRONMENTAL JUSTICE

## Summary: 

The goal of the following scripts is to determine if the closure of coal plants
has an impact on the health of known environmental justice communities. This was
done by downloading three different data sets:

1. EPA EJ Screening Data
    1. Plant level data set that provides demographic and emissions data within a 3 mile radius of the plant.
1. Census 2021 Block Group
    1. 2021 block group level census API data for the state of Montana. 
1. Marginal Damage Modeling Tool
    1. The Air Pollution Emission Experiments and Policy analysis (APEEP) to calculate MD.
        
With these data sets, coal plants are selected and analyzed for potential patternswith state percentile people of color. A deeper analysis of the high polluting  coal plants took place by determining if there were any coal plants that had a  greater population of people of color relative to the remainder of the state. One plant in particular, Colstrip, in Montana was identified as having a greater number of people of color than the state average population of people of color.This demographic information was graphed in QGIS and the marginal damage of the  PM emissions in the county of the plant was calculated.

## Conclusions:

1. The Colstrip Plant in Montana is a relatively high PM emitting plant that has a greater share of people of color near the plant in comparison to the state share of people of color, therefore impacting people of color disproportionately.
1. EPA dataset does not capture the full disproportionate amount of people of color in the surrounding areas of the plants. 
1. While the MD for the county that the Colstrip Plant is located is not necessarily just for the people in the rings, when coupled with the disproportionate demographics in the area, it could be recommended that the plant should close down.

## Instructions:
### A. Script filter.py
**Data:**
1. The EPA EJ Screening Data is required for the script. In order to get access to it, navigate to this link and select download where it says “Power Plants and Neighboring Communities (xlsx)” under the “Additional Graphs and Data” section.
1. The data file is very large and a separate csv will need to be created that has a list of the column names from the “Power Plants and Neighboring Communities (xlsx)” and another column that has an x in it marking the column names you’d like to bring into the script. 

**Purpose:**
1. This script filters through the large excel file that was downloaded from the EPA and renames the column names of the existing file in order to make it easier to analyze.

**Output:**
1.  The output of this script is "coal_plants_communities.csv" which will be used in later scripts for analysis. 

### B. Script census.py
**Data:**
1. The Census API is used for this script and will require an API key. 
1. Go to **https://api.census.gov/data/key_signup.html** and request an API key. 
1. The API link that is used is this: **https://api.census.gov/data/2020/acs/acs5**

**Purpose:**
1. This script calls an API to collect block group level data for the state of Montana. It then calculates the people of color by subtracting the total number of white people in the population from the total population. 
1. The script also produces a corresponding GEOID for each of the demographic data points.

**Output:**
1. It produces a "mt_poc.csv", which contains demographic information (number of people of color, white people, total population) for the state of Montana with its corresponding COUNTYFP and STATEFP. 
        
## C. Script high_emissions.py
**Data:**
1. The data for this script takes the csv file that was created from “filter.py”, specifically "coal_plants_communities.csv".

**Purpose:**
1. This script plots a regression of the annual net generation of coal plants to the PM Emissions.
1. The script generates a box plot of the state percentile people of color to PM Emissions. This will demonstrate if there is a relationship between the number of people of color relative to the state to the amount of PM emissions.
1. It also creates a horizontal bar graph that compares the state average people of color, to the population of people of color within the 3 mile radius near the coal plant.

**Output:**
1. This script shows that one plant in comparison to the other top emitting plants has a relatively high population of people of color in comparison to the state average.
1. Three png files:
    1. "Net_Gen_PM_Emissions.png", showing the net generation of all coal plants to their corresponding PM emissions.
    1. "State_pctile_poc_emissions.png", showing a box plot that plots the state percentile people of color to PM Emissions. 
    1. "POC_comparison.png", showing the of the top emitting plants comparing the population within the 3 mile radius near the plant to the state average people of color population.
    1. One csv file, “"high_emmissions_coal_plants.csv", listing the plants that are emitting more than 3000 PM tons.

## D. Script rings.py
**Data:**
1. This script uses the output from the “high_emissions.py”, specifically “"high_emmissions_coal_plants.csv".

**Purpose:**
1. This script builds rings around the plant located in Montana that is a high polluting plant with a relatively high population of people of color within those rings.
1. There are a series of rings (3, 10, 15, 20, 30, 40) in which units are in miles.
1. This script creates two geopackages that will be used later to input into QGIS.

**Output:**
1. Two gpkg files:
    1. "Mt_high_emissions.gpkg", with a “plant” layer showing where the plant is located based on the latitude and longitude of the plant.
    1. "Mt_high_emissions.gpkg", with a “ring” layer showing a series of rings around the plant.
    1. A csv file, "mt_plant_data.csv" showing the demographic and pollution information from the plant in Montana.

## E. Script plotting.py
**Data:**
1. This script pulls data in from the “rings.py”, specifically "ring_info.csv".

**Purpose:**
1. This script graphs the three dimensional relationship between the number of people of color within the different rings created in “rings.py” to the general share of people of color within the state.

**Output:**
1. The output shows that there is a larger share of people of color within the rings than the rest of the state. It also identifies that the EPA does not capture all of the disparities, given they only give information on the demographics within 3 miles of the plant.
1. One png file, “POC_high_emissions.png”, showing the distribution of people of color within Montana.

## F. Script join.py
**Data:**
1. This script uses 2021 census block data for the state of Montana (FIPS code = 30). Navigate to this link and under Census Block groups, select Montana and this file will automatically download: "cb_2021_30_bg_500k.zip".
1. This script also uses data pulled from the “census.py”, specifically "mt_poc.csv".
1. The script also uses the geopackage created in the “rings.py” script, specifically "mt_high_emissions.gpkg", layer="rings".

**Purpose:**
1. This script joins the demographic census data from the API to the shape file pulled from the link above. 
1. It also creates a spatial join of the geopackage rings layer, with the demographic information. This spatial join allows for the calculation of how many people of color within the rings  of the plant. 

**Output:**
1. The output is a csv file, "ring_info.csv", showing the demographic information within the rings created from the previous script, where the rings are in miles.

## G. Script md.py
**Data:**
1. This script uses data from The Air Pollution Emission Experiments and Policy analysis (APEEP) model. Navigate to this link and sign up in order to get access to the data file. Once you are logged in, navigate to APEEP Platform tab and select “Marginal Damages (2011) from Holland, Mansur, Muller, Yates AER forthcoming.xlsx” to download the file.
1. This file shows the Marginal Damage by county within the United States based on the toxin. 
1. The script uses data from the “rings.py”, specifically "mt_plant_data.csv".

**Purpose:**
1. This script calculates the marginal damage of PM pollution in the county where the plant is located. The script calculates the amount of tons of pollution of the plant and multiplies it by the marginal damage in the file.

**Output:**
1. The output is a csv file, "md_mt_plant.csv", that indicates the demographic and plant based data including the marginal damage for the pollution in the county.

## H. QGIS mt_plant_emissions.qgz
**Data:**
1. This QGIS file is made from the "mt_high_emissions.gpkg" file and contains the following layers:
    1. “rings”
    1. “plant”

**Purpose:**
1. This QGIS file looks at a few different things:
    1. The demographics of the state of Montana 
    1. The demographics with the rings around the high emitting plant
    1. This visual aid allows you to see the varying demographics and identify that there is a greater amount of people of color near the rings than the state.
  
**Output:**
1. A png of the state of Montana, it’s corresponding demographics, the plant and the rings by exporting to an image. Make sure the layers are in the following order:
    1. Mt_high_emissions - plant
    1. Mt_high_emissions - rings
    1. Mt_high_emissions
1. A png of just the rings, the plant, and the demographics within those rings by completing a spatial join within QGIS
    1. Create a new intersection layer by doing the below steps and then unclick the “Mt_high_emissions” layer and save as a png 
            1. By going to Vector → Data Management Tools → Join Attribute by Location → set it up like the following:
            ![GIS](interaction_gis.png)
