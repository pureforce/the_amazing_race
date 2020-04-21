"""
Created by: Jani Bizjak
Created on: 05.04.2020
"""

from multiprocessing import Value
from custom_exceptions import NegativeDistanceException
from utils import round_progress


class ProgressMonitor:
    """Prints progress while working on legs from different processes.

    ProgressMonitor prints progress after approximately every 5% of the total legs have been processed.
    The data is shared between multiple processes. The class itself takes care of concurrency of the data.
    """

    def __init__(self, total_legs, total_distance, leg_number=0, distance=0):
        """Initializes object, with 0 values. Leg number and distance are in shared memory.

        :param total_legs: int, total number of legs in the race
        :param total_distance: float, total distance in the race
        :param leg_number: int, number of last processed leg
        :param distance: float, distance so far after last processed leg
        """

        self.leg_number = Value('i', leg_number)
        self.distance = Value('f', distance)

        self.total_legs = total_legs
        self.total_distance = total_distance

        self.last_print_progress = Value('i', -1)

        #  Don't allow legs or distance to be 0 or it will try to divide by 0.
        if total_legs < 1 or total_distance < 1:
            raise NegativeDistanceException

    def increment_legs(self):
        """Increment processed legs by 1."""

        self.increment_legs_and_distance(1, 0)

    def increment_distance(self, additional_distance_traveled):
        """Increments processed distance.

        :param additional_distance_traveled: float, distance traveled in this leg
        """

        self.increment_distance(0, additional_distance_traveled)

    def increment_legs_and_distance(self, additional_legs=1, additional_distance=0, print_progress=True):
        """Increases both distance and leg count and also prints progress every 5%.

        :param additional_legs: int, number of legs processed in last step
        :param additional_distance: float, distance traveled in last step
        :param print_progress: boolean,
        """

        if additional_legs < 0 or additional_distance < 0:
            raise NegativeDistanceException

        with self.leg_number.get_lock():
            self.leg_number.value += additional_legs

        with self.distance.get_lock():
            self.distance.value += additional_distance

        if print_progress:
            self.print_progress()

    def print_progress(self, force_print=False):
        """Prints progress every 5%.

        Prints progress every 5%. If the numbers don't align correctly it will print it first time it rounds to multiply
        of 5. If force_print is used the method will print the result regardless of it being multiply of 5 or not.

        :param force_print: boolean, prints progress even if not dividable by 5
        """

        with self.leg_number.get_lock(), self.distance.get_lock(), self.last_print_progress.get_lock():
            progress = round_progress(self.leg_number.value / self.total_legs * 100)
            distance_progress = self.distance.value / self.total_distance * 100

            if self.last_print_progress.value != progress:  # Only print approximately every 5%
                self.last_print_progress.value = progress
                print("Completed %3i%% of the legs, %0.1f%% by distance traveled" % (progress, distance_progress))
            elif force_print:
                print("Completed %3i%% of the legs, %0.1f%% by distance traveled" % (progress, distance_progress))
