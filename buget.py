from dotenv import load_dotenv
import http.client
import json
import os

load_dotenv()

conn = http.client.HTTPSConnection("api.thucchien.ai")
payload = ''
headers = {
 'accept': 'application/json',
 'Authorization': f'Bearer {os.getenv("API_KEY")}'
}
conn.request("GET", "/key/info", payload, headers)
res = conn.getresponse()
data = res.read()


# Parse JSON response
response = json.loads(data.decode("utf-8"))


# Extract spend and max_budget
spend = response['info']['spend']
max_budget = response['info']['max_budget']


# Calculate remaining budget
remaining_budget = max_budget - spend


# Display results
print(f"Current Spend: ${spend:.2f}")
print(f"Maximum Budget: ${max_budget:.2f}")
print(f"Remaining Budget: ${remaining_budget:.2f}")
print(f"Budget Used: {(spend/max_budget)*100:.1f}%")
