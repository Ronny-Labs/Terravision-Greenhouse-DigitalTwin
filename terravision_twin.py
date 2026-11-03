import time
import random
import math

class SensorModule:
    """
    Simulates physical greenhouse sensors (Soil Moisture, Temperature, Humidity, and Light).
    Tailored for micro-climates like Kamrup, Assam.
    """
    def __init__(self):
        # Initial baseline environmental values
        self.soil_moisture_vwc = 35.0  # Volumetric Water Content (%)
        self.temperature_c = 26.5      # Temperature in Celsius
        self.humidity_pct = 70.0       # Relative Humidity (%)
        self.light_index = 450.0       # Ambient light index (LDR)

    def read_telemetry(self):
        """Introduces minor real-world fluctuations to simulate environmental dynamics."""
        self.soil_moisture_vwc += random.uniform(-1.5, 1.0)
        self.temperature_c += random.uniform(-0.5, 0.5)
        self.humidity_pct += random.uniform(-2.0, 2.0)
        self.light_index += random.uniform(-20, 20)

        # Keep values within realistic physical bounds
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
    Simulates an ATmega328P / Arduino Uno microcontroller.
    Evaluates live telemetry against hysteresis thresholds and controls actuators.
    """
    def __init__(self):
        # Actuator relay states (False = OFF, True = ON)
        self.relay_pump = False
        self.relay_fan = False
        self.relay_led = False
        self.relay_heater = False

    def calculate_vpd(self, temp_c, humidity_pct):
        """
        Calculates Vapor Pressure Deficit (VPD) in kilopascals (kPa) using the Tetens equation.
        Ideal range for most crops: 0.8 kPa to 1.2 kPa.
        """
        svp = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        avp = svp * (humidity_pct / 100.0)
        vpd = svp - avp
        return round(vpd, 3)

    def evaluate_control_logic(self, telemetry):
        """Applies strict threshold rules to trigger greenhouse actuators."""
        temp = telemetry["temperature"]
        humidity = telemetry["humidity"]
        moisture = telemetry["soil_moisture"]
        light = telemetry["light"]

        # 1. Hydration Loop: Water pump triggers if soil moisture drops below 30.0% VWC
        self.relay_pump = moisture < 30.0

        # 2. Thermal Regulation Loop: Heater triggers if temp drops below 18.0°C
        self.relay_heater = temp < 18.0

        # 3. Ventilation & Humidity Loop: Fan triggers if temp > 35.0°C or humidity > 85.0%
        self.relay_fan = (temp > 35.0) or (humidity > 85.0)

        # 4. Photoperiod Loop: PAR LED grow lights trigger if light drops below 300.0
        self.relay_led = light < 300.0

        # Calculate live VPD
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

    # Run a 5-cycle simulation test
    for cycle in range(1, 6):
        print(f"\n--- Simulation Cycle {cycle} ---")
        
        # Get live data from sensors
        telemetry = sensors.read_telemetry()
        print(f"📊 Telemetry -> Soil Moisture: {telemetry['soil_moisture']}% | "
              f"Temp: {telemetry['temperature']}°C | "
              f"Humidity: {telemetry['humidity']}% | "
              f"Light: {telemetry['light']}")

        # Evaluate MCU control actions and VPD
        actions = mcu.evaluate_control_logic(telemetry)
        print(f"🤖 MCU Actions -> Pump: {'ON' if actions['pump'] else 'OFF'} | "
              f"Fan: {'ON' if actions['fan'] else 'OFF'} | "
              f"LED: {'ON' if actions['led'] else 'OFF'} | "
              f"Heater: {'ON' if actions['heater'] else 'OFF'}")
        print(f"💨 Calculated VPD: {actions['vpd_kPa']} kPa")

        # Small delay between simulation ticks
        time.sleep(0.5)

    print("\n✅ Simulation completed successfully!")
