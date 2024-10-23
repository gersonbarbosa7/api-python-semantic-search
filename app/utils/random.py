import numpy as np
from datetime import datetime, timedelta
import random

# Function to generate a random publication date within the last year
def generate_random_date():
    days_delta = random.randint(0, 365)  # Random number of days in the last year
    return (datetime.now() - timedelta(days=days_delta)).date()