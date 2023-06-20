import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def isInVC(pos1, vel1, r1, pos2, vel2, r2, T=1000):
    '''
    Check if two agents are in each other's velocity triangle
    '''
    r = r2 + r1
    pos = pos2 - pos1
    vel = vel1 - vel2
    dist = pos - r
    if vel[0] == 0:
        m = 1000000
    else:
        m = vel[1]/vel[0]
    g = pos[0]
    f = pos[1]
    a = 1 + m**2
    b = -2*g - 2*m*f
    c = g**2 + f**2 - r**2
    delta = b**2 - 4*a*c
    if np.linalg.norm(vel) > np.linalg.norm(dist)/T:
        if delta < 0:
            return False
        return True
    return False


def isInMultiVC(dict, T=1000):
    '''
    checks if first agent is in any of the other obstacles' velocity triangles
    '''
    for i in range(len(dict)):
        if isInVC(dict[0]['pos'], dict[0]['vel'], dict[0]['r'], dict[i]['pos'], dict[i]['vel'], dict[i]['r'], T):
            return True
    return False


if __name__ == '__main__':
    pos1 = np.array([5, 6])
    vel1 = np.array([-1, 0])
    r1 = 0.25
    pos2 = np.array([1, 0])
    vel2 = np.array([1.5, 1])
    r2 = 1
    pos3 = np.array([0, 3])
    vel3 = np.array([0, 1.7])
    r3 = 1

    ################# test single obstacle V0 ###################
    print(isInVC(pos1, vel1, r1, pos2, vel2, r2))
    fig, ax = plt.subplots(1, 3)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(-2, 2)
    ax[0].add_patch(patches.Circle(pos1, r1, fill=False))
    ax[0].add_patch(patches.Circle(pos2, r2, fill=False))
    ax[0].arrow(pos1[0], pos1[1], vel1[0], vel1[1], width=0.05)
    ax[0].arrow(pos2[0], pos2[1], vel2[0], vel2[1], width=0.05)

    ax[1].add_patch(patches.Circle(pos2 - pos1, r1+r2, fill=False))
    ax[1].arrow(0, 0, vel1[0]-vel2[0], vel1[1]-vel2[1], width=0.05)

    # plt.show()

    ################# test multiple obstacle V0 ###################

    print(isInMultiVC([{'pos': pos1, 'vel': vel1, 'r': r1}, {
          'pos': pos2, 'vel': vel2, 'r': r2}, {'pos': pos3, 'vel': vel3, 'r': r3}]))
    # fig, ax = plt.subplots(1, 1)

    ax[2].add_patch(patches.Circle(pos1, r1, fill=False))
    ax[2].add_patch(patches.Circle(pos2, r2, fill=False))
    ax[2].add_patch(patches.Circle(pos3, r3, fill=False))
    ax[2].arrow(pos1[0], pos1[1], vel1[0], vel1[1], width=0.05)
    ax[2].arrow(pos2[0], pos2[1], vel2[0], vel2[1], width=0.05)
    ax[2].arrow(pos3[0], pos3[1], vel3[0], vel3[1], width=0.05)

    plt.show()
