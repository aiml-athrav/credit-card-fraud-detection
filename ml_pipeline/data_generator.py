import os
import pandas as pd
import numpy as np

def generate_synthetic_data(output_path: str, num_genuine: int = 25000, num_fraud: int = 500, random_state: int = 42):
    """
    Generates a highly realistic synthetic Credit Card Fraud dataset matching the Kaggle schema.
    Columns: Time, V1-V28 (PCA components), Amount, Class.
    """
    print(f"Generating synthetic dataset: {num_genuine} genuine, {num_fraud} fraud...")
    np.random.seed(random_state)
    
    # 1. Generate Genuine Transactions (Class = 0)
    genuine_data = {}
    genuine_data['Time'] = np.random.uniform(0, 172800, num_genuine) # 2 days in seconds
    
    # Genuine PCA features are roughly standard normal
    for i in range(1, 29):
        genuine_data[f'V{i}'] = np.random.normal(0.0, 1.0, num_genuine)
        
    # Amount is exponentially distributed with a lower mean
    genuine_data['Amount'] = np.random.exponential(scale=75.0, size=num_genuine) + 0.50
    genuine_data['Class'] = np.zeros(num_genuine, dtype=int)
    
    df_genuine = pd.DataFrame(genuine_data)
    
    # 2. Generate Fraudulent Transactions (Class = 1)
    fraud_data = {}
    fraud_data['Time'] = np.random.uniform(0, 172800, num_fraud)
    
    # Fraud PCA features have distinct shifted means (typical of the real Kaggle dataset)
    # V3, V4, V11, V12, V14, V17 are highly discriminative features
    shifted_features = {
        'V3': (-2.5, 1.5),
        'V4': (3.0, 1.5),
        'V10': (-2.0, 1.5),
        'V11': (2.5, 1.5),
        'V12': (-3.5, 1.5),
        'V14': (-4.5, 1.5),
        'V16': (-2.5, 1.5),
        'V17': (-5.0, 1.5),
    }
    
    for i in range(1, 29):
        col = f'V{i}'
        if col in shifted_features:
            mean, std = shifted_features[col]
            fraud_data[col] = np.random.normal(mean, std, num_fraud)
        else:
            # Other features have slightly elevated variance
            fraud_data[col] = np.random.normal(0.0, 1.5, num_fraud)
            
    # Fraud transactions usually have larger/different amounts
    fraud_data['Amount'] = np.random.exponential(scale=180.0, size=num_fraud) + 10.0
    fraud_data['Class'] = np.ones(num_fraud, dtype=int)
    
    df_fraud = pd.DataFrame(fraud_data)
    
    # Combine and Shuffle
    df_combined = pd.concat([df_genuine, df_fraud], ignore_index=True)
    df_combined = df_combined.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_combined.to_csv(output_path, index=False)
    print(f"Dataset generated successfully and saved to {output_path}")
    print(f"Fraud ratio: {num_fraud / (num_genuine + num_fraud):.4%} ({num_fraud}/{num_genuine + num_fraud})")
    
    return df_combined

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(output_dir, "creditcard_synthetic.csv")
    generate_synthetic_data(data_path)
