#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Start Script for Conflict-Free Scheduling System
This script provides a simplified interface for new users
"""

import os
import sys
import subprocess

def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🎓 CONFLICT-FREE SCHEDULING SYSTEM - QUICK START")
    print("=" * 60)
    print("Welcome! This script will help you get started quickly.")
    print()

def main():
    print_welcome()
    
    print("Choose an option:")
    print("1. Quick Demo (Generate sample schedule)")
    print("2. Interactive Mode (Customize your schedule)")
    print("3. View User Guide")
    print("4. Setup Environment (First time setup)")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🚀 Running Quick Demo...")
        print("This will generate a sample academic schedule using the graph coloring algorithm.")
        
        # Run main.py with echo inputs for quick demo
        cmd = 'echo -e "1\\nn\\nn\\nacademic\\nn" | python main.py'
        os.system(cmd)
        
        print("\n✅ Demo complete! Check the 'output' folder for your PDF schedule.")
        
    elif choice == "2":
        print("\n🖥️ Starting Interactive Mode...")
        print("You'll be asked to customize your scheduling preferences.")
        
        # Run main.py in interactive mode
        subprocess.run([sys.executable, "main.py"])
        
    elif choice == "3":
        print("\n📚 Opening User Guide...")
        user_guide_path = "USER_GUIDE.md"
        
        if os.path.exists(user_guide_path):
            # Try to open with default markdown viewer
            try:
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f"open {user_guide_path}")
                elif sys.platform.startswith('linux'):  # Linux
                    os.system(f"xdg-open {user_guide_path}")
                elif sys.platform.startswith('win'):  # Windows
                    os.system(f"start {user_guide_path}")
                else:
                    print(f"Please open {user_guide_path} in your preferred text editor.")
            except:
                print(f"Please open {user_guide_path} in your preferred text editor.")
        else:
            print("❌ User guide not found. Please check if USER_GUIDE.md exists.")
            
    elif choice == "4":
        print("\n🔧 Setting up environment...")
        print("This will install dependencies and set up the database.")
        
        confirm = input("Continue with setup? (y/n): ").lower().strip()
        if confirm == 'y':
            # Run setup script
            if os.path.exists("run.sh"):
                os.system("chmod +x run.sh && ./run.sh setup")
            else:
                print("Installing Python dependencies...")
                os.system("pip install -r requirements.txt")
                print("✅ Setup complete!")
        else:
            print("Setup cancelled.")
            
    elif choice == "5":
        print("\n👋 Goodbye! Thanks for using the Conflict-Free Scheduling System.")
        
    else:
        print("\n❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
