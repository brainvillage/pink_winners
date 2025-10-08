#!/usr/bin/env python3
"""
Linear Programming Solver Launcher - Pink Winners Team
Choose between GUI and CLI interfaces
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['numpy', 'scipy', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def run_gui():
    """Launch the GUI interface"""
    try:
        print("🚀 Starting GUI Linear Programming Solver...")
        subprocess.run([sys.executable, "linear_programming_interface.py"])
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("💡 Try running the CLI version instead")

def run_cli():
    """Launch the CLI interface"""
    try:
        print("🚀 Starting CLI Linear Programming Solver...")
        subprocess.run([sys.executable, "lp_solver_cli.py"])
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")

def main():
    print("=" * 60)
    print("🏆 LINEAR PROGRAMMING SOLVER - PINK WINNERS TEAM")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    print("\nChoose your interface:")
    print("1. 🖥️  GUI Interface (Graphical, with visualization)")
    print("2. 💻 CLI Interface (Command line, faster)")
    print("3. 📚 View README")
    print("4. 🚪 Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            run_gui()
            break
        elif choice == '2':
            run_cli()
            break
        elif choice == '3':
            if os.path.exists("README.md"):
                with open("README.md", 'r') as f:
                    print("\n" + "=" * 60)
                    print(f.read())
                    print("=" * 60)
            else:
                print("❌ README.md not found")
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()