import datetime
# delivery statuses
DELIVERED = "Delivered"
ON_ROUTE = "On Route"
AT_HUB = "At hub"
TRUCK_SPEED = 18  # miles per hour
START_OF_DAY = datetime.datetime(2000, 1, 1, 9, 30, 0)  # 9:30a
END_OF_DAY = datetime.datetime(2000, 1, 1, 13, 30, 0)  # 5:30p

# number of packages per truck
TRUCK_CAPACITY = 16