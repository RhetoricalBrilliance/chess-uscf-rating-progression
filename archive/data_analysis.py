import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load your dataset
df = pd.read_csv("your_file.csv")  # replace with your actual path

# Define the column names for months to each rating milestone
month_cols = ['Months to: 600', '800', '1000', '1200', '1400', '1600', '1800', '2000']

# Drop rows with missing values in relevant columns
data = df[['Age at First Tournament'] + month_cols].dropna()

# Store regression results
results = []

# Run a separate linear regression for each milestone
for col in month_cols:
    X = data[['Age at First Tournament']].values
    y = data[col].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    results.append({
        'Rating': col.replace('Months to: ', ''),
        'R² Score': round(r2, 3),
        'Intercept': round(model.intercept_, 3),
        'Slope': round(model.coef_[0], 3)
    })

# Convert results to a DataFrame and display
results_df = pd.DataFrame(results)
print(results_df)
