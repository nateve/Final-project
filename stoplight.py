import simpy
import random
from queue import Queue

NS_light = 'green'
EW_light = 'red'

Stats = dict()
Stats['cars_waiting'] = 0
Stats['car_count'] = 0
Stats['waiting_time'] = 0.0
Stats['red_time'] = 0.0
Stats['red_count'] = 0
Stats['green_time'] = 0.0
Stats['green_count'] = 0

arrive_count = 0
clear_delay = 3
total_time = 200.0

N_queue = Queue()
S_queue = Queue()
E_queue = Queue()
W_queue = Queue()

def arrive(queue, direction, light):
    global arrive_count

    while True:
        arrive_count += 1
        Stats['car_count'] += 1

        if light == 'red' or queue.qsize() > 0:
            queue.put_nowait((arrive_count, env.now))
            print("Car #%d arrived and joined the %s queue at position %d at time "
                  "%.3f." % (arrive_count, direction, queue.qsize(), env.now))
        else:
            print("Car #%d passed through a green light going %s with no cars waiting at time "
                  "%.3f." % (arrive_count, direction, env.now))
        next_arrival = random.uniform(3, 10)
        yield env.timeout(next_arrival)

def depart(queue, direction, light):
    while True:
        car_position, time_arrived = queue.get_nowait()
        time_waiting = env.now - time_arrived
        print("Car #%d departed at time %.3f, after waiting %.3f, leaving %d cars in the %s queue."
              % (car_position, env.now, time_waiting, queue.qsize(), direction))
        Stats['cars_waiting'] += 1
        Stats['waiting_time'] += time_waiting

        if light == 'red' or queue.qsize() == 0:
            return

        # add left on green rules here
        # pass turn direction

        yield env.timeout(clear_delay)



def light_status(direction, queue, red_time, green_time):

    while True:
        NS_light = 'green'
        EW_light = 'red'


        if (direction == 'N' or direction == 'S') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction, light=NS_light))

        if (direction == 'N' or direction == 'S'):
            print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))


        yield env.timeout(green_time)
        Stats['green_count'] += 1
        Stats['green_time'] += green_time

        NS_light = 'red'
        EW_light = 'green'

        if (direction == 'E' or direction == 'W') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction, light=EW_light))

        if (direction == 'W' or direction == 'E'):
            print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))


        yield env.timeout(red_time)
        Stats['red_count'] += 1
        Stats['red_time'] += red_time

env = simpy.Environment()

# constants for N/S
NS_green_time = random.uniform(10, 30)
NS_red_time = random.uniform(10, 30)

env.process(light_status(direction='N', queue=N_queue, green_time=NS_green_time, red_time=NS_red_time))
env.process(light_status(direction='S', queue=S_queue, green_time=NS_green_time, red_time=NS_red_time))
env.process(arrive(queue=N_queue, direction='N', light=NS_light))
env.process(arrive(queue=S_queue, direction='S', light=NS_light))

# constants for E/W

# need to fix this so the light chages in sync: E/W lights are red when N/S lights are green
env.process(light_status(direction='E', queue=E_queue, green_time=NS_green_time, red_time=NS_red_time))
env.process(light_status(direction='W', queue=W_queue, green_time=NS_green_time, red_time=NS_red_time))
env.process(arrive(queue=E_queue, direction='E', light=EW_light))
env.process(arrive(queue=W_queue, direction='W', light=EW_light))

env.run(until=total_time)

print("\n\n*** Summary ***\n\n")

# print("Mean length of green light: %.3f seconds"
#   % (Stats['green_time'] / float(Stats['green_count'])))
#
# print("Mean length of red light: %.3f seconds"
#   % (Stats['red_time'] / float(Stats['red_count'])))

print("Mean waiting time: %.3f seconds"
  % (Stats['waiting_time'] / float(Stats['car_count'])))

print(Stats)

#To Do:
#4 queues: N,S,E,W
#calculate maximum wait time and mean wait time for each street (N/S & E/W)
#add timing of light status as a parameter
#on busier road: green light longer and arrival times closer together (taken from random dist with smaller range)
