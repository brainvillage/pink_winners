# Linear Programming Solver - Pink Winners Team

A comprehensive interface for solving linear programming problems with both GUI and command-line options.

## Features

### 🖥️ GUI Interface (`linear_programming_interface.py`)
- **Interactive Problem Setup**: Easy input for variables, constraints, and objective function
- **Multiple Problem Types**: Support for maximization/minimization with ≤, ≥, = constraints
- **Real-time Visualization**: Plot feasible regions for 2-variable problems
- **Built-in Examples**: Production planning, diet problems, transportation, investment portfolio
- **Save/Load Problems**: JSON format for problem persistence
- **Detailed Results**: Complete solution analysis with sensitivity information

### 💻 Command Line Interface (`lp_solver_cli.py`)
- **Interactive Menu**: Step-by-step problem input
- **Quick Examples**: Pre-built example problems
- **File Operations**: Save and load problems in JSON format
- **Batch Processing**: Suitable for automated solving

## Installation

1. **Install Required Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Required Packages**:
   - `numpy` - Numerical computations
   - `scipy` - Linear programming solver
   - `matplotlib` - Visualization
   - `tkinter` - GUI framework (usually included with Python)

## Usage

### GUI Interface
```bash
python linear_programming_interface.py
```

**Features:**
- **Problem Setup Tab**: Define variables, constraints, and objective function
- **Solution Tab**: View detailed results and solution analysis
- **Visualization Tab**: Plot feasible regions (2D problems only)
- **Examples Tab**: Load pre-built example problems

### Command Line Interface
```bash
python lp_solver_cli.py
```

**Menu Options:**
1. Input new problem
2. Solve current problem
3. Save problem to file
4. Load problem from file
5. Run quick example
6. Exit

## Problem Format

### Standard Form
```
Maximize/Minimize: c₁x₁ + c₂x₂ + ... + cₙxₙ

Subject to:
  a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤/≥/= b₁
  a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤/≥/= b₂
  ...
  aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ ≤/≥/= bₘ
  
  x₁, x₂, ..., xₙ ≥ 0
```

## Example Problems

### 1. Production Planning
**Problem**: A company produces two products with different profit margins and resource constraints.

```
Maximize: 3x₁ + 2x₂  (profit)
Subject to:
  2x₁ + x₂ ≤ 100    (material constraint)
  x₁ + x₂ ≤ 80      (labor constraint)  
  x₁ ≤ 40           (machine constraint)
  x₁, x₂ ≥ 0
```

### 2. Diet Problem
**Problem**: Minimize cost while meeting nutritional requirements.

```
Minimize: 0.5x₁ + 0.3x₂  (cost)
Subject to:
  2x₁ + x₂ ≥ 10     (protein requirement)
  x₁ + 3x₂ ≥ 12     (vitamin requirement)
  x₁, x₂ ≥ 0
```

### 3. Transportation Problem
**Problem**: Minimize shipping costs while meeting demand.

```
Minimize: 2x₁ + 3x₂ + x₃  (transportation cost)
Subject to:
  x₁ + x₂ + x₃ ≥ 100    (demand constraint)
  2x₁ + x₂ + 3x₃ ≤ 200  (supply constraint)
  x₁, x₂, x₃ ≥ 0
```

## File Format

Problems are saved in JSON format:

```json
{
  "num_variables": 2,
  "num_constraints": 3,
  "objective_type": "maximize",
  "objective_coeffs": ["3", "2"],
  "constraints": [
    {
      "coeffs": ["2", "1"],
      "type": "<=",
      "bound": "100"
    }
  ]
}
```

## Advanced Features

### Visualization (GUI Only)
- **2D Feasible Region Plotting**: Visual representation of constraints
- **Constraint Lines**: See how constraints define the feasible region
- **Optimal Point Identification**: Locate the optimal solution graphically

### Solution Analysis
- **Optimal Value**: Maximum or minimum value of objective function
- **Optimal Variables**: Values of decision variables at optimum
- **Solution Status**: Feasible, infeasible, or unbounded
- **Iteration Count**: Number of simplex iterations

### Error Handling
- **Infeasible Problems**: Detection and reporting of impossible constraints
- **Unbounded Solutions**: Identification of problems with infinite optimal values
- **Numerical Issues**: Robust handling of computational problems

## Tips for Use

1. **Start Simple**: Begin with 2-variable problems to understand the interface
2. **Use Examples**: Load built-in examples to see proper problem formatting
3. **Visualize**: Use the visualization tab for 2D problems to understand solutions
4. **Save Work**: Save complex problems to avoid re-entering data
5. **Check Results**: Always verify that solutions make practical sense

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure all required packages are installed
- **GUI Not Opening**: Check tkinter installation (usually included with Python)
- **Solver Errors**: Verify constraint formatting and numerical values
- **Visualization Issues**: matplotlib backend problems (try different Python environments)

### Performance Notes
- **Large Problems**: GUI may be slow for problems with >10 variables
- **Memory Usage**: CLI interface is more efficient for large-scale problems
- **Precision**: Results accurate to ~6 decimal places

## Mathematical Background

This solver uses the **HiGHS** algorithm (via SciPy) which implements:
- **Dual Simplex Method**: Efficient for most linear programming problems
- **Interior Point Methods**: Alternative for large-scale problems
- **Presolving**: Automatic problem simplification and redundancy removal

## Team Pink Winners

Created for linear programming education and practical problem solving.

**Features Roadmap:**
- [ ] Sensitivity analysis
- [ ] Integer programming support
- [ ] Multi-objective optimization
- [ ] Web interface
- [ ] Advanced visualization options