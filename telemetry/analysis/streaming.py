from typing import Optional, Dict, Callable, List

class Streaming:
    def __init__(self):
        self.total_speed: float = 0.0
        self.count: int = 0
        self.features: Dict[str, Callable] = {}
        self.computed_features: Dict[str, List[float]] = {"average_speed": [], "coasting_time": []}
        self.configure_feature("average_speed", lambda telemetry: self.average_speed(telemetry.get("SpeedMs", 0)))
        self.configure_feature("coasting_time", self.coasting_time)
        self.last_lap_time: float = 0
        self.total_coasting_time: float = 0

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

    def get_features(self) -> Dict[str, List[float]]:
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

