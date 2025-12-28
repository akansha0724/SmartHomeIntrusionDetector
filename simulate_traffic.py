import pandas as pd
import numpy as np
import random
from datetime import datetime

devices = ['Smart Bulb', 'Smart Camera', 'Smart Plug', 'Thermostat', 'Smart Speaker']

def simulate_traffic(devices, n=200):
    data = []
    for _ in range(n):
        device = random.choice(devices)
        packets = random.randint(50, 150)
        # Inject anomaly 5% of the time
        if random.random() < 0.05:
            packets += random.randint(200, 400)
        timestamp = datetime.now()
        data.append([device, packets, timestamp])
    df = pd.DataFrame(data, columns=['Device', 'Packets', 'Timestamp'])
    return df
