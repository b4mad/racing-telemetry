from typing import Optional

class Streaming:
    def __init__(self):
        self.total_speed: float = 0.0
        self.count: int = 0

    def average_speed(self, current_speed: float) -> Optional[float]:
        """
        Calculate the running average speed.

        Args:
            current_speed (float): The current speed value.

        Returns:
            Optional[float]: The updated average speed, or None if no data has been processed.
        """
        self.total_speed += current_speed
        self.count += 1

        if self.count == 0:
            return None

        return self.total_speed / self.count
