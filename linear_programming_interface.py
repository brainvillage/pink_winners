#!/usr/bin/env python3
"""
Linear Programming Interface - Pink Winners Team
A comprehensive GUI for solving linear programming problems
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

class LinearProgrammingInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Programming Solver - Pink Winners")
        self.root.geometry("1200x800")
        
        # Variables for the problem
        self.num_variables = tk.IntVar(value=2)
        self.num_constraints = tk.IntVar(value=2)
        self.objective_type = tk.StringVar(value="maximize")
        
        # Storage for coefficients
        self.objective_coeffs = []
        self.constraint_coeffs = []
        self.constraint_bounds = []
        self.constraint_types = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Problem Setup Tab
        self.setup_tab = ttk.Frame(notebook)
        notebook.add(self.setup_tab, text="Problem Setup")
        self.create_setup_tab()
        
        # Solution Tab
        self.solution_tab = ttk.Frame(notebook)
        notebook.add(self.solution_tab, text="Solution & Results")
        self.create_solution_tab()
        
        # Visualization Tab
        self.viz_tab = ttk.Frame(notebook)
        notebook.add(self.viz_tab, text="Visualization")
        self.create_visualization_tab()
        
        # Examples Tab
        self.examples_tab = ttk.Frame(notebook)
        notebook.add(self.examples_tab, text="Examples")
        self.create_examples_tab()
        
    def create_setup_tab(self):
        # Main frame with scrollbar
        canvas = tk.Canvas(self.setup_tab)
        scrollbar = ttk.Scrollbar(self.setup_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Problem dimensions
        dim_frame = ttk.LabelFrame(scrollable_frame, text="Problem Dimensions", padding=10)
        dim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dim_frame, text="Number of Variables:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.num_variables, 
                   command=self.update_problem_size).grid(row=0, column=1, padx=5)
        
        ttk.Label(dim_frame, text="Number of Constraints:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        ttk.Spinbox(dim_frame, from_=0, to=20, textvariable=self.num_constraints,
                   command=self.update_problem_size).grid(row=0, column=3, padx=5)
        
        # Objective function
        obj_frame = ttk.LabelFrame(scrollable_frame, text="Objective Function", padding=10)
        obj_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(obj_frame, text="Maximize", variable=self.objective_type, 
                       value="maximize").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(obj_frame, text="Minimize", variable=self.objective_type, 
                       value="minimize").grid(row=0, column=1, sticky=tk.W)
        
        # Objective coefficients frame
        self.obj_coeffs_frame = ttk.Frame(obj_frame)
        self.obj_coeffs_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, pady=10)
        
        # Constraints frame
        self.constraints_frame = ttk.LabelFrame(scrollable_frame, text="Constraints", padding=10)
        self.constraints_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="Solve Problem", command=self.solve_problem).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_problem).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Problem", command=self.save_problem).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Problem", command=self.load_problem).pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initialize the problem setup
        self.update_problem_size()
        
    def create_solution_tab(self):
        # Results display
        results_frame = ttk.LabelFrame(self.solution_tab, text="Solution Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Solution summary
        summary_frame = ttk.LabelFrame(self.solution_tab, text="Solution Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.optimal_value_label = ttk.Label(summary_frame, text="Optimal Value: Not solved yet")
        self.optimal_value_label.pack(anchor=tk.W)
        
        self.status_label = ttk.Label(summary_frame, text="Status: Not solved yet")
        self.status_label.pack(anchor=tk.W)
        
    def create_visualization_tab(self):
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self.viz_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Visualization controls
        viz_controls = ttk.Frame(self.viz_tab)
        viz_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(viz_controls, text="Plot Feasible Region", 
                  command=self.plot_feasible_region).pack(side=tk.LEFT, padx=5)
        ttk.Button(viz_controls, text="Clear Plot", 
                  command=self.clear_plot).pack(side=tk.LEFT, padx=5)
        
    def create_examples_tab(self):
        examples_frame = ttk.Frame(self.examples_tab)
        examples_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(examples_frame, text="Example Problems", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Example buttons
        examples = [
            ("Production Planning", self.load_production_example),
            ("Diet Problem", self.load_diet_example),
            ("Transportation Problem", self.load_transportation_example),
            ("Investment Portfolio", self.load_investment_example)
        ]
        
        for name, command in examples:
            ttk.Button(examples_frame, text=name, command=command).pack(pady=5, fill=tk.X)
            
        # Example description
        self.example_desc = scrolledtext.ScrolledText(examples_frame, height=10)
        self.example_desc.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def update_problem_size(self):
        # Clear existing widgets
        for widget in self.obj_coeffs_frame.winfo_children():
            widget.destroy()
        for widget in self.constraints_frame.winfo_children():
            widget.destroy()
            
        # Create objective coefficient inputs
        ttk.Label(self.obj_coeffs_frame, text="Objective: ").grid(row=0, column=0)
        
        self.obj_entries = []
        for i in range(self.num_variables.get()):
            ttk.Label(self.obj_coeffs_frame, text=f"x{i+1}:").grid(row=0, column=2*i+1)
            entry = ttk.Entry(self.obj_coeffs_frame, width=8)
            entry.grid(row=0, column=2*i+2, padx=2)
            entry.insert(0, "1")  # Default value
            self.obj_entries.append(entry)
            
        # Create constraint inputs
        self.constraint_entries = []
        self.bound_entries = []
        self.type_combos = []
        
        for i in range(self.num_constraints.get()):
            # Constraint label
            ttk.Label(self.constraints_frame, text=f"Constraint {i+1}:").grid(row=i, column=0, sticky=tk.W)
            
            # Coefficient entries
            constraint_row = []
            for j in range(self.num_variables.get()):
                entry = ttk.Entry(self.constraints_frame, width=8)
                entry.grid(row=i, column=j+1, padx=2)
                entry.insert(0, "1")  # Default value
                constraint_row.append(entry)
            self.constraint_entries.append(constraint_row)
            
            # Constraint type
            type_combo = ttk.Combobox(self.constraints_frame, values=["<=", ">=", "="], width=5)
            type_combo.grid(row=i, column=self.num_variables.get()+1, padx=5)
            type_combo.set("<=")  # Default
            self.type_combos.append(type_combo)
            
            # Bound entry
            bound_entry = ttk.Entry(self.constraints_frame, width=8)
            bound_entry.grid(row=i, column=self.num_variables.get()+2, padx=2)
            bound_entry.insert(0, "0")  # Default value
            self.bound_entries.append(bound_entry)
            
    def solve_problem(self):
        try:
            # Get objective coefficients
            c = []
            for entry in self.obj_entries:
                c.append(float(entry.get()))
            
            # Convert to minimization if needed
            if self.objective_type.get() == "maximize":
                c = [-x for x in c]
                
            # Get constraint coefficients and bounds
            A_ub = []
            b_ub = []
            A_eq = []
            b_eq = []
            
            for i in range(self.num_constraints.get()):
                constraint_row = []
                for j in range(self.num_variables.get()):
                    constraint_row.append(float(self.constraint_entries[i][j].get()))
                
                bound_value = float(self.bound_entries[i].get())
                constraint_type = self.type_combos[i].get()
                
                if constraint_type == "<=":
                    A_ub.append(constraint_row)
                    b_ub.append(bound_value)
                elif constraint_type == ">=":
                    A_ub.append([-x for x in constraint_row])
                    b_ub.append(-bound_value)
                else:  # "="
                    A_eq.append(constraint_row)
                    b_eq.append(bound_value)
            
            # Convert to numpy arrays
            A_ub = np.array(A_ub) if A_ub else None
            b_ub = np.array(b_ub) if b_ub else None
            A_eq = np.array(A_eq) if A_eq else None
            b_eq = np.array(b_eq) if b_eq else None
            
            # Solve the problem
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
                           bounds=[(0, None) for _ in range(len(c))], method='highs')
            
            # Display results
            self.display_results(result, c)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error solving problem: {str(e)}")
            
    def display_results(self, result, c):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Format results
        results_str = "LINEAR PROGRAMMING SOLUTION\n"
        results_str += "=" * 50 + "\n\n"
        
        if result.success:
            results_str += f"Status: {result.message}\n\n"
            
            # Optimal value (convert back if maximization)
            optimal_value = result.fun
            if self.objective_type.get() == "maximize":
                optimal_value = -optimal_value
                
            results_str += f"Optimal {self.objective_type.get().title()} Value: {optimal_value:.6f}\n\n"
            
            # Optimal solution
            results_str += "Optimal Solution:\n"
            for i, value in enumerate(result.x):
                results_str += f"  x{i+1} = {value:.6f}\n"
                
            results_str += f"\nNumber of iterations: {result.nit}\n"
            
            # Update summary labels
            self.optimal_value_label.config(text=f"Optimal Value: {optimal_value:.6f}")
            self.status_label.config(text=f"Status: {result.message}")
            
        else:
            results_str += f"Status: {result.message}\n"
            results_str += "The problem could not be solved.\n"
            results_str += "This might be due to:\n"
            results_str += "- Infeasible constraints\n"
            results_str += "- Unbounded solution\n"
            results_str += "- Numerical issues\n"
            
            self.optimal_value_label.config(text="Optimal Value: No solution")
            self.status_label.config(text=f"Status: {result.message}")
        
        self.results_text.insert(tk.END, results_str)
        
    def plot_feasible_region(self):
        if self.num_variables.get() != 2:
            messagebox.showwarning("Warning", "Visualization only available for 2-variable problems")
            return
            
        try:
            self.ax.clear()
            
            # Create a grid of points
            x1 = np.linspace(-1, 10, 400)
            x2 = np.linspace(-1, 10, 400)
            X1, X2 = np.meshgrid(x1, x2)
            
            # Plot constraints
            for i in range(self.num_constraints.get()):
                a1 = float(self.constraint_entries[i][0].get())
                a2 = float(self.constraint_entries[i][1].get())
                b = float(self.bound_entries[i].get())
                constraint_type = self.type_combos[i].get()
                
                if constraint_type == "<=":
                    constraint = a1 * X1 + a2 * X2 <= b
                elif constraint_type == ">=":
                    constraint = a1 * X1 + a2 * X2 >= b
                else:  # "="
                    constraint = np.abs(a1 * X1 + a2 * X2 - b) < 0.1
                
                self.ax.contour(X1, X2, (a1 * X1 + a2 * X2 - b), levels=[0], colors='blue', alpha=0.6)
                
            # Plot feasible region (simplified)
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
            self.ax.set_xlabel('x1')
            self.ax.set_ylabel('x2')
            self.ax.set_title('Constraint Visualization')
            self.ax.grid(True, alpha=0.3)
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting: {str(e)}")
            
    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()
        
    def clear_problem(self):
        # Reset all entries to default values
        for entry in self.obj_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "1")
            
        for i in range(len(self.constraint_entries)):
            for entry in self.constraint_entries[i]:
                entry.delete(0, tk.END)
                entry.insert(0, "1")
            self.bound_entries[i].delete(0, tk.END)
            self.bound_entries[i].insert(0, "0")
            self.type_combos[i].set("<=")
            
        # Clear results
        self.results_text.delete(1.0, tk.END)
        self.optimal_value_label.config(text="Optimal Value: Not solved yet")
        self.status_label.config(text="Status: Not solved yet")
        
    def save_problem(self):
        try:
            problem_data = {
                "num_variables": self.num_variables.get(),
                "num_constraints": self.num_constraints.get(),
                "objective_type": self.objective_type.get(),
                "objective_coeffs": [entry.get() for entry in self.obj_entries],
                "constraints": []
            }
            
            for i in range(self.num_constraints.get()):
                constraint = {
                    "coeffs": [entry.get() for entry in self.constraint_entries[i]],
                    "type": self.type_combos[i].get(),
                    "bound": self.bound_entries[i].get()
                }
                problem_data["constraints"].append(constraint)
                
            filename = f"lp_problem_{self.num_variables.get()}vars_{self.num_constraints.get()}cons.json"
            with open(filename, 'w') as f:
                json.dump(problem_data, f, indent=2)
                
            messagebox.showinfo("Success", f"Problem saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving problem: {str(e)}")
            
    def load_problem(self):
        # This would typically use a file dialog, but for simplicity, we'll look for JSON files
        try:
            json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('lp_problem')]
            if not json_files:
                messagebox.showwarning("Warning", "No saved problems found")
                return
                
            # For simplicity, load the first found file
            filename = json_files[0]
            with open(filename, 'r') as f:
                problem_data = json.load(f)
                
            # Update problem dimensions
            self.num_variables.set(problem_data["num_variables"])
            self.num_constraints.set(problem_data["num_constraints"])
            self.objective_type.set(problem_data["objective_type"])
            
            # Recreate the interface
            self.update_problem_size()
            
            # Load objective coefficients
            for i, coeff in enumerate(problem_data["objective_coeffs"]):
                self.obj_entries[i].delete(0, tk.END)
                self.obj_entries[i].insert(0, coeff)
                
            # Load constraints
            for i, constraint in enumerate(problem_data["constraints"]):
                for j, coeff in enumerate(constraint["coeffs"]):
                    self.constraint_entries[i][j].delete(0, tk.END)
                    self.constraint_entries[i][j].insert(0, coeff)
                self.type_combos[i].set(constraint["type"])
                self.bound_entries[i].delete(0, tk.END)
                self.bound_entries[i].insert(0, constraint["bound"])
                
            messagebox.showinfo("Success", f"Problem loaded from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading problem: {str(e)}")
            
    def load_production_example(self):
        """Production Planning Example"""
        self.num_variables.set(2)
        self.num_constraints.set(3)
        self.objective_type.set("maximize")
        self.update_problem_size()
        
        # Objective: maximize 3x1 + 2x2 (profit)
        self.obj_entries[0].delete(0, tk.END)
        self.obj_entries[0].insert(0, "3")
        self.obj_entries[1].delete(0, tk.END)
        self.obj_entries[1].insert(0, "2")
        
        # Constraints
        constraints_data = [
            ([2, 1], "<=", 100),  # Material constraint
            ([1, 1], "<=", 80),   # Labor constraint
            ([1, 0], "<=", 40)    # Machine constraint
        ]
        
        for i, (coeffs, op, bound) in enumerate(constraints_data):
            for j, coeff in enumerate(coeffs):
                self.constraint_entries[i][j].delete(0, tk.END)
                self.constraint_entries[i][j].insert(0, str(coeff))
            self.type_combos[i].set(op)
            self.bound_entries[i].delete(0, tk.END)
            self.bound_entries[i].insert(0, str(bound))
            
        desc = """Production Planning Example:
        
A company produces two products (x1, x2) with profits of $3 and $2 respectively.

Constraints:
- Material: 2x1 + x2 ≤ 100 units
- Labor: x1 + x2 ≤ 80 hours  
- Machine: x1 ≤ 40 hours

Objective: Maximize profit = 3x1 + 2x2

This is a classic production optimization problem."""
        
        self.example_desc.delete(1.0, tk.END)
        self.example_desc.insert(tk.END, desc)
        
    def load_diet_example(self):
        """Diet Problem Example"""
        self.num_variables.set(2)
        self.num_constraints.set(2)
        self.objective_type.set("minimize")
        self.update_problem_size()
        
        # Objective: minimize 0.5x1 + 0.3x2 (cost)
        self.obj_entries[0].delete(0, tk.END)
        self.obj_entries[0].insert(0, "0.5")
        self.obj_entries[1].delete(0, tk.END)
        self.obj_entries[1].insert(0, "0.3")
        
        # Constraints
        constraints_data = [
            ([2, 1], ">=", 10),   # Protein requirement
            ([1, 3], ">=", 12)    # Vitamin requirement
        ]
        
        for i, (coeffs, op, bound) in enumerate(constraints_data):
            for j, coeff in enumerate(coeffs):
                self.constraint_entries[i][j].delete(0, tk.END)
                self.constraint_entries[i][j].insert(0, str(coeff))
            self.type_combos[i].set(op)
            self.bound_entries[i].delete(0, tk.END)
            self.bound_entries[i].insert(0, str(bound))
            
        desc = """Diet Problem Example:
        
Minimize the cost of a diet while meeting nutritional requirements.

Foods: x1 (meat), x2 (vegetables)
Costs: $0.50 and $0.30 per unit

Constraints:
- Protein: 2x1 + x2 ≥ 10 units
- Vitamins: x1 + 3x2 ≥ 12 units

Objective: Minimize cost = 0.5x1 + 0.3x2"""
        
        self.example_desc.delete(1.0, tk.END)
        self.example_desc.insert(tk.END, desc)
        
    def load_transportation_example(self):
        """Transportation Problem Example"""
        self.num_variables.set(3)
        self.num_constraints.set(2)
        self.objective_type.set("minimize")
        self.update_problem_size()
        
        # Objective: minimize transportation costs
        self.obj_entries[0].delete(0, tk.END)
        self.obj_entries[0].insert(0, "2")
        self.obj_entries[1].delete(0, tk.END)
        self.obj_entries[1].insert(0, "3")
        self.obj_entries[2].delete(0, tk.END)
        self.obj_entries[2].insert(0, "1")
        
        # Constraints
        constraints_data = [
            ([1, 1, 1], ">=", 100),  # Demand constraint
            ([2, 1, 3], "<=", 200)   # Supply constraint
        ]
        
        for i, (coeffs, op, bound) in enumerate(constraints_data):
            for j, coeff in enumerate(coeffs):
                self.constraint_entries[i][j].delete(0, tk.END)
                self.constraint_entries[i][j].insert(0, str(coeff))
            self.type_combos[i].set(op)
            self.bound_entries[i].delete(0, tk.END)
            self.bound_entries[i].insert(0, str(bound))
            
        desc = """Transportation Problem Example:
        
Minimize transportation costs for shipping goods.

Variables: x1, x2, x3 (shipment quantities)
Costs: $2, $3, $1 per unit

Constraints:
- Meet demand: x1 + x2 + x3 ≥ 100 units
- Supply limit: 2x1 + x2 + 3x3 ≤ 200 units

Objective: Minimize cost = 2x1 + 3x2 + x3"""
        
        self.example_desc.delete(1.0, tk.END)
        self.example_desc.insert(tk.END, desc)
        
    def load_investment_example(self):
        """Investment Portfolio Example"""
        self.num_variables.set(2)
        self.num_constraints.set(3)
        self.objective_type.set("maximize")
        self.update_problem_size()
        
        # Objective: maximize expected return
        self.obj_entries[0].delete(0, tk.END)
        self.obj_entries[0].insert(0, "0.08")
        self.obj_entries[1].delete(0, tk.END)
        self.obj_entries[1].insert(0, "0.12")
        
        # Constraints
        constraints_data = [
            ([1, 1], "<=", 10000),    # Budget constraint
            ([1, 0], ">=", 3000),     # Minimum in safe investment
            ([0, 1], "<=", 5000)      # Maximum in risky investment
        ]
        
        for i, (coeffs, op, bound) in enumerate(constraints_data):
            for j, coeff in enumerate(coeffs):
                self.constraint_entries[i][j].delete(0, tk.END)
                self.constraint_entries[i][j].insert(0, str(coeff))
            self.type_combos[i].set(op)
            self.bound_entries[i].delete(0, tk.END)
            self.bound_entries[i].insert(0, str(bound))
            
        desc = """Investment Portfolio Example:
        
Maximize expected return on investment portfolio.

Variables: x1 (safe bonds), x2 (risky stocks)
Returns: 8% and 12% respectively

Constraints:
- Budget: x1 + x2 ≤ $10,000
- Minimum safe: x1 ≥ $3,000
- Maximum risky: x2 ≤ $5,000

Objective: Maximize return = 0.08x1 + 0.12x2"""
        
        self.example_desc.delete(1.0, tk.END)
        self.example_desc.insert(tk.END, desc)

def main():
    root = tk.Tk()
    app = LinearProgrammingInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()