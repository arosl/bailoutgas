import math

# Input values
RMV = 11.3  # Respiratory Minute Volume
volume = 26  # Cylinder volume in liters
pressure = 180  # Cylinder pressure in bar
start_depth = 6  # Start depth in meters
stop_depth = 54  # Stop depth in meters
swim_speed = 15  # Swim speed in meters per minute
dpv_speed = 45  # DPV speed in meters per minute

def round_up(value):
    return math.ceil(value)

def round_down_to_nearest_10(value):
    return math.floor(value / 10) * 10

def calculate_total_free_liters(volume, pressure):
    return volume * pressure

def calculate_pressure(depth):
    return (depth / 10) + 1

def calculate_bailout_gas(free_liters, RMV, pressure):
    return free_liters / (RMV * pressure)

def generate_table_data(RMV, volume, pressure, start_depth, stop_depth, swim_speed, dpv_speed, step=3):
    RMV = round_up(RMV)
    free_liters = calculate_total_free_liters(volume, pressure)
    table_data = []
    
    for depth in range(start_depth, stop_depth + 1, step):
        P = calculate_pressure(depth)
        bailout_gas = calculate_bailout_gas(free_liters, RMV, P)
        rounded_bailout_gas = round_down_to_nearest_10(bailout_gas)
        swim_distance = rounded_bailout_gas * swim_speed
        dpv_distance = rounded_bailout_gas * dpv_speed
        table_data.append((depth, rounded_bailout_gas, swim_distance, dpv_distance))
        
    return table_data

def generate_latex_table(data, RMV, volume, pressure, swim_speed, dpv_speed, table_type):
    latex_table = "\\begin{tabular}{|c|c|c|c|}\n\\hline\n"
    latex_table += f"\\multicolumn{{4}}{{|c|}}{{{table_type} RMV: {RMV} L/min, Cylinder: {volume} L, Pressure: {pressure} bar}} \\\\ \n\\hline\n"
    latex_table += f"Depth (m) & Bailout Gas (min) & Swim Distance {swim_speed} m/min & DPV Distance {dpv_speed} m/min \\\\ \n\\hline\n"
    for depth, bailout_gas, swim_distance, dpv_distance in data:
        latex_table += f"{depth}m & {bailout_gas} min & {swim_distance} m & {dpv_distance} m \\\\ \n\\hline\n"
    latex_table += "\\end{tabular}\n"
    return latex_table

# Generate table data for normal RMV
normal_RMV_data = generate_table_data(RMV, volume, pressure, start_depth, stop_depth, swim_speed, dpv_speed)

# Generate LaTeX table for normal RMV
normal_RMV_table = generate_latex_table(normal_RMV_data, round_up(RMV), volume, pressure, swim_speed, dpv_speed, "Normal")

# Generate table data for bailout RMV (1.5 times the normal RMV)
bailout_RMV = RMV * 1.5
bailout_RMV_data = generate_table_data(bailout_RMV, volume, pressure, start_depth, stop_depth, swim_speed, dpv_speed)

# Generate LaTeX table for bailout RMV
bailout_RMV_table = generate_latex_table(bailout_RMV_data, round_up(bailout_RMV), volume, pressure, swim_speed, dpv_speed, "Bailout")

# Output the LaTeX code
latex_code = (
    "\\documentclass{article}\n"
    "\\begin{document}\n\n"
    + normal_RMV_table
    + "\\vspace{12pt}\n\n"
    + bailout_RMV_table
    + "\\end{document}"
)

print(latex_code)


