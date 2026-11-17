import time
import random
import math


class SensorModule:
    """
    Maintains a simplified illustrative greenhouse environment and reports
    simulated soil-moisture, temperature, humidity, and light readings.

    This is not a scientifically validated greenhouse model. It does not
    represent physical sensors, a specific greenhouse, or calibrated rates.
    """
    def __init__(self):
        # Illustrative starting values for the simulation.
        self.soil_moisture_vwc = 35.0  # Simulated soil-moisture value (%)
        self.temperature_c = 26.5      # Temperature in Celsius
        self.humidity_pct = 70.0       # Relative humidity (%)
        self.light_index = 450.0       # Simulated light index, not a PAR measurement

        # Configurable random drift ranges applied once per cycle. These small
        # per-cycle changes are illustrative, not calibrated environmental rates.
        self.soil_drift_range = (-0.15, 0.05)
        self.temperature_drift_range = (-0.15, 0.15)
        self.humidity_drift_range = (-0.5, 0.5)
        self.light_drift_range = (-20.0, 20.0)

        # Illustrative actuator effects applied once per cycle, not instantaneous
        # real-world rates or recommendations.
        self.pump_moisture_increase = 0.3
        self.fan_temperature_decrease = 0.25
        self.fan_humidity_decrease = 0.5
        self.heater_temperature_increase = 0.3
        self.led_temperature_increase = 0.05

    def _apply_environment_drift(self):
        """Apply configurable small random environmental changes once per cycle."""
        self.soil_moisture_vwc += random.uniform(*self.soil_drift_range)
        self.temperature_c += random.uniform(*self.temperature_drift_range)
        self.humidity_pct += random.uniform(*self.humidity_drift_range)
        self.light_index += random.uniform(*self.light_drift_range)

    def _apply_actuator_effects(self, actuator_states):
        """Apply the previous cycle's actuator effects once to this cycle's state."""
        if actuator_states["fan"]:
            self.temperature_c -= self.fan_temperature_decrease
            # Fan-driven humidity reduction is an illustrative assumption for
            # this simplified model, not a validated ventilation calculation.
            self.humidity_pct -= self.fan_humidity_decrease

        if actuator_states["heater"]:
            self.temperature_c += self.heater_temperature_increase

        if actuator_states["pump"]:
            self.soil_moisture_vwc += self.pump_moisture_increase

        # LED activation contributes only a small illustrative heat effect.
        if actuator_states["led"]:
            self.temperature_c += self.led_temperature_increase

    def _bound_environment(self):
        """Clamp simulated environmental variables to configured sensible bounds."""
        self.soil_moisture_vwc = max(0.0, min(100.0, self.soil_moisture_vwc))
        self.temperature_c = max(10.0, min(45.0, self.temperature_c))
        self.humidity_pct = max(10.0, min(100.0, self.humidity_pct))
        self.light_index = max(0.0, min(1000.0, self.light_index))

    def read_telemetry(self, previous_actuator_states):
        """Advance the environment once, then return readings from its new state.

        Actuator effects use the states from the preceding cycle. The first
        cycle passes all-OFF states, so no actuator effects are applied then.
        """
        self._apply_environment_drift()
        self._apply_actuator_effects(previous_actuator_states)
        self._bound_environment()

        return {
            "soil_moisture": round(self.soil_moisture_vwc, 2),
            "temperature": round(self.temperature_c, 2),
            "humidity": round(self.humidity_pct, 2),
            "light": round(self.light_index, 2)
        }


class TerravisionMCU:
    """
    Applies hysteresis rules to simulated readings and returns simulated
    actuator states. It does not connect to a physical microcontroller or
    control real equipment.
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
        """Update simulated actuator states using ON/OFF hysteresis thresholds."""
        temp = telemetry["temperature"]
        humidity = telemetry["humidity"]
        moisture = telemetry["soil_moisture"]
        light = telemetry["light"]

        # Hysteresis uses different switching thresholds in each direction.
        # Once ON, an actuator stays ON through the deadband; once OFF, it
        # stays OFF through the deadband. This avoids rapid threshold chatter.

        # Pump: turn ON below 30% moisture; once ON, turn OFF at 35% or above.
        if self.relay_pump:
            if moisture >= 35.0:
                self.relay_pump = False
        elif moisture < 30.0:
            self.relay_pump = True

        # Heater: turn ON below 18°C; once ON, turn OFF at 20°C or above.
        if self.relay_heater:
            if temp >= 20.0:
                self.relay_heater = False
        elif temp < 18.0:
            self.relay_heater = True

        # Fan: turn ON above either ON threshold. Turn OFF only after both
        # readings have fallen to their OFF thresholds or lower.
        if self.relay_fan:
            if temp <= 32.0 and humidity <= 80.0:
                self.relay_fan = False
        elif temp > 35.0 or humidity > 85.0:
            self.relay_fan = True

        # LED: thresholds apply to the light index, which is not a PAR reading.
        if self.relay_led:
            if light >= 350.0:
                self.relay_led = False
        elif light < 300.0:
            self.relay_led = True

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

    # Start with every actuator OFF. States calculated in one cycle are used
    # to update the environment at the beginning of the next cycle.
    previous_actuator_states = {
        "pump": False,
        "fan": False,
        "led": False,
        "heater": False,
    }

    # Run five simulation cycles
    for cycle in range(1, 6):
        print(f"\n--- Simulation Cycle {cycle} ---")

        # Update the environment once using prior-cycle states, then read it.
        telemetry = sensors.read_telemetry(previous_actuator_states)
        print(f"📊 Telemetry -> Soil Moisture: {telemetry['soil_moisture']}% | "
              f"Temp: {telemetry['temperature']}°C | "
              f"Humidity: {telemetry['humidity']}% | "
              f"Light: {telemetry['light']}")

        # Evaluate control from current readings; these states affect next cycle.
        actions = mcu.evaluate_control_logic(telemetry)
        print(f"🤖 MCU Actions -> Pump: {'ON' if actions['pump'] else 'OFF'} | "
              f"Fan: {'ON' if actions['fan'] else 'OFF'} | "
              f"LED: {'ON' if actions['led'] else 'OFF'} | "
              f"Heater: {'ON' if actions['heater'] else 'OFF'}")
        print(f"💨 Calculated VPD: {actions['vpd_kPa']} kPa")

        # Save only actuator states for the next environment update.
        previous_actuator_states = {
            "pump": actions["pump"],
            "fan": actions["fan"],
            "led": actions["led"],
            "heater": actions["heater"],
        }

        # Small delay between simulation ticks
        time.sleep(0.5)

    print("\n✅ Simulation completed successfully!")
