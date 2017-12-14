import simpy
import random
import time
from queue import Queue
import numpy as np
import matplotlib.pyplot as plt


def arrive(queue, direction):
    """
    A function to randomly generate when cars arrive from a uniform distribution, and
    update the queue when a car arrives and joins a queue in the particular direction.
    For the NS queues the cars arrive at a shorter time compared to the EW queues, simulating a busier NS road.
    :param queue: Queue input takes the values N_Queue, S_Queue, E_Queue, W_Queue
    :param direction: Direction the queue is traveling: takes the values N ,S, E, W
    :return:
    """
    global arrive_count
    global NS_light, EW_light

    while True:
        # instantiate the light variable based on the queue direction and the current status of that light
        if direction == 'N' or direction == 'S':
            light = NS_light
        else:
            light = EW_light

        # this is the position of the car in the queue
        arrive_count += 1
        # add the car to the total count
        Stats['car_count'] += 1

        # if the light is red, or there are cars ahead of this one in the queue, add this car's position
        # and arrival time to the end of the queue
        if light == 'red' or queue.qsize() > 0:
            queue.put((arrive_count, env.now))
            # print statement to show the status of the car joining the queue
            if print_sim: print("Car #{arrive_count} arrived and joined the {direction} queue at position {length} " 
                                "at time {time: .3f}.".format(arrive_count=arrive_count, direction=direction, length=queue.qsize(), time=env.now))
        # if the light is green, and there are no cars ahead of this one in the queue,
        # the car passes and is not added to the queue
        else:
            # print statement to show that a car entered the simulation and
            # passed through a green light without being added to a queue
            if print_sim: print("Car #{arrive_count} passed through a green light going {direction} with no cars waiting "
                                "at time {time: .3f}.".format(arrive_count=arrive_count, direction=direction, time=env.now))

        # if the car is on the North or South road, delay the arrival for the next car
        # for a random time taken from a uniform distribution with a smaller range
        if direction == 'N' or direction == 'S':
            next_arrival = random.uniform(1, 30)
        # if the car is on the East or West road, delay the arrival for the next car
        # for a random time taken from a uniform distribution with a larger range
        else:
            next_arrival = random.uniform(3, 60)
        yield env.timeout(next_arrival)


def depart(queue, direction):
    """
    A function to keep track of the cars which depart from a particular queue.  It calculates how long
    each car took to get through the intersection, and updates the total and max wait times for the simulation.
    :param queue: N_Queue, S_Queue, E_Queue, W_Queue
    :param direction: Which direction the queue is traveling: N/S/E/W
    :param light: Red or Green light status for the queue passed
    :return:
    """
    global cur_max_wait
    global NS_light, EW_light
    clear_delay = 3

    while True:
        # instantiate the light variable based on the queue direction and the current status of that light
        if direction == 'N' or direction == 'S':
            light = NS_light
        else:
            light = EW_light
        # if the light is red, or there are no cars in the queue, do not start the departure process
        if light == 'red' or queue.qsize() == 0:
            return
        # if the light is green, and there are cars in the queue, start releasing the cars
        else:
            # each departing car takes a constant value of 3 seconds to clear the intersection
            yield env.timeout(clear_delay)
            # remove the first car from the queue, and store its position and arrival time
            car_position, time_arrived = queue.get()
            # calculate the time the car took to get through the intersection after arrival
            time_waiting = env.now - time_arrived

            # print statement to show the status of the departing cars and the queue after departure
            if print_sim: print("Car #{arrive_count} departed at time {time: .3f}, after waiting {time_waiting: .3f}, leaving {length} cars in the "
                                "{direction} queue.".format(arrive_count=car_position, time=env.now, time_waiting=time_waiting, length=queue.qsize(), direction=direction))

            # if the time the car spent in the intersection is larger
            # than the current max time, set this time as the new max
            if time_waiting > cur_max_wait:
                cur_max_wait = time_waiting
                Stats['max_wait_time'] = cur_max_wait

            # update the values for the count of cars who waited in a queue, and the amount of time they waited
            Stats['cars_waiting'] += 1
            Stats['waiting_time'] += time_waiting

            # add left on green rules here
            # pass turn direction as parameter




def light_status(direction, queue, red_time, green_time):
    """
    A function to handle the change in light status from green to red or vice versa. It also
    keeps track of the red light duration and green light duration.
    :param direction:N/S/E/W
    :param queue:N_Queue, S_Queue, E_Queue, W_Queue
    :param red_time: duration of the red light for the NS queues
    :param green_time: duration of the green light for the NS queues
    :return:
    """

    global NS_light, EW_light

    while True:
        # NS light always starts green
        NS_light = 'green'
        EW_light = 'red'

        # if there are cars in the North or South queue, start the depart process for the queue
        if (direction == 'N' or direction == 'S') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction))

        # print statements to show when the NS light changes
        if direction == 'N' or direction == 'S':
            if print_sim: print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            if print_sim: print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))

        # the NS light stays green for the amount of the green_time parameter
        yield env.timeout(green_time)
        Stats['green_count'] += 1
        Stats['green_time'] += green_time

        # light changes status
        NS_light = 'red'
        EW_light = 'green'

        # if there are cars in the East or West queue, start the depart process for the queue
        if (direction == 'E' or direction == 'W') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction))

        # print statements to show when the EW light changes
        if direction == 'W' or direction == 'E':
            if print_sim: print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            if print_sim: print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))

        # the NS light stays red for the amount of the red_time parameter
        yield env.timeout(red_time)
        Stats['red_count'] += 1
        Stats['red_time'] += red_time


def run_sim(NS_green_time, total_time):
    """
    A function which instantiates the process and it runs till the total_time. The simulation always starts
    with a green NS light and red EW light. The red light time is always one minute minus the green light time.
    :param NS_green_time: The North/South green light duration which is passed from the for loop.
    :param total_time: A predefined duration in seconds. 600 seconds
    :return:
    """
    NS_red_time = 60 - NS_green_time

    env.process(light_status(direction='N', queue=N_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(light_status(direction='S', queue=S_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(arrive(queue=N_queue, direction='N'))
    env.process(arrive(queue=S_queue, direction='S'))

    env.process(light_status(direction='E', queue=E_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(light_status(direction='W', queue=W_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(arrive(queue=E_queue, direction='E'))
    env.process(arrive(queue=W_queue, direction='W'))

    env.run(until=total_time)


def calculate_ci(sample_vals):
    """
    :param sample_vals: a list of sample statistics values (means or maxs)
    :return: a list of 95% confidence intervals
    """
    n = len(sample_vals)
    # compute the average of all the means for this green time parameter
    sample_mean = np.mean(sample_vals)
    # compute the 95% confidence intervals for this green time parameter
    std_error_mean = np.std(sample_vals) / np.sqrt(n)
    margin_of_error = 1.96 * std_error_mean
    intervals = (sample_mean - margin_of_error,
                 sample_mean + margin_of_error)
    return intervals

def visualize_data(x, y, conf_intervals, metric):
    """
    A function for visualizating the plot
    :param x: An array plotted on the y-axis which contains all the green times during the entire duration of the simulation
    :param y: An array plotted on the x-axis which contains an average of the max or mean times in seconds that it takes
    for a car to get through the intersection for the entire duration of the simulation
    :param yerr: The standard error around the sample mean or max (sample standard deviation / sqrt(sample size n))
    :param metric: The metric to be plotted and labeled (max or mean)
    :return:
    """
    plt.style.use('ggplot')
    plt.plot(x, y)
    plt.errorbar(x, y, yerr=[(top-bot)/2 for top,bot in conf_intervals])
    min_idx = y.index(min(y))
    plt.plot(x[min_idx], y[min_idx], 'ro')
    plt.suptitle("{} Wait Time vs Duration of N/S Green Light".format(metric), fontsize=16)
    plt.title("with 95% confidence intervals", fontsize=10)
    plt.xlabel("Duration of N/S Green Light in seconds")
    plt.ylabel("{} wait time in seconds".format(metric))


    plt.interactive(False)
    plt.savefig('./{}_plot.png'.format(metric))
    plt.show()




if __name__ == '__main__':
    start = time.time()
    total_time = 600
    # instantiate collector variables to compute summary stats
    green_times = []
    sample_means = []
    sample_maxs = []
    mean_intervals = []
    max_intervals = []
    # to see print statements for each car, set this variable to True
    print_sim = False
    # set the sample size N for each green_time parameter
    N = 100
    print('N =', N)
    # iterate over increasing green_time parameter values between 1 and 59 seconds
    # (red light time values are always 60 seconds - green_time value)
    for green_time in range(0, 61, 2):
        # instantiate mean and max collectors for each parameter value
        means = []
        maxs = []
        # run N simulations for each parameter value
        for i in range(N):
            # reset the environment
            env = simpy.Environment()

            # reset the starting variables
            NS_light = 'green'
            EW_light = 'red'
            cur_max_wait = 0
            arrive_count = 0

            # reset the queues
            N_queue = Queue()
            S_queue = Queue()
            E_queue = Queue()
            W_queue = Queue()

            # reset the simulation stats dictionary
            Stats = dict()
            Stats['cars_waiting'] = 0
            Stats['car_count'] = 0
            Stats['waiting_time'] = 0.0
            Stats['max_wait_time'] = 0
            Stats['red_time'] = 0.0
            Stats['red_count'] = 0
            Stats['green_time'] = 0.0
            Stats['green_count'] = 0

            # run each simulation process for 10 minutes
            run_sim(NS_green_time=green_time, total_time=total_time)

            # empty out the queues that still have cars in them
            # and add their wait times to the Stats dictionary
            for queue in [N_queue, S_queue, E_queue, W_queue]:
                for car in range(queue.qsize()):
                    car_position, time_arrived = queue.get()
                    # calculate the time the car was waiting at the end of the simulation
                    time_waiting = total_time - time_arrived

                    # if the time the car spent in the intersection is larger
                    # than the current max time, set this time as the new max
                    if time_waiting > Stats['max_wait_time']:
                        Stats['max_wait_time'] = time_waiting

                    # update the values for the count of cars who waited in a queue, and the amount of time they waited
                    Stats['cars_waiting'] += 1
                    Stats['waiting_time'] += time_waiting

            # print out summary stats for the simulation
            if print_sim:
                print('\n\n*** Summary ***\n\n')

                print('Green light time:', green_time)
                print('Mean waiting time: %.3f seconds'
                      % (Stats['waiting_time'] / float(Stats['car_count'])))

                print('Max waiting time: %.3f seconds'
                      % Stats['max_wait_time'])

                print('\n')
                for k, v in Stats.items():
                    print(k, ':', v)


            # compute and store the average time to clear the intersection for this simulation
            means.append(Stats['waiting_time'] / float(Stats['car_count']))
            # compute and store the max time to clear the intersection for this simulation
            maxs.append(Stats['max_wait_time'])

        # compute the average of all the means for this green time parameter
        sample_mean = np.mean(means)
        # compute the 95% confidence intervals around the mean
        confidence_interval = calculate_ci(means)
        mean_intervals.append(confidence_interval)

        # compute the average of all the max times for this green time parameter
        sample_max = np.mean(maxs)
        # compute the 95% confidence intervals around the max
        confidence_interval = calculate_ci(maxs)
        max_intervals.append(confidence_interval)

        # collect the sample means, sample maxs, and their standard error
        # to plot against each green time parameter
        sample_means.append(sample_mean)
        sample_maxs.append(sample_max)
        green_times.append(green_time)

    print('Process took', time.time() - start, 'seconds')

    # plots of the max and mean against the green time parameters are shown and saved in the working directory
    visualize_data(x=green_times, y=sample_maxs, conf_intervals=max_intervals, metric='Max')
    visualize_data(x=green_times, y=sample_means, conf_intervals=mean_intervals, metric='Mean')