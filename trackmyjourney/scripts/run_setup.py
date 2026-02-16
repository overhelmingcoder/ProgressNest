#!/usr/bin/env python
"""
Quick setup script for TrackMyJourney
Run this script to set up the entire project
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 TrackMyJourney Quick Setup")
    print("=" * 50)
    
    # Get project directory - fix for __file__ error
    try:
        project_dir = Path(__file__).resolve().parent.parent
    except NameError:
        # Fallback if __file__ is not defined
        project_dir = Path.cwd()
    
    os.chdir(project_dir)
    
    print("📁 Project directory:", project_dir)
    
    # Run the complete setup
    try:
        subprocess.run([sys.executable, "scripts/complete_setup.py"], check=True)
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("\n🌐 To start the server, run:")
        print("   python manage.py runserver")
        print("\n🔗 Then visit:")
        print("   http://127.0.0.1:8000")
        print("\n👤 Admin login:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🎉 Enjoy your TrackMyJourney website!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("\n🔧 Try running manually:")
        print("   python scripts/complete_setup.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
