# -*- coding: utf-8 -*-

"""
General description
-------------------

The ``modelchain_example`` module shows a simple usage of the windpowerlib by
using the :class:`~.modelchain.ModelChain` class. The modelchains are
implemented to ensure an easy start into the Windpowerlib. They work like
models that combine all functions provided in the library. Via parameteres
desired functions of the windpowerlib can be selected. For parameters not being
specified default parameters are used.

There are mainly three steps. First you have to import your weather data, then
you need to specify your wind turbine, and in the last step call the
windpowerlib functions to calculate the feed-in time series.

This example requires the version v0.1.0 of windpowerlib. Install by:

    pip install 'windpowerlib>=0.1.0,<0.2.0'

Optional:

    pip install matplotlib
"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

import os
import pandas as pd

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

from windpowerlib import ModelChain
from windpowerlib import WindTurbine

# You can use the logging package to get logging messages from the windpowerlib
# Change the logging level if you want more or less messages
import logging
logging.getLogger().setLevel(logging.INFO)


##########################################################################
# 1. Get weather data
##########################################################################
logging.info("1. Get weather data")

# The data will be read into a pandas DataFrame with a MultiIndex.

# The first level contains the variable name as string (e.g. 'wind_speed') and
# the second level contains the height as integer at which it applies
# (e.g. 10, if it was measured at a height of 10 m).

# The first level will have the following columns:

# wind speed: `wind_speed` in m/s
# temperature `temperature` in K
# roughness length `roughness_length` in m
# pressure `pressure` in Pa

# read csv file
filename = os.path.join(os.path.dirname(__file__), 'weather.csv')
weather = pd.read_csv(filename, index_col=0, header=[0, 1],
                      date_parser=lambda idx: pd.to_datetime(idx, utc=True))

# change type of index to datetime and set time zone
weather.index = pd.to_datetime(weather.index).tz_convert('Europe/Berlin')

# change type of height from str to int by resetting columns
l0 = [_[0] for _ in weather.columns]
l1 = [int(_[1]) for _ in weather.columns]
weather.columns = [l0, l1]


##########################################################################
# 2. Initialize the wind turbines
##########################################################################

# This example shows two ways to initialize a WindTurbine object. You can
# either specify your own turbine, as done below for 'myTurbine', or fetch
# power and/or power coefficient curve data from data files provided by the
# windpowerlib, as done for the 'enerconE126'.

# Execute ``windpowerlib.wind_turbine.get_turbine_types()`` to see a table
# of all wind turbines for which power (coefficient) curve data is
# provided.

# specification of own wind turbine (Note: power coefficient values and
# nominal power have to be in Watt)
logging.info("2. Initialize the wind turbines")

my_turbine = {
    'name': 'myTurbine',
    'nominal_power': 3e6,  # in W
    'hub_height': 105,  # in m
    'rotor_diameter': 90,  # in m
    'power_curve': pd.DataFrame(
        data={'value': [p * 1000 for p in [
                  0.0, 26.0, 180.0, 1500.0, 3000.0, 3000.0]],  # in W
              'wind_speed': [0.0, 3.0, 5.0, 10.0, 15.0, 25.0]})  # in m/s
}
# initialize WindTurbine object
my_turbine = WindTurbine(**my_turbine)

# specification of wind turbine where power curve is provided
# if you want to use the power coefficient curve change the value of
# 'fetch_curve' to 'power_coefficient_curve'
enercon_e126 = {
    'name': 'E-126/4200',  # turbine name as in register
    'hub_height': 135,  # in m
    'rotor_diameter': 127,  # in m
    'fetch_curve': 'power_curve',  # fetch power curve #
    'data_source': 'oedb'  # data source oedb or name of csv file
}
# initialize WindTurbine object
e126 = WindTurbine(**enercon_e126)


##########################################################################
# 3. Calculate the output and evaluate the turbine
##########################################################################

# The modelchain.ModelChain is a class that provides all necessary steps to
# calculate the power output of a wind turbine. You can either use the default
# methods for the calculation steps, as done for my_turbine or choose different
# methods, as done for the 'e126'.

logging.info("3. Calculate the output and evaluate the turbine")

# power output calculation for my_turbine initialize ModelChain with default
# parameters and use run_model method to calculate power output
mc_my_turbine = ModelChain(my_turbine).run_model(weather)

# write power output time series to WindTurbine object
my_turbine.power_output = mc_my_turbine.power_output

# power output calculation for e126
# own specifications for ModelChain setup
modelchain_data = {
    'wind_speed_model': 'logarithmic',  # 'logarithmic' (default),
                                        # 'hellman' or
                                        # 'interpolation_extrapolation'
    'density_model': 'ideal_gas',  # 'barometric' (default), 'ideal_gas' or
                                   # 'interpolation_extrapolation'
    'temperature_model': 'linear_gradient',  # 'linear_gradient' (def.) or
                                             # 'interpolation_extrapolation'
    'power_output_model': 'power_curve',  # 'power_curve' (default) or
                                          # 'power_coefficient_curve'
    'density_correction': True,  # False (default) or True
    'obstacle_height': 0,  # default: 0
    'hellman_exp': None}  # None (default) or None

# initialize ModelChain with own specifications and use run_model method
# to calculate power output
mc_e126 = ModelChain(e126, **modelchain_data).run_model(weather)

# write power output time series to WindTurbine object
e126.power_output = mc_e126.power_output


##########################################################################
# 4. Plot or print the output
##########################################################################

logging.info("4. Plot or print the output")
# plot or print turbine power output (plot need matplotlib)
if plt:
    e126.power_output.plot(legend=True, label='Enercon E126')
    my_turbine.power_output.plot(legend=True, label='myTurbine')
    plt.show()
else:
    print(e126.power_output)
    print(my_turbine.power_output)

# plot or print power (coefficient) curve
if plt:
    if e126.power_coefficient_curve is not None:
        e126.power_coefficient_curve.plot(
            x='wind_speed', y='power coefficient', style='*',
            title='Enercon E126 power coefficient curve')
        plt.show()
    if e126.power_curve is not None:
        e126.power_curve.plot(x='wind_speed', y='value', style='*',
                              title='Enercon E126 power curve')
        plt.show()
    if my_turbine.power_coefficient_curve is not None:
        my_turbine.power_coefficient_curve.plot(
            x='wind_speed', y='power coefficient', style='*',
            title='myTurbine power coefficient curve')
        plt.show()
    if my_turbine.power_curve is not None:
        my_turbine.power_curve.plot(x='wind_speed', y='value', style='*',
                                    title='myTurbine power curve')
        plt.show()
else:
    if e126.power_coefficient_curve is not None:
        print(e126.power_coefficient_curve)
    if e126.power_curve is not None:
        print(e126.power_curve)
