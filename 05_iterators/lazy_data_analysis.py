from datetime import datetime, time
from itertools import count, filterfalse, groupby, islice
from random import normalvariate, randint, gauss

from scipy.stats import normaltest


def read_data(filename):
    with open(filename) as fd:
        for line in fd:
            data = line.strip().split(",")
            timestamp, value = map(int, data)
            yield datetime.fromtimestamp(timestamp), value


def read_fake_data(filename):
    # change mode every other day, and choose a new mode at random between 0 and 2
    # if mode == 0 send 60*60*24-1 a constant value (= a hundred) 
    # if mode == 1 send 60*60*24-1 random uniform values
    # if mode == 2 send 60*60*24-1 random normal values
    mode = 0
    for timestamp in count(): # increment by a second
        # test if timestamp is a new day
        if is_another_day(timestamp):
            mode = randint(0,2)
            print(mode)
        if mode == 0:
            value = 100
        elif mode == 1:
            value = randint(0,100)
        else:
            value = gauss(0,1)
        yield datetime.fromtimestamp(timestamp), value

def is_another_day(timestamp):
    # return true if timestamp is "yyyy-mm-dd 00:00:00"
    return datetime.fromtimestamp(timestamp).time() == time(0,0)

def groupby_day(iterable):
    key = lambda row: row[0].day
    for day, data_group in groupby(iterable, key):
        yield list(data_group)


def is_normal(data, threshold=1e-3):
    _, values = zip(*data)
    k2, p_value = normaltest(values)
    if p_value < threshold:
        return False
    return True


def filter_anomalous_groups(data):
    yield from filterfalse(is_normal, data)


def filter_anomalous_data(data):
    data_group = groupby_day(data)
    yield from filter_anomalous_groups(data_group)


if __name__ == "__main__":
    data = read_fake_data("fake_filename")
    anomaly_generator = filter_anomalous_data(data)
    first_five_anomalies = islice(anomaly_generator, 5)

    for data_anomaly in first_five_anomalies:
        start_date = data_anomaly[0][0]
        end_date = data_anomaly[-1][0]
        print(f"Anomaly from {start_date} - {end_date}")
