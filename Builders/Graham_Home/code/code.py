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
            self.drive(left_speed=-1, right_speed=-1, duration=0.5)

        # If only the left sensor is over the edge, turn to the right,
        # then drive straight backwards.
        elif self.left_edge_detected():
            self.drive(left_speed=-0.5, right_speed=0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.5)

        # If only the right sensor is over the edge, turn to the left,
        # then drive straight backwards.
        elif self.right_edge_detected():
            self.drive(left_speed=0.5, right_speed=-0.5, duration=0.25)
            self.drive(left_speed=-1, right_speed=-1, duration=0.5)

        # ******************************
        # 2. Scan for enemy and charge it!
        # ******************************

        # Check for enemy straight ahead
        if self.enemy_in_range_right() and self.enemy_in_range_left():
            # Charge!
            while (
                self.enemy_in_range_right()
                and self.enemy_in_range_left()
                and not (self.right_edge_detected() or self.left_edge_detected())
            ):
                self.drive(right_speed=1, left_speed=1)
            self.stop()

        # Check for enemy to right
        elif self.enemy_in_range_right():
            # Turn to the right for 0.5 seconds
            self.drive(left_speed=-0.5, right_speed=0.5, duration=1)

        # Check for enemy to left
        elif self.enemy_in_range_left():
            # Turn to the left for 0.5 seconds
            self.drive(left_speed=0.5, right_speed=-0.5, duration=1)

        # Spin and look for enemy
        else:
            # Turn to the left for 0.5 seconds
            self.drive(left_speed=0.5, right_speed=-0.5, duration=1)


if __name__ == "__main__":
    GrahamSumoBot().run()
