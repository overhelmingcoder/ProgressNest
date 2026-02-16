#!/bin/bash

echo "🚀 Setting up TrackMyJourney Platform..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Setup database
python scripts/setup_database.py

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Create sample data
python scripts/create_sample_data.py

echo "✅ Setup complete!"
echo "Run: python manage.py runserver"
echo "Visit: http://127.0.0.1:8000"




# 1.  venv\Scripts\activate  2. cd trackmyjourney 3. python manage.py runserver