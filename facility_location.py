import sys, os
from pulp import PULP_CBC_CMD, SCIP_CMD, GUROBI_CMD
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary, LpContinuous


class FacilityLocationProblem:
    def __init__(self, facilities, customers, capacities, implementation_costs, demand, fixed_costs, relaxed=True):
        self.facilities = facilities
        self.customers = customers
        self.implementation_costs = implementation_costs
        self.fixed_costs = fixed_costs
        self.capacities = capacities
        self.demand = demand
        self.model = LpProblem("FacilityLocationProblem", LpMinimize)

        self.x = None
        self.y = None

        self.relaxed = relaxed

    def setup_problem(self):
        # Variables
        # x: Continuous 0 <= x <= inf
        # y: Binary 0 <= y <= 1
        self.x = LpVariable.dicts("X",
                                  ((i, j) for i in self.facilities for j in self.customers),
                                  0, None, LpContinuous)
        self.y = LpVariable.dicts("Y", self.facilities, 0, 1, LpBinary)
        self.model += (lpSum(self.implementation_costs[i] * self.y[i] for i in self.facilities) +
                       lpSum(self.fixed_costs[j][i] * self.x[i, j] for i in self.facilities for j in self.customers),
                       "Objective")

        for j in self.customers:
            self.model += lpSum(self.x[i, j] for i in self.facilities) == 1, f"Customer_{j}"

        if self.relaxed:
            for i in self.facilities:
                self.model += (lpSum(self.x[i, j] * self.demand[j] for j in self.customers) <= self.capacities[i] *
                               self.y[i], f"Capacity_{i}")
        else:
            for i in self.facilities:
                self.model += (lpSum(self.x[i, j] * self.demand[j] for j in self.customers) <= self.capacities[i], f"Capacity_{i}")
                for j in self.customers:
                    self.model += self.x[i, j] <= self.y[i], f"Customer_{j}_{i}"

    def print_solution(self):
        status = {1: "Optimal", 0: "Not Solved", -1: "Infeasible", -2: "Unbounded", -3: "Undefined"}
        print(f"Status: {status[self.model.status]}")
        print(f"Custo: {abs(self.model.objective.value()) if self.model.objective else 0}")
        # unitary_cost = 3.5

        # wasted_capacity = sum(self.capacities[i] * (1 - self.y[i].varValue) for i in self.facilities)
        # used_demand = sum(self.demand[j] * self.x[i, j].varValue for i in self.facilities for j in self.customers)

        # wasted_price = (wasted_capacity - used_demand) * unitary_cost
        for i in self.facilities:
            if not self.y[i].varValue:
                continue
            print(f"Ponto de distribuição {i}: {'Sim' if self.y[i].varValue else 'Não'} - "
                  f"atendendo um total de {(sum(self.x[i, j].varValue for j in self.customers)):.2f}% clientes")
            for j in self.customers:
                if not self.x[i, j].varValue:
                    continue
                print(f"    Custo do local {j} ao ponto {i}: {self.x[i, j].varValue :.2f}")

        print(f"Pontos de distribuição usados: {int(sum(self.y[i].varValue for i in self.facilities))}")

    @staticmethod
    def get_solver(solver_name, logPath=None):
        time_limit = 300
        match solver_name:
            case "scip":
                print("Using SCIP solver")
                solver = SCIP_CMD(timeLimit=time_limit)
            case "gurobi":
                print("Using Gurobi solver")
                solver = GUROBI_CMD(timeLimit=time_limit, logPath=logPath)
            case _:
                print("Invalid solver name. Using default solver (CBC)")
                solver = PULP_CBC_CMD(timeLimit=time_limit)

        return solver

    def solve(self, solver_name, path):
        stdout = sys.stdout

        folder = f"{path}/{solver_name}"

        if solver_name is None:
            folder = f"{path}/default"
        if not os.path.exists(folder):
            os.makedirs(folder)
        sys.stdout = open(f"{folder}/log.txt", "w")

        solver = self.get_solver(solver_name, logPath=f"{folder}/log.txt")
        self.model.solve(solver)

        sys.stdout.close()

        sys.stdout = open(f"{folder}/out.txt", "w")
        self.print_solution()
        sys.stdout.close()

        sys.stdout = stdout


def read_data(filename):
    with open(filename, 'r') as file:
        num_facilities, num_customers = map(int, file.readline().split())
        facilities = list(range(num_facilities))
        customers = list(range(num_customers))

        capacities = {}
        implementation_costs = {}
        for i in range(num_facilities):
            capacity, implementation_cost = map(int, file.readline().split())
            capacities[facilities[i]] = capacity
            implementation_costs[facilities[i]] = implementation_cost

        demand = {}
        fixed_costs = {}

        for j in range(num_customers):
            data = list(map(int, file.readline().split()))
            demand[customers[j]] = data[0]
            fixed_costs[customers[j]] = {facilities[i]: data[i + 1] for i in range(num_facilities)}

        return facilities, customers, capacities, implementation_costs, demand, fixed_costs


def main(filename, solver_name=None, relaxed="true"):
    print(f"Reading data from {filename}")
    relaxed = True if relaxed == "true" else False
    print("Relaxed: ", relaxed)
    problem = FacilityLocationProblem(*read_data(filename), relaxed=relaxed)

    print("Setting up problem...")
    problem.setup_problem()

    try:
        print("Solving - ", end="")
        problem.solve(solver_name, path=f"output/{'relaxed' if relaxed else 'unrelaxed'}/{filename.split('.')[0]}")

        print("Done, output saved to output folder")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python facility_location.py <filename> [solver_name] [relaxed]")
        print("Available solvers: scip, gurobi, default")
    else:
        try:
            main(*sys.argv[1:])
        except Exception as e:
            print(e)
