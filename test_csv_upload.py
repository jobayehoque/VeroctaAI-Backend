#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')
from app import app

print('🧪 TESTING CSV UPLOAD FUNCTIONALITY')
print('=' * 50)

with app.test_client() as client:
    # First login to get a token
    print('\n1. Authenticating user...')
    login_data = {'email': 'test@example.com', 'password': 'testpass123'}
    response = client.post('/api/auth/login', json=login_data)
    
    if response.status_code == 200:
        access_token = response.get_json().get('access_token')
        print('   ✅ Authentication successful')
        
        # Test CSV upload
        print('\n2. Testing CSV Upload...')
        
        with open('test_data.csv', 'rb') as csv_file:
            data = {
                'file': (csv_file, 'test_data.csv'),
                'company_name': 'Test Corporation',
                'description': 'Test financial analysis'
            }
            
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.post('/api/upload', 
                                 data=data, 
                                 headers=headers,
                                 content_type='multipart/form-data')
            
            print(f'   Status: {response.status_code}')
            if response.status_code == 200:
                result = response.get_json()
                print(f'   Success: {result.get("success", False)}')
                print(f'   Spend Score: {result.get("spend_score", "N/A")}')
                print(f'   Transactions: {result.get("total_transactions_processed", "N/A")}')
                print(f'   Total Amount: ${result.get("total_amount_analyzed", "N/A")}')
                print('   ✅ CSV upload and analysis working!')
                
                # Test additional endpoints with the processed data
                print('\n3. Testing SpendScore endpoint...')
                response = client.get('/api/spend-score', headers=headers)
                print(f'   Status: {response.status_code}')
                if response.status_code == 200:
                    score_data = response.get_json()
                    print(f'   Score: {score_data.get("score", "N/A")}')
                    print('   ✅ SpendScore endpoint working')
                else:
                    print(f'   ❌ SpendScore failed: {response.get_data(as_text=True)}')
                
                # Test reports endpoint
                print('\n4. Testing Reports endpoint...')
                response = client.get('/api/reports', headers=headers)
                print(f'   Status: {response.status_code}')
                if response.status_code == 200:
                    reports_data = response.get_json()
                    print(f'   Success: {reports_data.get("success", False)}')
                    print(f'   Reports Count: {len(reports_data.get("reports", []))}')
                    print('   ✅ Reports endpoint working')
                    
            else:
                print(f'   ❌ Upload failed: {response.get_data(as_text=True)}')
    else:
        print('   ❌ Authentication failed')

print('\n' + '=' * 50)
print('🎯 CSV UPLOAD TESTING COMPLETE')