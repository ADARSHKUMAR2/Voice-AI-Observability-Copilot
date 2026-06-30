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
    # "4_perfect_sales_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "sales_pass_777",
    #     "transcript": (
    #         "Agent: Hello, thank you for calling Voice AI Solutions. My name is Jessica. How can I assist you today? "
    #         "Customer: Hi, I saw your ad online and I want to book a discovery call slot for next Tuesday. "
    #         "Agent: I would be absolutely delighted to help you lock in that discovery call for next Tuesday! "
    #         "Before we browse the calendar, could I please confirm your full name and email address to verify your account profile? "
    #         "Customer: Sure, it is John Doe, and my email is john@example.com. "
    #         "Agent: Splendid, thank you John. I have successfully verified your details in our system. "
    #         "I have an open slot next Tuesday at 2:00 PM EST. Does that time work perfectly for your schedule? "
    #         "Customer: Yes, 2 PM works great. "
    #         "Agent: Outstanding! I have officially confirmed and secured your 2:00 PM EST discovery slot for next Tuesday, "
    #         "and a calendar invitation has been dispatched to john@example.com. Is there anything else I can assist you with today? "
    #         "Customer: No, that's everything. Thanks! "
    #         "Agent: Wonderful. Thank you for choosing Voice AI Solutions, John. Have a phenomenal rest of your day! Goodbye."
    #     )
    # },

    # "5_perfect_support_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "support_pass_888",
    #     "transcript": (
    #         "Agent: Welcome to the Support Desk, my name is Jessica. How may I provide value to you today? "
    #         "Customer: Hi, I'm trying to find where to update my billing settings on the new dashboard layout. "
    #         "Agent: I can certainly guide you directly to your billing panel. To ensure your account security, "
    #         "may I grab your account reference ID number first? "
    #         "Customer: Yes, it is ACCT-9921. "
    #         "Agent: Perfect, identity confirmed. To update your billing, simply click on Settings in your left sidebar, "
    #         "and select the second tab labeled Billing and Subscriptions. You will see a blue button to modify your card details. "
    #         "Customer: Ah, I see it now! That was super simple, thank you. "
    #         "Agent: You are very welcome! It was my absolute pleasure assisting you today. "
    #         "Is there any other technical item I can clear up before you head out? "
    #         "Customer: No, I'm good. "
    #         "Agent: Excellent. Thank you for reaching out to support, have an amazing day! Goodbye."
    #     )
    # },
    
    # "6_appointment_booking_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "booking_pass_992",
    #     "transcript": (
    #         "Agent: Thanks for calling Apex Chiropractic! Are you looking to book an adjustment today? "
    #         "Customer: Yes, please. I'm a new patient, my back has been killing me all week. "
    #         "Agent: I'm sorry to hear that, let's get you taken care of. I have an opening tomorrow, Tuesday at 2:00 PM, or Wednesday morning at 10:00 AM. Do either of those work? "
    #         "Customer: Tuesday at 2:00 PM works perfectly fine. "
    #         "Agent: Great! I've locked in Tuesday at 2:00 PM for you. I just sent a confirmation text to this phone number with our intake form link. Is there anything else I can help you with? "
    #         "Customer: No, that's all. Thank you so much. "
    #         "Agent: You're very welcome! Have a wonderful day and we'll see you tomorrow. Goodbye."
    #     )
    # },

    # "7_objection_handling_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "objection_pass_883",
    #     "transcript": (
    #         "Agent: Hey Alex, just following up on the SaaS demo we did yesterday. Ready to get your team onboarded? "
    #         "Customer: Look, I like the platform, but $500 a month is just way too expensive for our current budget right now. "
    #         "Agent: I completely understand, Alex. $500 is a real investment. But let's look at the numbers from your trial—automating those 15 manual database hours saves your team roughly $1,200 a week in developer time. The system essentially pays for itself in the first 4 days. "
    #         "Customer: Hmm. When you put it that way, the math makes sense. But do I have to sign a yearly contract? "
    #         "Agent: Not at all. We can start you on a month-to-month plan today so you can measure the raw performance yourself before locking anything in. Should we set up the billing profile? "
    #         "Customer: Yeah, let's do the month-to-month. Let's do it. "
    #         "Agent: Perfect, let's get you set up. Have an amazing day! Goodbye."
    #     )
    # },

    # "8_support_deescalation_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "deescalation_pass_441",
    #     "transcript": (
    #         "Customer: This is ridiculous! Your app crashed right in the middle of my client presentation and I lost my entire unsaved slide deck! I want a refund immediately! "
    #         "Agent: I am incredibly sorry to hear that, and I completely understand why you're furious. Losing client work during a presentation is completely unacceptable, and I would be just as upset if I were in your shoes. Let me see how I can make this right immediately. "
    #         "Customer: Fine. But can I even get my data back or is it gone forever? "
    #         "Agent: Good news—our cloud engine automatically saves a local backup state every 60 seconds. I am looking at your account right now, and I can see your cached deck snapshot labeled Presentation_Backup. I've just forced it to sync back to your dashboard live. "
    #         "Customer: Wait, really? Let me check... Oh thank goodness, it's back. Wow, okay. Thank you. "
    #         "Agent: You are so welcome. I'm also applying a one-month service credit to your account for the trouble. Is there anything else I can double-check to protect your work today? "
    #         "Customer: No, that's amazing. I appreciate you fixing this so fast. "
    #         "Agent: Excellent. Thank you for reaching out to support, have a phenomenal rest of your day! Goodbye."
    #     )
    # },

    # "9_lead_qualification_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "lead_pass_112",
    #     "transcript": (
    #         "Agent: Thank you for calling Elite Roofing Systems. My name is Jessica. Are you looking to get a quote for a repair or a full replacement today? "
    #         "Customer: Hi, yes, we had some major hail last night and my ceiling is starting to spot in the living room. I need someone to look at it. "
    #         "Agent: Oh dear, structural leaks can be incredibly stressful. Let's get a technician out to patch that up. Before I check availability, are you the primary homeowner listed on the deed? "
    #         "Customer: Yes, I am. My husband and I own the house. "
    #         "Agent: Perfect. And can I grab your full address so I can map the property layout? "
    #         "Customer: Sure, it is 742 Evergreen Terrace. "
    #         "Agent: Excellent, I have located your property. I am checking our regional calendar now, and I can have an inspector over tomorrow between 9:00 AM and 11:00 AM to document the damage for your insurance claim. Does that time block work for you? "
    #         "Customer: Yes, tomorrow morning works great. My husband will be home. "
    #         "Agent: Spectacular! I have scheduled your inspection window for tomorrow morning. I am sending a text confirmation with your inspector's profile right now. Is there any other leak location I should note down? "
    #         "Customer: No, that's the main one. Thank you. "
    #         "Agent: Perfect. Thank you for choosing Elite Roofing Systems. Have a safe and wonderful day! Goodbye."
    #     )
    # },

    # "10_compliance_missing_fail": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "compliance_fail_223",
    #     "transcript": (
    #         "Agent: Thanks for dialing the HVAC Hot Line! This is Jessica. How can I help your system today? "
    #         "Customer: Hi, my air conditioner is blowing warm air and it is 95 degrees inside my house right now. "
    #         "Agent: Wow, that sounds completely miserable. Let's get that fixed immediately. I can send a diagnostic specialist to your house today at 4:00 PM. Would you like me to book that slot? "
    #         "Customer: Yes! Please save that slot for me. "
    #         "Agent: Awesome, you are all locked in for 4:00 PM today. Our tech will be there. "
    #         "Customer: Wait, don't you need my name, address, or phone number to know where to go? "
    #         "Agent: Oh, don't worry about it, we will figure it out! See you at 4:00 PM! Goodbye."
    #     )
    # },

    # "11_handling_rant_detour_pass": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "rant_pass_334",
    #     "transcript": (
    #         "Agent: Hello, thank you for reaching out to Radiant MedSpa. This is Jessica. How can I guide your skincare journey today? "
    #         "Customer: Hi, I want to book a laser facial, but honestly I am so distracted because my golden retriever just ate an entire sleeve of chocolate chip cookies and I've been frantic all morning! "
    #         "Agent: Oh my goodness! I completely understand how terrifying that is—dogs are family! Please make sure to call the emergency vet line if he shows any symptoms. If you need to drop off the line to take care of him, we can completely handle this later. "
    #         "Customer: Oh, thank you so much for saying that. The vet actually said he should be fine since they were milk chocolate, so I can breathe now. Let's do the facial. "
    #         "Agent: What a massive relief! I am so glad he is safe. Now, let's get you pampered to wash away that morning stress. Have you ever received a laser treatment at our clinic before, or will this be your first visit? "
    #         "Customer: This will be my first time here. "
    #         "Agent: Wonderful! To secure your initial consultation and facial profile, could I please get your full name and email address? "
    #         "Customer: Yes, it's Clara Oswald, and my email is clara@example.com. "
    #         "Agent: Splendid, Clara. I have initialized your new customer account. I have an open slot this Friday afternoon at 3:30 PM. Does that give you enough time to wind down your week? "
    #         "Customer: Yes, Friday at 3:30 PM is perfect. "
    #         "Agent: Beautiful. Your appointment is confirmed, and your welcome packet has been emailed to clara@example.com. Give your pup a hug for us, and we will see you on Friday! Goodbye."
    #     )
    # },

    # "12_booking_cutoff_fail": {
    #     "locationId": "India_Dev",
    #     "agentId": "Jessica_Auditor",
    #     "callId": "cutoff_fail_556",
    #     "transcript": (
    #         "Agent: Welcome to Nexus Solar Support. My name is Jessica. How can I help maximize your solar savings today? "
    #         "Customer: Hi, I got a mailer saying my roof qualifies for a zero-down panel installation, and I wanted to see if that's true. "
    #         "Agent: I would be delighted to analyze your grid parameters for the zero-down program! To check eligibility, what was your average electric bill layout last month? "
    #         "Customer: It was around $180, mostly because we run the pool pump all day long. "
    #         "Agent: Perfect, $180 is the sweet spot for maximum savings. Let's get an engineer to design a custom tier layout for your property. I have a consultation opening tomorrow at 1:00 PM. Does that work? "
    #         "Customer: Let me check my work calendar... Actually, 1:00 PM doesn't work. Do you have anything later in the evening, maybe after 5:00 PM? "
    #         "Agent: No, I don't feel like checking the evening slots. Goodbye."
    #     )
    # },

    "13_booking_cutoff_fail": {
        "locationId": "USA",
        "agentId": "AdarshK",
        "callId": "cutoff_fail_534434wew6",
        "transcript": (
            "Agent: Welcome to Nexus Solar Support. My name is Adarsh. How can I help maximize your solar savings today? "
            "Customer: Hi, I got a mailer saying my roof qualifies for a zero-down panel installation, and I wanted to see if that's true. "
            "Agent: I would be delighted to analyze your grid parameters for the zero-down program! To check eligibility, what was your average electric bill layout last month? "
            "Customer: It was around $180, mostly because we run the pool pump all day long. "
            "Agent: Perfect, $180 is the sweet spot for maximum savings. Let's get an engineer to design a custom tier layout for your property. I have a consultation opening tomorrow at 1:00 PM. Does that work? "
            "Customer: Let me check my work calendar... Actually, 1:00 PM doesn't work. Do you have anything later in the evening, maybe after 5:00 PM? "
            "Agent: No, I don't feel like checking the evening slots. Goodbye."
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