from time import sleep

from base_bot import SumoBotBase


class GrahamSumoBot(SumoBotBase):
    """
    My implementation of the sumo bot fighting routine.
    Other botmasters may define their own SumoBot classes which extend SumoBotBase,
    and add their own fight() method with their own personal fighting strategy.
    Good luck beating my strategy, though. ;)
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
            print("Backing straight up")
            self.drive(left_speed=-1, right_speed=-1, duration=0.5)

        # If only the left sensor is over the edge, turn to the right,
        # then drive straight backwards.
        elif self.left_edge_detected():
            print("Backing to right")
            self.drive(left_speed=-0.5, right_speed=0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.25)

        # If only the right sensor is over the edge, turn to the left,
        # then drive straight backwards.
        elif self.right_edge_detected():
            print("Backing to left")
            self.drive(left_speed=0.5, right_speed=-0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.25)

        # ******************************
        # 2. Scan for enemy and charge it!
        # ******************************

        # Check for enemy straight ahead
        if self.enemy_in_range_right() and self.enemy_in_range_left():
            # Charge!
            print("Charging boldly forward")
            self.drive(right_speed=1, left_speed=1)
            while (
                self.enemy_in_range_right()
                and self.enemy_in_range_left()
                and not (self.right_edge_detected() or self.left_edge_detected())
            ):
                sleep(0.1)
            self.stop()

        # Check for enemy to right
        elif self.enemy_in_range_right():
            print("Looking right")
            # Turn to the right for 0.5 seconds
            self.drive(left_speed=0.2, right_speed=-0.2, duration=0.25)

        # Check for enemy to left
        elif self.enemy_in_range_left():
            print("Looking left")
            # Turn to the left for 0.5 seconds
            self.drive(left_speed=-0.2, right_speed=0.2, duration=0.25)

        # Spin and look for enemy
        else:
            # Turn to the left for 0.5 seconds
            print("Spinning")
            self.drive(left_speed=-0.2, right_speed=0.2, duration=0.25)

    # def enemy_in_range_right(self):
    #     return False
    #
    # def enemy_in_range_left(self):
    #     return False

if __name__ == "__main__":
    bot = GrahamSumoBot()
    while 1:
        print(bot.left_edge_detected())
        sleep(0.5)
    #GrahamSumoBot().run()
