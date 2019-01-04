'''
Created on 22-Jun-2018

@author: Vishnu
'''

from .config import intent_classifier, Sentiment
from .config import Approvals, HRAppraise, HRApproval, JD, CreateJD, get_quest
from .config import Thanks, Attribute, Name, Work, Attr, Desig, Dial, Choose_Issue
from .config import Issue, Anonymity, AnonymityEmployee, HR, Harassment, HRissue, ITissue
from .queries import itissue, financeissue, adminissue, hrissue
from .queries import fillers_negative 
import random

def build_model(question, kern, ent_list):
    response = {}
    response['property'] = []
    response['property'].extend(ent_list)
    intent_label = intent_classifier(question['messageText'])
    if intent_label == 0 or question['messageSource'] == 'feedback' or question['messageSource'] == 'feedbackneg':
        if question['messageSource'] == 'messageFromBot':
            response['messageText'] = [["Hey there.! How are things.?"]]
            response['messageSource'] = 'feedback'
            response['filter'] = 'normal'
            return response
        sentiment = Sentiment(question['messageText'])
        if sentiment == 'positive' and question['messageSource'] == 'feedback' or sentiment == 'neutral' and question['messageSource'] == 'feedback':
            if question['filter'] == 'flag':
                response['property'] = Thanks(question['messageText'], response['property'])
            if question['filter'] == 'name':
                response['property'] = Name(question['messageText'], response['property'])
            if question['filter'] == 'work':
                response['property'] = Work(question['messageText'], response['property'])
            if question['filter'] == 'quest':
                response['property'] = get_quest(question['messageText'], response['property'])
            entity_list = ['Thanks']
            entity_dict_available = {k:v for d in response['property'] for k,v in d.items()}
            entity_list_available = list(entity_dict_available.keys())
            entity_list = [i for i in entity_list if i not in entity_list_available]
            for i in entity_list:
                if i == 'Thanks':
                    response['messageText'] = [["Oh that's great to know.!"], ["Would you like to thank any of your team mates?"], ["It would help them you know.!"]]
                    response['messageSource'] = 'feedback'
                    response['input'] = ['Yes', 'No']
                    response['filter'] = 'flag'
                    return response
                else:
                    continue
            response['messageSource'] = 'feedback'
            return response
        elif sentiment == 'negative' or question['messageSource'] == 'feedbackneg' or sentiment == 'neutral' and question['messageSource'] == 'feedbackneg':
            response['property'] = Harassment(question['messageText'], response['property'])
            if question['filter'] == 'empanonymity':
                response['property'] = AnonymityEmployee(question['messageText'], response['property'])
            if question['filter'] == 'hrissue':
                response['property'] = HRissue(question['messageText'], response['property'])
            if question['filter'] == 'dial':
                response['property'] = Dial(question['messageText'], response['property'])
            if {key: value for d in response["property"] for key, value in d.items()}.has_key('Harass'):
                response['messageText'] = [["Oh that's really unfortunate to hear! I am so sorry that it happened to you."], 
                                           ["Don't worry, I shall do everything from my end to set things right."],
                                           ["I could raise the issue with the concerned people."], 
                                           ["Do you want to maintain anonymity.?"]]
                response['messageSource'] = 'feedbackneg'
                response['input'] = ['Yes', 'No']
                response['filter'] = 'empanonymity'
                return response
            else:
                if question['filter'] == 'attr': 
                    response['property'] = Attribute(question['messageText'], response['property'])
                if question['filter'] == 'flag': 
                    response['property'] = Attr(question['messageText'], response['property'])
                if question['filter'] == 'raise':
                    response['property'] = Issue(question['messageText'], response['property'])
                if question['filter'] == 'desig':
                    response['property'] = Desig(question['messageText'], response['property'])
                if question['filter'] == 'hr':
                    response['property'] = HR(question['messageText'], response['property'])
                if question['filter'] == 'anonymity':
                    response['property'] = Anonymity(question['messageText'], response['property'])
                if question['filter'] == 'quest':
                    response['property'] = get_quest(question['messageText'], response['property'])
                entity_list = ['Attribute']
                entity_dict_available = {k:v for d in response['property'] for k,v in d.items()}
                entity_list_available = list(entity_dict_available.keys())
                entity_list = [i for i in entity_list if i not in entity_list_available]
                for i in entity_list:
                    if i == 'Attribute':
                        response['messageText'] = [["Oh what happened.?"], 
                                                   ["Would you like to attribute that to the people in your team, management, materials/system, environment or the process?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['input'] = ['Team', 'Management', 'Materials/System', 'Environment', 'Process']
                        response['filter'] = 'attr'
                        return response
                    else:
                        continue
                try:
                    if str({key: value for d in response["property"] for key, value in d.items()}['Attribute']) == 'Team':
                        response['messageText'] = [["What do you think was the issue with the people.?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['filter'] = 'flag'
                        return response
                    elif str({key: value for d in response["property"] for key, value in d.items()}['Attribute']) == 'Management':
                        response['messageText'] = [["What do you think was the issue with the management.?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['filter'] = 'flag'
                        return response
                    elif str({key: value for d in response["property"] for key, value in d.items()}['Attribute']) == 'Materials/System':
                        response['messageText'] = [["What do you think was the issue with the system.?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['filter'] = 'flag'
                        return response
                    elif str({key: value for d in response["property"] for key, value in d.items()}['Attribute']) == 'Environment':
                        response['messageText'] = [["What do you think was the issue with the environment.?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['filter'] = 'flag'
                        return response
                    elif str({key: value for d in response["property"] for key, value in d.items()}['Attribute']) == 'Process':
                        response['messageText'] = [["What do you think was the issue with the process.?"]]
                        response['messageSource'] = 'feedbackneg'
                        response['filter'] = 'flag'
                        return response
                except:
                    response['messageSource'] = 'feedbackneg'
                    return response
    elif intent_label == 1 or question['messageSource'] == 'HelpDesk':
        if question['messageSource'] == 'messageFromBot':
            response['messageText'] = [['Can you notify us regarding your issue ?']]
            response['messageSource'] = 'HelpDesk'
            response['filter'] = 'normal'
            return response
        response['property'] = Choose_Issue(question['messageText'], response['property'])
        if question['filter'] == 'flag':
            response['property'] = ITissue(question['messageText'], response['property'])
        if question['filter'] == 'quest':
            response['property'] = get_quest(question['messageText'], response['property'])
        try:
            if {key: value for d in response["property"] for key, value in d.items()}.has_key('FindIssue'):
                if str({key: value for d in response["property"] for key, value in d.items()}['FindIssue']) == 'it_issue':
                    response['messageText'] = [[random.choice(fillers_negative)], [random.choice(itissue)]]         
                    response['messageSource'] = 'HelpDesk'
                    response['filter'] = 'flag'
                    response['input'] = ['Yes', 'No']
                    return response  
                elif str({key: value for d in response["property"] for key, value in d.items()}['FindIssue']) == 'finance_issue':
                    response['messageText'] = [[random.choice(fillers_negative)], [random.choice(financeissue)]]
                    response['messageSource'] = 'HelpDesk'
                    response['filter'] = 'flag'
                    response['input'] = ['Yes', 'No']
                    return response
                elif str({key: value for d in response["property"] for key, value in d.items()}['FindIssue']) == 'admin_issue':
                    response['messageText'] = [[random.choice(fillers_negative)], [random.choice(adminissue)]]
                    response['messageSource'] = 'HelpDesk'
                    response['filter'] = 'flag'
                    response['input'] = ['Yes', 'No']
                    return response
                elif str({key: value for d in response["property"] for key, value in d.items()}['FindIssue']) == 'hr_issue':
                    response['messageText'] = [[random.choice(fillers_negative)], [random.choice(hrissue)]]
                    response['messageSource'] = 'HelpDesk'
                    response['filter'] = 'flag'
                    response['input'] = ['Yes', 'No']
                    return response
            else:
                response['messageText'] = [["Sorry I didn't get you.."], ["Can you please tell me about your issue.?"]]
                response['messageSource'] = 'HelpDesk'
                response['filter'] = 'normal'
                return response
        except:
            response['messageText'] = [["Sorry I didn't get you.."], ["Could you please tell me about your issue.?"]]
            response['messageSource'] = 'HelpDesk'
            response['filter'] = 'normal'
            return response
    elif intent_label == 3 or question['messageSource'] == 'recruitment': 
        if question['messageSource'] == 'messageFromBot':
            response['messageText'] = [["Your wish is my command.! What would you need.?"]]
            response['messageSource'] = 'recruitment'
            response['filter'] = 'normal'
            return response
        if question['filter'] == 'approve':
            response['property'] = Approvals(question['messageText'], response['property'])
        if question['filter'] == 'hrappraise':
            response['property'] = HRAppraise(question['messageText'], response['property'])
        if question['filter'] == 'jd':
            response['property'] = JD(question['messageText'], response['property'])
        if question['filter'] == 'createjd':
            response['property'] = CreateJD(question['messageText'], response['property'])
        if question['filter'] == 'quest':
            response['property'] = get_quest(question['messageText'], response['property'])
        entity_list = ['Approval']
        entity_dict_available = {k:v for d in response['property'] for k,v in d.items()}
        entity_list_available = list(entity_dict_available.keys())
        entity_list = [i for i in entity_list if i not in entity_list_available]
        for i in entity_list:
            if i == 'Approval':
                response['messageText'] = [["Do you have the approvals yet.?"]] 
                response['messageSource'] = 'recruitment'
                response['input'] = ['Yes', 'No']
                response['filter'] = 'approve'
                return response
            else:
                continue
        try:
            if {key: value for d in response["property"] for key, value in d.items()}.has_key('Approval'):
                if str({key: value for d in response["property"] for key, value in d.items()}['Approval']) == 'Yes':
                    response['messageText'] = [["I shall collect the same from the HR department then.!"]]
                    response['messageSource'] = 'messageFromBot'
                    response['filter'] = 'normal'
                    response['action'] = 'stop'
                    return response
                elif str({key: value for d in response["property"] for key, value in d.items()}['Approval']) == 'No':
                    response['messageText'] = [["Do you want me to appraise the HR Department for the same.?"]]
                    response['messageSource'] = 'recruitment'
                    response['input'] = ['Yes', 'No']
                    response['filter'] = 'hrappraise'
                    return response
        except:
            response['messageSource'] = 'recruitment'
            return response
    else:
        kernel_reply = kern.respond(question['messageText'])
        if not "Sorry, I didn't get you.." in kernel_reply:
            response = {}
            response['property'] = []
            response['messageText'] = [[kernel_reply]]
            response['messageSource'] = 'messageFromBot'
            response['filter'] = 'normal'
            return response
        else:
            response['messageText'] = [["Sorry, I didn't get you.."]]
            response['messageSource'] = 'messageFromBot'
            response['filter'] = 'normal'
            return response
