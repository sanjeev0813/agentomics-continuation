# Agentomics

This project uses agent-based modeling to simulate economic scenarios. It is built using the Langroid framework.

## Overview

The simulation consists of three types of agents:

*   **Households:** Households make decisions about consumption, savings, and labor participation. They can be employed or unemployed, and their decisions are influenced by factors such as income, savings, and interest rates.
*   **Firms:** Firms make decisions about production, hiring, and setting wages and prices. They aim to maximize their profits, and their decisions are influenced by factors such as demand and labor market conditions.
*   **Regulator:** The regulator can introduce macroeconomic shocks into the simulation, such as changes in interest rates, stimulus payments, and unemployment shocks.

The agents interact in two markets:

*   **Job Market:** Households and firms interact in the job market, where firms post vacancies and households apply for jobs.
*   **Housing Market:** The housing market is not yet fully implemented, but it will eventually allow households to make decisions about renting or buying a house.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

To run the simulation, simply execute the following command:

```bash
python -m agentomics.simulation
```

This will run the simulation with the default parameters and generate a report in `report.txt`. The simulation will also generate plots of the unemployment rate and Gini coefficient over time.

## Parameters

The simulation can be configured by modifying the parameters in the `main` function in `agentomics/simulation.py`. The following parameters are available:

*   **Number of Households:** The number of households in the simulation.
*   **Number of Firms:** The number of firms in the simulation.
*   **Number of Simulation Steps:** The number of steps to run the simulation for.
*   **Initial Data:** The initial data for the households can be loaded from a CSV file.
*   **Shocks:** The simulation can be configured to introduce various macroeconomic shocks, such as interest rate changes, stimulus payments, and unemployment shocks.
