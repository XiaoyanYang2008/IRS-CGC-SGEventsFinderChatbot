# SECTION 1 : PROJECT TITLE
### Singapore Event Finder Chatbot.
![logo](resources/event-finder.png)

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Singapore is one of the most popular tourist destinations in Asia. Most tourists are exposed to the typical tourist attractions like Sentosa and Zoo. Event Finda provides a unique range of events happening in Singapore, from exhibition for kids to dine & wine events for adults. However, their website is not the easiest to navigate and to find the events that are of interest to visitors.

This chatbot agent is created to introduce these unique events to tourists in a more interactive way. Tourists can ask the chatbot to find them event based on keywords. Based on the keywords provided by the tourists, our chatbot is also capable of recommending other events that the tourists might be interested in, based on their search so far with the chatbot. Even locals can ask our chatbot for event recommendation. 

Creation of the dialog intent with a good list of training phrases, has been a never ending task as we test proof the agent. We found that if we keep the training phrase too simple, the DialogFlow is unable to clearly identify the correct intent, often end up triggering the wrong intent. If we added too many entities in a single phrase, Dialogflow can’t match the intent and end up in the fallback intent.

The next biggest challenge is the integration to Google assistant. Documentation from both DialogFlow and Actions on Google is not detailed enough. And the lack of documentation for DialogFlow V2 API is also causing us a lot of time in debugging the code, instead of training our chatbot.

Eventually, we managed to get the basics working and able to successfully deploy a working chatbot agent. There are still test scenarios where the chatbot is unable to detect the intent. With more time, we can enhance the agent.


# SECTION 3 : CREDITS / PROJECT CONTRIBUTION
| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| TEA LEE SENG | A0198538J | Business idea generation, Google Assistant UI, API integration, Recommendation module | e0402079@u.nus.edu / TEALEESENG@gmail.com |
| NG SIEW PHENG | A0198525R  | Google Assistant UI, Search Event intent module, project video | e0402066@u.nus.edu |
| YANG XIAOYAN| A0056720L | Business idea generation, Google Assistant UI, API integration, Weather module, project report and video| e0401594@u.nus.edu |
| Tarun Rajkumar | A0198522X | Business idea generation, Google Assistant UI, data gathering and preparation, project report | e0402063@u.nus.edu |

# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO
SGEventFinderChatbot.mp4 - https://drive.google.com/file/d/1aH8vi-anz7sLB1W0GdiFZqQOuSOOSJ1i/view?usp=sharing

# SECTION 5 : USER GUIDE
1. Download the zip file and import the agent to your Dialogflow account.
2. Make sure Agent's Fulfilment Webhook url is pointing to https://www.tealeeseng.com/chat/
3. Try on "See how it works in Google Assistant." link. note: test console will not response as it doesn't provide features to meet our need, e.g. displaying images. 

## Developer Guide

To run Webhook server.
1. python3 -m venv IRS
2. source IRS/bin/activate
3. git clone https://github.com/XiaoyanYang2008/IRS-CGC-SGEventsFinderChatbot
4. cd IRS-CGC-SGEventsFinderChatbot
5. pip3 install -r webapp/requirements.txt
6. cd webapp/
7. python3 server.py
8. In another terminal, ./ngrok http 5001 
   for Dialogflow Fulfillment Webhook url. Take https ngrok URL as Google Assistant demand https channel. 
9. To debug, 
    - kill server.py at step 7, and 
    - runs pycharm community edition. 
    - open project on folder, IRS-CGC-SGEventsFinderChatbot. 
    - Mark webapps folder as Source Root, 
    - setup Project Interpreter with existing VirtualEnv" 
    - debug server.py
    - note: uses pycharm 2019.1.x. pycharm 2019.2.x needs to comments out server.py in pydevd_dont_trace_files.py under pycharm program folder. Refers bug report, https://youtrack.jetbrains.com/issue/PY-37609


To run Dialogflow agent,
1. create a new Dialogflow agent.
2. import ISS-Singapore-Events-Finder-xxxxx.zip into agent.
3. Update Fulfillment Webhook url. Takes https URL.
4. on Google Assistant, says "Talk to my test app"



