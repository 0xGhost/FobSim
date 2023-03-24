import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys

#init global var
xlsx_file = ' '
old_table = True

#handle console arguments
if len(sys.argv) == 2:
    xlsx_file = sys.argv[1]
else:
    xlsx_file = 'logreg_input.xlsx'


# Load data from xlsx file
data = pd.read_excel(xlsx_file, engine='openpyxl')



# Function to convert numbers to True if greater than 0 and False if less than or equal to 0
def to_bool(x):
    return x > 0

# Column you want to apply the function to

column_to_convert = 'fail time(secs)'
if old_table:
    column_to_convert = 'queue too long (fail) time(secs)'
data[column_to_convert] = data[column_to_convert].apply(to_bool)

# Replace these with the appropriate column names
feature_columns = ['injection rate(per sec)', 'tx per block']
target_column = 'fail time(secs)'
if old_table:
    target_column = 'queue too long (fail) time(secs)'


# Print the entire DataFrame
#print("Data:")
#print(data)

# Split the dataset into features (x) and target (y)
x = data[feature_columns]
y = data[target_column]

# Print the features (x) and target (y) DataFrames
print("\nFeatures (x):")
print(x)
print("\nTarget (y):")
print(y)


# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Create a logistic regression model and fit it to the training data
logreg = LogisticRegression()
logreg.fit(x_train, y_train)

# Make predictions on the test data
y_pred = logreg.predict(x_test)

# Evaluate the model
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nAccuracy Score:", accuracy_score(y_test, y_pred))

# Print coefficients and intercept
print("\nCoefficients:", logreg.coef_)
print("Intercept:", logreg.intercept_)