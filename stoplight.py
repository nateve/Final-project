import simpy
import random
from queue import Queue


def arrive(queue, direction, light):
    global arrive_count

    while True:
        arrive_count += 1
        Stats['car_count'] += 1

        if light == 'red' or queue.qsize() > 0:
            queue.put((arrive_count, env.now))
            if print_sim: print("Car #{arrive_count} arrived and joined the {direction} queue at position {length} " 
                                "at time {time: .3f}.".format(arrive_count=arrive_count, direction=direction, length=queue.qsize(), time=env.now))
        else:
            if print_sim: print("Car #{arrive_count} passed through a green light going {direction} with no cars waiting "
                                "at time {time: .3f}.".format(arrive_count=arrive_count, direction=direction, time=env.now))

        if direction == 'N' or direction == 'S':
            next_arrival = random.uniform(1, 10)
        else:
            next_arrival = random.uniform(5, 60)
        yield env.timeout(next_arrival)


def depart(queue, direction, light):
    global cur_max_wait
    clear_delay = 3

    while True:
        car_position, time_arrived = queue.get()
        time_waiting = env.now - time_arrived
        #print(env.now, time_arrived, time_waiting)
        if print_sim: print("Car #{arrive_count} departed at time {time: .3f}, after waiting {time_waiting: .3f}, leaving {length} cars in the "
                            "{direction} queue.".format(arrive_count=car_position, time=env.now, time_waiting=time_waiting, length=queue.qsize(), direction=direction))

        if time_waiting > cur_max_wait:
            cur_max_wait = time_waiting
            Stats['max_wait_time'] = cur_max_wait

        Stats['cars_waiting'] += 1
        Stats['waiting_time'] += time_waiting

        if light == 'red' or queue.qsize() == 0:
            return

        # add left on green rules here
        # pass turn direction as parameter

        yield env.timeout(clear_delay)


def light_status(direction, queue, red_time, green_time):
    global NS_light, EW_light

    while True:
        NS_light = 'green'
        EW_light = 'red'

        if (direction == 'N' or direction == 'S') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction, light=NS_light))

        if direction == 'N' or direction == 'S':
            if print_sim: print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            if print_sim: print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))

        yield env.timeout(green_time)
        Stats['green_count'] += 1
        Stats['green_time'] += green_time

        NS_light = 'red'
        EW_light = 'green'

        if (direction == 'E' or direction == 'W') and queue.qsize() > 0:
            env.process(depart(queue=queue, direction=direction, light=EW_light))

        if direction == 'W' or direction == 'E':
            if print_sim: print('\nThe {direction} light turned green at time {time: .3f}.'.format(direction=direction, time=env.now))
        else:
            if print_sim: print('\nThe {direction} light turned red at time {time: .3f}.'.format(direction=direction, time=env.now))


        yield env.timeout(red_time)
        Stats['red_count'] += 1
        Stats['red_time'] += red_time


def run_sim(NS_green_time, total_time):

    NS_red_time = 60 - NS_green_time

    env.process(light_status(direction='N', queue=N_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(light_status(direction='S', queue=S_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(arrive(queue=N_queue, direction='N', light=NS_light))
    env.process(arrive(queue=S_queue, direction='S', light=NS_light))

    env.process(light_status(direction='E', queue=E_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(light_status(direction='W', queue=W_queue, green_time=NS_green_time, red_time=NS_red_time))
    env.process(arrive(queue=E_queue, direction='E', light=EW_light))
    env.process(arrive(queue=W_queue, direction='W', light=EW_light))

    env.run(until=total_time)

    print('\n\n*** Summary ***\n\n')
    print('Green light time:', NS_green_time)
    print('Mean waiting time: %.3f seconds'
      % (Stats['waiting_time'] / float(Stats['car_count'])))

    print('Max waiting time: %.3f seconds'
      % Stats['max_wait_time'])

    if print_sim:
        print('\n')
        for k,v in Stats.items():
            print(k,':',v)


if __name__ == '__main__':
    print_sim = False

    for seconds in range(5,55,5):
        env = simpy.Environment()

        NS_light = 'green'
        EW_light = 'red'
        cur_max_wait = 0
        arrive_count = 0

        N_queue = Queue()
        S_queue = Queue()
        E_queue = Queue()
        W_queue = Queue()

        Stats = dict()
        Stats['cars_waiting'] = 0
        Stats['car_count'] = 0
        Stats['waiting_time'] = 0.0
        Stats['max_wait_time'] = 0
        Stats['red_time'] = 0.0
        Stats['red_count'] = 0
        Stats['green_time'] = 0.0
        Stats['green_count'] = 0

        run_sim(NS_green_time=seconds, total_time=3600)

