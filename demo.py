#!/usr/bin/env python3
"""
Demo script showing Linear Programming Solver capabilities
"""

import numpy as np
from scipy.optimize import linprog

def demo_production_problem():
    """Demonstrate a production planning problem"""
    print("🏭 PRODUCTION PLANNING PROBLEM")
    print("=" * 50)
    print("A factory produces two products: A and B")
    print("Product A: $3 profit per unit")
    print("Product B: $2 profit per unit")
    print()
    print("Constraints:")
    print("- Material: 2A + 1B ≤ 100 units")
    print("- Labor:    1A + 1B ≤ 80 hours")
    print("- Machine:  1A + 0B ≤ 40 hours")
    print()
    print("Question: How many of each product to maximize profit?")
    print()
    
    # Solve the problem
    c = [-3, -2]  # Negative for maximization
    A_ub = [[2, 1], [1, 1], [1, 0]]
    b_ub = [100, 80, 40]
    bounds = [(0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if result.success:
        print("📊 SOLUTION:")
        print(f"   Produce {result.x[0]:.0f} units of Product A")
        print(f"   Produce {result.x[1]:.0f} units of Product B")
        print(f"   Maximum profit: ${-result.fun:.2f}")
        print()
        
        # Check constraint usage
        print("📈 RESOURCE UTILIZATION:")
        material_used = 2*result.x[0] + 1*result.x[1]
        labor_used = 1*result.x[0] + 1*result.x[1]
        machine_used = 1*result.x[0]
        
        print(f"   Material: {material_used:.0f}/100 units ({material_used:.0f}%)")
        print(f"   Labor:    {labor_used:.0f}/80 hours ({labor_used/80*100:.0f}%)")
        print(f"   Machine:  {machine_used:.0f}/40 hours ({machine_used/40*100:.0f}%)")

def demo_diet_problem():
    """Demonstrate a diet optimization problem"""
    print("\n🥗 DIET OPTIMIZATION PROBLEM")
    print("=" * 50)
    print("Find the cheapest diet meeting nutritional needs")
    print("Food 1 (meat):      $0.50 per unit")
    print("Food 2 (vegetables): $0.30 per unit")
    print()
    print("Nutritional requirements:")
    print("- Protein:  2×Food1 + 1×Food2 ≥ 10 units")
    print("- Vitamins: 1×Food1 + 3×Food2 ≥ 12 units")
    print()
    
    # Solve the problem
    c = [0.5, 0.3]  # Minimize cost
    A_ub = [[-2, -1], [-1, -3]]  # Convert >= to <= by negating
    b_ub = [-10, -12]
    bounds = [(0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if result.success:
        print("📊 SOLUTION:")
        print(f"   Buy {result.x[0]:.2f} units of meat")
        print(f"   Buy {result.x[1]:.2f} units of vegetables")
        print(f"   Minimum cost: ${result.fun:.2f}")
        print()
        
        # Check nutritional content
        protein = 2*result.x[0] + 1*result.x[1]
        vitamins = 1*result.x[0] + 3*result.x[1]
        
        print("📈 NUTRITIONAL CONTENT:")
        print(f"   Protein:  {protein:.2f} units (required: ≥10)")
        print(f"   Vitamins: {vitamins:.2f} units (required: ≥12)")

def demo_investment_problem():
    """Demonstrate an investment portfolio problem"""
    print("\n💰 INVESTMENT PORTFOLIO PROBLEM")
    print("=" * 50)
    print("Optimize investment portfolio allocation")
    print("Safe bonds:  8% annual return")
    print("Risky stocks: 12% annual return")
    print()
    print("Constraints:")
    print("- Total budget: $10,000")
    print("- Minimum safe investment: $3,000")
    print("- Maximum risky investment: $5,000")
    print()
    
    # Solve the problem
    c = [-0.08, -0.12]  # Negative for maximization (returns)
    A_ub = [[1, 1], [-1, 0], [0, 1]]  # Budget, min safe, max risky
    b_ub = [10000, -3000, 5000]
    bounds = [(0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if result.success:
        print("📊 SOLUTION:")
        print(f"   Invest ${result.x[0]:.2f} in safe bonds")
        print(f"   Invest ${result.x[1]:.2f} in risky stocks")
        print(f"   Expected annual return: ${-result.fun:.2f}")
        print(f"   Return rate: {-result.fun/10000*100:.2f}%")
        print()
        
        print("📈 PORTFOLIO ANALYSIS:")
        total_invested = result.x[0] + result.x[1]
        safe_percent = result.x[0] / total_invested * 100
        risky_percent = result.x[1] / total_invested * 100
        
        print(f"   Total invested: ${total_invested:.2f}")
        print(f"   Safe allocation: {safe_percent:.1f}%")
        print(f"   Risky allocation: {risky_percent:.1f}%")

def main():
    print("🏆 LINEAR PROGRAMMING SOLVER DEMO")
    print("Pink Winners Team")
    print("=" * 60)
    
    # Run all demos
    demo_production_problem()
    demo_diet_problem()
    demo_investment_problem()
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print()
    print("These examples show how linear programming can solve:")
    print("✅ Production optimization")
    print("✅ Cost minimization")
    print("✅ Resource allocation")
    print("✅ Portfolio optimization")
    print()
    print("🚀 Try the interactive solver:")
    print("   python3 run_lp_solver.py")

if __name__ == "__main__":
    main()