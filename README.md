# SECTION 1 : PROJECT TITLE
### Singapore Event Finder Chatbot.
![logo](resources/event-finder.png)

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
write something here about the project?

# SECTION 3 : CREDITS / PROJECT CONTRIBUTION
| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| |  | Business idea generation, UI Design | @u.nus.edu |
| TEA LEE SENG | A0198538J | Business idea generation, Google Assistant UI, API integration, Recommendation module | e0402079@u.nus.edu / TEALEESENG@gmail.com |
| NG SIEW PHENG | A0198525R  | Google Assistant UI, Search Event intent module, project video | e0402066@u.nus.edu |
| |  | Business idea generation, KIE server design, OptaPlanner rules, Overall integration | @u.nus.edu |
| |  | Business idea generation, domain expert interview, data gathering and preparation, project report | @u.nus.edu |

# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO
SGEventFinderChatbot.mp4

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


To run Dialogflow agent,
1. create a new Dialogflow agent.
2. import ISS-Singapore-Events-Finder-xxxxx.zip into agent.
3. Update Fulfillment Webhook url. Takes https URL.
4. on Google Assistant, says "Talk to my test app"


# SECTION 6 : PROJECT REPORT / PAPER


# SECTION 7 : MISCELLANEOUS

as per https://github.com/IRS-RS/IRS-RS-2019-03-09-IS1PT-GRP-YOSS

sample markup, https://raw.githubusercontent.com/IRS-RS/IRS-RS-2019-03-09-IS1PT-GRP-YOSS/master/README.md
