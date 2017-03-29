import random
import timeit
from pycryptosat import Solver
from handlers.filehandler import FileHandler


class Sat(object):
    def generate_systems(self, **kwargs):
        # init
        fh = FileHandler()
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
        save_system_location = save_dir+"/systems"
        save_results_location = save_dir+"/results"
        save_systems = kwargs.get("save_systems", False)
        save_results = kwargs.get("save_results", False)
        bound = kwargs.get("bound", True)

        # Prep folder
        fh.makedir(save_dir)

        while n < max_n:
            m = min_m
            n += step
            tries = 0
            smallest_m_found = False
            result = []
            system = []

            while m < max_m:
                m += step
                if m < n:
                    m = n

                if 4 < m / n:
                    break

                validation_start = timeit.default_timer()
                eq = self.generate_rand_unique_system(n, m)
                key = `n` + ':' + `m`

                if eq:
                    # Update the lower bound
                    if bound and not smallest_m_found:
                        min_m = m - step
                        smallest_m_found = True

                    # Record times
                    print "Found: ", n, m
                    validation_time = timeit.default_timer() - validation_start
                    tries = 0
                    results.append([key, n, m, tries, validation_time])
                    result.append([key, n, m, tries, validation_time])
                    if save_systems:
                        systems.append([key, n, m, eq])
                        system.append([key, n, m, eq])

                elif max_tries == tries:
                    # print "Skipping: ", n, m
                    tries = 0
                    results.append([key, n, m, tries, -1])
                    result.append([key, n, m, tries, -1])
                    continue

                else:
                    # print 'Couldnt find for ' + `m` + ' Misses ' + `tries`
                    print n, "-", m, "-missing"
                    tries += 1
                    m -= step

            if save_systems:
                print "Saving systems..."
                save_systems_time = self.run_function_timed(fh.update_file, (save_system_location, system))
                print "Time taken: ", save_systems_time
            if save_results:
                print "Saving results..."
                save_results_time = self.run_function_timed(fh.update_file, (save_results_location, result))
                print "Time taken: ", save_results_time
        return results

    def run_function_timed(self, f, args):
        # print args
        start = timeit.default_timer()
        f(*args)
        time = timeit.default_timer() - start
        return time

    def generate_rand_system(self, n, m):
        """Generates a random homogenous system
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
        Give up after t tries
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
        Don't give up
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
        clauses = self.find_clauses(n)
        systems = self.find_systems(clauses, n, m)
        return systems

    def find_clauses(n):
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

    def find_system(self, clauses, system, n, m, depth):
        systems = []
        if depth > m:
            # print 'M: '+`m`
            # print 'Depth: '+`depth`
            # print 'something wierd is happening'
            # print 'System: '+`system`
            # print 'clauses: '+`clauses`
            return False

        # If length of system = m , then we have long enough system
        if len(system) == m:
            for i in range(0, len(system) - 1):
                if system[i] > system[i + 1]:
                    return False
            # print system
            sat = Sat()
            if sat.is_system_uniquely_satisfiable(system):

                return system
            else:
                return False

        # Else system is not long enough, we need to append to system
        else:
            # For each clause not in the system, add to system
            for clause in clauses:
                tail = list(clauses)
                tail.remove(clause)
                if clause not in system:
                    systemTemp = list(system)
                    systemTemp.append(clause)
                    sys = self.find_system(tail, systemTemp, n, m, depth + 1)
                    if sys:
                        return sys
        return False

    def find_systems(self, clauses, n, m):
        return self.find_system(clauses, [], n, m, 0)
