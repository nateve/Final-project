import simpy
import random
from queue import Queue

Stats = dict()
Stats['cars_waiting'] = 0
Stats['car_count'] = 0
Stats['waiting_time'] = 0.0
Stats['red_time'] = 0.0
Stats['red_count'] = 0
Stats['green_time'] = 0.0
Stats['green_count'] = 0

arrive_count = 0
clear_delay = 2
total_time = 200.0

queue = Queue()

def arrive(arrive_count, queue):
    global light

    while True:
        arrive_count += 1

        if light == 'red' or queue.qsize() > 0:
            queue.put_nowait((arrive_count, env.now))
            print("Car #%d arrived and joined the queue at position %d at time "
                  "%.3f." % (arrive_count, queue.qsize(), env.now))
        else:
            print("Car #%d passed through a green light with no cars waiting at time "
                  "%.3f." % (arrive_count, env.now))
            Stats['car_count'] += 1
        next_arrival = random.uniform(3, 10)
        yield env.timeout(next_arrival)

def depart(queue):
    while True:
        car_position, time_arrived = queue.get_nowait()
        time_waiting = env.now - time_arrived
        print("Car #%d departed at time %.3f, after waiting %.3f, leaving %d cars in the queue."
              % (car_position, env.now, time_waiting, queue.qsize()))
        Stats['car_count'] += 1
        Stats['cars_waiting'] += 1
        Stats['waiting_time'] += time_waiting

        if light == 'red' or queue.qsize() == 0:
            return

        yield env.timeout(clear_delay)

def light_status():
    global light, queue
    while True:
        light = 'green'
        print("\nThe light turned green at time %.3f." % env.now)

        if queue.qsize() > 0:
            env.process(depart(queue))


        green_time = random.uniform(10, 30)
        yield env.timeout(green_time)
        print('\nThe light stayed green for %.3f seconds' % green_time)
        Stats['green_count'] += 1
        Stats['green_time'] += green_time

        light = 'red'
        print("\nThe light turned red at time %.3f." % env.now)
        red_time = random.uniform(10,30)
        yield env.timeout(red_time)
        print('\nThe light stayed red for %.3f seconds' % red_time)
        Stats['red_count'] += 1
        Stats['red_time'] += red_time


env = simpy.Environment()
env.process(light_status())
env.process(arrive(arrive_count, queue))
env.run(until=total_time)

print("\n\n*** Summary ***\n\n")

print("Mean length of green light: %.3f seconds"
  % (Stats['green_time'] / float(Stats['green_count'])))

print("Mean length of red light: %.3f seconds"
  % (Stats['red_time'] / float(Stats['red_count'])))

print("Mean waiting time: %.3f seconds"
  % (Stats['waiting_time'] / float(Stats['cars_waiting'])))

print(Stats)

#To Do:
#4 queues: N,S,E,W
#calculate maximum wait time and mean wait time for each street (N/S & E/W)
#add timing of light status as a parameter
#on busier road: green light longer and arrival times closer together (taken from random dist with smaller range)
