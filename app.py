import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import predict
from flask_cors import CORS
import json
import random
import requests

# coding=utf8

app = Flask(__name__)
CORS(app)
answer = {}
baseIntent = 'welcome'
intent = ''

healthtips = """Establish regular exercise routines in your life.\nContinue to work on eating healthily; vigilance will always be needed to be successful.\nSee your doctor regularly for wellness exams and health/disease screenings/tests.\nIf you have symptoms, seek medical attention; don’t ignore warning signs of issues.\nAlong with your body, make efforts to stimulate and strengthen your brain as you age.\nMaintain satisfying social relationships.\nKeep involved in activities and pursuits that interest you.\nTry to maintain a positive attitude to support your resilience when life hands you setbacks.\nKeep your body hydrated with water.\nAvoid toxins and unhealthy environments.\nTake care of your skin.\nKnow your health numbers and what they mean, regardless of how healthy or unhealthy you are now.\nGet adequate sleep.\nSpend less time in front of the TV; at minimum, get up and move during commercials.\nLearn to relax more.\nFocus less on your weight, and more on your overall health.\nFind things to be grateful for in your life.\nDon’t forget to smile and laugh routinely.\nDo something fun every day.\nHave a sense of purpose in your life.\nLet go of the past, focus on what you can do to improve your present and future.\nGive your focused attention on what you can do to address your most unhealthy habit.\nRemind yourself it takes time and patience to change ingrained habits.\nKnow your family health history.\nEat a variety of foods, especially fruits and vegetables.\nLimit your use of alcohol.\nDon’t forget your dental health.\nDon’t forget your eye health.\nContinue to educate yourself about overall health and wellness, over time new findings result in updated recommendations from health experts.\nReplace bad habits with good ones.\nLearn to cook healthy foods you enjoy.\nLearn to modify recipes you love to make them more nutritious.\nAllow yourself to splurge periodically on special foods in limited quantities or frequencies.\nSlip vegetables into your favorite recipes.\nMake sure you get some good fats in your diet.\nStretch your body every day.\nEat more fish.\nStart each day with a healthy breakfast.\nSpend some time in solitude on a regular basis.\nWash your hands often.\nFocus on eating whole-grains when you eat bread products.\nMake sure that the protein foods you eat are leaner versions.\nDevelop a ‘gentle firmness’ with yourself; be kind but honest in your mental ‘self talk’.\nRemember that small changes can really add up and lead to big results.\nTry to eat more natural/raw/core foods, and less processed food.\nTry to eat a variety of food ‘colors’.\nTry to eat more volume and fewer calories in your diet.\nExperiment with food combinations and spices to see what you like.\nReward yourself for your positive efforts in ways that do not involve food whenever possible.\nEnjoy your food, take time to sit down and concentrate on what you are eating.\nWatch salt, sugar, harmful fats and other additive levels in your food.\nConsider taking vitamins and other supplements as recommended by your doctor or pharmacist.\nWhen someone asks you what you would like for a gift, be ready with a healthy idea.\nWrite down your health goals and prioritize them.\nTrack your progress on health goals so you have feedback to review.\nHave realistic expectations for yourself and your body.\nCompete only with yourself, not others.\nLook for healthy role models in your life.\nAsk for tips or advice from people in your life who are healthy and/or struggling with similar challenges.\nDevelop healthy rituals but be prepared to be flexible as needed.\nPlan and allow time for you to keep up with your healthy habits and routines.\nDon’t forget portion control.\nConcentrate of keeping your body strong and flexible.\nSeek to resolve nagging problems in your life.\nAccept the things in your life that you cannot change.\nDo something for others just because you can.\nTry to be spontaneous or try something new each week.\nGravitate towards healthy people whenever possible.\nUse your support systems.\nExpect setbacks and plan for them if possible.\nTake your medications as prescribed and report side effects to your physician.\nMake sure your physician(s) have complete information about your health.\nTake breaks during your work day.\nLearn to breathe properly.\nDon’t engage in wishful thinking about your health; take action, even small steps, as soon as you can to get going towards a healthier you.\nIf you are ill or have an injury, rest and/or get treatment.\nUse trusted websites for excellent health advice and/or recipes.\nListen to your body.\nAre you already managing a specific condition, like diabetes or arthritis? Read up on what you can continue to do to mitigate progression of the condition through any lifestyle changes.\nWatch the level of over the counter medications you use.\nMake sure you understand contraindications and/or interactions for any medication you take or conditions you have, including improper mixing of meds and other meds and/or food.\nJoin a health related class or program, a great way to get new ideas/tips and/or supports.\nCarry healthy snacks with you.\nRead nutrition labels regularly.\nGet rid of excess clutter in both your physical and mental world.\nStop doing what doesn’t work for you, and keep doing what does work for you.\nBe willing to try a new sport or physical activity at least once to see if you would enjoy it.\nDevelop an array of exercise and physical activity options in your life to keep active.\nKnow the key nutritious healthy or ‘super’ foods and include them in your diet.\nKeep educating yourself about health update information.\nRemember that while you may have your own health challenges, you are likely someone else’s role model in some aspect of their life.\nMake yourself ‘work’ for a special food through an exercise ‘payment’ first; you may find after the exercise you really don’t want the food.\nUnderstand that - as with all important aspects of life - being healthy will take some work and effort on your part and it will be worth it over the long haul.\nConsider rewarding yourself with cash; save up what you would have spent on unhealthy foods or tobacco and use the money to purchase something you would really love.\nWhenever you need to do so, just start over fresh, at the next meal, the next day, the next month, the next year, whichever comes first for you.\nUnderstand that being healthy or unhealthy is a choice you get to make continually through many daily decisions.\nThe more you develop other interests and activities in your life, the less appealing over eating or inactivity will be for you.\nThe way out of any rut is simple, just do it; get started in any way that you can.\nPost reminders, incentives or inspiration for yourself to see to help support your goals.\nDon’t ever give up on efforts to improve your health."""


@app.route('/')
def home():
    return "Welcome"


@app.route('/getResponse')
def getResponse():
    obj = request.args.get('object')
    obj = json.loads(obj)
    intent = obj['intent']
    text = obj['query']
    print(text)
    answer['response'], answer['intent'] = predict.chatbot_response(text)

    return jsonify(answer)


@app.route('/getAlternate')
def getAlternate():
    obj = request.args.get('object')
    obj = json.loads(obj)
    intent = obj['intent']

    tosend = {}

    if intent == 'medicine.alternate':
        query = obj['query']

        alternates = predict.findAlternate(query)
        seperator = '\n'
        altStr = seperator.join(alternates)

        tosend['response'] = altStr
        tosend['intent'] = baseIntent

        return jsonify(tosend)


@app.route('/findDoctor')
def findDoctor():
    obj = request.args.get('object')
    obj = json.loads(obj)
    intent = obj['intent']

    tosend = {}

    if intent == 'doctor.find':
        query = obj['query']

        doctors = predict.findDoctor("nagpur", query)
        altStr = ""
        for doc in doctors:
            altStr = altStr + doc['name'] + "\n" + \
                doc['address'] + "\n" + doc['phone'] + "\n\n"

        tosend['response'] = altStr
        tosend['intent'] = baseIntent

        return jsonify(tosend)

    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent

        return jsonify(tosend)


@app.route('/findAmbulance')
def findAmbulance():
    ambulance = ['Tiwari Ambulance services', 'Falcon Emergency Air and Train Ambulance Service',
                 'Om Sai Ambulance Service', 'Sagar Ambulance']
    tosend = {}

    obj = request.args.get('object')
    obj = json.loads(obj)
    intent = obj['intent']

    tosend = {}

    if intent == 'ambulance.find':
        query = obj['query']
        seperator = '\n'
        altStr = seperator.join(ambulance)
        tosend['response'] = ambulance[random.choice([0, 1, 2, 3])]
        tosend['intent'] = baseIntent
        return jsonify(tosend)

    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent
        return jsonify(tosend)


@app.route('/predictDisease')
def predictDisease():
    tosend = {}

    obj = request.args.get('object')
    print(obj)
    x = requests.get(
        'https://diseasepredtictor.herokuapp.com/getDisease?query='+obj)
    print(x.json()['disease'])
    tosend['response'] = x.json()['disease'][0]
    tosend['intent'] = baseIntent
    return jsonify(tosend)


@app.route('/findCovidStats')
def findCovidStats():
    stats = ['Maharashtra \t Cases:1.5M Recovered:1.3M',
             'Delhi \t Cases:1.2M Recovered:1M', 'Kerela \t Cases:0.8M Recovered 0.3M']
    tosend = {}
    seperator = '\n'
    altStr = seperator.join(stats)
    tosend['response'] = altStr
    tosend['intent'] = baseIntent
    return jsonify(tosend)


@app.route('/findHealthTips')
def findHealthTips():

    obj = request.args.get('object')
    obj = json.loads(obj)
    intent = obj['intent']

    tips = healthtips.split("\n")
    tosend = {}

    if intent == 'health.tips':
        query = obj['query']
        tosend['response'] = random.choice(tips)
        tosend['intent'] = baseIntent
        return jsonify(tosend)

    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent
        return jsonify(tosend)


if (__name__ == "__main__"):
    app.run()
