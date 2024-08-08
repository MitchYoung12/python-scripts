import requests
import pandas as pd
import matplotlib.pyplot as plt

# Replace token, owner, and repo
GITHUB_TOKEN = 'token'
ORG = 'org'

# Define the GitHub API URL
url = f'https://api.github.com/orgs/{ORG}/code-scanning/alerts'

# Headers for API request
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Make API request
response = requests.get(url, headers=headers)

# Check for success
if response.status_code == 200:
    alerts = response.json()
else:
    print(f"Failed to retrieve alerts: {response.status_code}")
    alerts = []

# Process data
if alerts:
    data = {
        'Rule ID': [],
        'Severity': [],
        'State': [],
        'Created At': [],
        'Updated At': []
    }
    for alert in alerts:
        data['Rule ID'].append(alert['rule']['id'])
        data['Severity'].append(alert['rule']['severity'])
        data['State'].append(alert['state'])
        data['Created At'].append(alert['created_at'])
        data['Updated At'].append(alert['updated_at'])

    # Create DF
    df = pd.DataFrame(data)

    # Convert date columns to datetime
    df['Created At'] = pd.to_datetime(df['Created At'])
    df['Updated At'] = pd.to_datetime(df['Updated At'])

    # Display the DF
    print(df)

    # Output to CSV
    csv_filename = 'code_scanning_alerts.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Data has been written to {csv_filename}")

else:
    print("No alerts found.")
