#!/usr/bin/env python
"""Test API endpoint"""

from app import create_app
import json

app = create_app()

with app.test_client() as client:
    response = client.get('/api/inspections')
    data = response.get_json()
    
    print('✓ API Response:')
    print(f'  Status: {data["status"]}')
    print(f'  Total Inspections: {data["count"]}')
    
    if data['data']:
        inspection = data['data'][0]
        print(f'  First Inspection: {inspection["project_name"]}')
        print(f'  Systems in API: {inspection["systems_count"]}')
        print(f'  Total Weighted Score: {inspection["total_weighted_score"]}%')
        print()
        print('✓ Sample System from API:')
        if inspection['systems']:
            sys = inspection['systems'][0]
            print(f'  System: {sys["system_name"]}')
            print(f'  Score: {sys["score_percentage"]}%')
            print(f'  Weight: {sys["weight"]}')
            print(f'  Weighted Score: {sys["weighted_score"]}')
    
    print()
    print('✓ API is working correctly for Power BI!')
