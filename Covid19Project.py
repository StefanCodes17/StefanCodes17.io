# Name: Stefan Kolev
# Title: Covid and Police Activity
# Resources: https://builtin.com/data-science/time-series-python https://www.ritchieng.com/machine-learning-evaluate-linear-regression-model/ python and library documentation textbook (Others are on abstract)
# URL: https://stefancodes17.github.io/StefanCodes17.io/

# In[68]:


# Imports
import pandas as pd
import folium
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns


# In[69]:

# Includes dates, case counts, borough division
# Load Covid Datasets
CovidDailyCounts = pd.read_csv("./datasets/Covid/COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv")
CovidByBoro = pd.read_csv("./datasets/Covid/CovidByBoro.csv")
CovidByRegion = pd.read_csv("./datasets/Covid/New_York_Forward_COVID-19_Daily_Hospitalization_Summary_by_Region.csv")
PopulationByBorough = pd.read_csv("./datasets/NewYork/NYC_Population_by_Borough.csv")
GeoInfo = pd.read_csv("./datasets/Covid/NewYorkBoroughGeoInformation.csv")


# In[70]:

# Broough divisions, arrest and shootings count for NYC
# Load Police Datasets
DailyArrestCount = pd.read_csv("./datasets/PoliceActivity/NYPD_Arrest_Data__Year_to_Date_.csv")
PastDailyArrestCount = pd.read_csv("datasets/PoliceActivity/NYPD_Arrests_Data__Historic_.csv")
DailyShootingsCount = pd.read_csv("./datasets/PoliceActivity/NYPD_Shooting_Incident_Data__Year_To_Date_.csv")


# In[71]:


# Covid Daily Counts Dataset
CovidDailyCounts['DATE_OF_INTEREST'] = pd.to_datetime(CovidDailyCounts['DATE_OF_INTEREST'])
fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.plot(CovidDailyCounts['DATE_OF_INTEREST'], CovidDailyCounts['CASE_COUNT'])
plt.rcParams.update({'font.size': 15})
plt.title("Daily Covid Case Count in New York")
plt.xlabel("Date")
plt.ylabel("Case Count")
plt.savefig('./visualizations/case_count.png')
plt.show()


# In[72]:


fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.plot(CovidDailyCounts['DATE_OF_INTEREST'], CovidDailyCounts['DEATH_COUNT'])
plt.title("Daily Covid Death Count in New York")
plt.xlabel("Date")
plt.ylabel("Case Count")
plt.savefig('./visualizations/death_count.png')
plt.show()


# In[73]:


plt.show()
fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.plot(CovidDailyCounts['DATE_OF_INTEREST'], CovidDailyCounts['HOSPITALIZED_COUNT'])
plt.title("Daily Covid Hospitalizations Count in New York")
plt.xlabel("Date")
plt.ylabel("Case Count")
plt.savefig('./visualizations/hosp_count.png')
plt.show()


# In[74]:


CovidByBoro["Borough"].unique()
CovidByBoro["Date"] = pd.to_datetime(CovidByBoro["Date"])


# In[75]:

# Seen throughout, tilts the x-axis labels
fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.ylabel("Daily Admit (per 10 thousand")
sns.scatterplot(x="Date", y="Admit_All_ages", data=CovidByBoro, hue="Borough")
plt.savefig('./visualizations/borough_viz.png')


# In[ ]:





# In[76]:


AdmitPerBorough = CovidByBoro.groupby(["Borough"]).sum()["Admit_All_ages"].transpose()
AdmitPerBoroughPop = pd.merge(PopulationByBorough, AdmitPerBorough, right_on="Borough", left_on="Borough", how="right")
AdmitPerBoroughPop["Admit_All_ages"] = AdmitPerBoroughPop["Admit_All_ages"] * 10000
plt.bar(AdmitPerBoroughPop["Borough"], AdmitPerBoroughPop["Admit_All_ages"] / AdmitPerBoroughPop["Population"])  
plt.xlabel("Borough")
plt.ylabel("Percent of Population Admitted to Hospital")
plt.title("Percent Hospital Admission for Each Borough")
plt.savefig('./visualizations/percenthosp_count.png')


# In[77]:


# mymap = folium.Map(location=[40.7, -73.9], zoom_start=10)
# GeoInfo_df = pd.merge(GeoInfo, AdmitPerBoroughPop, left_on="BoroName", right_on="Borough", how="left")
# mymap.choropleth(
#  geo_data=GeoInfo_df,
#  name='Choropleth',
#  data=GeoInfo_df,
#  columns=['Borough','Admit_All_ages'],
#  key_on="feature.properties.Admit_All_ages",
#  fill_color='YlGnBu',
#  fill_opacity=1,
#  line_opacity=0.2,
#  legend_name='Resident foreign population in %',
#  smooth_factor=0
# )
# mymap
# GeoInfo_df


# In[78]:


CovidByBoro.groupby(["Borough"]).sum()["Admit_All_ages"]


# In[79]:


CovidByRegion['As of Date'] = pd.to_datetime(CovidByRegion['As of Date'])
CovidByRegion = CovidByRegion.groupby(["Region", "As of Date"]).sum()


# In[80]:


fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.title("Total Patients Hospitalized Per Borough")
sns.lineplot(x="As of Date", y="Total Patients Hospitalized", data=CovidByRegion, hue="Region")
plt.legend(loc="upper right", prop={'size': 10})
plt.savefig('./visualizations/hosp_countborough.png')


# In[81]:


# Visualize Police Data
DailyArrestCount["ARREST_DATE"] = pd.to_datetime(DailyArrestCount["ARREST_DATE"])
ArrestPerBorough = DailyArrestCount.groupby(["ARREST_DATE", "ARREST_BORO"]).count()
fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.title("Daily Arrest Per Borough")
plt.ylabel("Count")
plt.xlabel("Date")
sns.scatterplot(x="ARREST_DATE", y="PD_DESC", data=ArrestPerBorough, hue="ARREST_BORO")
plt.legend(loc="upper right", prop={'size': 12})
plt.savefig('./visualizations/arrest_count.png')


# In[82]:


# Visualize Historic
fig,ax = plt.subplots()
fig.autofmt_xdate(rotation=45)
plt.title("Historic Daily Arrest Per Borough")
plt.ylabel("Count")
plt.xlabel("Date")
PastDailyArrestCount["ARREST_DATE"] = pd.to_datetime(PastDailyArrestCount["ARREST_DATE"])
PastArrestPerBorough = PastDailyArrestCount.groupby(["ARREST_DATE", "ARREST_BORO"]).count()
ax = sns.scatterplot(x="ARREST_DATE", y="PD_DESC", data=PastArrestPerBorough, hue="ARREST_BORO")
plt.legend(loc="upper right", prop={'size': 12})
ax.set(ylim=(0, 250))
plt.savefig('./visualizations/histarrest_count.png')


# 

# In[83]:




