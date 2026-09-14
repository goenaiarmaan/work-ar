# Setup script for vector database

import os
from knowledge_base import KnowledgeBase


def create_sample_data():
    """Create sample product data for testing"""
    
    data_dir = 'data/products'
    os.makedirs(data_dir, exist_ok=True)
    
    # Create pricing file
    pricing_content = """# Product Pricing 2025

## Subscription Plans

### Basic Plan - €29/month
- 1 user account
- 5GB storage
- Email support
- Basic analytics
- Mobile app access

### Premium Plan - €79/month
- Up to 10 users
- 50GB storage
- Priority email & chat support
- Advanced analytics
- API access
- Custom integrations
- Mobile app access

### Enterprise Plan - €299/month
- Unlimited users
- 500GB storage
- 24/7 phone, email & chat support
- Full analytics suite
- Unlimited API calls
- Custom integrations
- Dedicated account manager
- SLA guarantee
- On-premise option available

## One-time Products

### Product A - Professional Tool
Price: €149 (one-time)
License: Perpetual
Updates: 1 year included
Support: Email

### Product B - Enterprise Suite
Price: €499 (one-time)
License: Perpetual
Updates: Lifetime
Support: Priority phone & email

## Discounts

- Annual billing: 20% discount
- Non-profit: 30% discount
- Education: 40% discount
- Bulk licenses (50+): Contact sales

Last updated: January 2025
"""
    
    with open(os.path.join(data_dir, 'pricing.md'), 'w') as f:
        f.write(pricing_content)
    
    # Create FAQ file
    faq_content = """# Frequently Asked Questions

## Ordering & Payment

### Q: What payment methods do you accept?
A: We accept credit cards (Visa, MasterCard, Amex), PayPal, bank transfer, and purchase orders for enterprise customers.

### Q: Can I change my plan later?
A: Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and billing is prorated.

### Q: Do you offer refunds?
A: Yes, we offer a 30-day money-back guarantee for all subscription plans. No questions asked.

## Returns & Refunds

### Q: What is your return policy?
A: Products can be returned within 30 days of purchase. The product must be unused and in original packaging.

### Q: How do I return a product?
A: Contact our support team with your order number. We'll send you a prepaid return label and process your refund within 5 business days.

### Q: Are there any non-returnable items?
A: Downloaded software licenses and custom-made products cannot be returned unless defective.

## Shipping & Delivery

### Q: How long does shipping take?
A: 
- Netherlands: 1-2 business days
- Belgium & Germany: 2-3 business days
- Rest of EU: 3-5 business days
- International: 5-10 business days

### Q: Do you offer free shipping?
A: Yes, free shipping on orders over €50 within the Netherlands and over €100 in the EU.

### Q: Can I track my order?
A: Absolutely! You'll receive a tracking number via email once your order ships.

## Technical Support

### Q: How do I contact support?
A: 
- Email: support@company.com
- Phone: +31 20 1234567 (Mon-Fri, 9:00-17:00)
- Chat: Available on our website during business hours
- Emergency: emergency@company.com (24/7 for enterprise customers)

### Q: What is your response time?
A:
- Basic plan: Within 24 hours
- Premium plan: Within 4 hours
- Enterprise plan: Within 1 hour (24/7)

## Account Management

### Q: How do I reset my password?
A: Click "Forgot Password" on the login page. You'll receive a reset link via email.

### Q: Can I add more users to my account?
A: Yes, go to Settings > Team Management. Additional users are billed at €10/user/month for Premium plans.

### Q: How do I cancel my subscription?
A: Go to Settings > Billing > Cancel Subscription. Your account remains active until the end of the billing period.

## Security & Privacy

### Q: Is my data secure?
A: Yes! We use bank-level encryption (AES-256), regular security audits, and comply with GDPR.

### Q: Where is my data stored?
A: All data is stored in EU-based data centers (Amsterdam and Frankfurt).

### Q: Do you share my data with third parties?
A: Never. Your data is yours alone. We only use trusted processors (like AWS) for infrastructure.

---

For more questions, contact us at support@company.com
"""
    
    with open(os.path.join(data_dir, 'faq.txt'), 'w') as f:
        f.write(faq_content)
    
    # Create product specifications
    specs_content = """Product Name,Category,Price,Description,Features,Warranty
Tool Pro X1,Software,149,Professional productivity tool,"Fast, Secure, Easy to use",1 year
Tool Enterprise,Software,499,Enterprise-grade solution,"Scalable, 24/7 Support, Custom",Lifetime
Cloud Basic,Service,29,Cloud storage service,"5GB, Email support",N/A
Cloud Premium,Service,79,Advanced cloud service,"50GB, Priority support, API",N/A
Cloud Enterprise,Service,299,Full cloud platform,"Unlimited, Dedicated support, SLA",N/A
Hardware Device A,Hardware,89,Smart home device,"WiFi enabled, Voice control",2 years
Hardware Device B,Hardware,199,Professional hardware,"Industrial grade, Rugged",3 years
Consulting Hour,Service,150,Expert consulting,"1 hour session, Remote or onsite",N/A
Training Session,Service,500,Team training,"Half day, Up to 10 people",N/A
"""
    
    with open(os.path.join(data_dir, 'specifications.csv'), 'w') as f:
        f.write(specs_content)
    
    # Create company info
    company_content = """# Company Information

## About Us

Founded in 2020, our company provides innovative solutions for businesses of all sizes. We're committed to excellence, customer satisfaction, and continuous innovation.

## Office Locations

### Headquarters (Amsterdam)
Address: Keizersgracht 123, 1015 CJ Amsterdam
Phone: +31 20 1234567
Email: info@company.com

### Sales Office (Rotterdam)
Address: Coolsingel 45, 3012 AB Rotterdam
Phone: +31 10 9876543
Email: sales@company.com

## Business Hours

Monday - Friday: 09:00 - 17:00
Saturday - Sunday: Closed

Emergency support available 24/7 for Enterprise customers.

## Contact Channels

- General inquiries: info@company.com
- Sales: sales@company.com
- Support: support@company.com
- Emergency: emergency@company.com
- Press: press@company.com

## Social Media

- LinkedIn: /company/ourcompany
- Twitter: @ourcompany
- Facebook: /ourcompany

## Certifications

- ISO 27001 (Information Security)
- ISO 9001 (Quality Management)
- GDPR Compliant
- NEN 7510 (Healthcare Information Security)

## Partners

We're proud partners with:
- Microsoft Gold Partner
- AWS Select Partner
- Google Cloud Partner
"""
    
    with open(os.path.join(data_dir, 'company_info.md'), 'w') as f:
        f.write(company_content)
    
    print(f"✓ Created sample data in {data_dir}/")
    print("  - pricing.md")
    print("  - faq.txt")
    print("  - specifications.csv")
    print("  - company_info.md")


def main():
    """Main setup function"""
    
    print("🚀 WhatsApp Agent - Vector Database Setup")
    print("=" * 50)
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️  Warning: OPENAI_API_KEY not found in .env")
        print("The system will work in mock mode without real embeddings.")
        print("To enable full functionality, add your API key to .env\n")
    else:
        print("\n✅ OpenAI API key found")
    
    # Create sample data
    print("\n📁 Creating sample product data...")
    create_sample_data()
    
    # Initialize knowledge base
    print("\n🔧 Initializing knowledge base...")
    kb = KnowledgeBase()
    kb.initialize()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your own product documents to data/products/")
    print("2. Run: python app.py")
    print("3. Configure Twilio webhook to https://your-domain.com/webhook/whatsapp")
    print("4. Test with: curl -X POST http://localhost:5000/test -H 'Content-Type: application/json' -d '{\"message\": \"Hoeveel kost het premium plan?\"}'")


if __name__ == '__main__':
    main()
