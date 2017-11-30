# Title: StopLight Simulator

## Team Member(s): 

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
3)  North-South Traffic -> Uniformly distributed around a lower mean
4)  East/West Traffic -> Uniformly distributed around a higher mean
5)  Arrival time of cars at the intersection -> Uniformly distributed
6)  Direction that a car can go -> Left/Right/Straight - Randomly generated.
7)  Cycle time of a traffic signal -> 60 secs
8)  Sensors -> None used.

Hypothesis:

1) Peak hours: We expect the wait time to reduce by 25% during peak hours.
2) Non- peak hours : We expect the wait time to reduce by more than 40%.


### Simulation's variables of uncertainty
List and describe your simulation's variables of uncertainty (where you're using pseudo-random number generation). 
For each such variable, how did you decide the range and which probability distribution to use?  
Do you think it's a good representation of reality?

To simulate the stoplight scenario, we will have 4 queue data structures running North/South, East/West.
We will have 4 continous random variables for the time intervals between when the cars arrive at each queue. These will all be drawn from a uniform probability distribution, with various ranges.
We also want to simulate that one of the roads is busier than the other, since this is often true in reality. To do this, the North & South queue time intervals could be drawn from a uniform distribution between 2 seconds and 30 seconds, while the East and West queue intervals could range from 2 seconds to 3 minutes.

In addition to car arrival times, each queue will have a discrete random variable for which direction the car goes at the light from 3 choices: straight, left, or right. To start we may use random.choice() and use the default uniform probability distribution to identify which direction the car will go. However, it is probably more likely cars on the busier road will go straight than turn onto the less busy road, and we could weight the probabilities to reflect that.

In reality, our random variables for time intervals between cars are really dependent on the time of day and location. Most intersections would have a rush hour in the morning and at the end of the work day. If the intersection is located near a lot of restaurants, lunch and dinner times would also have higher flows of traffic. The direction random variables are really dependent on the intersection as well. For example, if there is a popular destination East of the intersection, it's probably much more likely that cars coming from the North, South, and East running queues will go the direction that orients them East at the light. To represent this situation realistically we could pick a familiar intersection and imagine the probability distributions that make sense.


## Instructions on how to use the program:
The inputs to the program will be the duration of the stoplight changing color, the time intervals at which the cars arrive at the intersection, the number of cars that are allowed to pass through during one green cycle and lastly, the direction that the car takes. 

The program would calculate the average waiting time for a particular car in different stop time intervals and hence, deciding the optimal time for the stop signal.

## Sources Used:

1.) A traffic simulator in C++ for reference:
  <http://www.dreamincode.net/forums/topic/343059-traffic-light-simulation/>
2.) https://people.sc.fsu.edu/~jburkardt/classes/isc_2009/monte_carlo_simulation.pdf 
