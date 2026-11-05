import time
import random
import math

class SensorModule:
    """
    Generates simulated soil-moisture, temperature, humidity, and light readings.
    These are not measurements from physical sensors or a region-specific
    climate model.
    """
    def __init__(self):
        # Illustrative starting values for the simulation
        self.soil_moisture_vwc = 35.0  # Illustrative simulated soil-moisture value (%)
        self.temperature_c = 26.5      # Temperature in Celsius
        self.humidity_pct = 70.0       # Relative Humidity (%)
        self.light_index = 450.0       # Simulated light index, not a PAR measurement

    def read_telemetry(self):
        """Adds randomized changes to the simulated readings."""
        self.soil_moisture_vwc += random.uniform(-1.5, 1.0)
        self.temperature_c += random.uniform(-0.5, 0.5)
        self.humidity_pct += random.uniform(-2.0, 2.0)
        self.light_index += random.uniform(-20, 20)

        # Keep soil moisture, humidity, and light within configured bounds
        self.soil_moisture_vwc = max(0.0, min(100.0, self.soil_moisture_vwc))
        self.humidity_pct = max(10.0, min(100.0, self.humidity_pct))
        self.light_index = max(0.0, self.light_index)

        return {
            "soil_moisture": round(self.soil_moisture_vwc, 2),
            "temperature": round(self.temperature_c, 2),
            "humidity": round(self.humidity_pct, 2),
            "light": round(self.light_index, 2)
        }


class TerravisionMCU:
    """
    Applies single-threshold rules to simulated readings and returns simulated
    actuator states. It does not connect to a physical microcontroller or
    control real equipment; the rules do not implement hysteresis.
    """
    def __init__(self):
        # Simulated actuator states (False = OFF, True = ON)
        self.relay_pump = False
        self.relay_fan = False
        self.relay_led = False
        self.relay_heater = False

    def calculate_vpd(self, temp_c, humidity_pct):
        """
        Estimates Vapor Pressure Deficit (VPD) in kilopascals (kPa) from the
        supplied temperature and humidity using the Tetens equation. This
        estimate is not validated for agricultural use.
        """
        svp = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        avp = svp * (humidity_pct / 100.0)
        vpd = svp - avp
        return round(vpd, 3)

    def evaluate_control_logic(self, telemetry):
        """Uses single thresholds to calculate simulated actuator states."""
        temp = telemetry["temperature"]
        humidity = telemetry["humidity"]
        moisture = telemetry["soil_moisture"]
        light = telemetry["light"]

        # 1. Simulated pump state is ON below the illustrative moisture threshold
        self.relay_pump = moisture < 30.0

        # 2. Simulated heater state is ON below the illustrative temperature threshold
        self.relay_heater = temp < 18.0

        # 3. Simulated fan state is ON above either illustrative threshold
        self.relay_fan = (temp > 35.0) or (humidity > 85.0)

        # 4. Simulated LED state uses a light-index threshold; the index is not PAR
        self.relay_led = light < 300.0

        # Estimate VPD from the simulated temperature and humidity
        current_vpd = self.calculate_vpd(temp, humidity)

        return {
            "pump": self.relay_pump,
            "fan": self.relay_fan,
            "led": self.relay_led,
            "heater": self.relay_heater,
            "vpd_kPa": current_vpd
        }


# ==========================================
# MAIN EXECUTION SIMULATION LOOP
# ==========================================
if __name__ == "__main__":
    print("🌿 Initializing Terravision Digital Twin Simulation...")
    sensors = SensorModule()
    mcu = TerravisionMCU()

    # Run five simulation cycles
    for cycle in range(1, 6):
        print(f"\n--- Simulation Cycle {cycle} ---")
        
        # Generate simulated readings
        telemetry = sensors.read_telemetry()
        print(f"📊 Telemetry -> Soil Moisture: {telemetry['soil_moisture']}% | "
              f"Temp: {telemetry['temperature']}°C | "
              f"Humidity: {telemetry['humidity']}% | "
              f"Light: {telemetry['light']}")

        # Calculate simulated actuator states and estimate VPD
        actions = mcu.evaluate_control_logic(telemetry)
        print(f"🤖 MCU Actions -> Pump: {'ON' if actions['pump'] else 'OFF'} | "
              f"Fan: {'ON' if actions['fan'] else 'OFF'} | "
              f"LED: {'ON' if actions['led'] else 'OFF'} | "
              f"Heater: {'ON' if actions['heater'] else 'OFF'}")
        print(f"💨 Calculated VPD: {actions['vpd_kPa']} kPa")

        # Small delay between simulation ticks
        time.sleep(0.5)

    print("\n✅ Simulation completed successfully!")
