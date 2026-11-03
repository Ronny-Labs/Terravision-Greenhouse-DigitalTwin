# Terravision-Greenhouse-DigitalTwin 🌿

An AI-Assisted Closed-Loop Intelligent Sustainable Farming Ecosystem tailored for micro-climates like Kamrup, Assam.

---

## 🏆 Project Overview & Exhibition Background
* **Project Name:** TERRAVISION
* **Achievement:** 1st Place at the Cluster Science Exhibition 
* **Institution:** Jawahar Navodaya Vidyalaya (JNV), Rangia, Kamrup, Assam
* **Core Concept:** This project transitions from a physical Arduino/microcontroller prototype into a robust **Digital Twin Simulation** on GitHub. It models real-time environmental telemetry and automated closed-loop agricultural control systems.

---

## 🔬 System Architecture & Scientific Principles
The digital twin models real-world greenhouse dynamics using two primary software modules:

1. **`SensorModule`:**
   * Simulates continuous physical sensor feeds for regional micro-climates (Kamrup, Assam).
   * Tracks **Soil Moisture (VWC %)**, **Temperature (°C)**, **Relative Humidity (% RH)**, and **Ambient Light (Lux/LDR index)**.
   * Introduces controlled randomized environmental fluctuations to test system resilience.

2. **`TerravisionMCU` (Microcontroller Logic):**
   * Mimics an ATmega328P / Arduino Uno controller architecture.
   * Enforces strict **Embedded Hysteresis Control** thresholds to prevent relay chatter and optimize energy/resource usage:
     * **Hydration Loop:** Triggers micro-drip water pump (`RELAY_1_PUMP`) when soil moisture drops below **30.0% VWC**.
     * **Thermal Regulation Loop:** Triggers heating element (`RELAY_HEATER`) when temperature drops below **18.0°C** (frost defense).
     * **Ventilation & Humidity Loop:** Triggers exhaust fan (`RELAY_2_FAN`) if temperature exceeds **35.0°C** or relative humidity exceeds **85.0% RH**.
     * **Photoperiod Loop:** Triggers supplemental PAR spectrum grow lights (`RELAY_3_LED`) if ambient light falls below **300.0 index**.

---

## 🚀 How to Run the Digital Twin
1. Ensure you have Python installed along with `numpy`.
2. Place the `terravision_twin.py` script in your repository directory.
3. Run the simulation script from your terminal:
   ```bash
   python terravision_twin.py
  
