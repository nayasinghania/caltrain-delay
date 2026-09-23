import joblib
import pandas as pd
from joblib import Parallel, delayed
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

print("Loading data...")
df = pd.read_csv("data/data.csv")

X = df.drop(columns=["delay"])
y = df["delay"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining XGBoost Model:")
model = XGBRegressor(n_estimators=100, random_state=42, verbosity=1, eval_metric="rmse")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=10)
print("Completed XGBoost Model Training")

y_pred = model.predict(X_test)

print("\nXGBoost Model Results:")
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.3f} minutes")
print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.3f} minutes")
print(f"R²:   {r2_score(y_test, y_pred):.3f}")

print("\n Saving XGBoost Model as joblib")
joblib.dump(model, "api/xgboost.pkl")
