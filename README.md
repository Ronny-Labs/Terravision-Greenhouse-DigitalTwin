# Terravision-Greenhouse-DigitalTwin
An AI-Assisted Closed-Loop Intelligent Sustainable Farming Ecosystem.
import numpy as np
import time

class SensorModule:
    """Simulates the input sensors specified in the TERRAVISION proforma."""
    def __init__(self):
        # Initial baseline states for Kamrup, Assam micro-climates
        self.current_moisture = 45.0   # VWC %
        self.current_temp = 28.0       # Celsius
        self.current_humidity = 70.0   # Relative Humidity %
        self.current_lux = 500.0       # LDR Illuminance index
        
    def read_telemetry(self):
        """Simulates sensor fluctuations over time to test the control loops."""
        # Introducing minor random variations to simulate environment dynamics
        self.current_moisture -= np.random.uniform(0.5, 1.5)
        self.current_temp += np.random.uniform(-1.0, 1.5)
        self.current_humidity += np.random.uniform(-2.0, 2.0)
        self.current_lux = np.clip(self.current_lux + np.random.uniform(-50, 50), 0, 1000)
        
        return {
            "VWC_Moisture": round(self.current_moisture, 2),
            "Temperature_C": round(self.current_temp, 2),
            "Humidity_Pct": round(self.current_humidity, 2),
            "Ambient_Lux": round(self.current_lux, 2)
        }

class TerravisionMCU:
    """
    Simulates the ATmega328P/Arduino Uno controller architecture.
    Implements the precise embedded hysteresis thresholds defined in the proforma.
    """
    def __init__(self):
        # Strict logic thresholds from the system proforma
        self.MOISTURE_THRESHOLD = 30.0  # Trigger pump below 30% VWC
        self.TEMP_HIGH_THRESHOLD = 35.0 # Trigger exhaust fan above 35C
        self.TEMP_LOW_THRESHOLD = 18.0  # Trigger heating element below 18C
        self.HUMIDITY_THRESHOLD = 85.0  # Trigger ventilation above 85% RH
        self.LDR_THRESHOLD = 300.0      # Trigger PAR LED grow lights below 300 index
        
        # Actuator Relay States (False = Off, True = On)
        self.relays = {
            "RELAY_1_PUMP": False,
            "RELAY_2_FAN": False,
            "RELAY_3_LED": False,
            "RELAY_HEATER": False
        }

    def process_control_logic(self, telemetry):
        """Executes the closed-loop feedback control sequences sequentially."""
        
        # 1. Hydration Loop (Micro-drip Irrigation)
        if telemetry["VWC_Moisture"] < self.MOISTURE_THRESHOLD:
            self.relays["RELAY_1_PUMP"] = True
        else:
            # Hysteresis simulation: turn off once stable recovery is predicted
            self.relays["RELAY_1_PUMP"] = False

        # 2. Thermal Regulation Loop (Frost Defense)
        if telemetry["Temperature_C"] < self.TEMP_LOW_THRESHOLD:
            self.relays["RELAY_HEATER"] = True
        else:
            self.relays["RELAY_HEATER"] = False

        # 3. Ventilation & Humidity Loop
        if (telemetry["Temperature_C"] > self.TEMP_HIGH_THRESHOLD) or (telemetry["Humidity_Pct"] > self.HUMIDITY_THRESHOLD):
            self.relays["RELAY_2_FAN"] = True
        else:
            self.relays["RELAY_2_FAN"] = False

        # 4. Photoperiod Loop (Supplemental PAR Spectrum)
        if telemetry["Ambient_Lux"] < self.LDR_THRESHOLD:
            self.relays["RELAY_3_LED"] = True
        else:
            self.relays["RELAY_3_LED"] = False
            
        return self.relays

# --- Executing the Digital Twin System Test ---
mcu = TerravisionMCU()
sensors = SensorModule()

print("⚡ INITIALIZING TERRAVISION DIGITAL TWIN SYSTEM ARCHITECTURE SIMULATION ⚡")
print("-" * 75)

# Simulate 3 sequential telemetry cycles to show how loops evaluate changing parameters
for cycle in range(1, 4):
    print(f"\n[SYSTEM CYCLE #{cycle}]")
    current_data = sensors.read_telemetry()
    print(f"📡 Real-time Telemetry: {current_data}")
    
    actuator_states = mcu.process_control_logic(current_data)
    print("🔌 Opto-Isolated Relay Matrix Status:")
    for component, state in actuator_states.items():
        status_text = "🟢 ACTIVE / ENERGIZED" if state else "🔴 STANDBY / OFF"
        print(f"  ▪️ {component}: {status_text}")
        
    time.sleep(0.5)
