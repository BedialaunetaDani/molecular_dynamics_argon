import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import imageio
import simulate as sim


def GIF_2D(gif_name, data_file, num_frames, box_dim):
    """
    Generates frames for the time evolution of particles in 2D
    and stores them in "tmp-plot" folder as "pair_int_2D{:05d}.png". 

    Parameters
    ----------
    gif_name : str
        Name of the GIF file to be generated
    data_file : str
        Name of the CSV file in which the data is stored
    num_frames : int
        Number of total frames generated (max is 99999)
    box_dim : float
        Dimensions of the simulation box

    Returns
    -------
    None
    """

    time, pos, vel = sim.load_data(data_file)
    num_tsteps = len(time) 
    save_frame = [int(i*(num_tsteps-1)/(num_frames-1)) for i in range(num_frames-1)] + [int(num_tsteps)-1] # timesteps in which to save frames

    if "tmp-plot" not in os.listdir():
        os.mkdir("tmp-plot")

    # Create figure and save initial position
    print("PLOTTING AND SAVING FRAMES... ({}/{})\r".format(1, num_frames), end="")
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    for f, t in enumerate(save_frame):
        print("PLOTTING AND SAVING FRAMES... ({}/{})\r".format(f+1, num_frames), end="")

        ax = plot_pos_2D(ax, pos[t], box_dim)
        ax.set_title("dimensionless t={:0.3f}".format(time[t]))
        fig.tight_layout()
        fig.savefig("tmp-plot/pair_int_2D{:05d}.png".format(f))
        plt.cla() # clear axis

    plt.clf()
    print("\n", end="")

    print("BUILDING GIF... ")
    with imageio.get_writer(gif_name, mode='I', duration=3/num_frames) as writer: # 30 fps
        for filename in ["tmp-plot/pair_int_2D{:05d}.png".format(f) for f in range(len(save_frame))]:
            image = imageio.imread(filename)
            writer.append_data(image)
    print("DONE")

    return

def GIF_3D(gif_name, data_file, num_frames, box_dim):
    """
    Generates frames for the time evolution of particles in 2D
    and stores them in "tmp-plot" folder as "pair_int_2D{:05d}.png". 

    Parameters
    ----------
    gif_name : str
        Name of the GIF file to be generated
    data_file : str
        Name of the CSV file in which the data is stored
    num_frames : int
        Number of total frames generated (max is 99999)
    box_dim : float
        Dimensions of the simulation box

    Returns
    -------
    None
    """

    time, pos, vel = sim.load_data(data_file)
    num_tsteps = len(time) 
    save_frame = [int(i*(num_tsteps-1)/(num_frames-1)) for i in range(num_frames-1)] + [int(num_tsteps)-1] # timesteps in which to save frames

    if "tmp-plot" not in os.listdir():
        os.mkdir("tmp-plot")

    # Create figure and save initial position
    print("PLOTTING AND SAVING FRAMES... ({}/{})\r".format(1, num_frames), end="")
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    for f, t in enumerate(save_frame):
        print("PLOTTING AND SAVING FRAMES... ({}/{})\r".format(f+1, num_frames), end="")

        ax = plot_pos_3D(ax, pos[t], box_dim)
        ax.set_title("dimensionless t={:0.3f}".format(time[t]))
        fig.tight_layout()
        fig.savefig("tmp-plot/pair_int_3D{:05d}.png".format(f))
        plt.cla() # clear axis

    plt.clf()
    print("\n", end="")

    print("BUILDING GIF... ")
    with imageio.get_writer(gif_name, mode='I', duration=3/num_frames) as writer: # 30 fps
        for filename in ["tmp-plot/pair_int_3D{:05d}.png".format(f) for f in range(len(save_frame))]:
            image = imageio.imread(filename)
            writer.append_data(image)
    print("DONE")

    return

def plot_pos_2D(ax, pos, L, central_box=True, relative_pos=False):
    """
    Plots positions of particles (and box) in 2D

    Parameters
    ----------
    ax : matplotlib axis
        Axis in which to plot the particles
    pos : np.ndarray(N,2)
        Positions of the atoms in Cartesian space
    L : float
        Dimensions of the simulation box
    central_box : bool
        If True, plots square box
    relative_pos : bool
        If True, plots line between closest pairs of all particles

    Returns
    -------
    ax : matplotlib axis
        Axis in which particles have been plotted
    """

    # plot central box and its eight neighbours
    for i in range(pos.shape[0]): # plot for all particles
        if central_box:
            ax.plot(pos[i,0]  , pos[i,1]  , ".", color="black") # central box
        else: 
            ax.plot(pos[i,0]  , pos[i,1]  , "r.") # central box
        ax.plot(pos[i,0]+L, pos[i,1]  , "r.")
        ax.plot(pos[i,0]  , pos[i,1]+L, "r.")
        ax.plot(pos[i,0]+L, pos[i,1]+L, "r.")
        ax.plot(pos[i,0]-L, pos[i,1]  , "r.")
        ax.plot(pos[i,0]  , pos[i,1]-L, "r.")
        ax.plot(pos[i,0]-L, pos[i,1]-L, "r.")
        ax.plot(pos[i,0]-L, pos[i,1]+L, "r.")
        ax.plot(pos[i,0]+L, pos[i,1]-L, "r.")

    if central_box: # plot square for central box
        ax.plot([0,0,L,L,0],[0,L,L,0,0], "g-") 

    if relative_pos:
        rel_pos, rel_dist = sim.atomic_distances(pos, L)
        for i in range(pos.shape[0]):
            for j in range(pos.shape[0]):
                if i == j: continue
                ax.plot([pos[i,0], pos[i,0]+rel_pos[j,i,0]], [pos[i,1], pos[i,1]+rel_pos[j,i,1]], "b--")

    ax.set_xlim(-L/2, 3*L/2)
    ax.set_ylim(-L/2, 3*L/2)

    ax.set_xlabel("dimensionless x coordinate")
    ax.set_ylabel("dimensionless y coordinate")

    # set axis' ticks inside figure
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    return ax

def plot_pos_3D(ax, pos, L, central_box=True, relative_pos=False, outer_boxes=False):
    """
    Plots positions of particles (and box) in 3D

    Parameters
    ----------
    ax : matplotlib axis
        Axis in which to plot the particles
    pos : np.ndarray(N,3)
        Positions of the atoms in Cartesian space
    L : float
        Dimensions of the simulation box
    central_box : bool
        If True, plots square box
    relative_pos : bool
        If True, plots line between closest pairs of all particles

    Returns
    -------
    ax : matplotlib axis
        Axis in which particles have been plotted
    """
    
    # plot central box and its eight neighbours
    for i in range(pos.shape[0]): # plot for all particles
        if central_box:
            ax.plot(pos[i,0]  , pos[i,1]  , ".", color="black") # central box
        else: 
            ax.plot(pos[i,0]  , pos[i,1]  , pos[i,2]  , "r.") # central box
        if outer_boxes:
            ax.plot(pos[i,0]+L, pos[i,1]  , pos[i,2]  , "r.") # permutations + _ _
            ax.plot(pos[i,0]  , pos[i,1]+L, pos[i,2]  , "r.")
            ax.plot(pos[i,0]  , pos[i,1]  , pos[i,2]+L, "r.")

            ax.plot(pos[i,0]+L, pos[i,1]+L, pos[i,2]  , "r.") # permutations + + _
            ax.plot(pos[i,0]  , pos[i,1]+L, pos[i,2]+L, "r.")
            ax.plot(pos[i,0]+L, pos[i,1]  , pos[i,2]+L, "r.")

            ax.plot(pos[i,0]+L, pos[i,1]+L, pos[i,2]+L, "r.") # permutations + + + 

            ax.plot(pos[i,0]-L, pos[i,1]  , pos[i,2]  , "r.") # permutations - _ _
            ax.plot(pos[i,0]  , pos[i,1]-L, pos[i,2]  , "r.")
            ax.plot(pos[i,0]  , pos[i,1]  , pos[i,2]-L, "r.")

            ax.plot(pos[i,0]-L, pos[i,1]-L, pos[i,2]  , "r.") # permutations - - _
            ax.plot(pos[i,0]-L, pos[i,1]  , pos[i,2]-L, "r.")
            ax.plot(pos[i,0]  , pos[i,1]-L, pos[i,2]-L, "r.")

            ax.plot(pos[i,0]-L, pos[i,1]-L, pos[i,2]-L, "r.") # permutatinos - - - 
                
            ax.plot(pos[i,0]-L, pos[i,1]+L, pos[i,2]  , "r.") # permutations - + _
            ax.plot(pos[i,0]+L, pos[i,1]-L, pos[i,2]  , "r.")
            ax.plot(pos[i,0]-L, pos[i,1]  , pos[i,2]+L, "r.")
            ax.plot(pos[i,0]+L, pos[i,1]  , pos[i,2]-L, "r.")
            ax.plot(pos[i,0]  , pos[i,1]+L, pos[i,2]-L, "r.")
            ax.plot(pos[i,0]  , pos[i,1]-L, pos[i,2]+L, "r.")

            ax.plot(pos[i,0]+L, pos[i,1]-L, pos[i,2]-L, "r.") # permutations + - -
            ax.plot(pos[i,0]-L, pos[i,1]+L, pos[i,2]-L, "r.")
            ax.plot(pos[i,0]-L, pos[i,1]-L, pos[i,2]+L, "r.")

            ax.plot(pos[i,0]-L, pos[i,1]+L, pos[i,2]+L, "r.") # permutations + + -
            ax.plot(pos[i,0]+L, pos[i,1]-L, pos[i,2]+L, "r.")
            ax.plot(pos[i,0]+L, pos[i,1]+L, pos[i,2]-L, "r.")

            ax.set_xlim(-L, 2*L)
            ax.set_ylim(-L, 2*L)
            ax.set_zlim(-L, 2*L)

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_zlim(0, L)
    if central_box: # plot square for central box
        ax.plot([0,L,L,0,0],[0,0,L,L,0],[0,0,0,0,0], "g-")
        ax.plot([0,0,L,L],[0,0,0,0],[0,L,L,0],"g-")
        ax.plot([0,0,0],[0,L,L],[L,L,0],"g-")
        ax.plot([0,L,L],[L,L,L],[L,L,0],"g-") 
        ax.plot([L,L],[0,L],[L,L],"g-")  

    if relative_pos:
        rel_pos, rel_dist = sim.atomic_distances(pos, L)
        for i in range(pos.shape[0]):
            for j in range(pos.shape[0]):
                    if i == j: continue
                    ax.plot([pos[i,0], pos[i,0]+rel_pos[j,i,0]], [pos[i,1], pos[i,1]+rel_pos[j,i,1]],[pos[i,2],pos[i,2]+rel_pos[j,i,2]], "b--")

    
    ax.set_xlabel("$x/\sigma$")
    ax.set_ylabel("$y/\sigma$")
    ax.set_zlabel("($z/\sigma$)")

    # set axis' ticks inside figure
    ax.tick_params(axis="x",direction="in")
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="z",direction="in")
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.zaxis.set_ticks_position('both')

    return ax


def E_vs_t(data_file, box_dim, kinetic_potential=False):
    """
    Plots energy as a function of time

    Parameters
    ----------
    data_file : str
        Name of the CSV file in which the data is stored
    box_dim : float
        Dimensions of the simulation box
    kinetic_potential : bool
        If True, plots also kinetic and potential energies

    Returns
    -------
    None
    """

    time, pos, vel = sim.load_data(data_file)

    E_total = []
    E_kinetic = []
    E_potential = []
    for k, t in enumerate(time):
        E_kinetic += [sim.kinetic_energy(vel[k])] 
        E_potential += [sim.potential_energy(pos[k], box_dim)]
        E_total += [E_kinetic[-1] + E_potential[-1]] 

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(time, E_total, "-", label="total E", color="black")
    if kinetic_potential:
        ax.plot(time, E_kinetic, "-", label="kinetic E", color="red")
        ax.plot(time, E_potential, "-", label="potential E", color="blue")
        ax.legend(loc="best")

    ax.set_xlim(0, np.max(time))

    ax.set_xlabel("dimensionless time")
    ax.set_ylabel("dimensionless energy")

    # set axis' ticks inside figure
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    plt.show()
    plt.clf()

    return


def E_conservation(data_file, box_dim):
    """
    Plots (E - average(E))/E as a function of time (where E = energy)

    Parameters
    ----------
    data_file : str
        Name of the CSV file in which the data is stored
    box_dim : float
        Dimensions of the simulation box

    Returns
    -------
    None
    """

    time, pos, vel = sim.load_data(data_file)

    E_total = []
    for k, t in enumerate(time):
        E_total += [sim.total_energy(pos[k], vel[k], box_dim)] 
    E_total = np.array(E_total)

    rel_AE = (E_total - np.average(E_total))/E_total

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(time, rel_AE, "-", color="black")

    ax.set_xlim(0, np.max(time))

    ax.set_xlabel("dimensionless time")
    ax.set_ylabel("relative energy difference")

    # set axis' ticks inside figure
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    plt.show()
    plt.clf()

    return


def reldist_vs_t(data_file, i, j, box_dim):
    """
    Plots relative distance between particles `i` and `j` as a function of time

    Parameters
    ----------
    data_file : str
        Name of the CSV file in which the data is stored
    i : int
        Number of the particle that constitutes the pair
    j : int
        Number of the particle that constitutes the pair
    box_dim : float
        Dimensions of the simulation box

    Returns
    -------
    None
    """

    time, pos, vel = sim.load_data(data_file)

    rel_dist = []
    for k, t in enumerate(time):
        rel_dist += [np.linalg.norm(pos[k, i, :] - pos[k, j, :])] 

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(time, rel_dist, "-", color="black")

    ax.set_xlabel("dimensionless time")
    ax.set_ylabel("relative_distance(i={},j={})/$\sigma$".format(i,j))

    # set axis' ticks inside figure
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    plt.show()
    plt.clf()

    return