from dataclasses import dataclass


@dataclass
class Measurement:
    electricity_consumption_low: float
    electricity_consumption_high: float
    electricity_production_low: float
    electricity_production_high: float
    gas_consumption: float
    current_electricity_consumption: float

