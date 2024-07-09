from datetime import datetime
import os
import pandas as pd

import influxdb_client
from .retrieval_strategy import RetrievalStrategy

class InfluxRetrievalStrategy(RetrievalStrategy):

    def __init__(self) -> None:
        (self.org, self.token, self.url) = self._get_influxdb2_config()

        self.influx = influxdb_client.InfluxDBClient(
            url=self.url, token=self.token, org=self.org, timeout=(10_000, 600_000)
        )
        # if self.influx.ping():
        #     logging.debug(f"Influx: Connected to {self.url}")
        # else:
        #     logging.error(f"Influx: Connection to {self.url} failed")
        #     sys.exit(1)

        self.query_api = self.influx.query_api()


    def _get_influxdb2_config(self) -> tuple[str, str, str] | Exception:
        """Get InfluxDB2 configuration from environment variables."""
        org = os.environ.get("B4MAD_RACING_INFLUX_ORG", "b4mad")

        _INFLUXDB2_TOKEN = os.environ.get("B4MAD_RACING_INFLUX_TOKEN")  # noqa: N806

        if _INFLUXDB2_TOKEN is None or _INFLUXDB2_TOKEN == "":
            raise Exception(
                "B4MAD_RACING_INFLUX_TOKEN",
            )

        token = _INFLUXDB2_TOKEN

        _INFLUXDB2_SERVICE_HOST = os.environ.get("INFLUXDB2_SERVICE_HOST")  # noqa: N806
        _INFLUXDB2_SERVICE_PORT = os.environ.get("INFLUXDB2_SERVICE_PORT", 8086)  # noqa: N806
        _INFLUXDB2_SERVICE_PROTOCOL = os.environ.get("INFLUXDB2_SERVICE_PROTOCOL", "http")  # noqa: N806

        if _INFLUXDB2_SERVICE_HOST is None:
            raise Exception(
                "INFLUXDB2_SERVICE_HOST",
            )

        url = f"{_INFLUXDB2_SERVICE_PROTOCOL}://{_INFLUXDB2_SERVICE_HOST}:{_INFLUXDB2_SERVICE_PORT}/"

        return (org, token, url)

    def retrieve_data(self, filters):
        # if filters is an integer
        if isinstance(filters, int):
            return self.session_df(session_id=filters)
        if isinstance(filters, dict):
            return self.session_df(**filters)
            # if "session_id" in filters:
            #     return self.session_df(session_id=filters["session_id"])
            # if "session_id" in filters and "lap_number" in filters:
            #     return self.session_df(
            #         session_id=filters["session_id"], lap_number=filters["lap_number"]
            #     )
        return None

    def session_df(self, **kwargs):
        kwargs["measurement"] = "fast_laps"
        kwargs["bucket"] = "fast_laps"
        df = self._session_df(**kwargs)
        if df.empty:
            kwargs["measurement"] = "laps_cc"
            kwargs["bucket"] = "racing"
            df = self._session_df(**kwargs)
        return df

    def _session_df(
        self,
        session_id,
        lap_number=None,
        start="-365d",
        end="now()",
        measurement="fast_laps",
        bucket="fast_laps",
        aggregate="",
        fields=[],
        drop_tags=False,
        driver="",
        session_type="Race"
    ):
        if isinstance(start, datetime):
            start = start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if isinstance(end, datetime):
            end = end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        query = f"""
        from(bucket: "{bucket}")
        |> range(start: {start}, stop: {end})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> filter(fn: (r) => r["SessionId"] == "{session_id}")
        """

        if fields:
            query += f"""
            |> filter(fn: (r) => r["_field"] == "{fields[0]}")
            """
            for field in fields[1:]:
                query += f"""
                or r["_field"] == "{field}"
                """
            query += ")\n"

        if session_type:
            query += f"""
            |> filter(fn: (r) => r["SessionTypeName"] == "{session_type}")
            """

        if driver:
            query += f"""
            |> filter(fn: (r) => r["user"] == "{driver}")
            """

        if aggregate:
            # downsample to 1Hz
            query += f"""
            |> aggregateWindow(every: {aggregate}, fn: last, createEmpty: false)
            """

        query += """
        |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        """

        if lap_number:
            query += f"""
        |> filter(fn: (r) => r["CurrentLap"] == "{lap_number}")
        """

        query += """
        |> sort(columns: ["_time"], desc: false)
        """

        # drop columns that are not needed
        if drop_tags:
            query += """
            |> drop(columns: ["_start", "_stop", "_measurement", "host", "topic", "user"])
            """

        # print(query)
        df = self.query_api.query_data_frame(query=query)
        # set pd options to display all columns
        # pd.set_option("display.max_columns", None)
        # print(df)
        if df.empty:
            return df

        game = df["GameName"].iloc[0]
        if game == "Assetto Corsa Competizione":
            # flip y axis
            df["x"] = df["WorldPosition_x"]
            df["y"] = df["WorldPosition_z"] * -1
            df["WorldPosition_x"] = df["x"]
            df["WorldPosition_y"] = df["y"]
        if game == "Automobilista 2":
            df["x"] = df["WorldPosition_x"]
            df["y"] = df["WorldPosition_z"]
            df["WorldPosition_x"] = df["x"]
            df["WorldPosition_y"] = df["y"]
        if game == "Richard Burns Rally":
            # rotate 90 degrees to the left
            df["x"] = df["WorldPosition_y"]
            df["y"] = df["WorldPosition_x"]
            df["WorldPosition_x"] = -df["x"]
            df["WorldPosition_y"] = df["y"]


        df["id"] = df["SessionId"].astype(str) + "-" + df["CurrentLap"].astype(str)

        df = df[df["Gear"] != 0]

        return df
