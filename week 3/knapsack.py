from pulp import LpProblem, LpVariable, LpInteger, LpMinimize, LpStatus

prob = LpProblem("KnapsackProblem", LpMinimize)

quantity_vars = [LpVariable(f'quantity{i}', lowBound=0, cat=LpInteger) for i in range(1, 7)]
costs = [215, 275, 335, 355, 420, 580]
total_allowance = 1605

prob += sum(cost * qty for cost, qty in zip(costs, quantity_vars)) == total_allowance
prob += quantity_vars[5] >= 1
prob += sum(quantity_vars)

status = prob.solve()

if LpStatus[status] == 'Optimal':
    print("Valid solution found:")
    total_cost = 0
    for i, qty_var in enumerate(quantity_vars, start=1):
        qty = qty_var.varValue
        print(f"Quantity of Item {i}: {int(qty)}")
        total_cost += costs[i - 1] * qty
    print(f"Total Cost: {int(total_cost)}")
else:
    print("No valid solution exists.")
