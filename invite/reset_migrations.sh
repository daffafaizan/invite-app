# Only run this file if you need to reset migrations for some special use cases.
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/migrations/__pycache__/*" -delete
# find . -path "*/migrations/__pycache__/*" -not -name "__init__*.pyc" -delete