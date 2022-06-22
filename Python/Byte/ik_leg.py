# Inverse Kinematic for legs
import numpy as np

# foot = [x_foot, y_foot, z_foot] foot coordinates with respect to the SCO from (side)
# side = (1||0) (left||right)


def ikl(foot, side):
    if side == 1:
        direction_flag = 1
    elif side == 0:
        direction_flag = -1
    else:
        error_flag = 'Flag Error'
    # shoulder distance
    dsh = 45
    l1 = 100
    l2 = 100

    # Ik frontal left leg
    dist = np.sqrt((np.float_(foot[0]) ** 2) + (np.float_(foot[1]) ** 2))
    h = np.sqrt((dist ** 2) - (dsh ** 2))

    alpha = np.arctan2(h, dsh)
    beta = np.arctan2(np.float_(foot[1]), np.float_(foot[0]))
    q1 = alpha + beta

    r = np.sqrt((h ** 2) + (np.float_(foot[2]) ** 2))

    p = (((r ** 2) - (l1 ** 2)) - (l2 ** 2) ) / (2 * l1 * l2)
    q3 = np.arctan2(direction_flag * np.sqrt(1 - (p ** 2)), p)

    gamma = np.arctan2(-np.float_(foot[2]), h)
    sigma = np.arctan2((l2 * np.sin(q3)), (l1 + (l2 * np.cos(q3))))
    q2 = gamma + sigma
    q = [[q1], [q2], [q3]]
    return q
""""
foot_lf = [[-40.09383547], [-96.35519486], [-25.02596527], [1. ]]
foot_rf = [[71.2006896], [-32.44902731], [54.16582855], [1. ]]
foot_lb = [[51.2006896 ], [12.44902731], [34.16582855], [1. ]]
foot_rb = [[-20.09383547], [76.35519486], [-5.02596527], [ 1.]]

print(ikl(foot_rb,0))
#print(foot_lf)
"""
