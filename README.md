<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PreReact-Backend</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 20px;
      max-width: 800px;
    }
    pre, code {
      background: #f4f4f4;
      padding: 4px 8px;
      border-radius: 4px;
      overflow-x: auto;
    }
    pre {
      padding: 10px;
    }
    h1, h2, h3 {
      border-bottom: 1px solid #ccc;
      padding-bottom: 5px;
    }
    ul {
      margin-left: 20px;
    }
  </style>
</head>
<body>

  <h1>PreReact-Backend</h1>
  <p><strong>PreReact-Backend</strong> is a Python-based backend project for processing and analyzing sensor data.
  It includes modules for sensor management, the calculation of Short-Time Fourier Transforms (STFT) with additional metrics
  (such as energy, standard deviation, peaks, and peak-to-peak values), and an interactive command-line interface (<code>SensorConsole</code>)
  for data exploration and manipulation.</p>

  <h2>Features</h2>
  <ul>
    <li><strong>Sensor Management</strong>
      <ul>
        <li>Loading sensor data from HDF5 files</li>
        <li>Storing sensor data with attributes (ID, alias, sensor type, measurement time, etc.)</li>
        <li>Managing features (e.g., RAW signal) and STFT objects</li>
      </ul>
    </li>
    <li><strong>STFT Calculation</strong>
      <ul>
        <li>Calculates the STFT for given sensor data</li>
        <li>Additional metrics:
          <ul>
            <li>Energy</li>
            <li>Standard Deviation</li>
            <li>Peak-to-Peak Value</li>
            <li>Two Highest Peaks</li>
          </ul>
        </li>
        <li>Flexible window functions (e.g., Hann, rectangular)</li>
      </ul>
    </li>
    <li><strong>Command-line Interface (<code>SensorConsole</code>)</strong>
      <ul>
        <li>Interactive commands to load, save, select, and update sensors</li>
        <li>Commands to add, remove, and revaluate (recompute) individual STFTs</li>
        <li>Display all features and STFTs for easy verification</li>
      </ul>
    </li>
  </ul>

  <h2>Installation</h2>
  <h3>Requirements</h3>
  <ul>
    <li>Python 3.8+</li>
    <li>Dependencies:
      <ul>
        <li><a href="https://numpy.org/">NumPy</a></li>
        <li><a href="https://www.h5py.org/">h5py</a></li>
      </ul>
    </li>
  </ul>

  <h3>Installation via pip</h3>
  <pre><code>python -m venv venv
# On Linux/MacOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install numpy h5py
</code></pre>
  <p>Then clone the repository:</p>
  <pre><code>git clone https://github.com/yourusername/PreReact-Backend.git
cd PreReact-Backend
</code></pre>

  <h2>Project Structure</h2>
  <pre><code>PreReact-Backend/
├── backend/
│   ├── console.py             # Command-line interface (SensorConsole)
│   ├── data/
│   │   ├── DeviceData.py      # Loading and saving sensors (HDF5)
│   │   └── sensor_module.py   # Sensor class including STFT management
│   ├── generics/
│   │   ├── Feature.py         # Feature class (e.g., RAW signal)
│   │   └── STFT.py            # STFT class with calculations and metrics
│   └── utils/
│       ├── SensorType.py      # Definitions and helper functions for sensor types
│       ├── windows.py         # Creation of window functions (Hann, rectangular, etc.)
│       └── saveable.py        # Base class for saveable objects
├── README.html                # This README (in HTML)
└── requirements.txt           # List of Python dependencies (optional)
</code></pre>

  <h2>Usage</h2>
  <h3>Starting SensorConsole</h3>
  <pre><code>python backend/console.py
</code></pre>
  <p>After starting, you will see the prompt <code>&gt;&gt;&gt;</code>. Available commands include:</p>
  <ul>
    <li><strong>load &lt;directory&gt;</strong>: Loads sensor data from a specified directory (HDF5 files).</li>
    <li><strong>select &lt;sensor_id&gt;</strong>: Selects a sensor by its ID.</li>
    <li><strong>list_features</strong>: Lists all available features of the selected sensor.</li>
    <li><strong>list_stfts</strong>: Lists all STFTs of the selected sensor.</li>
    <li><strong>add_stft &lt;stft_id&gt; &lt;window_size&gt; &lt;window_type&gt; &lt;hop_size&gt;</strong>: Adds a new STFT if the ID is not already taken. The STFT is automatically computed if the RAW signal is available.</li>
    <li><strong>remove_stft &lt;stft_id&gt;</strong>: Removes an STFT by its ID.</li>
    <li><strong>revaluate_stft &lt;stft_id&gt;</strong>: Recalculates a specific STFT.</li>
    <li><strong>revaluate_all</strong>: Recalculates all STFTs for the sensor.</li>
    <li><strong>save &lt;directory&gt;</strong>: Saves all sensor data (including features and STFTs) to a specified directory (as HDF5).</li>
    <li><strong>exit</strong>: Exits the console.</li>
  </ul>

  <h2>Planned / To Do</h2>
  <ul>
    <li>Implementation of evaluation algorithms using static methods</li>
    <li>Embedding ML/AI into evaluation algorithm</li>
    <li>Implementation of dataset changing awareness incl. distance measurement of measurements</li>
    <li>Topological data analysis & holomorphy</li>
    <li>Web integration using django</li>
    <li>Parallelization</li>
  </ul>

  <h2>Development</h2>
  <p>If you want to contribute to the project:</p>
  <ol>
    <li>Fork the repository.</li>
    <li>Create a new branch (<code>git checkout -b feature/my-feature</code>).</li>
    <li>Make your changes and commit them.</li>
    <li>Submit a pull request.</li>
  </ol>

  <h2>License</h2>
  <p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

</body>
</html>
