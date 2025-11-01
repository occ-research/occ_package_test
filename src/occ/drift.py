import xarray as xr
import numpy as np


def detrend(da, variable_name):
    '''Alternative function for dedrifting without momlevel or numpy's polyfit.
    
    Takes:
    
    1) DataArray (NOT a DataSet) and 
    
    2) The name of the variable you are dedrifting, given as a string (i.e., 'ssh', 'zos', 'so', etc...).
    The variable name is used to name new arrays explicitly.
    
    Returns a DataSet with arrays containing slope, intercept, trendline and the new dedrifted DataArray.
    '''
    # Check if xarray has a time dimension
    if 'time' not in da.dims:
        raise ValueError("DataArray must have 'time' dimension")
    
    # Reminder to provide variable name for convenient renaming or array
    if type(variable_name) is not str:
        raise TypeError(f'String expected as Variable_name, instead got {type(variable_name).__name__}')

    # Convert time to integers relative to the start (i.e., time[0] == 0) and take mean
    t_values = np.arange(len(da['time']))

    t_mean = t_values.mean()

    # Calculate the mean of data along the time dimension
    # This returns the center point of the time dimension
    da_mean = da.mean(dim='time')

    # Reshape time_values to avoid broadcasting errors
    # this just turns the v_values array into a xarray data array with a time dimension
    t_reshaped = xr.DataArray(t_values, dims=['time'])

    # Calculate slope
    # This is computing slope as the covariance / variance 
    # See here for explanation: http://faculty.washington.edu/swithers/seestats/SeeingStatisticsFiles/seeing/reg/slopeformulas/slopeFormulas.html
    # The slope is dependent on t_mean .. so your slope will be dependent on the time period over which you are
    # computing the slope. If there is a lot of drift happening then t_mean will be highly dependent
    # on time period ....
    
    slope = ((da - da_mean) * (t_reshaped - t_mean)).sum(dim='time') / ((t_reshaped - t_mean) ** 2).sum()
    
    # Calculate intercept of the trend line .... this is different than the first value of the data_array
    intercept = da_mean - slope * t_mean

    # Calculate the trend
    trend = slope * t_reshaped + intercept

    # Detrend the data by subtracting the trend without subtracting the intercept
    # intercept should not be removed because the data should be centered around initial pressure rather than 0 Pa
    detrended = da - (slope * t_reshaped)
    
    dsout = xr.Dataset()
    dsout[f'{variable_name}_slope'] = slope
    dsout[f'{variable_name}_intercept'] = intercept
    dsout[f'{variable_name}_dedrifted'] = detrended
    dsout[f'{variable_name}_trend'] = trend
    dsout[f'{variable_name}_raw'] = da
    return dsout