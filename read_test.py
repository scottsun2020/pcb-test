import time

IIO_PATH = "/sys/bus/iio/devices/iio:device0"
SCALE_FILE = f"{IIO_PATH}/in_voltage_scale"

# Read scale factor (e.g., 0.050354003 V per LSB)
with open(SCALE_FILE, 'r') as f:
    scale = float(f.read().strip())

# Read all 8 channels
for ch in range(8):
    raw_file = f"{IIO_PATH}/in_voltage{ch}_raw"
    with open(raw_file, 'r') as f:
        raw = int(f.read().strip())
    voltage = raw * scale / 1000
    print(f"AIN{ch}: {voltage:.3f} V")

    time.sleep(0.1)
