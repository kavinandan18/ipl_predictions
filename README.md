# IPL Predictions

IPL Predictions is a Django web application for making and managing predictions for IPL matches.

## Features

- View upcoming IPL matches
- Make predictions for match outcomes
- Edit and delete predictions
- ...

## Installation

1. Clone the repository:

   ```bash
   https://github.com/kavinandan18/ipl_predictions.git
   cd ipl_predictions

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (if needed)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

2. Visit http://localhost:8000/ to access the Django development server.


3. Contributing

If you would like to contribute to the project, please follow our Contribution Guidelines.