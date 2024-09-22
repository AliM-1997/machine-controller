import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), '../model/model.pkl')
model_path = os.path.abspath(model_path)
model = joblib.load(model_path)

test_data_path = 'C:/Users/Amort/OneDrive/Desktop/final-project/machine-controller/prediction/data/raw/accurate_machine_failure_data.csv'
test_data = pd.read_csv(test_data_path)

X_test = test_data[['Air Temperature (K)', 'Process Temperature (K)', 'Rotational Speed (RPM)', 'Torque (Nm)', 'Tool Wear (hours)']]
y_test = test_data['Failure Type']

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

print("Classification Report:")
print(classification_report(y_test, y_pred))

with open('model_performance.txt', 'w') as f:
    f.write(f"Accuracy: {accuracy * 100:.2f}%\n")
    f.write("Classification Report:\n")
    f.write(classification_report(y_test, y_pred))
