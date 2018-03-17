"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#
import math

Min = [(1000,13.333), (600,11.428), (400,15), (200,15), (0, 15)]
Max = [(1000,26), (600,28), (400,30), (200,32), (0,34)]
VALID_DISTANCES = [1000,600,400,200]

def valid_input(control_dist_km, brevet_dist_km):
    """
    args: it is to know if the control_dist_km is valid
    """
    if control_dist_km >= (brevet_dist_km * 1.2):
        print("Control distance cannot be longer than 1.2 * brevet distance0")
        return False
    elif control_dist_km < 0:
        print("Control distance must greater than 0")
        return False
    elif brevet_dist_km not in VALID_DISTANCES:
        print("Please choose the brevet distance properly")
        return False
    else:
        return True


def calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, time_function):

   # time = arrow.get(brevet_start_time, 'YYYY-MM-DD HH:mm')

    if not valid_input(control_dist_km, brevet_dist_km):
            return

    #control_dis == 0:
    if control_dist_km == 0:
        return arrow.get(brevet_start_time).isoformat()


    current = control_dist_km

    #this is for the open time
    #the problem is the minutes here, doesnt change
    if time_function == 0:
        for item in Max:
                if current >= item[0]:
                    minn, hour = math.modf((current - item[0]) * 1.0 / item[1])
                    minn = minn*60
                    brevet_start_time = brevet_start_time.shift(hours=round(hour), minutes=round(minn))
                    current = item[0]

        return brevet_start_time.isoformat()



    #this is for the close time
    if time_function == 1:
            for item in Min:
                if 600*1.1 <= current <= 1000*1.2:
                    part = 600 / 15
                    minn, hour = math.modf(part + ((current - 600) * 1.0/ 11.428))
                    minn = minn * 60
                    brevet_start_time = brevet_start_time.shift(hours=round(hour), minutes=round(minn))
                    return brevet_start_time.isoformat()

                elif 1000 * 1.2 < current <= 1300 *1.2 :
                    part = 600/15 + 400/11.428
                    minn, hour = math.modf(part + ((current - 1000) * 1.0 / 13.333))
                    brevet_start_time = brevet_start_time.shift(hours=round(hour), minutes=round(minn * 60))
                    return brevet_start_time.isoformat()

                else:
                    minn,hour = math.modf((current * 1.0) / 15)
                    brevet_start_time = brevet_start_time.shift(hours=round(hour), minutes=round(minn * 60))
                    return brevet_start_time.isoformat()


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    return calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, 0)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    return calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, 1)
