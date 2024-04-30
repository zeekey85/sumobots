from time import sleep

from base_bot import SumoBotBase
from settings import *


class BasicSumoBot(SumoBotBase):
    """
    Basic implementation of the sumo bot fighting routine.
    Other botmasters may define their own SumoBot classes which extend SumoBotBase,
    and add their own fight() method with their own personal fighting strategy.
    """

    def fight(self):
        """
        Robot fighting routine.
        """
        # *************************************
        # 1. Back away from the edge if needed
        # *************************************

        # If both sensors are over the edge, drive straight backwards.
        if self.left_edge_detected() and self.right_edge_detected():
            print("Backing straight up and turning around")
            self.drive(left_speed=-1, right_speed=-1, duration=0.3)
            self.drive(left_speed=-1, right_speed=1, duration=0.4)

        # If only the left sensor is over the edge, turn to the right,
        # then drive straight backwards.
        elif self.left_edge_detected():
            print("Backing to right and turning around")
            self.drive(left_speed=-0.5, right_speed=0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.3)
            self.drive(left_speed=-1, right_speed=1, duration=0.4)

        # If only the right sensor is over the edge, turn to the left,
        # then drive straight backwards.
        elif self.right_edge_detected():
            print("Backing to left and turning around")
            self.drive(left_speed=0.5, right_speed=-0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.3)
            self.drive(left_speed=1, right_speed=-1, duration=0.4)

        # ******************************
        # 2. Scan for enemy and charge it!
        # ******************************

        # Check for enemy straight ahead
        charge_time = 0
        if self.enemy_in_range_right() and self.enemy_in_range_left():
            # Charge!
            print("Charging boldly forward")
            charge_time = 0
            # TODO: Full speed lifts up edge sensors & gives false positive for edge - fix me
            self.drive(right_speed=0.7, left_speed=0.7)
            while (
                self.enemy_in_range_right()
                and self.enemy_in_range_left()
                and not (self.right_edge_detected() or self.left_edge_detected())
                and charge_time < MAX_CHARGE
            ):
                sleep(CHARGE_INTERVAL)
                charge_time += CHARGE_INTERVAL
            self.stop()
            if charge_time >= MAX_CHARGE:
                # Back up to charge again
                print("Backing up and turning away from opponent")
                self.drive(left_speed=-1, right_speed=-0.8, duration=0.7)

        # Check for enemy to right
        else:
            right_distance = self.right_distance()
            left_distance = self.left_distance()
            if right_distance < MAX_DISTANCE:
                print("Looking right")
                # Turn to the right - set turn duration inversely proportional to enemy distance
                self.drive(left_speed=0.5, right_speed=-0.5, duration=0.2*((MAX_DISTANCE-right_distance)/MAX_DISTANCE))

            # Check for enemy to left
            elif left_distance < MAX_DISTANCE:
                print("Looking left")
                # Turn to the left - set turn duration inversely proportional to enemy distance
                self.drive(left_speed=-0.5, right_speed=0.5, duration=0.2*((MAX_DISTANCE-left_distance)/MAX_DISTANCE))

            # Spin and look for enemy
            else:
                # Turn to the left
                print("Spinning")
                self.drive(left_speed=-1, right_speed=1, duration=0.05)

if __name__ == "__main__":
    BasicSumoBot().run()
