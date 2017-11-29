Create a FORK of this repository to store your code, data, and documentation for the final project. Detailed instructions for this assignment are in the course Moodle site.  The reason I'm asking you to fork this empty repository instead of creating a stand-alone repository is that it will be much easier for me and all students in the course to find all of our projects for code review and for grading. You can even get code review from students in the other section of IS590PR this way.

Even though your fork of this repository shall remain public, you'll still need to explicitly add any students on your team as Collaborators in the Settings. That way you can grant them write privileges.

DELETE the lines from TEMPLATE up.

TEMPLATE for your report:

# Title: 
_StopLight Simulator_

## Team Member(s):
(Note: Don't put your email addresses here (which is public).  If a student wants their NAME hidden as well, due to optional FERPA regulations, they can be listed purely by their GitHub ID).

-Akhila Khanapuri
-Roshini Seshadri
-Natalie DeClerck

# Monte Carlo Simulation Scenario & Purpose:
We plan to simulate the flow of traffic at a stoplight in a 4-way intersection. For simplicity, both roads will be 2-way single-lane streets that allow the cars to go straight or turn either direction at the stoplight.
The purpose of the simulation would be to test the stoplight changing color at different time intervals in order to optimize the best timing for the intersection. To do this we will assume sensors are not used to check for traffic. 

### Hypothesis before running the simulation:



### Simulation's variables of uncertainty
List and describe your simulation's variables of uncertainty (where you're using pseudo-random number generation). 
For each such variable, how did you decide the range and which probability distribution to use?  
Do you think it's a good representation of reality?

To simulate the stoplight scenario, we will have 4 queue data structures running North/South, East/West.
We will have 4 continous random variables for the time intervals between when the cars arrive at each queue. These will all be drawn from a uniform probability distribution, with various ranges.
We also want to simulate that one of the roads is busier than the other, since this is often true in reality. To do this, the North & South queue time intervals could be drawn from a uniform distribution between 2 seconds and 30 seconds, while the East and West queue intervals could range from 2 seconds to 3 minutes.

In addition to car arrival times, each queue will have a discrete random variable for which direction the car goes at the light from 3 choices: straight, left, or right. To start we may use random.choice() and use the default uniform probability distribution to identify which direction the car will go. However, it is probably more likely cars on the busier road will go straight than turn onto the less busy road, and we could weight the probabilities to reflect that.

In reality, our random variables for time intervals between cars are really dependent on the time of day and location. Most intersections would have a rush hour in the morning and at the end of the work day. If the intersection is located near a lot of restaurants, lunch and dinner times would also have higher flows of traffic. The direction random variables are really dependent on the intersection as well. For example, if there is a popular destination East of the intersection, it's probably much more likely that cars coming from the North, South, and East running queues will go the direction that orients them East at the light. To represent this situation realistically we could pick a familiar intersection and imagine the probability distrubtions that make sense.


## Instructions on how to use the program:


## Sources Used:

A traffic simulator in C++ for reference:
<http://www.dreamincode.net/forums/topic/343059-traffic-light-simulation/>
