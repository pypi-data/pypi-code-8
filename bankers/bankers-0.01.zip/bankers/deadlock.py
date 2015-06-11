# -*- encoding: utf-8 -*-

class Deadlock(object):
    def __init__(self):
        self.resource_rest_vector = None
        self.requirements = None
        self.occupancies = None
    
    def find_process_that_meets_requirements(self):
        found_process = -1
        for i in range(len(self.requirements)):
            if self.is_process_not_fitting_requirements(self.requirements[i][0]):
                continue
            for j in range(len(self.resource_rest_vector)):
                if self.requirements[i][j] > self.resource_rest_vector[j]:
                    break
                if j == len(self.resource_rest_vector)-1:
                    found_process = i
        return found_process

    def is_process_not_fitting_requirements(self, i):
        return i == -1

    def update_matrices(self, found_process):
        for i in range(len(self.resource_rest_vector)):
            counter = self.requirements[found_process][i]
            self.occupancies[found_process][i] += counter
            self.resource_rest_vector[i] -= counter
            self.resource_rest_vector[i] += self.occupancies[found_process][i]
            self.occupancies[found_process][i] = -1
            self.requirements[found_process][i] = -1

    def set_resource_rest_vector(self, resource_vector):
        for i in range(len(resource_vector)):
            sum = 0
            for j in range(len(self.occupancies)):
                sum += self.occupancies[j][i]
            self.resource_rest_vector.append(resource_vector[i] - sum)

    def find_deadlock(self):
        for i in range(len(self.requirements)):
            process = self.find_process_that_meets_requirements()
            if self.is_process_not_fitting_requirements(process):
                return True
            self.update_matrices(process)
        return False
