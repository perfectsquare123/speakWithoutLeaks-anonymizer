import pandas as pd
import os

# Sample CSV with a text and label column
sample_data = {
    "text": [
        "John Doe's email is john.doe@example.com and he lives in New York.",
        "Alice paid with credit card 4111-1111-1111-1111 on January 1, 2023.",
        "Michael called 123-456-7890 to book a flight to Berlin.",
        "Contact jane.smith87@gmail.com or +1-234-567-8910 for more information."
    ],
    "label": [1, 0, 2, 3]  # sample classification labels
}

df_sample = pd.DataFrame(sample_data)

# Create directories if not present
os.makedirs("data", exist_ok=True)

# Save to CSV
test_csv_path = "data/sample_test_input.csv"
df_sample.to_csv(test_csv_path, index=False)

test_csv_path