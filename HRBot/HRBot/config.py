'''
Created on 22-Jun-2018

@author: Vishnu
'''

import re
import os
import base64
from sklearn.externals import joblib
from .models import RequestCache, UserCache
import aiml
import dill
# from textblob import TextBlob
from .mappings import yesorno, attribute_list, issue_list, employee_issues, issue
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

os.chdir('C:/Users/hp/eclipse-workspace/HRBot/HRBot/')
brain_file = 'QA.brn'

def create_cache(CACHE_ID):
    try:
        req_cache = RequestCache.objects.get(cache_id=CACHE_ID)
    except RequestCache.DoesNotExist:
        kern_medical = aiml.Kernel()
        kern_medical.bootstrap(brainFile=brain_file)
        kernel_str = dill.dumps(kern_medical)
        kernel_str = base64.b64encode(kernel_str)
        req_cache = RequestCache.objects.create(cache_id=CACHE_ID, cache=[],
                                                user=UserCache.objects
                                                .create(aiml_kernel=kernel_str)
                                                )
    return req_cache

def Approvals(text, cache_list):
    text = text.lower()
    for key, value in yesorno.items():
        for i in value:
            dict_appr = {}
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_appr['Approval'] = key
                cache_list = remove_duplicate(cache_list, 'Approval')
                cache_list.append(dict_appr)
    return cache_list

def HRAppraise(text, cache_list):
    text = text.lower()
    for key, value in yesorno.items():
        for i in value:
            dict_appr = {}
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_appr['HRAppraise'] = key
                cache_list = remove_duplicate(cache_list, 'HRAppraise')
                cache_list.append(dict_appr)
    return cache_list

def HRApproval(text, cache_list):
    text = text.lower()
    for key, value in yesorno.items():
        for i in value:
            dict_appr = {}
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_appr['HRApproval'] = key 
                cache_list = remove_duplicate(cache_list, 'HRApproval')
                cache_list.append(dict_appr)
    return cache_list

def JD(text, cache_list):
    text = text.lower()
    for key, value in yesorno.items():
        for i in value:
            dict_jd = {}
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_jd['JD'] = key 
                cache_list = remove_duplicate(cache_list, 'JD')
                cache_list.append(dict_jd)
    return cache_list

def CreateJD(text, cache_list):
    text = text.lower()
    for key, value in yesorno.items():
        for i in value:
            dict_jd = {}
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_jd['CreateJD'] = key
                cache_list = remove_duplicate(cache_list, 'CreateJD')
                cache_list.append(dict_jd)
    return cache_list

def Thanks(text, cache_list):
    text = text.lower()
    dict_thanks = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_thanks['Thanks'] = key
                cache_list=remove_duplicate(cache_list, 'Thanks')
                cache_list.append(dict_thanks)
    return cache_list

def Attribute(text, cache_list):
    text=text.lower()
    dict_attribute = {}
    for key, value in attribute_list.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                    dict_attribute['Attribute'] = key
                    cache_list=remove_duplicate(cache_list, 'Attribute')
                    cache_list.append(dict_attribute)
    return cache_list

def Issue(text, cache_list):
    text = text.lower()
    dict_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_issue['Issue'] = key
                cache_list=remove_duplicate(cache_list, 'Issue')
                cache_list.append(dict_issue)
    return cache_list

def Anonymity(text, cache_list):
    text = text.lower()
    dict_anonymity = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_anonymity['Anonymity'] = key
                cache_list=remove_duplicate(cache_list, 'Anonymity')
                cache_list.append(dict_anonymity)
    return cache_list

def AnonymityEmployee(text, cache_list):
    text = text.lower()
    dict_anonymity_emp = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_anonymity_emp['Anonymity_Emp'] = key
                cache_list=remove_duplicate(cache_list, 'Anonymity_Emp')
                cache_list.append(dict_anonymity_emp)
    return cache_list

def HR(text, cache_list):
    text = text.lower()
    dict_hr = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_hr['HR'] = key
                cache_list=remove_duplicate(cache_list, 'HR')
                cache_list.append(dict_hr)
    return cache_list

def ITissue(text, cache_list):
    text=text.lower()
    dict_it_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_it_issue['IT_issue'] = key
                cache_list=remove_duplicate(cache_list, 'IT_issue')
                cache_list.append(dict_it_issue)
    return cache_list

def Userissue(text, cache_list):
    text=text.lower()
    dict_user_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_user_issue['User_issue'] = key
                cache_list=remove_duplicate(cache_list, 'User_issue')
                cache_list.append(dict_user_issue)
    return cache_list

def Solveissue(text, cache_list):
    text=text.lower()
    dict_solve_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_solve_issue['Solve_issue'] = key
                cache_list=remove_duplicate(cache_list, 'Solve_issue')
                cache_list.append(dict_solve_issue)
    return cache_list

def HRissue(text, cache_list):
    text=text.lower()
    dict_hr_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_hr_issue['HR_issue'] = key
                cache_list=remove_duplicate(cache_list, 'HR_issue')
                cache_list.append(dict_hr_issue)
    return cache_list

def Dial(text, cache_list):
    text=text.lower()
    dict_hr_issue = {}
    for key, value in yesorno.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_hr_issue['Dial'] = key
                cache_list=remove_duplicate(cache_list, 'Dial')
                cache_list.append(dict_hr_issue)
    return cache_list

def Name(text, cache_list):
    text = text.lower()
    dict_appr = {}
    if len(text) > 0:
        dict_appr['Name'] = text
        cache_list = remove_duplicate(cache_list, 'Name')
        cache_list.append(dict_appr)
    return cache_list

def Work(text, cache_list):
    text = text.lower()
    dict_appr = {}
    if len(text) > 0:
        dict_appr['Work'] = text
        cache_list = remove_duplicate(cache_list, 'Work')
        cache_list.append(dict_appr)
    return cache_list

def Attr(text, cache_list):
    text = text.lower()
    dict_appr = {}
    if len(text) > 0:
        dict_appr['Attr'] = text
        cache_list = remove_duplicate(cache_list, 'Attr')
        cache_list.append(dict_appr)
    return cache_list

def Desig(text, cache_list):
    text=text.lower()
    dict_attribute = {}
    for i in issue_list:
        match = re.compile(r"\b%s\b"%(i))
        ent = match.findall(text)
        if len(ent) > 0:
                dict_attribute['Post'] = i
                cache_list=remove_duplicate(cache_list, 'Post')
                cache_list.append(dict_attribute)
    return cache_list

def Choose_Issue(text, cache_list):
    text=text.lower()
    dict_find_issue = {}
    for key, value in issue.items():
        for i in value:
            match=re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) > 0:
                dict_find_issue['FindIssue'] = key
                cache_list=remove_duplicate(cache_list, 'FindIssue')
                cache_list.append(dict_find_issue)
    return cache_list

def Harassment(text, cache_list):
    text=text.lower()
    dict_attribute = {}
    for i in employee_issues:
        match = re.compile(r"\b%s\b"%(i))
        ent = match.findall(text)
        if len(ent) > 0:
                dict_attribute['Harass'] = i
                cache_list=remove_duplicate(cache_list, 'Harass')
                cache_list.append(dict_attribute)
    return cache_list

def get_quest(text, cache_list):
    text = text.lower()
    dict_quest = {}
    for key, value in yesorno.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            ent = match.findall(text)
            if len(ent) != 0:
                dict_quest['Question'] = key
                cache_list = remove_duplicate(cache_list, 'Question')
                cache_list.append(dict_quest)
    return cache_list

# def Sentiment(text):
#     text = text.lower()
#     txt=TextBlob(text)
#     polarity = list(txt.sentiment)
#     polarity = polarity[0]
#     if polarity > 0:
#         sentiment = 'positive'
#         return sentiment
#     elif polarity < 0:
#         sentiment = 'negative'
#         return sentiment
#     elif polarity == 0:
#         sentiment = 'neutral'
#         return sentiment
    
def Sentiment(text):
    text = text.lower()
    sid = SIA()
    ss = sid.polarity_scores(text) 
    v = list(ss.values())
    k = list(ss.keys())
    maximum = k[v.index(max(v))]
    polarity_check = {'neg': 'negative', 'neu': 'neutral', 'pos': 'positive'}
    return polarity_check[maximum]

def intent_classifier(text):
    text_list = []
    text_list.append(str(text))
    clf = joblib.load('intent_model.pkl')
    label = clf.predict(text_list)
    return label[0]

def remove_duplicate(lists, key_name):
    if len(lists) != 0:
        for dicts in lists:
            if key_name in dicts:
                lists.remove(dicts)
    return lists
