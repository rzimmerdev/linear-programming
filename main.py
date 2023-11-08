import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary

class FacilityLocationProblem:
    def __init__(self, facilities, customers, profits, fixed_costs, capacities):
        self.facilities = facilities
        self.customers = customers
        self.profits = profits
        self.fixed_costs = fixed_costs
        self.capacities = capacities
        self.model = LpProblem("FacilityLocationProblem", LpMaximize)

    def setup_problem(self):
        self.serve = LpVariable.dicts("Serve",
                                      ((f, c) for f in self.facilities for c in self.customers),
                                      0, None, LpBinary)
        self.open_facility = LpVariable.dicts("Open", self.facilities, 0, None, LpBinary)
        self.model += lpSum(self.profits[c][f] * self.serve[f, c] for f in self.facilities for c in self.customers) - \
                      lpSum(self.fixed_costs[f] * self.open_facility[f] for f in self.facilities)

        for c in self.customers:
            self.model += lpSum(self.serve[f, c] for f in self.facilities) == 1, f"Demand_{c}"

        for f in self.facilities:
            self.model += lpSum(self.serve[f, c] for c in self.customers) <= self.capacities[f] * self.open_facility[f], f"Capacity_{f}"

    def solve(self. solver_type=None):
        if solver_type:
            solver = getSolver(solver_type)
            self.model.solve(solver)
        else:
            self.model.solve()

    def print_solution(self):
        print(f"Status: {LpStatus[self.model.status]}")
        print(f"Total Profit: {value(self.model.objective)}")
        for f in self.facilities:
            print(f"{f} open: {self.open_facility[f].varValue}")
            for c in self.customers:
                print(f"  Serve {c}: {self.serve[f, c].varValue}")

def read_data(filename):
    with open(filename, 'r') as file:
        num_facilities, num_customers = map(int, file.readline().split())
        facilities = [f'Facility{i+1}' for i in range(num_facilities)]
        customers = [f'Customer{j+1}' for j in range(num_customers)]
        
        capacities = {}
        fixed_costs = {}
        for i in range(num_facilities):
            capacity, cost = map(int, file.readline().split())
            capacities[facilities[i]] = capacity
            fixed_costs[facilities[i]] = cost
        
        profits = {}
        for j in range(num_customers):
            data = list(map(int, file.readline().split()))
            demand = data[0]
            profits[customers[j]] = {facilities[i]: data[i+1] for i in range(num_facilities)}
            
        return facilities, customers, profits, fixed_costs, capacities

def main(filename, solver_type=None):
    facilities, customers, profits, fixed_costs, capacities = read_data(filename)
    problem = FacilityLocationProblem(facilities, customers, profits, fixed_costs, capacities)
    problem.setup_problem()
    problem.solve(solver_type)
    problem.print_solution()

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python facility_location.py <filename> [solver]")
    else:
        filename = sys.argv[1]
        solver = sys.argv[2] if len(sys.argv) == 3 else None
        main(filename, solver)

