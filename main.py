#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 18:14:27 2023

@author: OdairTrujillo
"""

import io
import base64
from flask import Flask, render_template, Response
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend to avoid issues with GUI
import matplotlib.pyplot as plt
import psutil
import threading
import time

app = Flask(__name__)

cpu_data = []
ram_data = []
network_data = []
nvme_data = []
refresh_rate = 5

def read_system_parameters():
    """
    Reads the current system parameters for CPU, RAM, Network, and NVMe storage usage.
    """
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    network_usage = psutil.net_io_counters().bytes_sent
    nvme_usage = psutil.disk_usage('/').percent

    return cpu_usage, ram_usage, network_usage, nvme_usage

def plot_data():
    """
    Generates the system usage plot as an image.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each system metric
    cpu_line, = ax.plot(cpu_data, label='CPU', color='red')
    ram_line, = ax.plot(ram_data, label='RAM', color='green')
    network_line, = ax.plot(network_data, label='Network', color='blue')
    nvme_line, = ax.plot(nvme_data, label='NVMe Storage', color='yellow')

    # Set plot parameters
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 100)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Usage (%)')
    ax.set_title('System Usage')
    ax.legend()

    # Save the figure to a BytesIO object
    output = io.BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)

    return output

@app.route('/plot.png')
def plot_png():
    """
    Serves the system usage plot as a PNG image.
    """
    output = plot_data()
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/')
def index():
    """
    Renders the main HTML page with the embedded system usage plot.
    """
    return render_template('index.html')

def update_data():
    """
    Continuously updates the system usage data every 3 seconds.
    """
    while True:
        cpu_usage, ram_usage, network_usage, nvme_usage = read_system_parameters()
        cpu_data.append(cpu_usage)
        ram_data.append(ram_usage)
        network_data.append(network_usage)
        nvme_data.append(nvme_usage)

        # Keep the data lists limited to the last 60 entries (60 seconds)
        if len(cpu_data) > 60:
            cpu_data.pop(0)
            ram_data.pop(0)
            network_data.pop(0)
            nvme_data.pop(0)

        time.sleep(refresh_rate)

if __name__ == '__main__':
    # Start a thread to update system data in the background
    data_thread = threading.Thread(target=update_data)
    data_thread.daemon = True
    data_thread.start()

    # Run the Flask app
    app.run(debug=True)
