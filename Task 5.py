import pandas as pd 
import matplotlib.pyplot as plt 
import geopandas as gpd
import country_converter as coco


#Reading and Cleaning the Initial File
df = pd.read_excel(r"C:\Users\rakee\OneDrive\Desktop\DS\Computer practicals rug\2\asd.xlsx")
df.pop("Estimates Start After")
df.pop('Units')
df.pop('Scale')
df.pop('Country/Series-specific Notes')
def cleaner(asd, dfa):
    dfa = dfa[dfa[asd] != ":"]
cleaner('2015',df)
cleaner('2016',df)
cleaner('Change in Inflation',df)

#creating a GeoDataFrame object and loading in naturalearh_lowres
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#adding ISO 3 naming to the df data frame
input_countries = list(df['Country'])
ISO3 = coco.convert(names=input_countries, to= "ISO3")
df['ISO_3'] = ISO3

#fixing some ISO3 naming errors in the world dataframe 
cor_iso = world[world['iso_a3'] != "-99"]
wrong_iso = world[world['iso_a3'] == "-99"]
asd = coco.convert(names = list(wrong_iso['name']),to = "ISO3")
wrong_iso.pop('iso_a3')
wrong_iso['iso_a3'] = asd
all_ok = gpd.GeoDataFrame(pd.concat([cor_iso, wrong_iso], ignore_index=True) )

#merging df and all_ok
merged_df = all_ok.merge(df, left_on = 'iso_a3', right_on = 'ISO_3', how= 'left')

#ploting merged_df
ax = merged_df.plot(column='Change in Inflation', cmap ='bwr', figsize=(15,9),legend =True, linewidth=0.6, edgecolor ="black",missing_kwds={
  "color": "lightgrey","edgecolor": "White",      "hatch": "///",      "label": "Missing values"},vmax = 60,vmin = -60)

ax.set_title('Inflation Change (in percentages) in 2016', fontdict = {'fontsize':25})
ax.set_axis_off()
plt.savefig(r"C:\Users\rakee\OneDrive\Desktop\DS\Computer practicals rug\2\Task5.png",format="png")
plt.show()

     
            





