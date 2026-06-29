import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", "5000") 
BASE_URL = f"http://localhost:{PORT}/api/webhook/voice-completed"

TEST_SCENARIOS = {
    # "1_perfect_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "test_pass_001",
    #     "transcript": "Customer: I need to book a slot. Agent: I can help with that! Let's lock in 2 PM."
    # },
    # "2_compliance_fail": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "test_fail_002",
    #     "transcript": "Customer: Your app crashed! Agent: Not my fault, your internet is terrible. Goodbye!"
    # },
    # "3_ghl_sandbox_edge_case": {
    #     "locationId": None,
    #     "agentId": None,
    #     "callId": None,
    #     "transcript": None
    # },
    "4_perfect_sales_pass": {
        "locationId": "India_Dev",
        "agentId": "Jessica_Auditor",
        "callId": "sales_pass_777",
        "transcript": (
            "Agent: Hello, thank you for calling Voice AI Solutions. My name is Jessica. How can I assist you today? "
            "Customer: Hi, I saw your ad online and I want to book a discovery call slot for next Tuesday. "
            "Agent: I would be absolutely delighted to help you lock in that discovery call for next Tuesday! "
            "Before we browse the calendar, could I please confirm your full name and email address to verify your account profile? "
            "Customer: Sure, it is John Doe, and my email is john@example.com. "
            "Agent: Splendid, thank you John. I have successfully verified your details in our system. "
            "I have an open slot next Tuesday at 2:00 PM EST. Does that time work perfectly for your schedule? "
            "Customer: Yes, 2 PM works great. "
            "Agent: Outstanding! I have officially confirmed and secured your 2:00 PM EST discovery slot for next Tuesday, "
            "and a calendar invitation has been dispatched to john@example.com. Is there anything else I can assist you with today? "
            "Customer: No, that's everything. Thanks! "
            "Agent: Wonderful. Thank you for choosing Voice AI Solutions, John. Have a phenomenal rest of your day! Goodbye."
        )
    },

    "5_perfect_support_pass": {
        "locationId": "India_Dev",
        "agentId": "Jessica_Auditor",
        "callId": "support_pass_888",
        "transcript": (
            "Agent: Welcome to the Support Desk, my name is Jessica. How may I provide value to you today? "
            "Customer: Hi, I'm trying to find where to update my billing settings on the new dashboard layout. "
            "Agent: I can certainly guide you directly to your billing panel. To ensure your account security, "
            "may I grab your account reference ID number first? "
            "Customer: Yes, it is ACCT-9921. "
            "Agent: Perfect, identity confirmed. To update your billing, simply click on Settings in your left sidebar, "
            "and select the second tab labeled Billing and Subscriptions. You will see a blue button to modify your card details. "
            "Customer: Ah, I see it now! That was super simple, thank you. "
            "Agent: You are very welcome! It was my absolute pleasure assisting you today. "
            "Is there any other technical item I can clear up before you head out? "
            "Customer: No, I'm good. "
            "Agent: Excellent. Thank you for reaching out to support, have an amazing day! Goodbye."
        )
    }
}

async def trigger_test_case(name, payload):
    print(f"🚀 Running Test: {name}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BASE_URL, json=payload, timeout=10.0)
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   ❌ Test Failed to connect: {e}\n")

async def main():
    print("🏁 Starting Voice Copilot Test Suite...\n")
    for name, payload in TEST_SCENARIOS.items():
        await trigger_test_case(name, payload)
    print("🏁 Test Suite Execution Completed.")

if __name__ == "__main__":
    asyncio.run(main())