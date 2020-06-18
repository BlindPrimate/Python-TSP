from scheduling import Scheduler
import sys
import datetime



def run_simulation(start_time):
    scheduler = Scheduler(2)
    scheduler.simulate_day()



def show_interface():
    while True:
        print("Choose an option:")
        print("1. Track Individual Package")
        print("2. Display Route Schedules for the Day")
        print("\n")
        print("Type 'exit' to quit")
        print("\n")
        choice = input("> ")

        if choice == "exit":
            sys.exit()
        elif int(choice) == 1:
            print("individual package")
        elif int(choice) == 2:
            print("All Route Schedules")
        else:
            print("Sorry, we didn't recognize your input")



if __name__ == "__main__":

    start_of_day = datetime.datetime(2000, 1, 1, 9, 30)

    run_simulation(start_of_day)

    # show_interface()






