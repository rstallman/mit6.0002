# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Shrijan Karmacharya
# Collaborators (discussion):
# Time: 12:00 hrs

import pylab, numpy
import re
import math, random
import matplotlib.pyplot as plt

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    x_mean = pylab.mean(x)
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x_mean)**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    return [pylab.polyfit(x, y, d) for d in degs]

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = float(reduce(lambda x, y: x+y, y))/len(y)
    # Numpy arrays can be added
    r_sq = float(1 - (reduce(lambda x, y: x+y, (y - estimated) ** 2)
                 / reduce(lambda x, y: x+y, [(y[i] - mean) ** 2 for i in range(0, len(y))])))
    return float(r_sq)


def binom(model, x):
    val = 0
    for n in range (0, len(model)):
        val += model[n] * (x ** (len (model) - n - 1))

    return val


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    colors = ["red", "green", "orange", "purple", "pink", "yellow"]
    fig = plt.figure()
    for model in models:
        # Self coded poly val calcuator binom used, y based on x values on any degree polynomial
        # estimated = [binom(model, i) for i in x[:]]
        plt.plot (x, y, 'bo')
        estimated = pylab.polyval(model, x)
        r_s = r_squared(y, estimated)
        if len(model) == 2:
            lbl = 'R sq = ' + str(r_s) + ' \n' + str (len (model) - 1) + ' degree\n' + ' SE over slope = ' + str(se_over_slope(x, y, estimated,model))
        else:
            lbl = 'R sq = ' + str(r_s) + ' \n' + str(len(model) - 1) + ' degree'
        plt.xlabel('Year')
        plt.ylabel('Temperature')
        plt.title(lbl + ' regression for temperature SD with 5 year moving average')
        plt.plot(x , estimated, 'r-')

        plt.show()




def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    city_avgs = []
    for year in years:
        # could be 366 for leap
        avg_temp_list = []
        for city in multi_cities:
            cityTemp = climate.get_yearly_temp(city, year)
            avgCityTemp = reduce(lambda x, y: x + y, cityTemp)/(365 if year % 4 != 0 else 366)
            avg_temp_list.append(avgCityTemp)
        city_avgs.append(reduce(lambda x,y: x + y, avg_temp_list[:])/ len(avg_temp_list))
    return pylab.array(city_avgs)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg = []
    for i in range(0, len(y)):
        end_lim = i - window_length + 1
        end_range = range(end_lim, i + 1) if end_lim >= 0 else range(0, i + 1)
        count = 0
        total = 0
        for j in end_range:
            count += 1
            total += y[j]
        moving_avg.append(float(total)/ count)
    return pylab.array(moving_avg)


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return math.sqrt(reduce(lambda x, y: x+ y, (y - estimated) ** 2)/ len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    city_sd = []
    for year in years:
        # could be 366 for leap
        sd_list = []
        for city in multi_cities:
            cityTemp = climate.get_yearly_temp (city, year)
            avgCityTemp = reduce (lambda x, y: x + y, cityTemp) / (365 if year % 4 != 0 else 366)
            sd_list.append (math.sqrt(reduce(lambda x, y: x + y, [(t - avgCityTemp) ** 2 for t in cityTemp])/ len(cityTemp)))
        city_sd.append (reduce (lambda x, y: x + y, sd_list[:]) / len (sd_list))
    return pylab.array (city_sd)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    fig = plt.figure ()
    for model in models:
        # Self coded poly val calcuator binom used, y based on x values on any degree polynomial
        # estimated = [binom(model, i) for i in x[:]]
        plt.plot (x, y, 'bo')
        estimated = pylab.polyval (model, x)
        r_m_s_e = rmse(y, estimated)
        lbl = 'RMSE = ' + str (r_m_s_e) + ' \n' + str (len (model) - 1) + ' degree'
        plt.xlabel ('Year')
        plt.ylabel ('Temperature')
        plt.title (lbl + ' regression for national annual avg temp')
        plt.plot (x, estimated, 'r-')

        plt.show ()

# if __name__ == '__main__':

climate = Climate ('data.csv')

    # Part A.4
# sample = [climate.get_daily_temp('NEW YORK',1,10, y) for y in range(1961, 2009)]
# print sample
# climate = Climate('data.csv')
# sample = gen_cities_avg(climate, ['NEW YORK'], range(1961, 2009))


# Part B
# sample = gen_cities_avg(climate, CITIES, range(1961, 2009))
# models = generate_models(range(1961, 2009), sample, [1, 2])
# evaluate_models_on_training(range(1961, 2009), sample, models)


# Part C
# moving_avg = moving_average(sample, 5)
#
# models = generate_models(range(1961, 2009), moving_avg, [1, 2])
# evaluate_models_on_training(range(1961, 2009), moving_avg, models)

# Part D.2
# training = gen_cities_avg(climate, CITIES, range(1961, 2009))
# train_moving_avg = moving_average(training, 5)
# models = generate_models(range(1961, 2009), train_moving_avg, [1, 2, 20])
# evaluate_models_on_training(range(1961, 2009), train_moving_avg, models)
# testing = gen_cities_avg(climate, CITIES, range(2010, 2015))
# test_moving_avg = moving_average(testing, 5)
# evaluate_models_on_testing(range(2010, 2015), test_moving_avg, models)




# Part E
# TODO: replace this line with your code
training_sd = gen_std_devs(climate, CITIES, range(1961, 2009))
train_moving_avg = moving_average(training_sd, 5)
models = generate_models(range(1961, 2009), train_moving_avg, [1, 2, 20])
evaluate_models_on_training(range(1961, 2009), train_moving_avg, models)



