# TERRAVISION V2.0 — Digital Twin 🌿

A Python-based software continuation of TERRAVISION, a collaborative Arduino
smart greenhouse project. This repository contains a greenhouse simulation
that is an early step towards exploring digital twin concepts. It is not
connected to the original physical greenhouse or its sensors.

## Project Progression

- **V1.0 — TERRAVISION: Smart Greenhouse:** The original team-built physical
  greenhouse project, developed for the JNV Cluster Science Exhibition.
- **V2.0 — TERRAVISION: Digital Twin:** A software continuation exploring
  simulated greenhouse readings, hysteresis-based actuator control, and
  illustrative environmental feedback.

**Original project:** [Smart-Greenhouse-IOT](https://github.com/Ronny-Labs/Smart-Greenhouse-IOT)

## V1.0: Original Team Project

TERRAVISION V1.0 was a collaborative Arduino-based smart greenhouse project
developed for the JNV Cluster Science Exhibition. The team received 1st place.

My primary contribution was the physical construction and hardware integration
of the greenhouse prototype. I also assisted with research, project information
materials, and documentation. Through the project, I gained practical exposure
to electronic components, sensors, relay modules, wiring, and soldering. I also
learned about the software and control-logic side through collaboration with
teammates.

## V2.0: Current Implementation

The repository currently includes `terravision_twin.py`, a small simulation
that maintains evolving values for soil moisture, temperature, humidity, and a
light index. Each cycle applies configurable randomized environmental drift
and the previous cycle's actuator states once, then generates readings from
the updated environment. The model also bounds the simulated environmental
values.

The illustrative actuator effects applied once per simulation cycle are:

- **Pump:** increases simulated soil moisture.
- **Fan:** decreases simulated temperature and humidity. The humidity reduction
  is an illustrative assumption.
- **Heater:** increases simulated temperature.
- **LED:** contributes a small simulated heat effect.

The actuator states are calculated from the current readings using hysteresis
control and influence the environment on the following cycle. The simulation
also estimates VPD from simulated temperature and humidity and prints five
cycles to the terminal.

This is a simplified illustrative simulation, not a scientifically validated
greenhouse model. Its actuator-effect values and environmental drift are not
calibrated real-world rates or growing recommendations. The environmental
feedback uses simplified fixed effects and does not model complex interactions
between greenhouse variables. Readings are simulated; the actuator states do not
control real equipment, and the script does not connect to the physical
prototype or its sensors. The light reading is an index, not a PAR measurement.
VPD is an estimate and has not been validated for agricultural use. The script
does not include AI/ML features, a dashboard, data logging, or hardware
integration.

The control logic uses separate ON and OFF thresholds for each actuator. This
prevents rapid switching around the control boundary while preserving actuator
states through their deadbands.

### Hysteresis Control Behavior

The actuator rules are intentionally simple and illustrative:

- **Pump:** turns ON when soil moisture falls below 30%. Once ON, it stays ON
  until moisture reaches 35% or higher, then turns OFF.
- **Heater:** turns ON when temperature drops below 18°C. Once ON, it stays ON
  until temperature reaches 20°C or higher, then turns OFF.
- **Fan:** turns ON when temperature exceeds 35°C or humidity exceeds 85%.
  Once ON, it stays ON until both temperature is at or below 32°C and humidity
  is at or below 80%.
- **LED:** turns ON when light falls below 300. Once ON, it stays ON until light
  reaches 350 or higher, then turns OFF.

These deadbands allow actuator states to persist through their respective
operating ranges and reduce rapid ON/OFF chatter around threshold values.

## Run the Simulation

Requires Python 3. No third-party packages are needed.

```bash
python terravision_twin.py
```

The script prints five cycles, with a short pause between cycles.

## Planned Development

Future work may include:

- Making the simulated environmental changes more realistic and configurable.
- Recording readings to a file, including CSV logging, and visualizing trends.
- Building a dashboard for the simulation.
- Exploring how a software model could better represent the physical greenhouse.
- Exploring sensor or microcontroller integration as a separate future step.

These are plans, not completed features.

## Project Status

**Basic greenhouse simulation implemented with hysteresis-based simulated
actuator control and illustrative environmental feedback; further development
planned.**
