from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import os

print(os.getcwd())

gdp = pd.read_csv("all_data.csv")
print(gdp.head())
print(gdp.info())
print(len(gdp))

"""
Has life expectancy increased over time in the six nations?
Has GDP increased over time in the six nations?
All of the countries´ GDP has increased during the years. China has recorded biggest increase in GDP, followed by Chile and Zimbabwe.
With that also life expectancy has increased, since both GDP and life expectancy are strongly correlated. 
Is there a correlation between GDP and life expectancy of a country?
All correlation values are almost reaching 1, so there is strong correlation between GDP and life expectancy.
What is the average life expectancy in these nations?
What is the distribution of that life expectancy?

What is interesting about this data is fact that even thought USA has multiple times higher GDP than Chile or Germany, 
these two countries have still higher average life expectancies. This shows us that even thought GDP is strongly correlated with life expectancy in each country, 
life expectancy depends more on quality of health system services provided to people and the way of life, healthy habits and healthy lifestyle of these people. 
"""


"What five countries are represented in the data?"
print(gdp["Country"].unique())
countries = gdp["Country"].unique().tolist()

"What years are represented in the data?"
print(gdp["Year"].unique())

"How many rows are there for each country (careful, this one can be a bit tricky)?"
print(gdp.groupby("Country").count())


gdp.rename(columns={"Life expectancy at birth (years)" : "Leaby"}, inplace=True)
print(gdp.head())

fig, ax = plt.subplots(2, 1, figsize=(15,20))
sns.pointplot(x="Year", y="GDP", hue="Country", data=gdp, ax=ax[0])
ax[0].set(ylabel="GDP in Trillions of U.S. Dollars")
ax[0].legend(loc='upper left')

sns.pointplot(x="Year", y="Leaby", hue="Country", data=gdp, ax=ax[1])
ax[1].set(ylabel="Life expectancy at birth (years)")
plt.savefig("GDP and LE over years")
plt.show()



"""
Which countries have the highest and lowest GDP?
Which countries have the highest and lowest life expectancy?
"""

"""
Based on the visualization, choose one part the data to research 
a little further so you can add some real world context to the visualization. 
You can choose anything you like, or use the example question below.
What happened in China between 1991-2016 that increased the GDP so drastically?

"""

"Is there a correlation between GDP and life expectancy of a country?"

fig, ax = plt.subplots(3, 2, figsize=(15,10))
ax = ax.flatten()

for i, country in enumerate(countries):
    
    subset = gdp[gdp["Country"] == country]
    sns.lineplot(x="Leaby", y="GDP", data=subset, ax=ax[i])
    ax[i].set_title("Leaby to GDP for " + country)
plt.tight_layout()
plt.savefig("GDP to LE for each country")
#plt.show()




"What is the average life expectancy in these nations?"

print(gdp.groupby("Country")["Leaby"].mean())

"What is the distribution of that life expectancy?"

fig, ax = plt.subplots(3, 2, figsize=(15,10))
ax = ax.flatten()

for i, country in enumerate(countries):
    subset = gdp[gdp["Country"] == country]
    sns.histplot(x="Leaby", data=subset, bins=20, ax=ax[i])
    ax[i].set_title("Leaby distribution for " + country)
plt.tight_layout()
#plt.show()

plt.figure(figsize=(18, 6))
sns.histplot(data=gdp, x="Leaby", hue="Country", bins=50, kde=False, multiple="dodge")
plt.xlabel("Life expectancy at birth (years)")
plt.ylabel("Count")
plt.title("Distribution of Life Expectancy by Country")
plt.savefig("hist LE for all countries")
#plt.show()


sns.scatterplot(x="Leaby", y="GDP", hue="Country",  data=gdp)
plt.savefig("scatter LE to GDP for all countries")
#plt.show()
plt.clf()

"""
Trends
Growth rate of GDP per country
Change in life expectancy per country over time

Correlation
Correlation between GDP and life expectancy globally or per country

"""

gdp_rate = gdp.groupby("Country").apply(
    lambda x: (x["GDP"].iloc[-1] / x["GDP"].iloc[0])**(1/(x["Year"].iloc[-1]-x["Year"].iloc[0])) - 1
).reset_index(name="Average GDP growth rate")
gdp_rate["Average GDP growth rate [%]"] = (gdp_rate["Average GDP growth rate"] * 100).round(4)
print("THIS IS GDP GROWTH RATE ", gdp_rate)

le_rate = gdp.groupby("Country").apply(
    lambda x: (x["Leaby"].iloc[-1] / x["Leaby"].iloc[0])**(1/(x["Year"].iloc[-1]-x["Year"].iloc[0])) - 1
).reset_index(name="Average LE growth rate")
le_rate["Average LE growth rate [%]"] = (le_rate["Average LE growth rate"] * 100).round(4)
print("THIS IS LIFE EXP. GROWTH RATE ", le_rate)


corrs = (
    gdp.groupby("Country")
       .apply(lambda x: x["GDP"].corr(x["Leaby"]))
       .reset_index(name="Correlation between GDP and LE")
)
corrs["Correlation between GDP and LE"] = (corrs["Correlation between GDP and LE"]).round(4)
print(corrs)


fig, ax = plt.subplots(figsize=(6, len(corrs)*0.5))  # height adjusts to number of rows
ax.axis('off')

corrs_table = ax.table(
    cellText=corrs.values,
    colLabels=corrs.columns,
    loc='center'
)

plt.savefig("corr_gdp_leaby_table.png", dpi=300, bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(figsize=(6, len(gdp_rate)*0.5))  # height adjusts to number of rows
ax.axis('off')

gdp_table = ax.table(
    cellText=gdp_rate.values,
    colLabels=gdp_rate.columns,
    loc='center'
)

plt.savefig("gdp_growth.png", dpi=300, bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(figsize=(6, len(le_rate)*0.5))  # height adjusts to number of rows
ax.axis('off')

le_table = ax.table(
    cellText=le_rate.values,
    colLabels=le_rate.columns,
    loc='center'
)

plt.savefig("le_growth.png", dpi=300, bbox_inches='tight')
plt.show()