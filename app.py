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

healthtips = """	Establish regular exercise routines in your life.
	Continue to work on eating healthily; vigilance will always be needed to be successful.
	See your doctor regularly for wellness exams and health/disease screenings/tests.
	If you have symptoms, seek medical attention; don’t ignore warning signs of issues.
	Along with your body, make efforts to stimulate and strengthen your brain as you age.
	Maintain satisfying social relationships.
	Keep involved in activities and pursuits that interest you.
	Try to maintain a positive attitude to support your resilience when life hands you setbacks.
	Keep your body hydrated with water.
	Avoid toxins and unhealthy environments.
	Take care of your skin.
	Know your health numbers and what they mean, regardless of how healthy or unhealthy you are now.
	Get adequate sleep.
	Spend less time in front of the TV; at minimum, get up and move during commercials.
	Learn to relax more.
	Focus less on your weight, and more on your overall health.
	Find things to be grateful for in your life.
	Don’t forget to smile and laugh routinely.
	Do something fun every day.
	Have a sense of purpose in your life.
	Let go of the past, focus on what you can do to improve your present and future.
	Give your focused attention on what you can do to address your most unhealthy habit.
	Remind yourself it takes time and patience to change ingrained habits.
	Know your family health history.
	Eat a variety of foods, especially fruits and vegetables.
	Limit your use of alcohol.
	Don’t forget your dental health.
	Don’t forget your eye health.
	Continue to educate yourself about overall health and wellness, over time new findings result in updated recommendations from health experts.
	Replace bad habits with good ones.
	Learn to cook healthy foods you enjoy.
	Learn to modify recipes you love to make them more nutritious.
	Allow yourself to splurge periodically on special foods in limited quantities or frequencies.
	Slip vegetables into your favorite recipes.
	Make sure you get some good fats in your diet.
	Stretch your body every day.
	Eat more fish.
	Start each day with a healthy breakfast.
	Spend some time in solitude on a regular basis.
	Wash your hands often.
	Focus on eating whole-grains when you eat bread products.
	Make sure that the protein foods you eat are leaner versions.
	Develop a ‘gentle firmness’ with yourself; be kind but honest in your mental ‘self talk’.
	Remember that small changes can really add up and lead to big results.
	Try to eat more natural/raw/core foods, and less processed food.
	Try to eat a variety of food ‘colors’.
	Try to eat more volume and fewer calories in your diet.
	Experiment with food combinations and spices to see what you like.
	Reward yourself for your positive efforts in ways that do not involve food whenever possible.
	Enjoy your food, take time to sit down and concentrate on what you are eating.
	Watch salt, sugar, harmful fats and other additive levels in your food.
	Consider taking vitamins and other supplements as recommended by your doctor or pharmacist.
	When someone asks you what you would like for a gift, be ready with a healthy idea.
	Write down your health goals and prioritize them.
	Track your progress on health goals so you have feedback to review.
	Have realistic expectations for yourself and your body.
	Compete only with yourself, not others.
	Look for healthy role models in your life.
	Ask for tips or advice from people in your life who are healthy and/or struggling with similar challenges.
	Develop healthy rituals but be prepared to be flexible as needed.
	Plan and allow time for you to keep up with your healthy habits and routines.
	Don’t forget portion control.
	Concentrate of keeping your body strong and flexible.
	Seek to resolve nagging problems in your life.
	Accept the things in your life that you cannot change.
	Do something for others just because you can.
	Try to be spontaneous or try something new each week.
	Gravitate towards healthy people whenever possible.
	Use your support systems.
	Expect setbacks and plan for them if possible.
	Take your medications as prescribed and report side effects to your physician.
	Make sure your physician(s) have complete information about your health.
	Take breaks during your work day.
	Learn to breathe properly.
	Don’t engage in wishful thinking about your health; take action, even small steps, as soon as you can to get going towards a healthier you.
	If you are ill or have an injury, rest and/or get treatment.
	Use trusted websites for excellent health advice and/or recipes.
	Listen to your body.
	Are you already managing a specific condition, like diabetes or arthritis? Read up on what you can continue to do to mitigate progression of the condition through any lifestyle changes.
	Watch the level of over the counter medications you use.
	Make sure you understand contraindications and/or interactions for any medication you take or conditions you have, including improper mixing of meds and other meds and/or food.
	Join a health related class or program, a great way to get new ideas/tips and/or supports.
	Carry healthy snacks with you.
	Read nutrition labels regularly.
	Get rid of excess clutter in both your physical and mental world.
	Stop doing what doesn’t work for you, and keep doing what does work for you.
	Be willing to try a new sport or physical activity at least once to see if you would enjoy it.
	Develop an array of exercise and physical activity options in your life to keep active.
	Know the key nutritious healthy or ‘super’ foods and include them in your diet.
	Keep educating yourself about health update information.
	Remember that while you may have your own health challenges, you are likely someone else’s role model in some aspect of their life.
	Make yourself ‘work’ for a special food through an exercise ‘payment’ first; you may find after the exercise you really don’t want the food.
	Understand that - as with all important aspects of life - being healthy will take some work and effort on your part and it will be worth it over the long haul.
	Consider rewarding yourself with cash; save up what you would have spent on unhealthy foods or tobacco and use the money to purchase something you would really love.
	Whenever you need to do so, just start over fresh, at the next meal, the next day, the next month, the next year, whichever comes first for you.
	Understand that being healthy or unhealthy is a choice you get to make continually through many daily decisions.
	The more you develop other interests and activities in your life, the less appealing over eating or inactivity will be for you.
	The way out of any rut is simple, just do it; get started in any way that you can.
	Post reminders, incentives or inspiration for yourself to see to help support your goals.
	Don’t ever give up on efforts to improve your health."""


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
	    tosend['response'] = altStr
	    tosend['intent'] = baseIntent
	    return jsonify(tosend)
	
    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent



@app.route('/predictDisease')
def predictDisease():
    tosend={}

    obj = request.args.get('query')
    print(obj)
    x = requests.get('https://diseasepredtictor.herokuapp.com/getDisease?query='+obj)
    print(x.json()['disease'])
    tosend['response'] = x.json()['disease'][0]
    tosend['intent'] = baseIntent
    return jsonify(tosend)



@app.route('/findCovidStats')
def findCovidStats():
    stats=['Maharashtra \t Cases:1.5M Recovered:1.3M','Delhi \t Cases:1.2M Recovered:1M','Kerela \t Cases:0.8M Recovered 0.3M']
    tosend={}
    seperator = '\n'
    altStr = seperator.join(stats)
    tosend['response'] = altStr
    tosend['intent'] = baseIntent
    return jsonify(tosend)


@app.route('/findHealthTips')
def findHealthTips():
    tips=healthtips.split("\n")
    tosend={}
    tosend['response'] = random.choice(tips)
    tosend['intent'] =  baseIntent
    return jsonify(tosend)



if (__name__ == "__main__"):
    app.run()
