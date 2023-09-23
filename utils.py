
def pace_to_seconds(pace):
    """Converts a running pace in the format mm:ss to seconds."""
    minutes, seconds = map(int, pace.split(':'))
    return minutes * 60 + seconds


# Function to calculate speed
def cal_speed(dist, time):
    return dist / time


# Function to calculate distance travelled
def cal_dis(speed, time):
    return speed * time


# Function to calculate time taken
def cal_time(dist, speed):
    return dist / speed


def calc_time(miles, s_pace):
    seconds = s_pace * miles
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    length = '%d:%02d:%02d' % (hour, min, sec)
    fraction_of_hour = hour + (min / 60) + (sec / 3600)
    return length, fraction_of_hour
