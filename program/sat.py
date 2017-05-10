#! /usr/bin/python2.7

"""
Logic for producing uniquely satisfiable instances using Cryptominisat package
"""

import random
from pycryptosat import Solver
from handlers.filehandler import FileHandler
from handlers.processhandler import ProcessHandler
import operator
from handlers.plothandler import PlotHandler
import timeit
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Sat(object):
    def generate_systems(self, **kwargs):
        """
        Generate instances by searching through combinations of n and m
        Save these results as files
        :param kwargs: 
        :return: Results of time taken to search
        """
        # init
        fh = FileHandler()
        ph = ProcessHandler()
        results = [['key', 'n', 'm', 'tries', 'vTime']]
        systems = []

        # params
        step = kwargs.get("step", 1)
        max_tries = kwargs.get("max_tries", 10)
        min_m = kwargs.get("min_m", 4)
        n = kwargs.get("n", 4)
        max_n = kwargs.get("max_n", 100)
        max_m = kwargs.get("max_m", 100)
        save_dir = "./../assets/sat_run/{0}-n-{1}_{2}-m-{3}_step-{4}".format(n, max_n, min_m, max_m, step)
        save_system_location = save_dir + "/systems"
        save_results_location = save_dir + "/results"
        save_systems = kwargs.get("save_systems", False)
        save_results = kwargs.get("save_results", False)
        bound = kwargs.get("bound", False)
        limit = kwargs.get("limit", False)
        threshold_search = kwargs.get("threshold_search", False)

        # Prep folder
        fh.makedir(save_dir)

        while n < max_n:
            m = min_m
            n += step
            tries = 0
            found = 0
            smallest_m_found = False
            result = []
            system = []

            while m < max_m:
                # Handle iterations
                m += step
                if m < n:
                    m = n
                elif threshold_search and m == n and limit:
                    m = (2 * n) - (0.5 * limit )
                if 4 < m / n or (found and found == limit):
                    break

                key = `n` + ':' + `m`
                validation_start = timeit.default_timer()
                generate_time, eq = ph.run_function_timed(self.generate_rand_unique_system, (n, m), return_args=True)

                # Found unique system
                if eq:
                    # Update params
                    tries = 0
                    found += 1

                    # Update the lower bound
                    if bound and not smallest_m_found:
                        min_m = m - step
                        smallest_m_found = True

                    # Record times
                    print "Found: ", n, m
                    validation_time = timeit.default_timer() - validation_start
                    results.append([key, n, m, tries, validation_time, generate_time])
                    result.append([key, n, m, tries, validation_time, generate_time])

                    # Save data
                    if save_systems:
                        systems.append([key, n, m, eq])
                        system.append([key, n, m, eq])
                        self.save_system(n, m, eq)

                # Failed to find and tried too many times
                elif max_tries == tries:
                    print "Skipping: ", n, m
                    tries = 0
                    results.append([key, n, m, tries, -1, -1])
                    result.append([key, n, m, tries, -1, -1])
                    continue

                # Failed to find, try again
                else:
                    # print 'Couldnt find for ' + `m` + ' Misses ' + `tries`
                    # print n, "-", m, "- missing"
                    tries += 1
                    m -= step

            if save_systems:
                print "Saving systems..."
                save_systems_time = ph.run_function_timed(fh.update_file, (save_system_location, system))
                print "Time taken: ", save_systems_time
            if save_results:
                print "Saving results..."
                save_results_time = ph.run_function_timed(fh.update_file, (save_results_location, result))
                print "Time taken: ", save_results_time
        return results

    def generate_rand_system(self, n, m):
        """
        Generates a random homogenous system
        Try n times to pull a unique random set of three variables from the pool.
        :param n: 
        :param m: 
        :return: A 2d array of systems
        """
        pool = range(1, n + 1)
        system = []
        tries = 3
        i = 0

        while i < m:
            clause = random.sample(pool, 3)
            clause.sort()

            if tries == 0:
                return False
            elif clause in system:
                tries -= 1
            else:
                system.append(clause)
                i += 1

        return system

    def generate_rand_unique_system(self, n, m):
        """
        Generates a random homogenous system that is uniquely satisfiable
        First generates a system and then checks if uniquely satisfiable
        Try n times to generate system
        :param n: 
        :param m: 
        :return: A 2d array of systems
        """
        tries = 3

        while True:
            system = self.generate_rand_system(n, m)

            if tries == 0:
                return False
            elif system:
                if self.is_system_uniquely_satisfiable(system, n):
                    return system
                else:
                    tries -= 1
            else:
                tries -= 1

    def generate_systems_fix_n(self):
        """
        Generate a system forcing n to stay static and allow m to vary
        Give up after n tries
        :return: Null
        """
        sat = Sat()
        n = 50
        max_m = 1000
        tries = 10

        for m in range(555, max_m):
            eq = sat.generate_rand_unique_system(n, m)
            if eq:
                tries = 10
                print 'Found: ' + `m`
                # print eq
            else:
                print 'Couldnt find for ' + `m`
                tries -= 1
                print tries
                if tries == 0:
                    print 'Sequence of misses'
                    return

    def generate_systems_fix_n_force(self):
        """
        Generate a system forcing n to stay static and allowing m to vary
        Don't give up, that is, keep trying until a system is found
        :return: Null
        """
        sat = Sat()
        n = 50
        m = 555
        max_m = 1000
        misses = 0
        while m < max_m:
            m += 1
            eq = sat.generate_rand_unique_system(n, m)
            if eq:
                misses = 0
                print "Found: ", m
                # print eq
            else:
                misses += 1
                m -= 1
                print 'Couldnt find for ' + `m` + ' Misses ' + `misses`

    def is_system_uniquely_satisfiable(self, system, n):
        """
        Tests unique satisfiable by banning all zero solution
        :param system: 
        :param n: 
        :return: 
        """
        # Prep solver
        solver = Solver()
        for clause in system:
            solver.add_xor_clause(clause, False)

        # Ban all zero
        solver.add_clause(range(1, n + 1))

        sat, sol = solver.solve()

        return not sat

    def find_equations(self, n, m):
        """
        Find unique systems by searching combinations, rather than picking at random.
        That is, find systems of equations "systematically"
        :param n: 
        :param m: 
        :return: 
        """
        clauses = self.find_clauses(n)
        systems = self.find_systems(clauses, n, m)
        return systems

    def find_clauses(self, n):
        """
        Helper that finds all unique combinations of clauses
        :param n: 
        :return: A 2d array of all combinations of 
        """
        pool = range(1, n + 1)
        clauses = []
        for x in pool:
            for y in pool:
                for z in pool:
                    if x == y or x == z or y == z:
                        continue

                    clause = [x, y, z]
                    clause.sort()

                    if clause not in clauses:
                        clauses.append(clause)
        return clauses

    def find_systems(self, clauses, system, n, m, depth):
        """
        Find all systems using recursive method
        :param clauses: 
        :param system: 
        :param n: 
        :param m: 
        :param depth: 
        :return: A system of equations
        """

        # Base Case
        # If length of system = m, then we have long enough system
        if len(system) == m:
            for i in range(0, len(system) - 1):
                if system[i] > system[i + 1]:
                    return False
            # print system
            sat = Sat()
            if sat.is_system_uniquely_satisfiable(system, n):
                return True
            else:
                return False

        # Recursive Case
        # Else, system is not long enough, we need to append to system
        else:
            systems = []

            # For each clause not in the system, add to system
            for clause in clauses:

                # Remove this clause from the pool
                tail = list(clauses)
                tail.remove(clause)

                # Add this clause to the current system and validate
                system_temp = list(system)
                system_temp.append(clause)
                unique_system = self.find_systems(tail, system_temp, n, m, depth + 1)

                # Check if it is a uniquely satisfiable instance or is it a return call
                if isinstance(unique_system, bool) and unique_system:
                    systems.append(system_temp)
                elif unique_system:
                    systems = systems + unique_system

            return systems

    def run_solver(self, **kwargs):
        """
        Run Traces through systems and record times
        Looking for systems that are faster with gauss off => K-local consistent
        :param kwargs: 
        :return: Null
        """
        fh = FileHandler()
        ph = ProcessHandler()
        results = []
        skip = kwargs.get("outstanding", False)
        completed = []
        if fh.read_from_file("./../assets/systems_run/run"):
            for result in fh.read_from_file("./../assets/systems_run/run"):
                completed.append(result[0])

        for filename in ph.run_command('ls -v ./../assets/systems/'):
            # Init
            path = './../assets/systems/' + filename
            system = fh.read_from_file(path)
            split = filename.split("_")
            n = split[0]
            m = split[1]

            # Skip completed systems
            key = "{0}:{1}".format(n, m)
            if skip and key in completed:
                continue
            print key

            # Create cryptominisat system
            input = self.prepare_cryptominisat_system(n, m, system)
            fh.write_to_file_simple("./../assets/systems_run/temp_storage", input)

            # run gauss off
            cmd = "./../assets/sat/cryptominisat/build/cryptominisat5 --verb=0 ./../assets/systems_run/temp_storage"
            time_a, out_a = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

            # run gauss on
            cmd = "./../assets/sat/cryptominisat/build_gauss/cryptominisat5 --verb=0 ./../assets/systems_run/temp_storage"
            time_b, out_b = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

            # Save
            results.append([key, n, m, time_a, time_b, time_b - time_a])
            fh.update_file("./../assets/systems_run/run", results)

    def prepare_cryptominisat_system(self, n, m, system):
        """
        Helper to translate a python system to a cryptominisat system
        Save this translation into a file for processing
        :param n: 
        :param m: 
        :param system: 
        :return: 
        """
        # init
        input = [
            'p cnf {0} {1}'.format(n, m)
        ]

        # Grab clauses
        for clause in system:
            input.append("x{0} {1} -{2} 0".format(int(clause[0]), int(clause[1]), int(clause[2])))

        # Ensures uniquely satisfiable
        input.append(" ".join([str(i) for i in range(1, int(n) + 1)]) + " 0")

        # Return
        return input

    def find_pool(self, clauses):
        """
        Helper to find variables used
        Redundant
        :param clauses: 
        :return: A list of integers used in clauses
        """
        variables = []
        for clause in clauses:
            for variable in clause:
                if variable not in variables:
                    variables.append(variable)
        return variables

    def save_systems(self, systems):
        """
        Save a set of systems of equations to a file
        :param systems: 
        :return: 
        """
        for system in systems:
            # n, m, system
            self.save_system(system[1], system[2], system[3])

    def save_system(self, n, m, system):
        """
        Save a system of equations to file
        :param n: 
        :param m: 
        :param system: 
        :return: 
        """
        fh = FileHandler()
        path = "./../assets/systems/{0}_{1}".format(n, m)
        fh.write_to_file(path, system)

    def load_results(self):
        """
        Load Sat Solver execution results
        :return: 
        """
        fh = FileHandler()
        results = fh.read_from_file("./../assets/systems_run/run")
        return results

    def convert_system_to_graph(self, n, m, system):
        """
        Convert a system of equations to a Traces graph
        First construction used in checking for Automorphisms
        :param system: 
        :return: 
        """

        # Empty matrix of correct size
        width = n + m
        A = np.zeros((width, width))

        # Insert edges
        c = 0
        for clause in system:
            for i in range(0, 3):
                A[clause[i] - 1][n + c] = 1
            # Increment
            c = c + 1

        # Make Symmetric
        A = np.maximum(A, A.transpose())

        # Prepare Positioning
        L = range(0, n)
        R = range(n, n + m)

        # Prepare Labels
        labels = range(1, n + 1) + ["C" + str(i) for i in range(1, m + 1)]
        labels_dict = {}
        for i in range(0, n + m):
            labels_dict[i] = labels[i]

        # Construct Graph
        G = nx.from_numpy_matrix(A)
        pos = nx.spring_layout(G)
        pos = dict()
        pos.update((n, (i, 1)) for i, n in enumerate(R))  # put nodes from X at x=1
        pos.update((n, (i, 2)) for i, n in enumerate(L))  # put nodes from Y at x=2
        nx.draw(G, pos)
        nx.draw_networkx_labels(G, pos, labels_dict)
        plt.draw()
        # plt.show()

        return G

    def convert_system_to_construction(self, n, m, system):
        """
        Convert a system of equations into a Traces graph
        Second construction after checking for automorphisms
        :param n: 
        :param m: 
        :param system: 
        :return: 
        """
        width = (2 * n) + (4 * m)
        A = np.zeros((width, width))

        # Insert edges
        c = 0
        for clause in system:
            c_pos = (2 * n) + c
            # 0 0 0
            A[(clause[0] * 2) - 2][c_pos] = 1
            A[(clause[1] * 2) - 2][c_pos] = 1
            A[(clause[2] * 2) - 2][c_pos] = 1
            # 0 1 1
            A[(clause[0] * 2) - 2][c_pos + 1] = 1
            A[(clause[1] * 2) - 1][c_pos + 1] = 1
            A[(clause[2] * 2) - 1][c_pos + 1] = 1
            # 1 0 1
            A[(clause[0] * 2) - 1][c_pos + 2] = 1
            A[(clause[1] * 2) - 2][c_pos + 2] = 1
            A[(clause[2] * 2) - 1][c_pos + 2] = 1
            # 1 1 0
            A[(clause[0] * 2) - 1][c_pos + 3] = 1
            A[(clause[1] * 2) - 1][c_pos + 3] = 1
            A[(clause[2] * 2) - 2][c_pos + 3] = 1

            # Increment
            c = c + 4

        # Make Symmetric
        A = np.maximum(A, A.transpose())

        # Prepare Positioning
        L = range(0, 2 * n)
        R = range(2 * n, width)

        # Prepare Labels
        labels_dict = {}
        labels = []
        for i in range(1, n + 1):
            labels.append("{0}F".format(i))
            labels.append("{0}T".format(i))
        for i in range(1, m + 1):
            labels.append("C{0}_1".format(i))
            labels.append("C{0}_2".format(i))
            labels.append("C{0}_3".format(i))
            labels.append("C{0}_4".format(i))
        for i in range(0, width):
            labels_dict[i] = labels[i]

        # Construct Graph
        G = nx.from_numpy_matrix(A)
        pos = nx.spring_layout(G)
        pos = dict()
        pos.update((n, (i, 1)) for i, n in enumerate(R))  # put nodes from X at x=1
        pos.update((n, (i, 2)) for i, n in enumerate(L))  # put nodes from Y at x=2
        nx.draw(G, pos)
        nx.draw_networkx_labels(G, pos, labels_dict)
        plt.draw()
        # plt.show()

        return G

    def is_k_consistent(self, n, m, system):
        """
        Looking for systems that are faster with gauss off => K-local consistent
        :param n: 
        :param m: 
        :param system: 
        :return: 
        """
        ph = ProcessHandler()
        fh = FileHandler()

        # Create cryptominisat system
        input = self.prepare_cryptominisat_system(n, m, system)
        fh.write_to_file_simple("./../assets/construction/temp", input)

        # run gauss off
        cmd = "./../assets/sat/cryptominisat/build/cryptominisat5 --verb=0 ./../assets/construction/temp"
        time_a, out_a = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

        # run gauss on
        cmd = "./../assets/sat/cryptominisat/build_gauss/cryptominisat5 --verb=0 ./../assets/construction/temp"
        time_b, out_b = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

        # If Gauss On - Gauss Off > Threshold (sec)
        threshold = time_b - time_a > float(1)

        return threshold
