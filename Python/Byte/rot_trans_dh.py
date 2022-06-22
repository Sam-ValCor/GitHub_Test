# Those are the functions for the rotations and translations based on the Denavit Hartenberg (DH)
import numpy as np
import constants as cnts
# Rotations:


# DH: x rotation matrix
def x_rot(theta_rx):
    rx = [[1, 0, 0, 0],
          [0, np.cos(theta_rx), -np.sin(theta_rx), 0],
          [0, np.sin(theta_rx), np.cos(theta_rx), 0],
          [0, 0, 0, 1]]
    return rx


# DH: y rotation matrix
def y_rot(theta_ry):
    ry = [[np.cos(theta_ry), 0, np.sin(theta_ry), 0],
          [0, 1, 0, 0],
          [-np.sin(theta_ry), 0, np.cos(theta_ry), 0],
          [0, 0, 0, 1]]
    return ry


# DH: z rotation matrix
def z_rot(theta_rz):
    rz = [[np.cos(theta_rz), -np.sin(theta_rz), 0, 0],
          [np.sin(theta_rz), np.cos(theta_rz), 0, 0],
          [0, 0, 1, 0],
          [0, 0, 0, 1]]
    return rz

# Translations


# DH: x translation matrix
def x_trans(x_dist):
    tx = [[1, 0, 0, x_dist],
          [0, 1, 0, 0],
          [0, 0, 1, 0],
          [0, 0, 0, 1]]
    return tx

# DH: y translation matrix
def y_trans(y_dist):
    ty = [[1, 0, 0, 0,],
          [0, 1, 0, y_dist],
          [0, 0, 1, 0],
          [0, 0, 0, 1]]
    return ty

# DH: z translation matrix
def z_trans(z_dist):
    tz = [[1, 0, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 1, z_dist],
          [0, 0, 0, 1]]
    return tz

# print(y_trans(90))