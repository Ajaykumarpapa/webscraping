#!/usr/bin/env python3
"""Create test data for sentiment analysis and topic modeling"""

import pandas as pd

# Create sample test data
test_data = {
    'title': [
        'Great service',
        'Terrible experience',
        'Good quality products',
        'Very disappointed',
        'Excellent delivery',
        'Poor customer service',
        'Fresh vegetables',
        'Damaged items',
        'Fast delivery',
        'Late delivery but good quality'
    ],
    'content': [
        'BigBasket provides great service and fresh products. I am very satisfied.',
        'Worst experience ever. Items were damaged and delivery was late.',
        'Good quality products and reasonable prices. Would recommend.',
        'Very disappointed with the service. Items were missing from my order.',
        'Excellent delivery service. Products arrived on time and fresh.',
        'Poor customer service. They did not respond to my complaints.',
        'Fresh vegetables and fruits. Quality is consistently good.',
        'Damaged items received. Packaging was poor.',
        'Fast delivery and good quality. Very happy with the service.',
        'Delivery was late but the quality of products was good.'
    ],
    'rating': [
        '5.0', '1.0', '4.0', '2.0', '5.0',
        '1.0', '4.5', '1.5', '5.0', '3.0'
    ]
}

df = pd.DataFrame(test_data)
df.to_csv('bigbasket_reviews.csv', index=False, encoding='utf-8')
print(f"Created test data with {len(df)} reviews")
print("\nSample data:")
print(df.head())
