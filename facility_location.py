import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary, SCIP_CMD, GUROBI_CMD


class FacilityLocationProblem:
    def __init__(self, facilities, customers, profits, fixed_costs, capacities):
        self.facilities = facilities
        self.customers = customers
        self.profits = profits
        self.fixed_costs = fixed_costs
        self.capacities = capacities
        self.model = LpProblem("FacilityLocationProblem", LpMaximize)

        self.serve = None
        self.open_facility = None

    def setup_problem(self):
        self.serve = LpVariable.dicts("Serve",
                                      ((f, c) for f in self.facilities for c in self.customers),
                                      0, None, LpBinary)
        self.open_facility = LpVariable.dicts("Open", self.facilities, 0, None, LpBinary)
        self.model += (lpSum(self.profits[c][f] * self.serve[f, c] for f in self.facilities for c in self.customers) -
                       lpSum(self.fixed_costs[f] * self.open_facility[f] for f in self.facilities))

        for c in self.customers:
            self.model += lpSum(self.serve[f, c] for f in self.facilities) == 1, f"Demand_{c}"

        for f in self.facilities:
            self.model += (lpSum(self.serve[f, c] for c in self.customers) <= self.capacities[f] *
                           self.open_facility[f], f"Capacity_{f}")

    def solve(self, solver_name=None):
        if solver_name:
            solver = self.get_solver(solver_name)
            self.model.solve(solver)
        else:
            self.model.solve()

    def print_solution(self):
        status = {1: "Optimal", 0: "Not Solved", -1: "Infeasible", -2: "Unbounded", -3: "Undefined"}
        print(f"Status: {status[self.model.status]}")
        print(f"Total Profit: {self.model.objective.value() if self.model.objective else 0}")
        for f in self.facilities:
            print(f"{f} open: {self.open_facility[f].varValue}")
            for c in self.customers:
                print(f"  Serve {c}: {self.serve[f, c].varValue}")

    @staticmethod
    def get_solver(solver_name):
        match solver_name:
            case "SCIP":
                solver = SCIP_CMD()
            case "GUROBI":
                solver = GUROBI_CMD()
            case _:
                print("Invalid solver name. Using default solver.")
                solver = SCIP_CMD()

        return solver


def read_data(filename):
    with open(filename, 'r') as file:
        num_facilities, num_customers = map(int, file.readline().split())
        facilities = [f'Facility{i + 1}' for i in range(num_facilities)]
        customers = [f'Customer{j + 1}' for j in range(num_customers)]

        capacities = {}
        fixed_costs = {}
        for i in range(num_facilities):
            capacity, cost = map(int, file.readline().split())
            capacities[facilities[i]] = capacity
            fixed_costs[facilities[i]] = cost

        profits = {}
        for j in range(num_customers):
            data = list(map(int, file.readline().split()))
            # demand = data[0]
            profits[customers[j]] = {facilities[i]: data[i + 1] for i in range(num_facilities)}

        return facilities, customers, profits, fixed_costs, capacities


def main(filename, solver_name=None):
    facilities, customers, profits, fixed_costs, capacities = read_data(filename)
    problem = FacilityLocationProblem(facilities, customers, profits, fixed_costs, capacities)
    problem.setup_problem()
    problem.solve(solver_name)
    problem.print_solution()


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python facility_location.py <filename> [solver_name]")
    else:
        main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
