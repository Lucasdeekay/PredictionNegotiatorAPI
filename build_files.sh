# Install python dependencies
python3.9 -m ensurepip --upgrade
python3.9 -m pip install -r requirements.txt

# Collect static files (adjust paths as needed)
python3.9 manage.py collectstatic --no-input