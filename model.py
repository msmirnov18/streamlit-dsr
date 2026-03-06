from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

df = pd.read_csv("https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv")

model = RandomForestRegressor(n_estimators=100, random_state=123)

X, y = df[['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']], df['Life Expectancy (IHME)']

# We know these columns are clean and all values are numbers
assert X.isna().sum().sum() == 0
assert y.isna().sum().sum() == 0

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=123)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"R^2: {r2_score(y_test, y_pred):.3f}")           # e.g., 0.85 = 85% explained
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f} years")  # e.g., 2.5 years off

joblib.dump(model, "model.joblib")
print("Model saved!")