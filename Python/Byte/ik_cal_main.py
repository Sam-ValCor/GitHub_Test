# IK calculation for byte
import constants as cnts
import numpy as np
import rot_trans_dh as rt_dh
import ik_leg as ik_l
# pose_d = [[dx], [dy], [dz], [roll], [pitch], [yaw]] # from the world respectively
# foot_ij (for each one) = [[foot_ijx], [foot_ijy], [foot_ijx], [1]] #coordinates
#
def ik_calc(pose_d, lf_foot, rf_foot,  lb_foot, rb_foot):
    # ndarray.flatten(order='C')
    d1 = cnts.D1
    d2 = cnts.D2
    z_home = cnts.DZ_HOME

    # Desired orientation (rad)
    roll = np.float_(pose_d[3])
    pitch = np.float_(pose_d[4])
    yaw = np.float_(pose_d[5])

    #r_roll = np.round((), cnts.ROUND)
    r_roll = rt_dh.x_rot(roll)
    r_pitch = rt_dh.y_rot(pitch)
    r_yaw = rt_dh.z_rot(yaw)

    #r_r = np.round(np.matmul(np.matmul(r_roll, r_pitch), r_yaw), cnts.ROUND)
    r_r = np.matmul(np.matmul(r_roll, r_pitch), r_yaw)

    # Desired translations (int?)
    dx = np.float_(pose_d[0])
    dy = np.float_(pose_d[1])
    dz = np.float_(pose_d[2])

    t_dz = dz + z_home
    tr_x = rt_dh.x_trans(dx)
    tr_y = rt_dh.y_trans(dy)
    tr_z = rt_dh.z_trans(t_dz)

    r_tr = np.matmul(np.matmul(tr_x, tr_y), tr_z)

    # The required transformation
    hw_r = np.matmul(r_r, r_tr)

    # reference system for the legs respect the world
    hr_lf = np.round(np.matmul(np.matmul(np.matmul(rt_dh.y_trans(d2 / cnts.HALF), rt_dh.x_trans(d1 / cnts.HALF))
                                         , rt_dh.z_rot(np.pi / cnts.HALF)), rt_dh.x_rot(np.pi / cnts.HALF)), cnts.ROUND)

    hr_rf = np.round(np.matmul(np.matmul(np.matmul(rt_dh.y_trans(-d2 / cnts.HALF), rt_dh.x_trans(d1 / cnts.HALF))
                                         , rt_dh.z_rot(-np.pi / cnts.HALF)), rt_dh.x_rot(np.pi / cnts.HALF)), cnts.ROUND)

    hr_lb = np.round(np.matmul(np.matmul(np.matmul(rt_dh.y_trans(d2 / cnts.HALF), rt_dh.x_trans(-d1 / cnts.HALF))
                                         , rt_dh.z_rot(np.pi / cnts.HALF)), rt_dh.x_rot(np.pi / cnts.HALF)), cnts.ROUND)

    hr_rb = np.round(np.matmul(np.matmul(np.matmul(rt_dh.y_trans(-d2 / cnts.HALF), rt_dh.x_trans(-d1 / cnts.HALF)),
                                         rt_dh.z_rot(-np.pi / cnts.HALF)), rt_dh.x_rot(np.pi / cnts.HALF)), cnts.ROUND)

    # Transforms systems for leg-shoulders
    hw_llf = np.matmul(hw_r, hr_lf)
    hw_lrf = np.matmul(hw_r, hr_rf)
    hw_llb = np.matmul(hw_r, hr_lb)
    hw_lrb = np.matmul(hw_r, hr_rb)

    # Feet positions (each one is respect its shoulder)
    # frontal left foot
    foot_llf = np.float_(np.matmul(np.linalg.pinv(hw_llf), lf_foot))
    # frontal right foot
    foot_lrf = np.float_(np.matmul(np.linalg.pinv(hw_lrf), rf_foot))
    # back left foot
    foot_llb = np.float_(np.matmul(np.linalg.pinv(hw_llb), lb_foot))
    # back right foot
    foot_lrb = np.float_(np.matmul(np.linalg.pinv(hw_lrb), rb_foot))


    # IK q result for each
    q_lf = ik_l.ikl(foot_llf, cnts.LEFT_FLAG)
    q_rf = ik_l.ikl(foot_lrf, cnts.RIGHT_FLAG)
    q_lb = ik_l.ikl(foot_llb, cnts.LEFT_FLAG)
    q_rb = ik_l.ikl(foot_lrb, cnts.RIGHT_FLAG)

    legs_q = np.array(np.float_([q_lf, q_rf, q_lb, q_rb]))
    legs_q_1d =  legs_q.flatten()
    #return d1, d2, z_home, roll, pitch, yaw, r_roll
    return legs_q_1d
"""
# For testing
pose_dtest = np.float_([[0], [0], [-10], [0], [0], [0]])
foot_lf = [[100], [70], [0], [1]]
foot_rf = [[100], [-70], [0], [1]]
foot_lb = [[-100], [70], [0], [1]]
foot_rb = [[-100], [-70], [0], [1]]
print(ik_calc(pose_dtest, foot_lf, foot_rf, foot_lb, foot_rb))
#print(4 * pose_dtest[3])
"""