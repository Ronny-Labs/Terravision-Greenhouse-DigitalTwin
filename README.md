# TERRAVISION V2.0 — Digital Twin 🌿

A Python-based software continuation of TERRAVISION, a collaborative Arduino
smart greenhouse project. This repository contains a greenhouse simulation
that is an early step towards exploring digital twin concepts. It is not
connected to the original physical greenhouse or its sensors.

## Project Progression

- **V1.0 — TERRAVISION: Smart Greenhouse:** The original team-built physical
  greenhouse project, developed for the JNV Cluster Science Exhibition.
- **V2.0 — TERRAVISION: Digital Twin:** A software continuation exploring
  simulated greenhouse readings and simple automated-control rules.

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

The repository currently includes `terravision_twin.py`, a small greenhouse
simulation that:

- Generates changing, randomized values for soil moisture, temperature,
  humidity, and a light index.
- Applies simple threshold rules to produce simulated pump, fan, LED, and
  heater states.
- Estimates VPD using the simulated temperature and humidity.
- Prints five simulation cycles to the terminal.

This is a greenhouse simulation and an early step towards a digital twin; it
does not connect to the physical prototype or its sensors. The readings are
simulated, and the actuator states do not control real equipment. The light
reading is an index, not a PAR measurement. The script's thresholds and
starting values are illustrative and are not validated growing recommendations.
The VPD value is an estimate calculated from simulated temperature and humidity;
it has not been validated for agricultural use.

The control rules currently use single thresholds. They do not implement
hysteresis. The script also does not currently include a dashboard, data
logging, hardware connection, or AI/ML features.

## Run the Simulation

Requires Python 3. No third-party packages are needed.

```bash
python terravision_twin.py
```

The script prints five cycles, with a short pause between cycles.

## Planned Development

Future work may include:

- Making the simulated environmental changes more realistic and configurable.
- Recording readings to a file and visualizing trends.
- Building a dashboard for the simulation.
- Exploring how a software model could represent the physical greenhouse.
- Investigating data analysis or AI-based features after the simulation and
  data are developed further.
- Exploring sensor or microcontroller integration as a separate future step.

These are plans, not completed features.

## Project Status

**Basic greenhouse simulation implemented; further development planned.**
