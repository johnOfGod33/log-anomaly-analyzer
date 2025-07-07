# Log Anomaly Analyzer

## Description

Log Anomaly Analyzer is a Python tool that processes log files to detect security anomalies, generate alert reports, and visualize event statistics.

## How it works

The tool reads a log file asynchronously, detects patterns of critical events, and generates a PDF report with alert details and a frequency histogram. An interactive menu lets you process logs, view alerts, and create reports easily.

## Features

- Asynchronous log file reading
- Automatic anomaly detection (3 critical events in 30 seconds)
- Professional PDF report with event frequency histogram
- Simple interactive CLI menu

## Tech Stack

- Python 3.8+
- matplotlib
- fpdf
- asyncio

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/johnOfGod33/log-anomaly-analyzer.git
   cd log-anomaly-analyzer
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   cd src
   python main.py
   ```
