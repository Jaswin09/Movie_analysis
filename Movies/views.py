from django.shortcuts import render
import pickle
from .forms import NameForm

from .main import *
import requests
url = "https://imdb8.p.rapidapi.com/auto-complete"
headers = {
                'x-rapidapi-key': "1a7f74979cmsh0afbb5dc9f14367p100610jsn8db2e6ad11e1",
                'x-rapidapi-host': "imdb8.p.rapidapi.com"
            }
def hello(request):
    global name, img, d, res, rec
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            data = request.POST.get('your_name')
            querystring = {"q": str(data)}
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            img = response['d'][0]['i']['imageUrl']
            d = response['d'][0]['y']
            name = response['d'][0]['l']
            test_data_set = build_test_set(data)
            preprocessed_test_set = text_processor.process_texts(test_data_set)
            classified_result_labels = []
            for tweet in preprocessed_test_set:
                classified_result_labels.append(NBayesClassifier.classify(extract_features(tweet[0])))
            if classified_result_labels.count('positive') > classified_result_labels.count('negative'):
                res = "Overall Positive Sentiment"
                percent1 = (100 * classified_result_labels.count('positive') / len(classified_result_labels))
                if percent1 > 90:
                    rec = "Highly Recommended"
                elif percent1 > 75 and percent1 < 90:
                    rec = "Recommended"
                elif percent1 > 60 and percent1 < 75:
                    rec = "Above Average"
            else:
                res = "Overall Negative Sentiment"
                print("Negative Sentiment Percentage = " + str(
                    100 * classified_result_labels.count('negative') / len(classified_result_labels)) + "%")
                percent = (100 * classified_result_labels.count('negative') / len(classified_result_labels))
                if percent > 85:
                    rec = "Not Recommended"
                elif percent > 70 and percent < 85:
                    rec = "Poorly Recommended"
                elif percent < 70:
                    rec = "Below Average"
        return render(request, 'index.html', {'data': name,'res':img,'d':d,'r':res,'rec':rec})
    else:
        name = None
        img = None
        d = None
        res = None
        rec = None
        print("Inappropriate")
    return render(request, 'index.html',{'data':name,'res':img,'d':d,'r':res,'rec':rec})






