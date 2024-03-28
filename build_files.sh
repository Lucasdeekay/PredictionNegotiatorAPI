# Install python dependencies
python3 -m ensurepip --upgrade
pip install -r requirements.txt

# Collect static files (adjust paths as needed)
python manage.py collectstatic --no-input