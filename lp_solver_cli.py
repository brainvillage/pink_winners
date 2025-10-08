#!/usr/bin/env python3
"""
Command Line Linear Programming Solver - Pink Winners Team
A simple CLI interface for solving linear programming problems
"""

import numpy as np
from scipy.optimize import linprog
import json

class LPSolverCLI:
    def __init__(self):
        self.problem = {}
        
    def input_problem(self):
        """Interactive input for linear programming problem"""
        print("=" * 50)
        print("LINEAR PROGRAMMING SOLVER - PINK WINNERS")
        print("=" * 50)
        
        # Get problem dimensions
        num_vars = int(input("Enter number of variables: "))
        num_constraints = int(input("Enter number of constraints: "))
        
        # Get objective function
        print(f"\nObjective Function:")
        obj_type = input("Maximize or Minimize? (max/min): ").lower()
        
        print(f"Enter coefficients for objective function:")
        c = []
        for i in range(num_vars):
            coeff = float(input(f"Coefficient for x{i+1}: "))
            c.append(coeff)
            
        # Convert to minimization if needed
        if obj_type.startswith('max'):
            c = [-x for x in c]
            self.problem['maximize'] = True
        else:
            self.problem['maximize'] = False
            
        # Get constraints
        print(f"\nConstraints:")
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        
        for i in range(num_constraints):
            print(f"\nConstraint {i+1}:")
            constraint_coeffs = []
            for j in range(num_vars):
                coeff = float(input(f"  Coefficient for x{j+1}: "))
                constraint_coeffs.append(coeff)
                
            constraint_type = input("  Constraint type (<=, >=, =): ").strip()
            bound = float(input("  Right-hand side value: "))
            
            if constraint_type == "<=":
                A_ub.append(constraint_coeffs)
                b_ub.append(bound)
            elif constraint_type == ">=":
                A_ub.append([-x for x in constraint_coeffs])
                b_ub.append(-bound)
            else:  # "="
                A_eq.append(constraint_coeffs)
                b_eq.append(bound)
                
        # Store problem data
        self.problem.update({
            'c': c,
            'A_ub': np.array(A_ub) if A_ub else None,
            'b_ub': np.array(b_ub) if b_ub else None,
            'A_eq': np.array(A_eq) if A_eq else None,
            'b_eq': np.array(b_eq) if b_eq else None,
            'num_vars': num_vars
        })
        
    def solve(self):
        """Solve the linear programming problem"""
        print("\n" + "=" * 50)
        print("SOLVING...")
        print("=" * 50)
        
        try:
            # Set bounds (non-negativity constraints)
            bounds = [(0, None) for _ in range(self.problem['num_vars'])]
            
            # Solve using scipy
            result = linprog(
                c=self.problem['c'],
                A_ub=self.problem['A_ub'],
                b_ub=self.problem['b_ub'],
                A_eq=self.problem['A_eq'],
                b_eq=self.problem['b_eq'],
                bounds=bounds,
                method='highs'
            )
            
            self.display_results(result)
            
        except Exception as e:
            print(f"Error solving problem: {e}")
            
    def display_results(self, result):
        """Display the solution results"""
        print("\n" + "=" * 50)
        print("SOLUTION RESULTS")
        print("=" * 50)
        
        if result.success:
            print(f"Status: {result.message}")
            print(f"Iterations: {result.nit}")
            
            # Calculate optimal value (convert back if maximization)
            optimal_value = result.fun
            if self.problem['maximize']:
                optimal_value = -optimal_value
                
            obj_type = "Maximum" if self.problem['maximize'] else "Minimum"
            print(f"\n{obj_type} Value: {optimal_value:.6f}")
            
            print(f"\nOptimal Solution:")
            for i, value in enumerate(result.x):
                print(f"  x{i+1} = {value:.6f}")
                
            # Sensitivity analysis (basic)
            print(f"\nSolution Analysis:")
            print(f"  - All variables are non-negative: {all(x >= -1e-10 for x in result.x)}")
            print(f"  - Solution is at vertex of feasible region")
            
        else:
            print(f"Status: {result.message}")
            print("\nThe problem could not be solved.")
            print("Possible reasons:")
            print("  - Infeasible constraints (no solution exists)")
            print("  - Unbounded solution (infinite optimal value)")
            print("  - Numerical issues")
            
    def save_problem(self, filename):
        """Save problem to JSON file"""
        try:
            # Convert numpy arrays to lists for JSON serialization
            save_data = {}
            for key, value in self.problem.items():
                if isinstance(value, np.ndarray):
                    save_data[key] = value.tolist()
                else:
                    save_data[key] = value
                    
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            print(f"Problem saved to {filename}")
            
        except Exception as e:
            print(f"Error saving problem: {e}")
            
    def load_problem(self, filename):
        """Load problem from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            # Convert lists back to numpy arrays
            for key in ['A_ub', 'b_ub', 'A_eq', 'b_eq']:
                if data.get(key) is not None:
                    data[key] = np.array(data[key])
                    
            self.problem = data
            print(f"Problem loaded from {filename}")
            
        except Exception as e:
            print(f"Error loading problem: {e}")

def quick_example():
    """Run a quick example problem"""
    print("QUICK EXAMPLE: Production Planning Problem")
    print("Maximize: 3x1 + 2x2 (profit)")
    print("Subject to:")
    print("  2x1 + x2 <= 100  (material)")
    print("  x1 + x2 <= 80    (labor)")
    print("  x1 <= 40         (machine)")
    print("  x1, x2 >= 0")
    
    # Define the problem
    c = [-3, -2]  # Negative for maximization
    A_ub = [[2, 1], [1, 1], [1, 0]]
    b_ub = [100, 80, 40]
    bounds = [(0, None), (0, None)]
    
    # Solve
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    print(f"\nSolution:")
    print(f"Status: {result.message}")
    print(f"Maximum profit: {-result.fun:.2f}")
    print(f"x1 (product 1): {result.x[0]:.2f}")
    print(f"x2 (product 2): {result.x[1]:.2f}")

def main():
    solver = LPSolverCLI()
    
    while True:
        print("\n" + "=" * 50)
        print("LINEAR PROGRAMMING SOLVER MENU")
        print("=" * 50)
        print("1. Input new problem")
        print("2. Solve current problem")
        print("3. Save problem")
        print("4. Load problem")
        print("5. Quick example")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            solver.input_problem()
        elif choice == '2':
            if solver.problem:
                solver.solve()
            else:
                print("No problem defined. Please input a problem first.")
        elif choice == '3':
            if solver.problem:
                filename = input("Enter filename (with .json extension): ")
                solver.save_problem(filename)
            else:
                print("No problem to save.")
        elif choice == '4':
            filename = input("Enter filename: ")
            solver.load_problem(filename)
        elif choice == '5':
            quick_example()
        elif choice == '6':
            print("Thank you for using LP Solver!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()