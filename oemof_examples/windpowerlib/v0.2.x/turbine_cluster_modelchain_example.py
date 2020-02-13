"""
The ``turbine_cluster_modelchain_example`` module shows how to calculate the
power output of wind farms and wind turbine clusters with the windpowerlib.
A cluster can be useful if you want to calculate the feed-in of a region for
which you want to use one single weather data point.

Functions that are used in the ``modelchain_example``, like the initialization
of wind turbines, are imported and used without further explanations.

SPDX-FileCopyrightText: 2019 oemof developer group <contact@oemof.org>
SPDX-License-Identifier: MIT
"""
import pandas as pd
import logging
import os
import requests
from windpowerlib import (WindFarm, WindTurbine, WindTurbineCluster,
                          TurbineClusterModelChain)

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None


def get_weather_data(filename='weather.csv', **kwargs):
    r"""
    Imports weather data from a file.

    The data include wind speed at two different heights in m/s, air
    temperature in two different heights in K, surface roughness length in m
    and air pressure in Pa. The file is located in the example folder of the
    windpowerlib. The height in m for which the data applies is specified in
    the second row.

    Parameters
    ----------
    filename : str
        Filename of the weather data file. Default: 'weather.csv'.

    Other Parameters
    ----------------
    datapath : str, optional
        Path where the weather data file is stored.
        Default: 'windpowerlib/example'.

    Returns
    -------
    :pandas:`pandas.DataFrame<frame>`
            DataFrame with time series for wind speed `wind_speed` in m/s,
            temperature `temperature` in K, roughness length `roughness_length`
            in m, and pressure `pressure` in Pa.
            The columns of the DataFrame are a MultiIndex where the first level
            contains the variable name as string (e.g. 'wind_speed') and the
            second level contains the height as integer at which it applies
            (e.g. 10, if it was measured at a height of 10 m).

    """

    if "datapath" not in kwargs:
        kwargs["datapath"] = os.path.dirname(__file__)

    file = os.path.join(kwargs["datapath"], filename)

    if not os.path.isfile(file):
        logging.debug("Download weather data for example.")
        req = requests.get("https://osf.io/59bqn/download")
        with open(file, "wb") as fout:
            fout.write(req.content)

    # read csv file
    weather_df = pd.read_csv(
        file,
        index_col=0,
        header=[0, 1],
        date_parser=lambda idx: pd.to_datetime(idx, utc=True),
    )

    # change type of index to datetime and set time zone
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert(
        "Europe/Berlin"
    )

    return weather_df


def initialize_wind_turbines():
    r"""
    Initializes three :class:`~.wind_turbine.WindTurbine` objects.

    This function shows three ways to initialize a WindTurbine object. You can
    either use turbine data from the OpenEnergy Database (oedb) turbine library
    that is provided along with the windpowerlib, as done for the
    'enercon_e126', or specify your own turbine by directly providing a power
    (coefficient) curve, as done below for 'my_turbine', or provide your own
    turbine data in csv files, as done for 'dummy_turbine'.

    To get a list of all wind turbines for which power and/or power coefficient
    curves are provided execute `
    `windpowerlib.wind_turbine.get_turbine_types()``.

    Returns
    -------
    Tuple (:class:`~.wind_turbine.WindTurbine`,
           :class:`~.wind_turbine.WindTurbine`,
           :class:`~.wind_turbine.WindTurbine`)

    """

    # specification of wind turbine where data is provided in the oedb
    # turbine library
    enercon_e126 = {
        "turbine_type": "E-126/4200",  # turbine type as in register
        "hub_height": 135,  # in m
    }
    # initialize WindTurbine object
    e126 = WindTurbine(**enercon_e126)

    # specification of own wind turbine (Note: power values and nominal power
    # have to be in Watt)
    my_turbine = {
        "nominal_power": 3e6,  # in W
        "hub_height": 105,  # in m
        "power_curve": pd.DataFrame(
            data={
                "value": [
                    p * 1000
                    for p in [0.0, 26.0, 180.0, 1500.0, 3000.0, 3000.0]
                ],  # in W
                "wind_speed": [0.0, 3.0, 5.0, 10.0, 15.0, 25.0],
            }
        ),  # in m/s
    }
    # initialize WindTurbine object
    my_turbine = WindTurbine(**my_turbine)

    return my_turbine, e126


def initialize_wind_farms(my_turbine, e126):
    r"""
    Initializes two :class:`~.wind_farm.WindFarm` objects.

    This function shows how to initialize a WindFarm object. A WindFarm needs
    a wind turbine fleet specifying the wind turbines and their number or
    total installed capacity (in Watt) in the farm. Optionally, you can provide
    a wind farm efficiency (which can be constant or dependent on the wind
    speed) and a name as an identifier. See :class:`~.wind_farm.WindFarm` for
    more information.

    Parameters
    ----------
    my_turbine : :class:`~.wind_turbine.WindTurbine`
        WindTurbine object with self provided power curve.
    e126 : :class:`~.wind_turbine.WindTurbine`
        WindTurbine object with power curve from the OpenEnergy Database
        turbine library.

    Returns
    -------
    tuple(:class:`~.wind_farm.WindFarm`, :class:`~.wind_farm.WindFarm`)

    """

    # specification of wind farm data where turbine fleet is provided in a
    # pandas.DataFrame
    # for each turbine type you can either specify the number of turbines of
    # that type in the wind farm (float values are possible as well) or the
    # total installed capacity of that turbine type in W
    wind_turbine_fleet = pd.DataFrame(
        {
            "wind_turbine": [my_turbine, e126],  # as windpowerlib.WindTurbine
            "number_of_turbines": [6, None],
            "total_capacity": [None, 12.6e6],
        }
    )
    # initialize WindFarm object
    example_farm = WindFarm(
        name="example_farm", wind_turbine_fleet=wind_turbine_fleet
    )

    # specification of wind farm data (2) containing a wind farm efficiency
    # wind turbine fleet is provided using the to_group function
    example_farm_2_data = {
        "name": "example_farm_2",
        "wind_turbine_fleet": [
            my_turbine.to_group(6),
            e126.to_group(total_capacity=12.6e6),
        ],
        "efficiency": 0.9,
    }
    # initialize WindFarm object
    example_farm_2 = WindFarm(**example_farm_2_data)

    return example_farm, example_farm_2


def initialize_wind_turbine_cluster(example_farm, example_farm_2):
    r"""
    Initializes a :class:`~.wind_turbine_cluster.WindTurbineCluster` object.

    Function shows how to initialize a WindTurbineCluster object. A
    WindTurbineCluster consists of wind farms that are specified through the
    `wind_farms` parameter. Optionally, you can provide a name as an
    identifier.

    Parameters
    ----------
    example_farm : :class:`~.wind_farm.WindFarm`
        WindFarm object without provided efficiency.
    example_farm_2 : :class:`~.wind_farm.WindFarm`
        WindFarm object with constant wind farm efficiency.

    Returns
    -------
    :class:`~.wind_turbine_cluster.WindTurbineCluster`

    """

    # specification of cluster data
    example_cluster_data = {
        "name": "example_cluster",
        "wind_farms": [example_farm, example_farm_2],
    }
    # initialize WindTurbineCluster object
    example_cluster = WindTurbineCluster(**example_cluster_data)

    return example_cluster


def calculate_power_output(weather, example_farm, example_cluster):
    r"""
    Calculates power output of wind farms and clusters using the
    :class:`~.turbine_cluster_modelchain.TurbineClusterModelChain`.

    The :class:`~.turbine_cluster_modelchain.TurbineClusterModelChain` is a
    class that provides all necessary steps to calculate the power output of a
    wind farm or cluster. You can either use the default methods for the
    calculation steps, as done for 'example_farm', or choose different methods,
    as done for 'example_cluster'.

    Parameters
    ----------
    weather : :pandas:`pandas.DataFrame<frame>`
        Contains weather data time series.
    example_farm : :class:`~.wind_farm.WindFarm`
        WindFarm object without provided efficiency.
    example_cluster : :class:`~.wind_turbine_cluster.WindTurbineCluster`
        WindTurbineCluster object.

    """
    example_farm.efficiency = 0.9
    # power output calculation for example_farm
    # initialize TurbineClusterModelChain with default parameters and use
    # run_model method to calculate power output
    mc_example_farm = TurbineClusterModelChain(example_farm).run_model(weather)
    # write power output time series to WindFarm object
    example_farm.power_output = mc_example_farm.power_output

    # power output calculation for turbine_cluster
    # own specifications for TurbineClusterModelChain setup
    modelchain_data = {
        "wake_losses_model": "wind_farm_efficiency",
        # 'dena_mean' (default), None,
        # 'wind_farm_efficiency' or name
        #  of another wind efficiency curve
        #  see :py:func:`~.wake_losses.get_wind_efficiency_curve`
        "smoothing": True,  # False (default) or True
        "block_width": 0.5,  # default: 0.5
        "standard_deviation_method": "Staffell_Pfenninger",  #
        # 'turbulence_intensity' (default)
        # or 'Staffell_Pfenninger'
        "smoothing_order": "wind_farm_power_curves",  #
        # 'wind_farm_power_curves' (default) or
        # 'turbine_power_curves'
        "wind_speed_model": "logarithmic",  # 'logarithmic' (default),
        # 'hellman' or
        # 'interpolation_extrapolation'
        "density_model": "ideal_gas",  # 'barometric' (default), 'ideal_gas' or
        # 'interpolation_extrapolation'
        "temperature_model": "linear_gradient",  # 'linear_gradient' (def.) or
        # 'interpolation_extrapolation'
        "power_output_model": "power_curve",  # 'power_curve' (default) or
        # 'power_coefficient_curve'
        "density_correction": True,  # False (default) or True
        "obstacle_height": 0,  # default: 0
        "hellman_exp": None,
    }  # None (default) or None
    # initialize TurbineClusterModelChain with own specifications and use
    # run_model method to calculate power output
    mc_example_cluster = TurbineClusterModelChain(
        example_cluster, **modelchain_data
    ).run_model(weather)
    # write power output time series to WindTurbineCluster object
    example_cluster.power_output = mc_example_cluster.power_output

    return


def plot_or_print(example_farm, example_cluster):
    r"""
    Plots or prints power output and power (coefficient) curves.

    Parameters
    ----------
    example_farm : :class:`~.wind_farm.WindFarm`
        WindFarm object without provided efficiency.
    example_cluster : :class:`~.wind_turbine_cluster.WindTurbineCluster`
        WindTurbineCluster object.

    """

    # plot or print power output
    if plt:
        example_cluster.power_output.plot(legend=True, label='example cluster')
        example_farm.power_output.plot(legend=True, label='example farm')
        plt.xlabel('Wind speed in m/s')
        plt.ylabel('Power in W')
        plt.show()
    else:
        print(example_cluster.power_output)
        print(example_farm.power_output)


def run_example():
    r"""
    Runs the example.

    """
    # You can use the logging package to get logging messages from the
    # windpowerlib. Change the logging level if you want more or less messages:
    # logging.DEBUG -> many messages
    # logging.INFO -> few messages
    logging.getLogger().setLevel(logging.DEBUG)

    weather = get_weather_data("weather.csv")
    my_turbine, e126 = initialize_wind_turbines()
    example_farm, example_farm_2 = initialize_wind_farms(my_turbine, e126)
    example_cluster = initialize_wind_turbine_cluster(
        example_farm, example_farm_2
    )
    calculate_power_output(weather, example_farm, example_cluster)
    plot_or_print(example_farm, example_cluster)


if __name__ == "__main__":
    run_example()
