import numpy as np
import matplotlib.pyplot as plt
from random import random

def gen_exponential_outcome(lam):
    '''
    Generates an outcome for an exponential
    distribution, given a lambda.
    '''
    return -lam*np.log(random())

def create_exponential_outcome_function(lam):
    def f():
        return -lam*np.log(random())
    return f

def triangular_outcome_function():
    while True:
        outcome = (random(), random())
        if outcome[0] + outcome[1] < 1: # self-select outcomes not in the triangle.
            return outcome[0]


def run_trial(start, finish, subintervals, outcome_generator, num_of_points):
    '''
    Runs a trial given a set of parameters.
    Returns the area scaled heights of rectangles
    for a histogram.
    '''
    results = [0 for i in range(subintervals)]

    bucket_step = (finish - start) / subintervals
    divisions = [i * bucket_step for i in range(subintervals+1)]

    i = 0
    while i < num_of_points:
        outcome = outcome_generator()
        if start < outcome < finish:
            prev = 0
            j = 1
            while j < len(divisions): # place each outcome into the proper bucket.
                if divisions[prev] < outcome < divisions[j]:
                    results[j-1] += 1
                    break
                prev = j
                j += 1
            i += 1

    for event in range(len(results)):
        results[event] /= (num_of_points * bucket_step)

    return results

def run_exponential_sim(ax):
    '''
    Given a subplot, plots the results of a simulation that
    models an exponential distribution. 

    Returns nothing.
    '''

    # Note that the sim assumes that points ONLY 
    # should fall in the range from (start, finish)
    # so it will eliminate points not in the range.
    # The result of this is that the area under the
    # bar graph will always be 1 while that under 
    # the curve will not. Good parameters mask this
    # flaw.

    curve = 'Ideal Curve'
    data = 'Simulation Results'
    ax.set_title('Exponential Distribution')

    start = 0
    finish = 120
    lam = 30 # lam signifies the average time between events for an exponential distribution of probabilities.
    subintervals = 24
    num_of_points = 10000 # Number of random outcomes selected.

    x = np.linspace(start, finish, 256)
    k = 1/lam
    y = (k)*np.exp(-k*x) # graph that fits the histogram.

    f = create_exponential_outcome_function(lam)

    results = run_trial(start, finish, subintervals, f, num_of_points)

    # The histogram step has to be different from the bucket step because
    # the histogram uses start and finish as endpoints AND delineators.
    hist_step = (finish - start) / (subintervals-1) 

    divisions = [(i * hist_step) for i in range(subintervals)]

    ax.plot(x,y, label=curve)
    ax.hist(divisions, subintervals, weights=results, edgecolor='black',label=data)

    ax.legend()

def run_triangular_sim(ax):
    '''
    Given a subplot plots the results of a sim that
    models a non-uniform distribution. Namely, it
    simulates the distribution of x values from random
    points in R^2 that fall in the triangle bounded
    by (0,0) (0,1) & (1,0).

    Returns nothing; plots histogram and ideal graph.
    '''

    curve = 'Ideal Curve'
    data = 'Simulation Results'
    ax.set_title('Arbitrary (Triangular) Distribution')

    start = 0
    finish = 1
    subintervals = 20
    num_of_points = 100000 # Number of random outcomes selected.

    x = np.linspace(start, finish, 256)
    y = 2 - 2*x # graph that fits the histogram.

    f = triangular_outcome_function

    results = run_trial(start, finish, subintervals, f, num_of_points)

    hist_step = (finish - start) / (subintervals-1) 

    divisions = [(i * hist_step) for i in range(subintervals)]

    ax.plot(x,y, label=curve)
    ax.hist(divisions, subintervals, weights=results, edgecolor='black',label=data)

    ax.legend()

if __name__ == '__main__':

    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,10))

    print('Simulating Exponential Probability Distribution... ', end='')

    run_exponential_sim(ax1)

    print('done.')
    print('Simulating "Triangular" Probability Distribution... ', end='')

    run_triangular_sim(ax2)

    print('done.')
    print('Displaying Histograms of simulation results.')

    plt.show()
