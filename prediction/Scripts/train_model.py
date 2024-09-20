import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

data_path = 'data/raw/accurate_machine_failure_data.csv'
data = pd.read_csv(data_path)

print("Column names:")
print(data.columns)

X = data[['Air Temperature (K)', 'Process Temperature (K)', 'Rotational Speed (RPM)', 'Torque (Nm)', 'Tool Wear (hours)']]
y = data['Failure Type']

assert X.notnull().all().all(), "Features contain missing values"
assert y.notnull().all(), "Target contains missing values"

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

output_dir = 'model'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

model_path = os.path.join(output_dir, 'model.pkl')
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
