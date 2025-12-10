import random as rnd
import numpy
from numpy import random
import math
import time
from deap import base, creator, tools
from rlv_empirical_data import database

num_particles = 15
max_iter = 100
runs = 1


def OptimizerwithLevy(Max_iter, SearchAgents_no, dim, lb, ub, objf, Elite_agents, Inferior_agents):

    # initialize of Sentinel, Elite, Inferior

    Sentinel_signal = 0

    Global_pos = numpy.zeros((1 ,dim))
    Global_score = numpy.ones(1 ) *math.inf

    Elite_pos = numpy.zeros((7 ,5 ,dim))
    Elite_score = numpy.ones((7 ,5) ) *math.inf

    Inferior_pos = numpy.zeros((8 ,5 ,dim))
    Inferior_score = numpy.ones((8 ,5) ) *math.inf


    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim

    # Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    Convergence_curve = numpy.zeros(Max_iter)
    fitness = numpy.ones((15) ) *math.inf

    # Loop counter
    print('optimizer is optimizing  "' + objf + '"')

    for i in range(0, SearchAgents_no):
        for j in range(dim):
            Positions[i, j] =(ub[j] - lb[j]) * random.random() + lb[j]

        # Calculate objective function for each search agent
        fitness[i] = eval(objf)(Positions[i, :])

    # Sorting
    Positions = sorted(Positions, key=eval(objf))
    fitness.sort()

    Global_score = fitness[0]
    Global_pos = Positions[0].copy()

    for i in range(0, len(Elite_score)):
        Elite_score[i, 0] = fitness[i]
        Elite_pos[i, 0] = Positions[i].copy()

    for i in range(0, len(Inferior_score)):
        Inferior_score[i, 0] = fitness[7 + 1]
        Inferior_pos[i, 0] = Positions[7 + 1].copy()

    for it in range(0, Max_iter):

        a = 1 * (1 - it / Max_iter)

        if it == 0:
            lo = 1
        else:
            lo = 0

            # Population Update
        for comm in range(lo, 5):

            for i in range(0, len(Elite_score)):

                for j in range(dim):
                    # E position update
                    z_value = 0.1
                    m_value = 0.1
                    c_value = 0.1
                    step = levy_flight(z_value, m_value, c_value)[0]
                    Elite_pos[i, comm, j] = Positions[i][j] - rnd.random() * step
                Elite_score[i, comm] = eval(objf)(Elite_pos[i, comm, :])

            for i in range(0, len(Inferior_score)):
                # Inferior position update

                for j in range(dim):

                    if rnd.random() > 0.5:
                        Inferior_pos[i, comm, j] = (rnd.random() * (ub[j] - lb[j])) + lb[j]
                    else:

                        u = rnd.randint(0, 14)
                        Inferior_pos[i, comm, j] = Inferior_pos[i, comm, j] + a * rnd.random() * (
                                    Inferior_pos[i, comm, j] - Inferior_pos[i, comm, j])

                Inferior_score[i, comm] = eval(objf)(Inferior_pos[i, comm, :])

                if Inferior_score[i, comm] < Global_score:

                    # Signal for regrouping
                    Sentinel_signal = 1
                    # Perform regrouping

                    # get min for every agent and sent that value to position and fitness

                    Int_score = numpy.concatenate((Elite_score, Inferior_score), axis=0)
                    Int_pos = numpy.concatenate((Elite_pos, Inferior_pos), axis=0)
                    Bets = Int_score.min(axis=1)

                    for i in range(0, SearchAgents_no):
                        array4 = list(Int_score[i])
                        t = array4.index(Bets[i])
                        fitness[i] = Int_score[i, t]
                        Positions[i] = Int_pos[i, t, :]

                    # Sorting
                    Positions = sorted(Positions, key=eval(objf))  # Personal Bests
                    fitness.sort()

                    if fitness[0] < Global_score:
                        Global_score = fitness[0]
                        Global_pos = Positions[0].copy()

                    for i in range(0, len(Elite_score)):
                        Elite_score[i, 0] = fitness[i]
                        Elite_pos[i, 0] = Positions[i].copy()

                    for i in range(0, len(Inferior_score)):
                        Inferior_score[i, 0] = fitness[7 + i]
                        Inferior_pos[i, 0] = Positions[7 + i].copy()

        # Position Update after 5 iter of Elite
        for i in range(0, len(Elite_score)):

            for j in range(dim):
                c1 = 1.49445  # cognitive
                c2 = 1.49445  # social
                r1 = rnd.random()  # randomizations
                r2 = rnd.random()
                # E position update toward global best
                Elite_pos[i, comm, j] = (r1 * (Positions[i][j] - Elite_pos[i][4][j])) + (
                            r2 * (Global_pos[j] - Elite_pos[i][4][j]))
            Elite_score[i, comm] = eval(objf)(Elite_pos[i, comm, :])

        # Sorting
        Int_score = numpy.concatenate((Elite_score, Inferior_score), axis=0)
        Int_pos = numpy.concatenate((Elite_pos, Inferior_pos), axis=0)
        Bets = Int_score.min(axis=1)

        for i in range(0, SearchAgents_no):
            array4 = list(Int_score[i])
            t = array4.index(Bets[i])
            fitness[i] = Int_score[i, t]
            Positions[i] = Int_pos[i, t, :]

        Positions = sorted(Positions, key=eval(objf))
        fitness.sort()

        if fitness[0] < Global_score:
            Global_score = fitness[0]
            Global_pos = Positions[0].copy()

        for i in range(0, len(Elite_score)):
            Elite_score[i, 0] = fitness[i]
            Elite_pos[i, 0] = Positions[i].copy()

        for i in range(0, len(Inferior_score)):
            Inferior_score[i, 0] = fitness[7 + i]
            Inferior_pos[i, 0] = Positions[7 + i].copy()

        Convergence_curve[it] = Global_score

        if it % 1 == 0:
            print(["At iteration " + str(it * 5) + " the best fitness is " + str(Global_score)])

    return Global_score, Convergence_curve
