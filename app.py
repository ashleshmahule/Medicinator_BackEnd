import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import predict
from flask_cors import CORS
import json
import requests
import random


app = Flask(__name__)
CORS(app)
answer = {}
baseIntent = 'welcome'
intent = ''


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

        doctors = predict.findDoctor("Nagpur", query)
        seperator = '\n'
        altStr = seperator.join(doctors)

        tosend['response'] = altStr
        tosend['intent'] = baseIntent

        return jsonify(tosend)

    else:
        tosend['response'] = "Sorry, couldn't understand"
        tosend['intent'] = baseIntent

        return jsonify(tosend)


@app.route('/getDiagnosis')
def getDiagnosis():
    sym = request.args.get('symptoms')
    x = requests.get('https://diseasepredtictor.herokuapp.com/getDisease?query='+sym)    
    return(x.text)

@app.route('/getHealthTips')
def getHealthTips():

    healthtips=['1. Establish regular exercise routines in your life.', '2. Continue to work on eating healthily; vigilance will always be needed to be successful.', '3. See your doctor regularly for wellness exams and health/disease screenings/tests.', '4. If you have symptoms, seek medical attention; don’t ignore warning signs of issues.', '5. Along with your body, make efforts to stimulate and strengthen your brain as you age.', '6. Maintain satisfying social relationships.', '7. Keep involved in activities and pursuits that interest you.', '8. Try to maintain a positive attitude to support your resilience when life hands you', 'setbacks.', '9. Keep your body hydrated with water.', '10. Avoid toxins and unhealthy environments.', '11. Take care of your skin.', '12. Know your health numbers and what they mean, regardless of how healthy or', 'unhealthy you are now.', '13. Get adequate sleep.', '14. Spend less time in front of the TV; at minimum, get up and move during commercials.', '15. Learn to relax more.', '16. Focus less on your weight, and more on your overall health.', '17. Find things to be grateful for in your life.', '18. Don’t forget to smile and laugh routinely.', '19. Do something fun every day.', '20. Have a sense of purpose in your life.', '21. Let go of the past, focus on what you can do to improve your present and future.', '22. Give your focused attention on what you can do to address your most unhealthy habit.', '23. Remind yourself it takes time and patience to change ingrained habits.', '24. Know your family health history.', '25. Eat a variety of foods, especially fruits and vegetables.', '26. Limit your use of alcohol.', '27. Don’t forget your dental health.', '28. Don’t forget your eye health.', '29. Continue to educate yourself about overall health and wellness, over time new findings', 'result in updated recommendations from health experts.', '30. Replace bad habits with good ones.', '31. Learn to cook healthy foods you enjoy.', '32. Learn to modify recipes you love to make them more nutritious.', '33. Allow yourself to splurge periodically on special foods in limited quantities or', 'frequencies.', '34. Slip vegetables into your favorite recipes.', '35. Make sure you get some good fats in your diet.', '36. Stretch your body every day.', '37. Eat more fish.', '38. Start each day with a healthy breakfast.', '39. Spend some time in solitude on a regular basis.', '40. Wash your hands often.', '41. Focus on eating whole-grains when you eat bread products.', '42. Make sure that the protein foods you eat are leaner versions.', '43. Develop a ‘gentle firmness’ with yourself; be kind but honest in your mental ‘self talk’.', '44. Remember that small changes can really add up and lead to big results.', '45. Try to eat more natural/raw/core foods, and less processed food.', '46. Try to eat a variety of food ‘colors’.', '47. Try to eat more volume and fewer calories in your diet.', '48. Experiment with food combinations and spices to see what you like.', '49. Reward yourself for your positive efforts in ways that do not involve food whenever', 'possible.', '50. Enjoy your food, take time to sit down and concentrate on what you are eating.', '51. Watch salt, sugar, harmful fats and other additive levels in your food.', '52. Consider taking vitamins and other supplements as recommended by your doctor or', 'pharmacist.', '53. When someone asks you what you would like for a gift, be ready with a healthy idea.', '54. Write down your health goals and prioritize them.', '55. Track your progress on health goals so you have feedback to review.', '56. Have realistic expectations for yourself and your body.', '57. Compete only with yourself, not others.', '58. Look for healthy role models in your life.', '59. Ask for tips or advice from people in your life who are healthy and/or struggling with', 'similar challenges.', '60. Develop healthy rituals but be prepared to be flexible as needed.', '61. Plan and allow time for you to keep up with your healthy habits and routines.', '62. Don’t forget portion control.', '63. Concentrate of keeping your body strong and flexible.', '64. Seek to resolve nagging problems in your life.', '65. Accept the things in your life that you cannot change.', '66. Do something for others just because you can.', '67. Try to be spontaneous or try something new each week.', '68. Gravitate towards healthy people whenever possible.', '69. Use your support systems.', '70. Expect setbacks and plan for them if possible.', '71. Take your medications as prescribed and report side effects to your physician.', '72. Make sure your physician(s) have complete information about your health.', '73. Take breaks during your work day.', '74. Learn to breathe properly.', '75. Don’t engage in wishful thinking about your health; take action, even small steps, as', 'soon as you can to get going towards a healthier you.', '76. If you are ill or have an injury, rest and/or get treatment.', '77. Use trusted websites for excellent health advice and/or recipes.', '78. Listen to your body.', '79. Are you already managing a specific condition, like diabetes or arthritis? Read up on', 'what you can continue to do to mitigate progression of the condition through any', 'lifestyle changes.', '80. Watch the level of over the counter medications you use.', '81. Make sure you understand contraindications and/or interactions for any medication you', 'take or conditions you have, including improper mixing of meds and other meds and/or', 'food.', '82. Join a health related class or program, a great way to get new ideas/tips and/or', 'supports.', '83. Carry healthy snacks with you.', '84. Read nutrition labels regularly.', '85. Get rid of excess clutter in both your physical and mental world.', '86. Stop doing what doesn’t work for you, and keep doing what does work for you.', '87. Be willing to try a new sport or physical activity at least once to see if you would enjoy it.', '88. Develop an array of exercise and physical activity options in your life to keep active.', '89. Know the key nutritious healthy or ‘super’ foods and include them in your diet.', '90. Keep educating yourself about health update information.', '91. Remember that while you may have your own health challenges, you are likely someone', 'else’s role model in some aspect of their life.', '92. Make yourself ‘work’ for a special food through an exercise ‘payment’ first; you may find', 'after the exercise you really don’t want the food.', '93. Understand that - as with all important aspects of life - being healthy will take some', 'work and effort on your part and it will be worth it over the long haul.', '94. Consider rewarding yourself with cash; save up what you would have spent on', 'unhealthy foods or tobacco and use the money to purchase something you would really', 'love.', '95. Whenever you need to do so, just start over fresh, at the next meal, the next day, the', 'next month, the next year, whichever comes first for you.', '96. Understand that being healthy or unhealthy is a choice you get to make continually', 'through many daily decisions.', '97. The more you develop other interests and activities in your life, the less appealing over', 'eating or inactivity will be for you.', '98. The way out of any rut is simple, just do it; get started in any way that you can.', '99. Post reminders, incentives or inspiration for yourself to see to help support your goals.', '100. Don’t ever give up on efforts to improve your health.']
    num1 = random.randrange(100)

    return (healthtips[num1])


@app.route('/getCovidStatus')
def getCovidStatus():
    x = requests.get('https://api.covid19api.com/summary')    
    return(x.text)


if (__name__ == "__main__"):
    app.run()
