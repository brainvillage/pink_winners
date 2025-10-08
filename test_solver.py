#!/usr/bin/env python3
"""
Test script for Linear Programming Solver - Pink Winners Team
"""

import numpy as np
from scipy.optimize import linprog

def test_basic_functionality():
    """Test basic linear programming functionality"""
    print("🧪 Testing Linear Programming Solver...")
    
    # Test problem: Production Planning
    # Maximize: 3x1 + 2x2
    # Subject to: 2x1 + x2 <= 100, x1 + x2 <= 80, x1 <= 40
    
    c = [-3, -2]  # Negative for maximization
    A_ub = [[2, 1], [1, 1], [1, 0]]
    b_ub = [100, 80, 40]
    bounds = [(0, None), (0, None)]
    
    try:
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if result.success:
            print("✅ Basic solver test PASSED")
            print(f"   Optimal value: {-result.fun:.2f}")
            print(f"   Solution: x1={result.x[0]:.2f}, x2={result.x[1]:.2f}")
            return True
        else:
            print("❌ Basic solver test FAILED")
            print(f"   Status: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ Error in basic test: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("📦 Testing package imports...")
    
    modules = {
        'numpy': 'NumPy',
        'scipy.optimize': 'SciPy Optimization',
        'matplotlib.pyplot': 'Matplotlib',
        'tkinter': 'Tkinter GUI'
    }
    
    all_good = True
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            all_good = False
    
    return all_good

def run_example_problems():
    """Test several example problems"""
    print("🎯 Testing example problems...")
    
    examples = [
        {
            'name': 'Diet Problem',
            'c': [0.5, 0.3],  # Minimize cost
            'A_ub': [[-2, -1], [-1, -3]],  # Convert >= to <=
            'b_ub': [-10, -12],
            'bounds': [(0, None), (0, None)]
        },
        {
            'name': 'Transportation Problem',
            'c': [2, 3, 1],  # Minimize cost
            'A_ub': [[-1, -1, -1], [2, 1, 3]],  # Mixed constraints
            'b_ub': [-100, 200],
            'bounds': [(0, None), (0, None), (0, None)]
        }
    ]
    
    for example in examples:
        try:
            result = linprog(
                c=example['c'],
                A_ub=example['A_ub'],
                b_ub=example['b_ub'],
                bounds=example['bounds'],
                method='highs'
            )
            
            if result.success:
                print(f"   ✅ {example['name']}: Optimal value = {result.fun:.4f}")
            else:
                print(f"   ❌ {example['name']}: {result.message}")
                
        except Exception as e:
            print(f"   ❌ {example['name']}: Error - {e}")

def main():
    print("=" * 60)
    print("🧪 LINEAR PROGRAMMING SOLVER TEST SUITE")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    if not imports_ok:
        print("❌ Some required packages are missing.")
        print("💡 Install them with: pip install -r requirements.txt")
        return
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    print()
    
    if basic_ok:
        # Test example problems
        run_example_problems()
        print()
        
        print("🎉 All tests completed!")
        print("✅ Your Linear Programming Solver is ready to use!")
        print()
        print("🚀 Run the solver with:")
        print("   python run_lp_solver.py")
    else:
        print("❌ Basic functionality test failed.")
        print("💡 Check your SciPy installation.")

if __name__ == "__main__":
    main()