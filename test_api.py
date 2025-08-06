import requests

url = "http://127.0.0.1:5000/parse"
files = {'file': open(r'C:\Users\admin\Pictures\custom_parseur\tmp\invoice1.pdf', 'rb')}
data = {'template': 'sample_template'}

response = requests.post(url, files=files, data=data)

# Debug: print raw response text
print("Status code:", response.status_code)
print("Response text:", response.text)