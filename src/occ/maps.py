import matplotlib.path as mpath
import matplotlib.pyplot as plt 
import numpy as np
import cartopy.crs as ccrs


def south_pole_map(cols=1, rows=1, fig_size=(12,8), max_extent=-55, facecolor='white'):
  ''' 
  User note: In order to call the function, begin cell with: fig, ax = south_pole_map(**args).
  Neglecting "fig, ax =" at the begeinning will not map your data to the existing axes.
   
  This function sets up a polar projection centered at the South Pole, which DataArrays can be plotted over.
   
  Optional arguments accepted for figure size, maximum (northward) extent and facecolor. Any number of columns and/or rows are also accepted for multiple subplots.
   
  If creating multiple subplots, ax=ax[*index*] must be passed in the plot call for each array.
   
  By default, these are set to (12,8), -50ºS and gray, respectively. Columns/Rows set to 1 by default – specifying axes in which to plot data is not necessary when using default column number.
  '''

  fig,ax = plt.subplots(figsize=fig_size, ncols=cols, nrows=rows, subplot_kw={'projection': ccrs.SouthPolarStereo(), 'facecolor':facecolor}, layout='constrained')

  theta = np.linspace(0, 2*np.pi, 100)
  center, radius = [0.5, 0.5], 0.5
  verts = np.vstack([np.sin(theta), np.cos(theta)]).T
  circle = mpath.Path(verts * radius + center)

  if rows>1 and cols>1:
    for i in range(rows):
      for j in range(cols):
        ax[i,j].set_boundary(circle, transform=ax[i,j].transAxes)

        # lat/long map extents. shows south pole out to 50ºS
        ax[i,j].set_extent([-180, 180, -90, max_extent], ccrs.PlateCarree())
  elif cols>1 and rows==1:
    for i in range(cols):
      ax[i].set_boundary(circle, transform=ax[i].transAxes)

      # lat/long map extents. shows south pole out to 50ºS
      ax[i].set_extent([-180, 180, -90, max_extent], ccrs.PlateCarree())
  elif rows>1 and cols==1:
    for i in range(rows):
      ax[i].set_boundary(circle, transform=ax[i].transAxes)

      # lat/long map extents. shows south pole out to 50ºS
      ax[i].set_extent([-180, 180, -90, max_extent], ccrs.PlateCarree())
  else:
    ax.set_boundary(circle, transform=ax.transAxes)

      # lat/long map extents. shows south pole out to 50ºS
    ax.set_extent([-180, 180, -90, max_extent], ccrs.PlateCarree())


  #must return fig, ax when creating multiple subplots in a function
  return fig, ax