"""
Updated by: Jani Bizjak
Updated at: 05.04.2020
"""


class PartialSummary:
    """Class for storing and working with leg data of each participant in the race."""

    def __init__(self, distance=0.0, speed=100.0, transport=None):
        """Initializes summary object for each person. Summary object contains distance, speed and transportation.

        :param distance: float distance traveled until now
        :param speed: float, average speed until now
        :param transport: list of strings or None
        """

        self.distance = distance
        self.speed = speed
        self.transport = [] if transport is None else transport

    def print(self):
        """Prints distance traveled, speed and all different types of transport taken"""

        print("Traveled %0.2fkms\nAt an avg speed of %0.4f km/h" % (self.distance, self.speed))
        print("Took: ", ', '.join(self.transport))

    def add_new_leg(self, leg):
        """Add data from a new leg to this summary.

        :param leg: dictionary from json, containing {speed, distance and transport} keys
        """

        self.add_new_data(leg["speed"], leg["distance"], leg["transport"])

    def add_new_data(self, speed, distance, transport):
        """Add new data to this summary.

        :param speed: int, speed
        :param distance: float, distance
        :param transport: string or list, of transport types
        """

        """
        distance = speed * time  => time = distance / speed  #
        average_speed = (distance1 + distance2) / (time1 + time2)
        average_speed = (distance1 + distance2) / (distance1 / speed1  +  distance2 / speed2) =
                      = (distance1 + distance2) * (speed1 * speed2) / (distance1 * speed2 + distance2 * speed2)
        """
        self.speed = self.speed * float(speed) * (self.distance + float(distance)) \
                    / (self.distance * float(speed) + float(distance) * self.speed)
        self.distance += float(distance)  # This needs to be after speed

        if isinstance(transport, list):  # Check if transport is single string or a list of strings
            for transport_type in transport:  # Check each element individually if its already in the list otherwise add
                if transport_type not in self.transport:
                    self.transport.append(transport_type)
        else:
            self.transport.append(transport)

