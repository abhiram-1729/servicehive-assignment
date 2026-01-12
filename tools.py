def mock_lead_capture(name: str, email: str, platform: str):
    """
    This is a mock function that simulates pushing lead data into our CRM.
    In a production environment, this would call an API like Salesforce or HubSpot.
    
    Args:
        name: The customer's full name.
        email: Their primary contact email.
        platform: The social media platform they use (YouTube, Instagram, etc.).
    """
    # Simply logging the data to the console for demonstration purposes
    print(f"\n[SYSTEM] Lead captured: {name} | {email} | {platform}")
    
    # Returning a confirmation message that the AI can use to acknowledge the user
    return f"Success: Lead for {name} ({email}) on {platform} has been recorded in the CRM."
