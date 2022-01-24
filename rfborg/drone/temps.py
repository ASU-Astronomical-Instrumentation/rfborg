import numpy as np

def get_temp_data():
    # Get raw 16 bit ADC values from on-chip temperature sensors
    ps_temp_raw = np.loadtxt("/sys/bus/iio/devices/iio:device0/in_temp0_ps_temp_raw",dtype="int32")
    pl_temp_raw = np.loadtxt("/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_raw",dtype="int32")
    return ps_temp_raw, pl_temp_raw

def calc_temp(raw):
    # Calculate temperature in Celsius from raw 16 bit ADC values
    # Ref: Equation 2-7, SYSMON User Guide UG580 (v1.10.1) Xilinx
    return raw*501.3743/2.**16-273.6777

def read_temps():
    ps_raw, pl_raw = get_temp_data()
    return calc_temp(ps_raw), calc_temp(pl_raw)
