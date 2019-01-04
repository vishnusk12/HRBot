'''
Created on 22-Jun-2018

@author: Vishnu
'''

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from .config import create_cache
from .model import build_model
from .queries import fillers_positive, fillers_negative
import random
import dill
import base64

@permission_classes((permissions.AllowAny,))
class Bot(viewsets.ViewSet):
    def create(self, request):
        CACHE_ID = 'CONSTANT5'
        question = request.data
        if 'user_id' in question:
            CACHE_ID = question['user_id']
        req_cache = create_cache(CACHE_ID)
        if question['messageSource'] == 'userInitiatedReset':
            req_cache.delete()
            question['messageSource'] = 'messageFromBot'
            question['filter'] = 'normal'
            question['messageText'] = [['Hi..I am your Virtual Assistant.'], ['How may I help you..?'], 
                                       ['Please Select a category.']]
            question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']                        
            return Response(question)
        kern = dill.loads(base64.b64decode(req_cache.user.aiml_kernel))
        question = build_model(question, kern, req_cache.cache)
        if 'property' in question:
            req_cache.cache = question['property']
            req_cache.user.aiml_kernel = base64.b64encode(dill.dumps(kern))
            req_cache.user.save()
            req_cache.save()
        if {key: value for d in question["property"] for key, value in d.items()}.has_key('Thanks') and question['messageSource'] == 'feedback':
            if str({key: value for d in question["property"] for key, value in d.items()}['Thanks']) == 'Yes':
                question['messageText'] = [["Whom would you like to thank.?"]]
                question['messageSource'] = 'feedback'
                question['filter'] = 'name'
                reply = question
                try:
                    if {key: value for d in question["property"] for key, value in d.items()}.has_key('Name') and question['messageSource'] == 'feedback' and question['filter'] == 'name':
                        question['messageText'] = [["Cool."], ["Thanks for mentioning the names."], 
                                                   ['Would you like to have more assistance.?']]
                        question['messageSource'] = 'feedback'
                        question['filter'] = 'quest'
                        question['input'] = ['Yes', 'No']
                        reply = question
                        try:
                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                question['messageText'] = [['How can I be of further assistance.?'], ['Please Select a category.']]
                                question['messageSource'] = 'messageFromBot'
                                question['filter'] = 'normal'
                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                reply = question
                                req_cache.delete()
                                return Response(reply)
                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                question['messageSource'] = 'messageFromBot'
                                question['filter'] = 'normal'
                                question['action'] = 'stop'
                                reply = question
                                req_cache.delete()
                                return Response(reply)
                        except:
                            question['messageSource'] = 'feedback'
                            reply = question
                            return Response(reply)
                except:
                    question['messageSource'] = 'feedback'
                    reply = question
                    return Response(reply)
            elif str({key: value for d in question["property"] for key, value in d.items()}['Thanks']) == 'No':
                question['messageText'] = [["Alright. How has it been working with the teams.?"]]
                question['messageSource'] = 'feedback'
                question['filter'] = 'work'
                reply = question
                try:
                    if {key: value for d in question["property"] for key, value in d.items()}.has_key('Work') and question['messageSource'] == 'feedback' and question['filter'] == 'work':
                        question['messageText'] = [["Okay."], ["I have recorded your response"], 
                                                   ['Would you like to have more assistance.?']]
                        question['messageSource'] = 'feedback'
                        question['filter'] = 'quest'
                        question['input'] = ['Yes', 'No']
                        reply = question
                        try:
                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                question['messageText'] = [['How can I be of further assistance.?'], ['Please Select a category.']]
                                question['messageSource'] = 'messageFromBot'
                                question['filter'] = 'normal'
                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                reply = question
                                req_cache.delete()
                                return Response(reply)
                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                question['messageSource'] = 'messageFromBot'
                                question['filter'] = 'normal'
                                question['action'] = 'stop'
                                reply = question
                                req_cache.delete()
                                return Response(reply)
                        except:
                            question['messageSource'] = 'feedback'
                            reply = question
                            return Response(reply)
                except:
                    question['messageSource'] = 'feedback'
                    reply = question
                    return Response(reply)
        elif {key: value for d in question["property"] for key, value in d.items()}.has_key('Attr') and question['messageSource'] == 'feedbackneg':
            question['messageText'] = [["Hmm. I understand."], ["I could raise the issue, if you'd want me to."]]
            question['messageSource'] = 'feedbackneg'
            question['input'] = ['Yes', 'No']
            question['filter'] = 'raise'
            reply = question
            try:
                if {key: value for d in question["property"] for key, value in d.items()}.has_key('Issue'):
                    if str({key: value for d in question["property"] for key, value in d.items()}['Issue']) == 'Yes':
                        question['messageText'] = [["To whom would you like me to raise the issue.?"]]
                        question['messageSource'] = 'feedbackneg'
                        question['filter'] = 'desig'
                        question['input'] = ['Manager', 'HR', 'Head HR']    
                        reply = question
                        try:
                            if {key: value for d in question["property"] for key, value in d.items()}.has_key('Post'):
                                question['messageText'] = [["Thank You for your time."], 
                                                           ["I will raise the issue to the concerned authority."],
                                                           ['Would you like to have more assistance.?']]
                                question['messageSource'] = 'feedbackneg'
                                question['filter'] = 'quest'
                                question['input'] = ['Yes', 'No']
                                reply = question
                                try:
                                    if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                        question['messageText'] = [['How can I be of further assistance.?'], 
                                                                   ['Please Select a category.']]
                                        question['messageSource'] = 'messageFromBot'
                                        question['filter'] = 'normal'
                                        question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                        reply = question
                                        req_cache.delete()
                                        return Response(reply)
                                    elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                        question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                        question['messageSource'] = 'messageFromBot'
                                        question['filter'] = 'normal'
                                        question['action'] = 'stop'
                                        reply = question
                                        req_cache.delete()
                                        return Response(reply)
                                except:
                                    question['messageSource'] = 'feedbackneg'
                                    reply = question
                                    return Response(reply)
                        except:
                            question['messageSource'] = 'feedbackneg'
                            reply = question
                            return Response(reply)
                    elif str({key: value for d in question["property"] for key, value in d.items()}['Issue']) == 'No':
                        question['messageText'] = [["Anyhow I have recorded it."], 
                                                   ["I shall suggest to the HR to take a note of this and probably work on it."], 
                                                   ["Do you mind me doing that?"]]
                        question['messageSource'] = 'feedbackneg'
                        question['filter'] = 'hr'
                        question['input'] = ['Yes', 'No']
                        reply = question
                        try:
                            if {key: value for d in question["property"] for key, value in d.items()}.has_key('HR'):
                                if str({key: value for d in question["property"] for key, value in d.items()}['HR']) == 'Yes':
                                    question['messageText'] = [["Done."], 
                                                               ["Lets hope that such things don't happen to you again."],
                                                               ['Would you like to have more assistance.?']]
                                    question['messageSource'] = 'feedbackneg'
                                    question['filter'] = 'quest'
                                    question['input'] = ['Yes', 'No']
                                    reply = question
                                    try:
                                        if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                            question['messageText'] = [['How can I be of further assistance.?'], 
                                                                       ['Please Select a category.']]
                                            question['messageSource'] = 'messageFromBot'
                                            question['filter'] = 'normal'
                                            question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                            reply = question
                                            req_cache.delete()
                                            return Response(reply)
                                        elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                            question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                            question['messageSource'] = 'messageFromBot'
                                            question['filter'] = 'normal'
                                            question['action'] = 'stop'
                                            reply = question
                                            req_cache.delete()
                                            return Response(reply)
                                    except:
                                        question['messageSource'] = 'feedbackneg'
                                        reply = question
                                        return Response(reply)
                                elif str({key: value for d in question["property"] for key, value in d.items()}['HR']) == 'No':
                                    question['messageText'] = [["Alright."], 
                                                               ["Is it because you want to maintain anonymity.?"], 
                                                               ["If that's the case I could keep you anonymous and then intimate them."], 
                                                               ["What say?"]]
                                    question['messageSource'] = 'feedbackneg'
                                    question['filter'] = 'anonymity'
                                    question['input'] = ['Yes', 'No']
                                    reply = question
                                    try:
                                        if {key: value for d in question["property"] for key, value in d.items()}.has_key('Anonymity'):
                                            if str({key: value for d in question["property"] for key, value in d.items()}['Anonymity']) == 'Yes':
                                                question['messageText'] = [["Done."], 
                                                                           ["Lets hope that such things don't happen to you again."],
                                                                           ['Would you like to have more assistance.?']]
                                                question['messageSource'] = 'feedbackneg'
                                                question['filter'] = 'quest'
                                                question['input'] = ['Yes', 'No']
                                                reply = question
                                                try:
                                                    if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                        question['messageText'] = [['How can I be of further assistance.?'], 
                                                                                   ['Please Select a category.']]
                                                        question['messageSource'] = 'messageFromBot'
                                                        question['filter'] = 'normal'
                                                        question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                        reply = question
                                                        req_cache.delete()
                                                        return Response(reply)
                                                    elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                        question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                        question['messageSource'] = 'messageFromBot'
                                                        question['filter'] = 'normal'
                                                        question['action'] = 'stop'
                                                        reply = question
                                                        req_cache.delete()
                                                        return Response(reply)
                                                except:
                                                    question['messageSource'] = 'feedbackneg'
                                                    reply = question
                                                    return Response(reply)
                                            elif str({key: value for d in question["property"] for key, value in d.items()}['Anonymity']) == 'No':
                                                question['messageText'] = [["Fair enough."], 
                                                                           ["Lets hope that such things don't happen to you again."],
                                                                           ['Would you like to have more assistance.?']]
                                                question['messageSource'] = 'feedbackneg'
                                                question['filter'] = 'quest'
                                                question['input'] = ['Yes', 'No']
                                                reply = question
                                                try:
                                                    if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                        question['messageText'] = [['How can I be of further assistance.?'], 
                                                                                   ['Please Select a category.']]
                                                        question['messageSource'] = 'messageFromBot'
                                                        question['filter'] = 'normal'
                                                        question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                        reply = question
                                                        req_cache.delete()
                                                        return Response(reply)
                                                    elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                        question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                        question['messageSource'] = 'messageFromBot'
                                                        question['filter'] = 'normal'
                                                        question['action'] = 'stop'
                                                        reply = question
                                                        req_cache.delete()
                                                        return Response(reply)
                                                except:
                                                    question['messageSource'] = 'feedbackneg'
                                                    reply = question
                                                    return Response(reply)
                                    except:
                                        question['messageSource'] = 'feedbackneg'
                                        reply = question
                                        return Response(reply)
                        except:
                            question['messageSource'] = 'feedbackneg'
                            reply = question
                            return Response(reply)       
            except:
                question['messageSource'] = 'feedbackneg'
                reply = question
                return Response(reply)  
        elif {key: value for d in question["property"] for key, value in d.items()}.has_key('Anonymity_Emp') and question['messageSource'] == 'feedbackneg':
            if str({key: value for d in question["property"] for key, value in d.items()}['Anonymity_Emp']) == 'Yes':
                question['messageText'] = [["Do not worry at all, you would be treated as anonymous through the whole process."],
                                           ["Do you want to talk to our HR person regarding the same."]]
                question['messageSource'] = 'feedbackneg'
                question['filter'] = 'hrissue'
                question['input'] = ['Yes', 'No']
                reply = question
                try:
                    if {key: value for d in question["property"] for key, value in d.items()}.has_key('HR_issue'):
                        if str({key: value for d in question["property"] for key, value in d.items()}['HR_issue']) == 'Yes':
                            question['messageText'] = [["Fair enough, shall I Dial.?"]]
                            question['messageSource'] = 'feedbackneg'
                            question['input'] = ['Yes', 'No']
                            question['filter'] = 'dial'
                            reply = question
                            try:
                                if {key: value for d in question["property"] for key, value in d.items()}.has_key('Dial'):
                                    if str({key: value for d in question["property"] for key, value in d.items()}['Dial']) == 'Yes':
                                        question['messageText'] = [["Okay."], ["I am dialling."],
                                                                   ['Would you like to have more assistance.?']]
                                        question['messageSource'] = 'feedbackneg'
                                        question['filter'] = 'quest'
                                        question['input'] = ['Yes', 'No']
                                        reply = question
                                        try:
                                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                question['messageText'] = [['How can I be of further assistance.?'], 
                                                                           ['Please Select a category.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['action'] = 'stop'
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                        except:
                                            question['messageSource'] = 'feedbackneg'
                                            reply = question
                                            return Response(reply)
                                    elif str({key: value for d in question["property"] for key, value in d.items()}['Dial']) == 'No':
                                        question['messageText'] = [["Oh I see."], ["Okay."], 
                                                                   ["Just Cool down."], ["Everything will be fine."],
                                                                   ['Would you like to have more assistance.?']]
                                        question['messageSource'] = 'feedbackneg'
                                        question['filter'] = 'quest'
                                        question['input'] = ['Yes', 'No']
                                        reply = question
                                        try:
                                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                question['messageText'] = [['How can I be of further assistance.?'], 
                                                                           ['Please Select a category.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['action'] = 'stop'
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                        except:
                                            question['messageSource'] = 'feedbackneg'
                                            reply = question
                                            return Response(reply)
                            except:
                                question['messageSource'] = 'feedbackneg'
                                reply = question
                                return Response(reply)  
                        elif str({key: value for d in question["property"] for key, value in d.items()}['HR_issue']) == 'No':
                            question['messageText'] = [["Oh I see."], ["Okay."], 
                                                       ["Just Cool down."], ["Everything will be fine."],
                                                       ['Would you like to have more assistance.?']]
                            question['messageSource'] = 'feedbackneg'
                            question['filter'] = 'quest'
                            question['input'] = ['Yes', 'No']
                            reply = question
                            try:
                                if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                    question['messageText'] = [['How can I be of further assistance.?'], 
                                                               ['Please Select a category.']]
                                    question['messageSource'] = 'messageFromBot'
                                    question['filter'] = 'normal'
                                    question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                    reply = question
                                    req_cache.delete()
                                    return Response(reply)
                                elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                    question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                    question['messageSource'] = 'messageFromBot'
                                    question['filter'] = 'normal'
                                    question['action'] = 'stop'
                                    reply = question
                                    req_cache.delete()
                                    return Response(reply)
                            except:
                                question['messageSource'] = 'feedbackneg'
                                reply = question
                                return Response(reply)
                except:
                    question['messageSource'] = 'feedbackneg'
                    reply = question
                    return Response(reply)
            elif str({key: value for d in question["property"] for key, value in d.items()}['Anonymity_Emp']) == 'No':
                question['messageText'] = [["I appreciate your bravery."], 
                                           ["I'll do everything in my capacity for you. Don't worry."],
                                           ["Do you want to talk to our HR person regarding the same."]]
                question['messageSource'] = 'feedbackneg'
                question['filter'] = 'hrissue'
                question['input'] = ['Yes', 'No']
                reply = question
                try:
                    if {key: value for d in question["property"] for key, value in d.items()}.has_key('HR_issue'):
                        if str({key: value for d in question["property"] for key, value in d.items()}['HR_issue']) == 'Yes':
                            question['messageText'] = [["Fair enough, shall I Dial.?"]]
                            question['messageSource'] = 'feedbackneg'
                            question['input'] = ['Yes', 'No']
                            question['filter'] = 'dial'
                            reply = question
                            try:
                                if {key: value for d in question["property"] for key, value in d.items()}.has_key('Dial'):
                                    if str({key: value for d in question["property"] for key, value in d.items()}['Dial']) == 'Yes':
                                        question['messageText'] = [["Okay."], ["I am dialling."],
                                                                   ['Would you like to have more assistance.?']]
                                        question['messageSource'] = 'feedbackneg'
                                        question['filter'] = 'quest'
                                        question['input'] = ['Yes', 'No']
                                        reply = question
                                        try:
                                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                question['messageText'] = [['How can I be of further assistance.?'], 
                                                                           ['Please Select a category.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['action'] = 'stop'
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                        except:
                                            question['messageSource'] = 'feedbackneg'
                                            reply = question
                                            return Response(reply)
                                    elif str({key: value for d in question["property"] for key, value in d.items()}['Dial']) == 'No':
                                        question['messageText'] = [["Oh I see."], ["Okay."], ["Just Cool down."], 
                                                                   ["Everything will be fine."],
                                                                   ['Would you like to have more assistance.?']]
                                        question['messageSource'] = 'feedbackneg'
                                        question['filter'] = 'quest'
                                        question['input'] = ['Yes', 'No']
                                        reply = question
                                        try:
                                            if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                                question['messageText'] = [['How can I be of further assistance.?'], 
                                                                           ['Please Select a category.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                            elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                                question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                                question['messageSource'] = 'messageFromBot'
                                                question['filter'] = 'normal'
                                                question['action'] = 'stop'
                                                reply = question
                                                req_cache.delete()
                                                return Response(reply)
                                        except:
                                            question['messageSource'] = 'feedbackneg'
                                            reply = question
                                            return Response(reply)
                            except:
                                question['messageSource'] = 'feedbackneg'
                                reply = question
                                return Response(reply)  
                        elif str({key: value for d in question["property"] for key, value in d.items()}['HR_issue']) == 'No':
                            question['messageText'] = [["Oh I see."], ["Okay."], ["Just Cool down."], ["Everything will be fine."],
                                                       ['Would you like to have more assistance.?']]
                            question['messageSource'] = 'feedbackneg'
                            question['filter'] = 'quest'
                            question['input'] = ['Yes', 'No']
                            reply = question
                            try:
                                if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                                    question['messageText'] = [['How can I be of further assistance.?'], 
                                                               ['Please Select a category.']]
                                    question['messageSource'] = 'messageFromBot'
                                    question['filter'] = 'normal'
                                    question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                                    reply = question
                                    req_cache.delete()
                                    return Response(reply)
                                elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                                    question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                                    question['messageSource'] = 'messageFromBot'
                                    question['filter'] = 'normal'
                                    question['action'] = 'stop'
                                    reply = question
                                    req_cache.delete()
                                    return Response(reply)
                            except:
                                question['messageSource'] = 'feedbackneg'
                                reply = question
                                return Response(reply)
                except:
                    question['messageSource'] = 'feedbackneg'
                    reply = question
                    return Response(reply)
        elif {key: value for d in question["property"] for key, value in d.items()}.has_key('IT_issue') and question['messageSource'] == 'HelpDesk' and question['filter'] == 'flag':
            if str({key: value for d in question["property"] for key, value in d.items()}['IT_issue']) == 'Yes':
                question['messageText'] = [[random.choice(fillers_negative)], 
                                           ['Hold on! I shall connect you with a person who will guide you regarding the same and will help you solve the issue.'],
                                           ['This is the contact number of the person: ######'],
                                           ['Would you like to have more assistance.?']]
                question['messageSource'] = 'HelpDesk'
                question['filter'] = 'quest'
                question['input'] = ['Yes', 'No']
                reply = question
                try:
                    if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                        question['messageText'] = [['How can I be of further assistance.?'], 
                                                   ['Please Select a category.']]
                        question['messageSource'] = 'messageFromBot'
                        question['filter'] = 'normal'
                        question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                        reply = question
                        req_cache.delete()
                        return Response(reply)
                    elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                        question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                        question['messageSource'] = 'messageFromBot'
                        question['filter'] = 'normal'
                        question['action'] = 'stop'
                        reply = question
                        req_cache.delete()
                        return Response(reply)
                except:
                    question['messageSource'] = 'HelpDesk'
                    reply = question
                    return Response(reply)
            elif str({key: value for d in question["property"] for key, value in d.items()}['IT_issue']) == 'No':          
                question['messageText'] = [['Oh! I am really sorry!!'], 
                                           ["I couldn't understand what your real issue is."],
                                           ['Switching to human for further assistance.'],
                                           ['Would you like to have more assistance.?']]
                question['messageSource'] = 'HelpDesk'
                question['filter'] = 'quest'
                question['input'] = ['Yes', 'No']
                reply = question
                try:
                    if str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'Yes':
                        question['messageText'] = [['How can I be of further assistance.?'], 
                                                   ['Please Select a category.']]
                        question['messageSource'] = 'messageFromBot'
                        question['filter'] = 'normal'
                        question['input'] = ['Recruitment', 'FeedBack', 'HelpDesk']
                        reply = question
                        req_cache.delete()
                        return Response(reply)
                    elif str({key: value for d in question["property"] for key, value in d.items()}['Question']) == 'No':
                        question['messageText'] = [['Thank You for your time.'], ['See you again.']]
                        question['messageSource'] = 'messageFromBot'
                        question['filter'] = 'normal'
                        question['action'] = 'stop'
                        reply = question
                        req_cache.delete()
                        return Response(reply)
                except:
                    question['messageSource'] = 'HelpDesk'
                    reply = question
                    return Response(reply)
        elif {key: value for d in question["property"] for key, value in d.items()}.has_key('HRAppraise') and question['messageSource'] == 'recruitment':
            if str({key: value for d in question["property"] for key, value in d.items()}['HRAppraise']) == 'Yes':
                question['messageText'] = [["Do you have a JD created.?"]]
                question['messageSource'] = 'recruitment'
                question['input'] = ['Yes', 'No']
                question['filter'] = 'jd'
                reply = question
                try:
                    if {key: value for d in question["property"] for key, value in d.items()}.has_key('JD'):
                        if str({key: value for d in question["property"] for key, value in d.items()}['JD']) == 'Yes':
                            question['messageText'] = [["Can you send the JD by mail.?"], 
                                                       ["I shall send it to the HR department for approvals."]]
                            question['messageSource'] = 'messageFromBot'
                            question['filter'] = 'normal'
                            question['action'] = 'stop'
                            reply = question
                            return Response(reply)
                        elif str({key: value for d in question["property"] for key, value in d.items()}['JD']) == 'No':
                            question['messageText'] = [["Do you want me to create one for the role.?"]]
                            question['messageSource'] = 'recruitment'
                            question['input'] = ['Yes', 'No']
                            question['filter'] = 'createjd'
                            try:
                                if {key: value for d in question["property"] for key, value in d.items()}.has_key('CreateJD'):
                                    if str({key: value for d in question["property"] for key, value in d.items()}['CreateJD']) == 'Yes':
                                        question['messageText'] = [["Awesome! I'll create the JDs. Do send the resumes to this email ID."]]
                                        question['messageSource'] = 'messageFromBot'
                                        question['filter'] = 'normal'
                                        question['action'] = 'stop'
                                        reply = question
                                        return Response(reply)
                                    elif str({key: value for d in question["property"] for key, value in d.items()}['CreateJD']) == 'No':
                                        question['messageText'] = [["Do you have any previous candidate who had been hired for the role.?"], 
                                                                   ["I could take a look at their resume and then create the JD.!"]]
                                        question['messageSource'] = 'messageFromBot'
                                        question['filter'] = 'normal'
                                        question['action'] = 'stop'
                                        reply = question
                                        return Response(reply)  
                            except:
                                question['messageSource'] = 'recruitment'
                                reply = question
                                return Response(reply) 
                except:
                    question['messageSource'] = 'recruitment'
                    reply = question
                    return Response(reply)                          
            elif str({key: value for d in question["property"] for key, value in d.items()}['HRAppraise']) == 'No':
                question['messageText'] = [["I shall collect the same from the HR department then.!"]]
                question['messageSource'] = 'messageFromBot'
                question['filter'] = 'normal'
                question['action'] = 'stop'
                reply = question
                return Response(reply) 
        else:
            reply = question
        return Response(reply)
