import os

def valid_pdf(path):
    return os.path.isfile(path) and path.lower().endswith(".pdf")

def valid_positive_number(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False
