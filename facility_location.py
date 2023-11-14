import sys
from pulp import SCIP_CMD, GUROBI_CMD, LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpInteger


class FacilityLocationProblem:
    def __init__(self, facilities, customers, profits, fixed_costs, capacities, demand):
        self.facilities = facilities
        self.customers = customers
        self.implementation_costs = profits
        self.fixed_costs = fixed_costs
        self.capacities = capacities
        self.demand = demand
        self.model = LpProblem("FacilityLocationProblem", LpMinimize)

        self.x = None
        self.y = None

    def setup_problem(self):
        self.x = LpVariable.dicts("X",
                                  ((i, j) for i in self.facilities for j in self.customers),
                                  0, None, LpInteger)
        self.y = LpVariable.dicts("Y", self.facilities, 0, None, LpBinary)
        self.model += (lpSum(self.implementation_costs[j][i] * self.x[i, j]
                             for i in self.facilities for j in self.customers) -
                       lpSum(self.fixed_costs[i] * self.y[i] for i in self.facilities))

        for j in self.customers:
            self.model += lpSum(self.x[i, j] for i in self.facilities) == 1, f"Demand_{j}"

        for i in self.facilities:
            self.model += (lpSum(self.x[i, j] * self.demand[j] for j in self.customers) <= self.capacities[i] *
                           self.y[i], f"Capacity_{i}")

    def solve(self, solver_name=None):
        if solver_name:
            solver = self.get_solver(solver_name)
            self.model.solve(solver)
        else:
            self.model.solve()

    def print_solution(self):
        status = {1: "Optimal", 0: "Not Solved", -1: "Infeasible", -2: "Unbounded", -3: "Undefined"}
        print(f"Status: {status[self.model.status]}")
        print(f"Custo: {abs(self.model.objective.value()) if self.model.objective else 0}")
        for i in self.facilities:
            print(f"Ponto de distribuição {i}: {'Sim' if self.y[i].varValue else 'Não'}")
            for j in self.customers:
                print(f"  Alunos de {j} indo a {i}: {self.x[i, j].varValue}")

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
        facilities = list(range(num_facilities))
        customers = list(range(num_customers))

        capacities = {}
        fixed_costs = {}
        for i in range(num_facilities):
            capacity, cost = map(int, file.readline().split())
            capacities[facilities[i]] = capacity
            fixed_costs[facilities[i]] = cost

        profits = {}
        demand = {}

        for j in range(num_customers):
            data = list(map(int, file.readline().split()))
            demand[customers[j]] = data[0]
            profits[customers[j]] = {facilities[i]: data[i + 1] for i in range(num_facilities)}

        return facilities, customers, profits, fixed_costs, capacities, demand


def main(filename, solver_name=None):
    facilities, customers, profits, fixed_costs, capacities, demand = read_data(filename)
    problem = FacilityLocationProblem(facilities, customers, profits, fixed_costs, capacities, demand)
    problem.setup_problem()
    problem.solve(solver_name)
    problem.print_solution()


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python facility_location.py <filename> [solver_name]")
    else:
        main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
