import json
import os

source_path = '/Users/arian/Documents/FHNW/mss:ngs/sim_ngs.py'
target_path = '/Users/arian/Documents/FHNW/mss:ngs/sim_ngs.ipynb'

with open(source_path, 'r') as f:
    content = f.read()

# Define split markers
markers = [
    "# --- 1. Agenten ---",
    "# --- 2. Modell mit IMBMS Logik ---",
    "# --- Hilfsfunktionen ---",
    "# --- 3. Ausführung & Vergleich ---"
]

sections = []
last_pos = 0
for marker in markers:
    pos = content.find(marker)
    if pos == -1:
        print(f"Error: Marker '{marker}' not found")
        # Fallback: Treat as one block if markers fail (unlikely given I read the file)
        sections = [content]
        break
    
    sections.append(content[last_pos:pos].strip())
    last_pos = pos

if len(sections) > 1:
    sections.append(content[last_pos:].strip())

# Ensure we have 5 sections (0 to 4)
if len(sections) != 5:
    print(f"Warning: Expected 5 sections, got {len(sections)}. Notebook might be structured incorrectly.")

cells = []

# Cell 1: Intro
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# City Transport Simulation (Mesa)\n",
        "\n",
        "This notebook implements a multi-agent simulation of a city transport system using `mesa`.\n",
        "It compares two scenarios:\n",
        "1. **Baseline**: Status Quo behavior.\n",
        "2. **IMBMS**: An intelligent system that deploys extra Trams when passenger satisfaction drops."
    ]
})

# Cell 2: Imports
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": sections[0].splitlines(keepends=True)
})

# Cell 3: Agenten Intro
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 1. Agent Definitions\n",
        "\n",
        "We define two types of agents:\n",
        "- **PassengerAgent**: Commuters with a preferred mode (Bus/Tram). They have a satisfaction score that decays while waiting. Long waits can trigger a mode switch.\n",
        "- **VehicleAgent**: Buses or Trams. They move, collect passengers, and emit CO2. Buses can be delayed by construction."
    ]
})

# Cell 4: Agenten Code
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": sections[1].splitlines(keepends=True)
})

# Cell 5: Model Intro
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 2. Model Definition\n",
        "\n",
        "The `CityTransportModel` initializes the grid and agents. It collects data at each step.\n",
        "If `scenario='imbms'`, it monitors average satisfaction and deploys an extra tram if it falls below 80."
    ]
})

# Cell 6: Model Code
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": sections[2].splitlines(keepends=True)
})

# Cell 7: Helpers Intro
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 3. Helper Functions\n",
        "\n",
        "Helper functions for the DataCollector to compute model-level metrics."
    ]
})

# Cell 8: Helpers Code
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": sections[3].splitlines(keepends=True)
})

# Cell 9: Execution Intro
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Execution & Comparison\n",
        "\n",
        "We run both scenarios (Baseline vs IMBMS) for 150 steps and compare the results using Matplotlib."
    ]
})

# Cell 10: Execution Code
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": sections[4].splitlines(keepends=True)
})


notebook = {
 "cells": cells,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open(target_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Notebook created at {target_path}")
