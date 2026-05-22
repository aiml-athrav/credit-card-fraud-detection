import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report

# Import synthetic generator in case dataset is missing
from data_generator import generate_synthetic_data

def train_model_pipeline(data_path: str, model_save_path: str):
    """
    Loads data, preprocesses features, trains the classification model,
    evaluates it against standard fraud metrics, and serializes the pipeline.
    """
    # 1. Check/Generate Data
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Generating synthetic dataset first...")
        generate_synthetic_data(data_path)
        
    df = pd.read_csv(data_path)
    
    # 2. Separate Features and Target
    # Columns expected: Time, V1-V28, Amount, Class
    feature_cols = [col for col in df.columns if col != 'Class']
    X = df[feature_cols]
    y = df['Class']
    
    # 3. Stratified Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # 4. Feature Scaling (Fitting on train set only to prevent leakage)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 5. Model Training (Robust Ensemble with dual fallback)
    # We use Scikit-Learn's RandomForestClassifier with balanced class weight as a primary, high-performance
    # and widely compatible local option. We also attempt to load XGBoost if the user environment has it.
    classifier = None
    model_name = "RandomForest"
    
    try:
        from xgboost import XGBClassifier
        print("XGBoost detected. Training XGBoost Classifier...")
        # scale_pos_weight is genuine count / fraud count to handle imbalance
        neg_count = np.sum(y_train == 0)
        pos_count = np.sum(y_train == 1)
        scale_pos_weight = neg_count / pos_count
        
        classifier = XGBClassifier(
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            eval_metric="logloss",
            n_estimators=100
        )
        model_name = "XGBoost"
    except ImportError:
        print("XGBoost library not found. Falling back to Scikit-Learn RandomForestClassifier...")
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
        
    classifier.fit(X_train_scaled, y_train)
    
    # 6. Evaluation Metrics
    y_pred = classifier.predict(X_test_scaled)
    # Get probabilities for ROC-AUC
    if hasattr(classifier, "predict_proba"):
        y_prob = classifier.predict_proba(X_test_scaled)[:, 1]
    else:
        y_prob = classifier.decision_function(X_test_scaled)
        
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print("\n" + "="*50)
    print(f"MODEL EVALUATION REPORT ({model_name.upper()})")
    print("="*50)
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print(f"Precision:     {precision:.4f}  (Ability to avoid false fraud flags)")
    print(f"Recall:        {recall:.4f}  (Ability to capture actual fraud)")
    print(f"F1-Score:      {f1:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Genuine", "Fraud"]))
    print("="*50 + "\n")
    
    # 7. Serialize Pipeline and Metadata
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    pipeline_payload = {
        "model_name": model_name,
        "features": feature_cols,
        "scaler": scaler,
        "model": classifier,
        "metrics": {
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "roc_auc": float(roc_auc)
        }
    }
    
    joblib.dump(pipeline_payload, model_save_path)
    print(f"Model pipeline successfully saved to: {model_save_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "creditcard_synthetic.csv")
    
    # Save the model directly into the backend storage path for runtime loading
    backend_storage_dir = os.path.join(current_dir, "..", "backend", "storage")
    model_save_path = os.path.join(backend_storage_dir, "model_pipeline.joblib")
    
    train_model_pipeline(data_path, model_save_path)
