import numpy as np
import array
import math
import random
import numpy as np
from deap import base, creator, tools, algorithms
from rlv_empirical_data import database

class GWO:
    def __init__(self, objective_function, problem_size, search_space, num_wolves=5, num_iterations=100):
        self.objective_function = objective_function
        self.problem_size = problem_size
        self.search_space = search_space
        self.num_wolves = num_wolves
        self.num_iterations = num_iterations

    def initialize_wolves(self):
        return np.random.uniform(self.search_space[:, 0], self.search_space[:, 1], size=(self.num_wolves, self.problem_size))

    def update_alpha_beta_delta(self, wolves, fitness_values):
        sorted_indices = np.argsort(fitness_values)
        alpha, beta, delta = wolves[sorted_indices[:3]]
        return alpha, beta, delta

    def run(self):
        wolves = self.initialize_wolves()
        fitness_values = np.array([self.objective_function(wolf) for wolf in wolves])

        alpha, beta, delta = self.update_alpha_beta_delta(wolves, fitness_values)

        for iteration in range(self.num_iterations):
            a = 2 - 2 * iteration / self.num_iterations  # linearly decreases from 2 to 0

            for i in range(self.num_wolves):
                A1 = 2 * a * np.random.rand(self.problem_size) - a
                C1 = 2 * np.random.rand(self.problem_size)
                D_alpha = np.abs(C1 * alpha - wolves[i])
                X1 = alpha - A1 * D_alpha

                A2 = 2 * a * np.random.rand(self.problem_size) - a
                C2 = 2 * np.random.rand(self.problem_size)
                D_beta = np.abs(C2 * beta - wolves[i])
                X2 = beta - A2 * D_beta

                A3 = 2 * a * np.random.rand(self.problem_size) - a
                C3 = 2 * np.random.rand(self.problem_size)
                D_delta = np.abs(C3 * delta - wolves[i])
                X3 = delta - A3 * D_delta

                wolves[i] = (X1 + X2 + X3) / 3

            fitness_values = np.array([self.objective_function(wolf) for wolf in wolves])
            alpha, beta, delta = self.update_alpha_beta_delta(wolves, fitness_values)

        return alpha

# Your existing code

class optimizer:
    # create instance
    atm = database()

    # bounds
    alpha_min, alpha_max = 0, 40

    # set up configuration
    num_gen = 30  # number of generations
    num_ind = 100  # number of individuals in the initial population
    prob_cx = 0.6  # probability of cross-over
    prob_mt = 0.01  # probability of mutation
    eta = 5.0  # eta parameter for mate and mutate functions
    num_hof = 10  # hall of frame size


    # Modified solve method using GWO
    def solve(self):
        toolbox = self.toolbox
        num_gen = self.num_gen
        num_hof = self.num_hof
        search_space = np.array([[self.alpha_min, self.alpha_max]])
        problem_size = 1

        # GWO objective function
        def gwo_objective_function(alpha):
            # Get the values for minimize
            alpha, L, D, Qp_kpa, q = self.calculate(alpha)
            # Return a single objective value (you can customize this based on your needs)
            return Qp_kpa + q

        # GWO optimization
        gwo = GWO(gwo_objective_function, problem_size, search_space)
        optimized_alpha = gwo.run()

        # Create an individual with the optimized alpha
        ind = creator.Individual([optimized_alpha])
        ind.fitness.values = self.eval(ind)

        # Create a Hall of Fame to store the best individual
        hof = tools.HallOfFame(num_hof)
        hof.update([ind])

        return hof

# Rest of your code remains unchanged

if __name__ == "__main__":
    # Create an instance of the optimizer
    opt = optimizer()

    # Example: Set the values for y, ctrl_data, orb_data, tem_data, aero_data
    y = [1, 2, 3, 4, 5, 6]
    ctrl_data = [[1, 2, 3]]
    orb_data = [1, 2, 3]
    tem_data = [1, 2, 3]
    aero_data = [1, 2]

    # Get the optimized control values using GWO
    alpha, L, D = opt.get_values(y, ctrl_data, orb_data, tem_data, aero_data)


