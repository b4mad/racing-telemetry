from typing import Optional, Dict, Callable, List
import math

class Streaming:
    def __init__(self, average_speed: bool = False, coasting_time: bool = False, raceline_yaw: bool = False, **kwargs):
        self.total_speed: float = 0.0
        self.count: int = 0
        self.features: Dict[str, Callable] = {}
        self.computed_features: Dict[str, float] = {}

        if average_speed:
            self.configure_feature("average_speed", lambda telemetry: self.average_speed(telemetry.get("SpeedMs", 0)))
            self.computed_features["average_speed"] = 0
        if coasting_time:
            self.configure_feature("coasting_time", self.coasting_time)
            self.computed_features["coasting_time"] = 0
        if raceline_yaw:
            self.configure_feature("raceline_yaw", self.raceline_yaw)
            self.computed_features["raceline_yaw"] = 0
        self.last_lap_time: float = 0
        self.total_coasting_time: float = 0
        self.previous_x: float = 0
        self.previous_y: float = 0

    def configure_feature(self, name: str, feature_func: Callable):
        """
        Configure a new feature to be computed.

        Args:
            name (str): The name of the feature.
            feature_func (Callable): The function to compute the feature.
        """
        self.features[name] = feature_func
        self.computed_features[name] = []

    def notify(self, telemetry: Dict):
        """
        Process new telemetry data and compute configured features.

        Args:
            telemetry (Dict): The incoming telemetry data.
        """
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

    def coasting_time(self, telemetry: Dict) -> float:
        """
        Calculate the time spent coasting (no Throttle or Brake applied).

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The total time spent coasting in seconds.
        """
        current_lap_time = telemetry.get("CurrentLapTime", 0)
        throttle = telemetry.get("Throttle", 0)
        brake = telemetry.get("Brake", 0)

        if self.last_lap_time == 0:
            self.last_lap_time = current_lap_time
            return 0

        elapsed_time = current_lap_time - self.last_lap_time
        self.last_lap_time = current_lap_time

        if throttle == 0 and brake == 0:
            self.total_coasting_time += elapsed_time

        return self.total_coasting_time

    def raceline_yaw(self, telemetry: Dict) -> float:
        """
        Calculate the yaw based on the current and previous x and y coordinates.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The calculated yaw angle between -180 and 180 degrees.
        """
        current_x = telemetry.get("WorldPosition_x", 0)
        current_y = telemetry.get("WorldPosition_y", 0)

        if self.previous_x == 0 and self.previous_y == 0:
            self.previous_x = current_x
            self.previous_y = current_y
            return 0

        dx = current_x - self.previous_x
        dy = current_y - self.previous_y

        yaw = math.degrees(math.atan2(dy, dx))

        yaw = (yaw - 90) % 360
        if yaw > 180:
            yaw -= 360

        # if 0 <= yaw < 90:
        #     yaw = yaw - 90
        # elif -90 <= yaw < 0:
        #     yaw = yaw - 90
        # elif 90 <= yaw < 180:
        #     yaw = yaw - 90
        # elif -180 <= yaw < -90:
        #     yaw = yaw + 270

        self.previous_x = current_x
        self.previous_y = current_y

        return yaw

