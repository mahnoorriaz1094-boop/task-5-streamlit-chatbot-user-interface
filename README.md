# task-5-streamlit-chatbot-user-interface
## Features

- Chat interface with input box and response area
- CoreTech branding and a professional dark-themed layout
- Sidebar showing contact information (support, security, billing)
- Suggested questions for quick access
- Answers covering all CoreTech services: cloud, cybersecurity, software development, AI/ML, pricing, support, DevOps, and more
- Handles unrecognized questions with a fallback response

## Sample Questions

- What is CoreTech?
- What cloud services does CoreTech provide?
- How much does it cost?
- Does CoreTech offer AI and machine learning services?
- How can I contact support?

## Contact Information

- Support: support@coretech.io
- Security: security@coretech.io
- Billing: billing@coretech.io
- Phone: 1-800-CORETECH

## Screenshots

### Main Page
![Main Page](screenshots/app_main.png)

### Chat Conversation
![Chat](screenshots/app_chat.png)

### Sidebar with Contact Info
![Sidebar](screenshots/app_sidebar.png)

## Tech Used

- Python
- Streamlit
- Pandas
- difflib

## Notes

This was built as part of my internship tasks to practice converting a Python script into an interactive web application. The chatbot logic remains rule-based (no external AI model used) and relies entirely on the FAQ dataset provided in `coretech_faq.csv`.
