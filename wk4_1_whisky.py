# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:13:10 2020

@author: Daria
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralCoclustering
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show

#whisky = pd.read_csv(r'C:/Users/Daria/Documents/PythonScripts/whiskies.txt')
whisky = pd.read_csv(r"whiskies.csv",index_col=0)
whisky["Region"] = pd.read_csv(r"C:/Users/Daria/Documents/PythonScripts/regions.txt")
flavors = whisky.iloc[:, 2:14]
correlation_flavors = pd.DataFrame.corr(flavors)
correlation_whisky = pd.DataFrame.corr(flavors.transpose())

model= SpectralCoclustering(n_clusters=6, random_state =0)
model.fit(correlation_whisky)
np.sum(model.rows_, 1) #each whisky belongs to one of 6 clusters
np.sum(model.rows_, 0) # does each whicky belong to only 1 cluster?
model.row_labels_ # each observation belongs to this cluster
whisky= whisky.iloc[np.argsort(model.row_labels_ )]
whisky = whisky.reset_index(drop= True)
#correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())
#correlations = np.array(correlations)
corr = pd.DataFrame.corr(whisky.iloc[:, 2:14].transpose()) #DataFrame
correl = np.array(corr) # convert to NumPy array

plt.figure(figsize =(14,7))
plt.subplot(121)
plt.pcolor(correlation_whisky)
plt.colorbar()
plt.title('Original')
plt.axis('tight')

plt.subplot(122) #rows and columns transposed to show 6 clusters
plt.pcolor(correl)
plt.colorbar()
plt.title("Rearranged")
plt.axis("tight")
plt.savefig('whiskey.pdf')


#colors linked to regions
cluster_colors = ['#0173b2', '#de8f05', '#029e73', '#d55e00', '#cc78bc', '#ca9161']
regions = ["Speyside", "Highlands", "Lowlands", "Islands", "Campbelltown", "Islay"]
region_colors = dict(zip(regions, cluster_colors))

#correlation graph by whisky group and correlation
distilleries = list(whisky.Distillery)
correlation_colors = []
for i in range(len(distilleries)):
    for j in range(len(distilleries)):        
        if correl[i,j]<.70:                    # if low correlation,
            correlation_colors.append('white')         # just use white.
        else:                                          # otherwise,
            if whisky.Group[i]==whisky.Group[j]:                
                correlation_colors.append(cluster_colors[whisky.Group[i]]) # if the groups match,
                # color them by their mutual group.
            else:                                      # otherwise
                correlation_colors.append('lightgray') # color them lightgray.
                
#Bokeh interactive plot
source = ColumnDataSource(
    data = {
        "x": np.repeat(distilleries,len(distilleries)),
        "y": list(distilleries)*len(distilleries),
        "colors": correlation_colors,
        "correlations": correl.flatten(),
    }
)

output_file("Whisky Correlations.html", title="Whisky Correlations")
fig = figure(title="Whisky Correlations",
    x_axis_location="above", x_range=list(reversed(distilleries)), y_range=distilleries,
    tools="hover,box_zoom,reset")
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = "5pt"
fig.xaxis.major_label_orientation = np.pi / 3
fig.rect('x', 'y', .9, .9, source=source,
     color='colors', alpha='correlations')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {
    "Whiskies": "@x, @y",
    "Correlation": "@correlations",
}
#show(fig)

# =============================================================================
# #sample location plot
# points = [(0,0), (1,2), (3,1)]
# xs, ys = zip(*points)
# colors = ['#0173b2', '#de8f05', '#029e73']
# 
# output_file("Spatial_Example.html", title="Regional Example")
# location_source = ColumnDataSource(
#     data={
#         "x": xs,
#         "y": ys,
#         "colors": colors,
#     }
# )
# fig = figure(title = "Title",
#     x_axis_location = "above", tools="hover, save")
# fig.plot_width  = 800
# fig.plot_height = 1000
# fig.circle("x", "y", size=10, source=location_source,
#      color='colors', line_color = None)
# 
# hover = fig.select(dict(type = HoverTool))
# hover.tooltips = {
#     "Location": "(@x, @y)"
# }
#show(fig)
# =============================================================================

#actual location plot by distillery
def location_plot(title, colors):
    output_file(title+".html")
    location_source = ColumnDataSource(
        data = {
            "x": whisky[" Latitude"],
            "y": whisky[" Longitude"],
            "colors": colors,
            "regions": whisky.Region,
            "distilleries": whisky.Distillery
        }
    )
    
    fig = figure(title = title,
        x_axis_location = "above", tools="hover, save")
    fig.plot_width  = 600
    fig.plot_height = 1000
    fig.circle("x", "y", size=9, source=location_source, color='colors', line_color = None)
    fig.xaxis.major_label_orientation = np.pi / 3
    hover = fig.select(dict(type = HoverTool))
    hover.tooltips = {
        "Distillery": "@distilleries",
        "Location": "(@x, @y)"
    }
    show(fig)

region_cols = [region_colors[i] for i in list(whisky["Region"])]
classification_cols = [cluster_colors[j] for j in list(whisky.Group)] 
location_plot("Whisky Locations and Regions", region_cols)
location_plot("Whisky Locations and Groups", classification_cols)