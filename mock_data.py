import pandas as pd
from faker import Faker
import random

def generate_mock_data(num_records=20, output_file='faculty_data.csv'):
    """
    Generates mock faculty data for the Burnout Risk & Workload Analyzer.
    """
    fake = Faker()
    
    subjects = [
        'Data Structures', 'Physics', 'Machine Learning', 'Algorithms', 
        'Computer Networks', 'Operating Systems', 'Calculus', 'Software Engineering'
    ]
    
    data = []
    for _ in range(num_records):
        # Generate random float between 1.0 and 1.5 for complexity
        complexity = round(random.uniform(1.0, 1.5), 2)
        
        record = {
            'Faculty_ID': fake.unique.random_int(min=1000, max=9999),
            'Name': fake.name(),
            'Subject_Expertise': random.choice(subjects),
            'Subject_Complexity_Multiplier': complexity,
            'Classes_Per_Week': random.randint(8, 22),
            'Admin_Hours_Per_Week': random.randint(0, 10),
            'Max_Consecutive_Classes': random.randint(1, 4)
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Successfully generated {num_records} records in {output_file}")
    return df

if __name__ == "__main__":
    generate_mock_data()
