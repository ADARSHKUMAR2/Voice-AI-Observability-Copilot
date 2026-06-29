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
    },
    
    "6_appointment_booking_pass": {
        "locationId": "India_Dev",
        "agentId": "Jessica_Auditor",
        "callId": "booking_pass_992",
        "transcript": (
            "Agent: Thanks for calling Apex Chiropractic! Are you looking to book an adjustment today? "
            "Customer: Yes, please. I'm a new patient, my back has been killing me all week. "
            "Agent: I'm sorry to hear that, let's get you taken care of. I have an opening tomorrow, Tuesday at 2:00 PM, or Wednesday morning at 10:00 AM. Do either of those work? "
            "Customer: Tuesday at 2:00 PM works perfectly fine. "
            "Agent: Great! I've locked in Tuesday at 2:00 PM for you. I just sent a confirmation text to this phone number with our intake form link. Is there anything else I can help you with? "
            "Customer: No, that's all. Thank you so much. "
            "Agent: You're very welcome! Have a wonderful day and we'll see you tomorrow. Goodbye."
        )
    },

    "7_objection_handling_pass": {
        "locationId": "India_Dev",
        "agentId": "Jessica_Auditor",
        "callId": "objection_pass_883",
        "transcript": (
            "Agent: Hey Alex, just following up on the SaaS demo we did yesterday. Ready to get your team onboarded? "
            "Customer: Look, I like the platform, but $500 a month is just way too expensive for our current budget right now. "
            "Agent: I completely understand, Alex. $500 is a real investment. But let's look at the numbers from your trial—automating those 15 manual database hours saves your team roughly $1,200 a week in developer time. The system essentially pays for itself in the first 4 days. "
            "Customer: Hmm. When you put it that way, the math makes sense. But do I have to sign a yearly contract? "
            "Agent: Not at all. We can start you on a month-to-month plan today so you can measure the raw performance yourself before locking anything in. Should we set up the billing profile? "
            "Customer: Yeah, let's do the month-to-month. Let's do it. "
            "Agent: Perfect, let's get you set up. Have an amazing day! Goodbye."
        )
    },

    "8_support_deescalation_pass": {
        "locationId": "India_Dev",
        "agentId": "Jessica_Auditor",
        "callId": "deescalation_pass_441",
        "transcript": (
            "Customer: This is ridiculous! Your app crashed right in the middle of my client presentation and I lost my entire unsaved slide deck! I want a refund immediately! "
            "Agent: I am incredibly sorry to hear that, and I completely understand why you're furious. Losing client work during a presentation is completely unacceptable, and I would be just as upset if I were in your shoes. Let me see how I can make this right immediately. "
            "Customer: Fine. But can I even get my data back or is it gone forever? "
            "Agent: Good news—our cloud engine automatically saves a local backup state every 60 seconds. I am looking at your account right now, and I can see your cached deck snapshot labeled Presentation_Backup. I've just forced it to sync back to your dashboard live. "
            "Customer: Wait, really? Let me check... Oh thank goodness, it's back. Wow, okay. Thank you. "
            "Agent: You are so welcome. I'm also applying a one-month service credit to your account for the trouble. Is there anything else I can double-check to protect your work today? "
            "Customer: No, that's amazing. I appreciate you fixing this so fast. "
            "Agent: Excellent. Thank you for reaching out to support, have a phenomenal rest of your day! Goodbye."
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