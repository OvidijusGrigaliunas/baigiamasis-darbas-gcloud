import decimal


def get_accelerometer_speed(accel_data, time_step):
    g = decimal.Decimal(9.8)
    print(g)
    time_step = round(decimal.Decimal(time_step), 2)
    accel_speed = {"x": [], "y": [], "z": []}
    accel_speed["x"].append(accel_data[0]["accel_x"] * time_step)
    accel_speed["y"].append(accel_data[0]["accel_y"] * time_step)
    accel_speed["z"].append(accel_data[0]["accel_z"] * time_step)
    for i in range(1, len(accel_data) - 1):
        accel_speed["x"].append(accel_speed["x"][-1] + accel_data[i]["accel_x"] * time_step)
        accel_speed["y"].append(accel_speed["y"][-1] + (accel_data[i]["accel_y"] - g) * time_step)
        accel_speed["z"].append(accel_speed["z"][-1] + accel_data[i]["accel_z"] * time_step)
    return accel_speed
