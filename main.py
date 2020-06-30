##################
# Name: Eric Cleek
# ID: 001172916
##################

from scheduler import Scheduler
import sys
import datetime

# Majority of the logic is here including the route algorithms






def build_route_schedule(route, departure_time=datetime.datetime(2000, 1, 1, hour=9, minute=30, second=0)):
    """

    :param route:
    :param departure_time:
    :return:
    """
    schedule = []
    current_time = departure_time
    total_distance = 0
    for stop in route:
        stop_str = ""
        current_time += datetime.timedelta(hours=stop.travel_time)
        total_distance += stop.distance_to
        if stop.packages:
            for package in stop.packages:
                stop_str += "Package ID:    {} Address: {} {} {}    Expected Delivery Time: {}" \
                    .format(package.id, package.address, package.city, package.zip, current_time.strftime("%I:%M %p"))
            schedule.append(stop_str)
    return schedule


def get_package_info(hash_table, package_id):
    try:
        return hash_table.find(package_id)
    except LookupError:
        print("No such package found")


def print_package_info(package):
    info = "{}    {} {}, {}. {} {} {}" \
        .format(
        package.id,
        package.address,
        package.city,
        package.state,
        package.zip,
        package.status,
        package.delivered.strftime("%I:%M %p")
    )
    print(info)


def print_all_packages(hashtable):
    """
    Builds and displays package data for all packages currently in hash table.
    :return:
    """
    packages = [i for i in hashtable]
    packages.sort(key=lambda x: x.delivered)
    for package in packages:
        print_package_info(package)


def input_time():
    """
    Builds and displays UI for inputting package time.
    :return:
    """
    print("Time (24hr format): ")
    while True:
        try:
            raw_time = input("> ")
            time_obj = datetime.datetime.strptime(raw_time, "%H:%M")
            time_obj = time_obj.replace(year=2000, day=1, month=1)
            return time_obj
        except ValueError:
            print("Time format not recognized, please use 24hr format (e.g. 14:00 for 6pm)")


def input_package_id():
    """
    Builds and displays UI for inputting package ID.
    :return:
    """
    while True:
        print("Enter a package ID: ")
        try:
            return int(input("# "))
        except ValueError:
            print("You entered something other than a number.  Please enter an integer (0, 1, 2, etc.)")


if __name__ == "__main__":
    scheduler = Scheduler(2)

    while True:
        print("Choose an option:")
        print("1. Track Individual Package")
        print("2. Display status of All Packages")
        print("3. Display Route Schedules for the Day")
        print("\n")
        print("Type 'exit' to quit")
        print("\n")
        choice = input("> ")

        if choice == "exit":
            sys.exit()
        elif int(choice) == 1:  # status of single package
            id = input_package_id()
            time = input_time()
            scheduler.simulate_day(time)
            package = get_package_info(scheduler.package_hash, id)
            print_package_info(package)
            break
        elif int(choice) == 2:  # status of all packages
            time = input_time()
            scheduler.simulate_day(time)
            print_all_packages(scheduler.package_hash)
            break
        elif int(choice) == 3:  # print all routes at start of day
            for index, route in enumerate(scheduler.regular_routes):
                print("Route {}".format(index + 1))
                route_schedule = build_route_schedule(route)
                for stop in route_schedule:
                    print(stop)
            break
        else:
            print("Sorry, we didn't recognize your input")
