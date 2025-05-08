# littlebits-notprodready-testedsuccessfully-withprodends
littlebits-notprodready-testedsuccessfully-withprodends

# Team Name
Littlebits

## Overview
Welcome to our Agentic AI Incubation project submission! This repository houses the code and documentation for our cutting-edge solution.

SecureRide - Optimizes vehicle operations by leveraging AI to read calendar events and suggest trip plans, stops, route plans, and recommended safety measures.
ThreatAlertSystem - Enhances vehicle theft security by suggesting actions based on threat levels detected through steering fingerprints, facial recognition, door status, motion detection, and more. Currently using an IoT simulator, it will be upgraded for full IoT integration in the future.

Resulting in
- Improve decision-making for vehicle operations to automatically turn on/ suggest vechile set seat heating, switch on AC etc.
- Provide personalized recommendations for routes, stops, and vehicle safety suggestions.
- Ensure vehicle security through advanced AI monitoring.

## Explanation
Our project leverages cutting-edge technologies such as below to create web based AI-driven vechile assistant.
•	Flask,
•	Next.js,
•	Azure Cognitive Services
•	Semantic Kernel
to create a seamless web-based AI-driven vehicle assistant. The core functionality includes:
- Feature 1: Intelligent vehicle optimization based on user iuser query , calendar events, preferences, weather, and agenda.Suggests to set vechile seat heating based on decision making and weather extracted from weather API.
- Feature 2: Real-time route planning and stopover suggestions for energy efficiency.
- Feature 3: Advanced vehicle security monitoring and control using Semantic Kernel which integrates iot hub simulator to take required actions on owner vechile theft analysis , it takes actions like vechile locking, email alrets etc.

## Intent
The primary intent of our project is to provide a smart, AI-driven in-car assistant that enhances user comfort, safety, and efficiency. We aim to:
- Improve decision-making for vehicle operations to automatically turn on seat heating, AC etc.
- Provide personalized recommendations for routes, stops, and vehicle safety suggestions.
- Ensure vehicle security through advanced AI monitoring.

## Use Case
Assigned Industry Use Case: Automotive and Smart Mobility

Our solution leverages Flask, Next.js, Azure Cognitive Services, and Semantic Kernel to create a seamless web-based AI-driven vehicle assistant. It intelligently optimizes vehicle settings based on user queries, calendar events, preferences, weather, and agenda, suggesting actions like seat heating adjustments. It also provides real-time route planning and stopover suggestions for energy efficiency. Additionally, it enhances vehicle security through AI-driven monitoring and alerts, utilizing an IoT hub simulator for actions like vehicle locking and email notifications. This innovative use of generative AI ensures a smarter, safer, and more efficient driving experience.

## Contributors
This project was developed by a dedicated team of contributors:
- Littlebits Team

## Images

## Implementation
### Backend (`routes.py` and `vehicle_security_routes.py`)
- `routes.py`: Implements the vehicle optimization API using Flask. It integrates Azure Cognitive Services for sentiment analysis and key phrase extraction, Foundry AI for decision-making, and utility functions for vehicle preparation and seat heating adjustments.
- `vehicle_security_routes.py`: Provides APIs for vehicle security monitoring using Semantic Kernel. It includes endpoints for detecting anomalies and generating security alerts.

### Frontend (`app/page.tsx` and `semantic-kernel-vehicle-security/page.tsx`)
- `app/page.tsx`: Implements the main dashboard for vehicle optimization using Next.js. It provides a user-friendly interface for viewing AI recommendations, route plans, and vehicle settings.
http://localhost:3000/
- `semantic-kernel-vehicle-security/page.tsx`: Implements the vehicle security monitoring dashboard. It displays real-time security alerts and allows users to take corrective actions.
http://localhost:3000/semantic-kernel-vehicle-security

### Architecture
1. Frontend: Built with Next.js for a responsive and interactive user experience.
2. Backend: Flask APIs handle AI integrations and business logic.
3. AI Services: Azure Cognitive Services for NLP tasks, Foundry AI for decision-making, and Semantic Kernel for advanced reasoning.
4. Data Flow: User inputs are processed by the backend, which interacts with AI services and returns actionable insights to the frontend.

### Design Decisions
- Azure Cognitive Services: Chosen for its robust NLP capabilities.
- Semantic Kernel: Used for advanced reasoning and vehicle security monitoring.
- Next.js: Selected for its server-side rendering and seamless integration with APIs.

## Additional Information
- Future Plans: Extend the solution to support voice commands and integrate with IoT devices for real-time vehicle telemetry.
- Known Issues: Limited support for non-English languages in NLP tasks.
- Acknowledgments: Special thanks to the Azure AI team for their support and resources.


**steps to execute : BOTH front-end and back-end runs on endpoints**

PS \prod_ready_littlebits\littlebits\back-end-py> python main.py

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img1.png)

PS \prod_ready_littlebits\littlebits\front-end-nextjs> npm run dev      

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img2.png)

**Here is the code to test vechile-optimisation**

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img3.png)

**Results:**

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img4.png)

**The vechile security Page is as below with sematic-kernel implementation:**

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img5.png)

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img6.png)

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img7.png)

**Results:** Negative Test Case

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img8.png)

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img9.png)

**Results:**  Positive Test Case

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img10.png)

![Alt text](https://github.com/AI-Agent-Incubator-Month/littlebits-notprodready-testedsuccessfully-withprodends/blob/main/img11.png)

