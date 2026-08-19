import pandas as pd
import numpy as np

def calculate_burnout_risk(data_path='faculty_data.csv'):
    """
    Calculates the Burnout Risk Score based on a heuristic scoring engine.
    Risk = (1.5 * Class_Hours) + (1.0 * Admin_Hours) + Consecutive_Class_Penalty + Subject_Complexity_Weight
    """
    df = pd.read_csv(data_path)
    
    # 1. Base workload calculation
    # Using Classes_Per_Week directly as Class_Hours
    base_class_score = 1.5 * df['Classes_Per_Week']
    base_admin_score = 1.0 * df['Admin_Hours_Per_Week']
    
    # 2. Consecutive Class Penalty
    # Massive penalty (+20) if Max_Consecutive_Classes is 3 or higher
    consecutive_penalty = np.where(df['Max_Consecutive_Classes'] >= 3, 20, 0)
    
    # 3. Subject Complexity Weight
    # Weighting the multiplier to have a measurable impact on the 0-100 scale
    complexity_weight = df['Subject_Complexity_Multiplier'] * 5 
    
    # 4. Total Risk Score Calculation
    df['Burnout_Risk_Score'] = base_class_score + base_admin_score + consecutive_penalty + complexity_weight
    
    # Normalize score (cap at 100 max)
    df['Burnout_Risk_Score'] = df['Burnout_Risk_Score'].clip(upper=100).round(2)
    
    # 5. Risk Status Classification
    conditions = [
        (df['Burnout_Risk_Score'] <= 40),
        (df['Burnout_Risk_Score'] > 40) & (df['Burnout_Risk_Score'] <= 75),
        (df['Burnout_Risk_Score'] > 75)
    ]
    choices = ['Optimal', 'Warning', 'Critical']
    df['Risk_Status'] = np.select(conditions, choices, default='Unknown')
    
    return df

if __name__ == "__main__":
    # Test execution
    try:
        processed_df = calculate_burnout_risk()
        print(processed_df[['Name', 'Burnout_Risk_Score', 'Risk_Status']].head())
    except FileNotFoundError:
        print("Error: Please run mock_data.py first to generate faculty_data.csv")
