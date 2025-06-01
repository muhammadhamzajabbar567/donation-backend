import requests

# Test data matching your form fields
TEST_DATA = {
    "bpType": "Individual",
    "bpName": "Test Donor",
    "cnic": "1234567890123",
    "contactNumber": "1234567890",
    "email": "test@example.com",
    "address": "123 Test St",
    "country": "Testland",
    "city": "Testville",
    "userRole": "Donor",
    "donationPurpose": "Project",
    "projectID": "P001",
    "donationType": "Cash",
    "amount": "100.50",
    "paymentMethod": "Credit Card",
    "donationDate": "2023-12-01",
    "notes": "This is a test donation"
}

response = requests.post('http://localhost:5000/api/donations', json=TEST_DATA)
print(response.json())