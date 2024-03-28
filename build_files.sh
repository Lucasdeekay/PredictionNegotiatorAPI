# Install python dependencies
python3 -m ensurepip --upgrade
python3 -m pip install -r requirements.txt

# Collect static files (adjust paths as needed)
python3 manage.py collectstatic --no-input