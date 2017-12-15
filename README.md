# StopLight Simulator

## Team Members:

* Akhila Khanapuri
* Roshini Seshadri
* Natalie DeClerck

# Monte Carlo Simulation Scenario & Purpose:
We plan to simulate the flow of traffic at a stoplight in a 4-way intersection. For simplicity, both roads will be 2-way single-lane streets that allow the cars to go straight or turn either direction at the stoplight.
The purpose of the simulation would be to test the stoplight changing color at different time intervals in order to optimize the best timing for the intersection. To do this we will assume sensors are not used to check for traffic. 

### Hypothesis before running the simulation:
Configuration used:

1)  Intersection -> 4-way cross road
2)  Road -> Bi-directional traffic 
3)  North-South Traffic -> Time intervals between arriving cars uniformly distributed around a smaller range (1-30 seconds)
4)  East/West Traffic -> Time intervals between arriving cars uniformly distributed around a larger range (3-60 seconds)
5)  Direction that a car can go -> Left/Right/Straight - Randomly generated.
6)  Cycle time of a traffic signal -> 60 secs. North/South green light time is iterated as a parameter, and red light time is always 60 seconds - the green light time
7)  Sensors -> None used.

Hypothesis:

We expected average wait time to be lowest at a N/S green light time greater than 30 seconds, because we are simulating more traffic on the N/S road.


### Simulation's variables of uncertainty
List and describe your simulation's variables of uncertainty (where you're using pseudo-random number generation). 
For each such variable, how did you decide the range and which probability distribution to use?  
Do you think it's a good representation of reality?

To simulate the stoplight scenario, we have 4 queue data structures running North/South, East/West.
We will have 4 continuous random variables for the time intervals between when the cars arrive at each queue. These will all be drawn from a uniform probability distribution, with various ranges.
We want to simulate that one of the roads is busier than the other, since this is often true in reality. To do this, the North & South queue time intervals could be drawn from a uniform distribution between 1 seconds and 30 seconds, while the East and West queue intervals could range from 3 seconds to 1 minute.
In addition to car arrival times, each queue will have a discrete random variable for which direction the car goes at the light from 3 choices: straight, left, or right. We are using random.choice() with the default uniform probability distribution to identify which direction the car will go.
However, it is probably more likely cars on the busier road would go straight than turn onto the less busy road, and we could weight the probabilities to reflect that and make our simulation more realistic.

The N/S light always starts green in the simulation and an entire green-red light cycle is always 60 seconds. No yellow light is used.

Currently we are not considering the speed or acceleration time of the cars. Each car released after waiting at the intersection is delayed for a constant 3 seconds, to simulating the time it takes to clear the intersection.
In reality, our random variables for time intervals between cars would be really dependent on the time of day and location. Most intersections would have a rush hour in the morning and at the end of the work day. If the intersection were located near a lot of restaurants, lunch and dinner times would also have higher flows of traffic.
The direction random variables are really dependent on the intersection as well. For example, if there is a popular destination East of the intersection, it's probably much more likely that cars coming from the North, South, and East running queues will go the direction that orients them East at the light.
To represent this situation realistically we could have picked a familiar intersection and imagined the probability distributions that make sense. Our current implementation does not take these factors into account.


## Instructions on how to use the program:
The parameter to the program is the duration of the North/South green light within a 60-second light cycle. Currently we are iterating from 1-59 seconds and running the simulation on every odd number of seconds.
The sample size N can also be changed by the user. Each parameter value is currently run N=100 times, and summary statistics are calculated and plotted for each parameter value.

The program calculates the average time it takes for a car to get through the intersection after arriving, based on different light cycle times.

## Results:
Plots of the average max and mean values for each N/S green light duration are saved in the working directory.
These plots show 95% confidence intervals around each statistic, and the point at the minimum wait time is plotted in red, which can be used to decide the optimal green light time.

Our conclusion is that the optimal duration for the North/South green light is about 45 seconds. With this parameter, the average wait time for a car to get through the intersection is around 15 seconds.
While the average maximum wait time is more optimal at a shorter North/South green light time of about 40 seconds, the trend does not change significantly between 40-45 seconds of green light duration.
The max wait times are also slightly more variable than the means (larger confidence interval bounds), so we feel that 45 seconds works to minimize both the max and mean wait times.


## Sources Used:

1.) A traffic simulator in C++ for reference:
  <http://www.dreamincode.net/forums/topic/343059-traffic-light-simulation/>
  
2.) https://people.sc.fsu.edu/~jburkardt/classes/isc_2009/monte_carlo_simulation.pdf

3.) Example using SimPy: http://phillipmfeldman.org/Python/discrete_event_simulation/traffic_sim.py

4.) [SimPy documentation] (https://simpy.readthedocs.io/en/latest/simpy_intro/basic_concepts.html)
