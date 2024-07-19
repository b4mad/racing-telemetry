import math
from typing import Callable, Dict, List

import pandas as pd

import racing_telemetry.analysis.basic_stats as basic_stats


class Streaming:
    def __init__(
        self,
        average_speed: bool = False,
        coasting_time: bool = False,
        raceline_yaw: bool = False,
        ground_speed: bool = False,
        braking_point: bool = False,
        wheel_slip: bool = False,
        lift_off_point: bool = False,
        acceleration_point: bool = False,
        apex: bool = False,
        **kwargs
    ):
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
        if braking_point:
            self.configure_feature("braking_point", self.braking_point)
        if wheel_slip:
            # wheel_slip requires ground_speed to be computed
            self.configure_feature("ground_speed", self.ground_speed)
            self.configure_feature("wheel_slip", self.wheel_slip)
            # dont compute ground_speed twice
            ground_speed = False
        if ground_speed:
            self.configure_feature("ground_speed", self.ground_speed)
        if lift_off_point:
            self.configure_feature("lift_off_point", self.lift_off_point)
        if acceleration_point:
            self.configure_feature("acceleration_point", self.acceleration_point)
        if apex:
            self.configure_feature("apex", self.apex)

        self.last_lap_time: float = 0.0
        self.last_x: float = 0.0
        self.last_y: float = 0.0
        self.total_coasting_time: float = 0.0
        self.brake_pressed: bool = False
        self.last_brake_pressure: float = 0.0
        self.braking_point_found: bool = False
        self.brake_pressure_threshold: float = 0.1
        self.rate_of_change_threshold: float = 0.05
        self.last_throttle: float = 0.0
        self.lift_off_point_found: bool = False
        self.throttle_threshold: float = 0.9
        self.throttle_decrease_threshold: float = 0.1
        self.last_speed: float = 0.0
        self.acceleration_point_found: bool = False
        self.throttle_increase_threshold: float = 0.1
        self.speed_increase_threshold: float = 0.5
        self.x_positions: List[float] = []
        self.y_positions: List[float] = []
        self.distance_round_track: List[float] = []

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
        current_lap_time = telemetry.get("CurrentLapTime", 0.0)
        if current_lap_time < self.last_lap_time:
            # New lap started, reset detection flags
            self.braking_point_found = False
            self.lift_off_point_found = False
            self.acceleration_point_found = False

        self.elapsed_time = self._calculate_elapsed_time(current_lap_time)
        self.dx, self.dy = self._calculate_position_delta(telemetry.get("WorldPosition_x", 0.0), telemetry.get("WorldPosition_y", 0.0))

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
            return telemetry.get("SpeedMs", 0)

        dx, dy = self.dx, self.dy

        distance = math.sqrt(dx**2 + dy**2)
        speed = distance / self.elapsed_time

        return speed

    def braking_point(self, telemetry: Dict) -> float:
        """
        Determine the braking point based on brake pressure and its rate of change.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The DistanceRoundTrack when the braking point is detected, or -1 if not yet detected.
        """
        if self.braking_point_found:
            return self.computed_features["braking_point"]

        current_brake_pressure = telemetry.get("Brake", 0)

        time_difference = self.elapsed_time

        if time_difference > 0:
            rate_of_change = (current_brake_pressure - self.last_brake_pressure) / time_difference

            if current_brake_pressure > self.brake_pressure_threshold and rate_of_change > self.rate_of_change_threshold:
                self.braking_point_found = True
                return telemetry.get("DistanceRoundTrack", -1)

        self.last_brake_pressure = current_brake_pressure
        return -1

    def wheel_slip(self, telemetry: Dict) -> float:
        """
        Calculate the wheel slip based on the difference between ground speed and SpeedMs.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The wheel slip as a percentage between -1 and 1.
        """
        ground_speed = self.computed_features.get("ground_speed", 0.0)
        speed_ms = telemetry.get("SpeedMs", 0)

        if speed_ms == 0:
            return 0.0

        slip = (ground_speed - speed_ms) / speed_ms
        return max(min(slip, 1.0), -1.0)

    def lift_off_point(self, telemetry: Dict) -> float:
        """
        Determine the lift-off point based on throttle decrease.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The DistanceRoundTrack when the lift-off point is detected, or -1 if not yet detected.
        """
        if self.lift_off_point_found:
            return self.computed_features["lift_off_point"]

        current_throttle = telemetry.get("Throttle", 0)

        if self.last_throttle > self.throttle_threshold and (self.last_throttle - current_throttle) > self.throttle_decrease_threshold:
            self.lift_off_point_found = True
            return telemetry.get("DistanceRoundTrack", -1)

        self.last_throttle = current_throttle
        return -1

    def acceleration_point(self, telemetry: Dict) -> float:
        """
        Determine the acceleration point based on throttle increase and speed increase.

        Args:
            telemetry (Dict): The incoming telemetry data.

        Returns:
            float: The DistanceRoundTrack when the acceleration point is detected, or -1 if not yet detected.
        """
        if self.acceleration_point_found:
            return self.computed_features["acceleration_point"]

        current_throttle = telemetry.get("Throttle", 0)
        current_speed = telemetry.get("SpeedMs", 0)

        throttle_increase = current_throttle - self.last_throttle
        speed_increase = current_speed - self.last_speed

        if throttle_increase > self.throttle_increase_threshold and speed_increase > self.speed_increase_threshold:
            self.acceleration_point_found = True
            return telemetry.get("DistanceRoundTrack", -1)

        self.last_throttle = current_throttle
        self.last_speed = current_speed
        return -1

    def apex(self, telemetry: Dict) -> int:
        """
        Calculate the apex using the collected x and y positions.

        Args:
            telemetry (Dict): The incoming telemetry data (not used in this method).

        Returns:
            Dict: The apex information or None if it can't be calculated.
        """
        x = telemetry.get("WorldPosition_x", 0.0)
        y = telemetry.get("WorldPosition_y", 0.0)
        distance = telemetry.get("DistanceRoundTrack", 0.0)

        self.x_positions.append(x)
        self.y_positions.append(y)
        self.distance_round_track.append(distance)

        return -1

    def calculate_apex(self) -> float:
        """
        Trigger the apex calculation.

        Returns:
            Dict: The apex information or None if it can't be calculated.
        """
        df = pd.DataFrame({"WorldPosition_x": self.x_positions, "WorldPosition_y": self.y_positions})
        apex = basic_stats.apex(df)
        apex_distance = -1
        if apex:
            apex_distance = self.distance_round_track[apex["index"]]
        self.computed_features["apex"] = apex_distance
