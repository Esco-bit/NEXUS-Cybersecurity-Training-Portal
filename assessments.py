
PHISHING_ASSESSMENT = {
    "title": "Phishing Investigation",
    "category": "Email Security",
    "difficulty": "Beginner to Advanced",
    "questions": [
        {
            "id": 1,
            "difficulty": "Beginner",
            "points": 10,
            "question": "An email claims your account will be suspended unless you verify your details immediately. What is the strongest warning sign?",
            "options": [
                "The email contains a company logo",
                "The sender creates urgency and demands immediate action",
                "The email has a subject line",
                "The email contains a greeting"
            ],
            "answer": 1,
            "explanation": "Urgency and pressure are common social engineering techniques. Investigate the sender and request through an independent trusted channel."
        },
        {
            "id": 2,
            "difficulty": "Beginner",
            "points": 10,
            "question": "A message comes from security@micros0ft-support.example. What should you investigate first?",
            "options": [
                "The font used in the email",
                "The number of paragraphs",
                "The sender domain and possible character substitution",
                "The email signature colour"
            ],
            "answer": 2,
            "explanation": "The zero in micros0ft may be an attempt at typosquatting. Examine the actual sender domain carefully."
        },
        {
            "id": 3,
            "difficulty": "Beginner",
            "points": 10,
            "question": "An email link displays the text https://company.example but its actual destination is https://company-login.attacker.example. What is the concern?",
            "options": [
                "The displayed text does not match the actual destination",
                "The link uses HTTPS",
                "The URL contains a slash",
                "The website has a login page"
            ],
            "answer": 0,
            "explanation": "The actual destination is a different subdomain. Never trust displayed link text without inspecting the real destination."
        },
        {
            "id": 4,
            "difficulty": "Intermediate",
            "points": 10,
            "question": "An email has SPF=fail, DKIM=none and DMARC=fail. What does this indicate?",
            "options": [
                "The email is definitely safe",
                "The email has passed all authentication checks",
                "There are multiple email authentication failures requiring investigation",
                "The recipient's computer is infected"
            ],
            "answer": 2,
            "explanation": "These results indicate authentication problems. They raise suspicion but do not independently prove phishing."
        },
        {
            "id": 5,
            "difficulty": "Intermediate",
            "points": 10,
            "question": "A user reports opening a suspicious attachment. What should a SOC analyst do first?",
            "options": [
                "Delete all files on the computer",
                "Collect relevant evidence and assess the endpoint for suspicious activity",
                "Ignore the report",
                "Immediately publish the incident online"
            ],
            "answer": 1,
            "explanation": "Preserve evidence and follow incident response procedures. Assess the endpoint and determine whether containment is necessary."
        },
        {
            "id": 6,
            "difficulty": "Intermediate",
            "points": 10,
            "question": "An email passes SPF and DKIM but contains a suspicious payment request from an executive. What is the best conclusion?",
            "options": [
                "It must be legitimate",
                "It cannot be phishing",
                "It requires further investigation despite passing authentication",
                "The email server is necessarily compromised"
            ],
            "answer": 2,
            "explanation": "Authentication checks do not guarantee that a message is legitimate. Business email compromise can involve authenticated accounts."
        },
        {
            "id": 7,
            "difficulty": "Advanced",
            "points": 10,
            "question": "A suspicious email has a valid sender domain, but its Reply-To address belongs to an unrelated external domain. What should you investigate?",
            "options": [
                "Only the email font",
                "Whether the Reply-To mismatch is authorized or indicates impersonation",
                "The recipient's screen resolution",
                "The email's file size only"
            ],
            "answer": 1,
            "explanation": "A mismatch between From and Reply-To can redirect responses to an attacker. Verify the sender through trusted channels."
        },
        {
            "id": 8,
            "difficulty": "Advanced",
            "points": 10,
            "question": "Several employees receive nearly identical credential-reset emails within five minutes. What is the strongest SOC response?",
            "options": [
                "Treat each email as unrelated",
                "Delete the emails without investigation",
                "Correlate the messages, identify recipients and investigate shared indicators",
                "Disable the entire company network immediately"
            ],
            "answer": 2,
            "explanation": "Correlating messages helps identify a coordinated phishing campaign. Investigate scope, indicators and affected users."
        },
        {
            "id": 9,
            "difficulty": "Advanced",
            "points": 10,
            "question": "An employee clicked a suspicious link but reports that they did not enter credentials. What should the analyst do?",
            "options": [
                "Close the incident immediately",
                "Investigate browser activity, redirects, downloads and endpoint telemetry",
                "Assume credentials were stolen",
                "Reinstall the operating system immediately"
            ],
            "answer": 1,
            "explanation": "A click can expose a user to malicious downloads or exploit attempts. Investigate available telemetry before determining impact."
        },
        {
            "id": 10,
            "difficulty": "Advanced",
            "points": 10,
            "question": "A phishing investigation confirms a malicious email was delivered to 40 employees. What is the best next action?",
            "options": [
                "Investigate scope, preserve evidence, coordinate removal and follow incident response procedures",
                "Ignore the other recipients",
                "Delete the mail server",
                "Assume everyone entered their password"
            ],
            "answer": 0,
            "explanation": "Determine exposure, identify affected recipients, remove malicious messages where possible and coordinate containment and response."
        }
    ]
}
