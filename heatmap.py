import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
from pprint import pprint
import http.client, urllib.request, urllib.parse, urllib.error, base64
import dateutil.parser
import datetime
from scipy.stats import kde
import matplotlib.colors as colors
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm

###Things to do
#tracked time sometimes is slightly higher than journey time due to rounding error.  this makes the stealth time look negative.  need to have tracked time max out at journey time


#latlong = []
listOfCustomers=[]
#using manually downloaded .json file
with open('T0862August2017.json') as insights:
	exportdata = json.load(insights)
flip2017=-1 #-1 for 2017 and positive 1 for 2018
#get list of data points (stored as dictionaries) from the export 
ListOfSnapshots = exportdata['result'][0]



#look through each data point collected and make a list of unique customers (deviceIDs)
#for snapshot in ListOfSnapshots:
#	listOfCustomers.append(snapshot["deviceID"])
#	listOfCustomers = list(set(listOfCustomers)) ##removes duplicates
	
#plot all customers combined
latlong=[]
x=[]
y=[]
#data=[]
for snapshot in ListOfSnapshots:
	latlong.append([snapshot["latitude"],snapshot["longitude"]*flip2017])
	#x.append(snapshot["latitude"])
	#y.append(snapshot["longitude"])

data=numpy.asarray(latlong)
print(latlong)
#data = numpy.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 3]], 200)
#print(data)
#print(type(data))
x, y = data.T

# Create a figure with 6 plot areas
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(13, 10))
axes.axis("off")
 
# Everything starts with a Scatterplot
#axes[0].set_title('Scatterplot')
#axes[0].plot(x, y, 'ko')
# As you can see there is a lot of overplottin here!
 
# Thus we can cut the plotting window in several hexbins
nbins = 200
#axes[1].set_title('Hexbin')
#axes[1].hexbin(x, y, gridsize=nbins, cmap=plt.cm.BuGn_r)
 
# 2D Histogram
#axes[2].set_title('2D Histogram')
#axes[2].hist2d(x, y, bins=nbins, cmap=plt.cm.RdYlGn)
 
# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
k = kde.gaussian_kde(data.T)
xi, yi = numpy.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = k(numpy.vstack([xi.flatten(), yi.flatten()]))
 
# plot a density
#axes[3].set_title('Calculate Gaussian KDE')
#axes[3].pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.BuGn_r)
 
# add shading
#axes.set_title('2D Density with shading')

axes.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', norm=colors.LogNorm(vmin=0.001*zi.max(), vmax=1*zi.max()),
                   cmap=plt.cm.get_cmap('seismic'))

# contour
#axes.set_title('Contour')
#axes.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', norm=colors.LogNorm(vmin=0.001*zi.max(), vmax=1*zi.max()), cmap=plt.cm.get_cmap('seismic'))#cmap=plt.cm.BuGn_r)
#axes.contour(xi, yi, zi.reshape(xi.shape) )

	
fig.show()
fig.savefig("T0862heatmap2017.png", transparent=True)


# ###from https://matplotlib.org/gallery/images_contours_and_fields/pcolormesh_levels.html#sphx-glr-gallery-images-contours-and-fields-pcolormesh-levels-py
# levels = MaxNLocator(nbins=15).tick_values(zi.min(), zi.max())


# # pick the desired colormap, sensible levels, and define a normalization
# # instance which takes data values and translates those into levels.
# cmap = plt.get_cmap('PiYG')
# norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

# fig, (ax0, ax1) = plt.subplots(nrows=2)

# im = ax0.pcolormesh(xi, yi, zi, cmap=cmap, norm=norm)
# fig.colorbar(im, ax=ax0)
# ax0.set_title('pcolormesh with levels')


# # contours are *point* based plots, so convert our bound into point
# # centers
# cf = ax1.contourf(x[:-1, :-1] + dx/2.,
                  # y[:-1, :-1] + dy/2., z, levels=levels,
                  # cmap=cmap)
# fig.colorbar(cf, ax=ax1)
# ax1.set_title('contourf with levels')

# # adjust spacing between subplots so `ax1` title and `ax0` tick labels
# # don't overlap
# fig.tight_layout()

# plt.show()