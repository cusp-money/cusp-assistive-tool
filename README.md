# Cusp Money - An Assistive Tool for RIAs - A step towards financial inclusion.

Cusp Money connects you with Registered Investment Advisors who provide personalized financial advice in your preferred regional language. Our process is secure and tailored to your needs.

This repo was open sourced as part of [Sahamati BuildAAthon 2024](https://sahamati-buildaathon-2024.devfolio.co/overview).

## How It Works?
1. **Secure Data Sharing:** Share your financial data through an RBI-registered account aggregator.
2. **Personalized Interaction:** Have a 1:1 conversation with our CuspAI voice assistant to help advisors understand your needs closely.
3. **Expert Advice:** Our RIA uses your data and conversation insights to provide you with customized advice.
4. **Ongoing Support:** If you have questions or wish to discuss the advice, you can connect with CuspAI again for further clarification – as many times as needed.

## Structure of the code

There are two main services:

1. **Onboarding portal** - A streamlit app which uses saafe account aggregator and SahamatiNet proxy APIs to securely fetch user's financial accounts data and summarizes that into google doc.
2. **Voice call assistant** - A twilio based call assistant build around SarvamAI's regional language processing APIs and gemini's LLM APIs to interact with the user in a friendly and engaging manner requesting required information for advice and solving user's doubts when advice is available in the google doc.  

## Getting started

### Commands to start services

1. Start user onboarding app using following command:
   
   ```
   streamlit run app_user_onboarding.py --server.port 8080
   ```

2. Start voice assistant server to handle incoming voice calls using following command:
   
   ```
   python -m app_voice_assistant
   ```

3. Start the sahamati rahasya server

   ```
   docker run -p 8888:8080 gsasikumar/forwardsecrecy:V1.2
   ``` 


### Adding mock data

You can create a mock entity, populate it with data, and retrieve responses by specifying the scenario in the header.

1. Create the Mock Entity

   Refer to the documentation for detailed guidance: [Customisation of Mock Entity and Responses](https://developer.sahamati.org.in/technical-specifications/routerapi-specs/integration-using-simulator/customisation-of-mock-entity-and-responses)

2. Add Customised Responses to the Mock Entity

   For instructions on setting up customised responses, see: [Custom Responses Usage](https://developer.sahamati.org.in/technical-specifications/routerapi-specs/integration-using-simulator/custom-responses-usage.)

   We have provided a script to add mock data in the Sahamati AA simulator, run this command:

   ```
   python -m scripts.add_mock_responses_in_aa_simulator
   ```

