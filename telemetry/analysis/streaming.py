from typing import Optional, Dict, Callable, List
import math

class Streaming:
    def __init__(self, average_speed: bool = False, coasting_time: bool = False, raceline_yaw: bool = False, ground_speed: bool = False, **kwargs):
        self.total_speed: float = 0.0
        self.count: int = 0
        self.features: Dict[str, Callable] = {}
        self.computed_features: Dict[str, float] = {}

        if average_speed:
            self.configure_feature("average_speed", lambda telemetry: self.average_speed(telemetry.get("SpeedMs", 0)))
        if coasting_time:
            self.configure_feature("coasting_time", self.coasting_time)
        if raceline_yaw:
            self.configure_feature("raceline_yaw", self.raceline_yaw)
        if ground_speed:
            self.configure_feature("ground_speed", self.ground_speed)

        self.last_lap_time: float = 0.0
        self.last_x: float = 0.0
        self.last_y: float = 0.0
        self.total_coasting_time: float = 0.0

    def configure_feature(self, name: str, feature_func: Callable):
        """
        Configure a new feature to be computed.

        Args:
            name (str): The name of the feature.
            feature_func (Callable): The function to compute the feature.
        """
        self.features[name] = feature_func
        self.computed_features[name] = 0.0

    def notify(self, telemetry: Dict):
        """
        Process new telemetry data and compute configured features.

        Args:
            telemetry (Dict): The incoming telemetry data.
        """
        self.elapsed_time = self._calculate_elapsed_time(telemetry.get("CurrentLapTime", 0.0))
        self.dx, self.dy = self._calculate_position_delta(
            telemetry.get("WorldPosition_x", 0.0),
            telemetry.get("WorldPosition_y", 0.0)
        )

        for feature_name, feature_func in self.features.items():
            result = feature_func(telemetry)
            self.computed_features[feature_name] = result

    def get_features(self) -> Dict[str, float]:
        """
        Get the computed features.

        Returns:
            Dict[str, List[float]]: A dictionary of feature names and their computed values.
        """
        return self.computed_features

    def _calculate_elapsed_time(self, current_lap_time: float) -> float:
        """Calculate elapsed time since last update."""
        if self.last_lap_time == 0:
            self.last_lap_time = current_lap_time
            return 0
        elapsed_time = current_lap_time - self.last_lap_time
        self.last_lap_time = current_lap_time
        return elapsed_time

    def _calculate_position_delta(self, current_x: float, current_y: float) -> tuple[float, float]:
        """Calculate the change in position since last update."""
        if self.last_x == 0 and self.last_y == 0:
            self.last_x, self.last_y = current_x, current_y
            return 0.0, 0.0
        dx = current_x - self.last_x
        dy = current_y - self.last_y
        self.last_x, self.last_y = current_x, current_y
        return dx, dy

    def average_speed(self, current_speed: float) -> float:
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
            return 0.0

        return self.total_speed / self.count

    def coasting_time(self, telemetry: Dict) -> float:
        """
        Calculate the time spent coasting (no Throttle or Brake applied).

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The total time spent coasting in seconds.
        """
        if telemetry.get("Throttle", 0) == 0 and telemetry.get("Brake", 0) == 0:
            self.total_coasting_time += self.elapsed_time
        return self.total_coasting_time

    def raceline_yaw(self, telemetry: Dict) -> float:
        """
        Calculate the yaw based on the current and previous x and y coordinates.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The calculated yaw angle between -180 and 180 degrees.
        """

        dx, dy = self.dx, self.dy

        if dx == 0 and dy == 0:
            return 0.0

        yaw = math.degrees(math.atan2(dy, dx))

        yaw = (yaw - 90) % 360
        if yaw > 180:
            yaw -= 360

        return yaw

    def ground_speed(self, telemetry: Dict) -> float:
        """
        Calculate the ground speed based on x and y coordinates traveled between ticks.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The calculated ground speed in meters per second.
        """

        if self.elapsed_time == 0:
            return 0.0

        dx, dy = self.dx, self.dy

        distance = math.sqrt(dx**2 + dy**2)
        speed = distance / self.elapsed_time

        return speed

