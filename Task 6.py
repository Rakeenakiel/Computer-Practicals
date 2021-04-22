import pandas as pd 
import matplotlib.pyplot as plt 
import geopandas as gpd
import country_converter as coco
from shapely.geometry import Point
import adjustText as aT
#importing data
df = pd.read_excel(r"C:\Users\rakee\OneDrive\Desktop\DS\Computer practicals rug\2\Visualizations\Code\Data\Governance Effectivenes 2017.xlsx")

#creating a GeoDataFrame object and loading in naturalearh_lowres
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#fixing some ISO3 naming errors in the world dataframe 
cor_iso = world[world['iso_a3'] != "-99"]
wrong_iso = world[world['iso_a3'] == "-99"]
asd = coco.convert(names = list(wrong_iso['name']),to = "ISO3")
wrong_iso.pop('iso_a3')
wrong_iso['iso_a3'] = asd
all_ok = gpd.GeoDataFrame(pd.concat([cor_iso, wrong_iso], ignore_index=True))

#merging the tables
merged_df= all_ok.merge(df, left_on = "iso_a3", right_on = "Country Code", how="left")
merged_df = merged_df.sort_values(by='2017 [YR2017]')
#setting up the center point of each country for the label
centroids = [i.representative_point() for i in merged_df['geometry']]
merged_df['center']= centroids
merged_copy = merged_df.copy()
merged_copy.set_geometry('center',inplace=True)
merged_df['Country Code']=merged_df['Country Code'].fillna("")
#ploting merged_df
ax = merged_df.plot(column='2017 [YR2017]', cmap ='coolwarm_r', figsize=(15,9),legend =True, linewidth=0.6, edgecolor ="white",missing_kwds={
  "color": "lightgrey","edgecolor": "White",      "hatch": "///",      "label": "Missing values"},vmax =1.9, vmin=-0.2)

text = []

df.sort_values(by='2017 [YR2017]')
for x,y, label in zip(merged_copy.geometry.x,merged_copy.geometry.y,merged_df['Country Code']):
    text.append(plt.text(x,y,label,fontsize=12, color='black'))

minx, miny, maxx, maxy = merged_df.total_bounds
ax.set_xlim(-25, 45)
ax.set_ylim(30, 75)
aT.adjust_text(text, force_points= 0.3, force_text = 0.8,expand_points=(1,1), expand_text=(1,1), arrowprops=dict(arrowstyle="-", color='grey', lw=0.5))
ax.set_title('Government Effectiveness (Estimate) Index 2017', fontdict = {'fontsize':18})
ax.set_axis_off()
plt.savefig(r"C:\Users\rakee\OneDrive\Desktop\DS\Computer practicals rug\2\Task6.png",format="png")
plt.show()