import urllib2
import json
import string

token = ['Authorization','Bearer ...']      #insert auth token

def on_session_started(session_started_request, session):
    print ("Starting new session." )

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "diseaseIntent":
        return get_disease(intent)      
    elif intent_name == "usageIntent": 
        return get_usages(intent)
    elif intent_name == "alternateIntent": 
        return get_alternate(intent)
    elif intent_name == "sideEffectIntent": 
       return get_sideEffect(intent)
    elif intent_name == "AMAZON.HelpIntent": 
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return get_error_message()
        #raise ValueError("Invalid intent")
        
def get_error_message():
    session_attributes = {}
    card_title = "MedBook - Error"
    speech_output = "Sorry, I am not able to understand your question"
    reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop"
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    
        
def get_disease(intent):
    try:
        session_attributes = {}
        card_title = "MedBook - Disease Info"
        reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop"
        should_end_session = False
  
        disease_name = intent["slots"]["disease"]["value"]

        if (" " in disease_name) :
            disease_name=disease_name.replace(" ", "%20")

        url='http://www.healthos.co/api/v1/search/diseases/'+disease_name
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
        info = json.load(response)
    
        _str=info[0]['disease_info']
        if len( _str.split() )<15:
            _str = _str+" "+info[1]['disease_info']
        
        speech_output = _str
        speech_output+=". Do you wish to ask any other question?"
    
    except:
        speech_output = "Sorry , I am not sure about this one."
        speech_output+=" Do you wish to ask any other question?"
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    

def get_usages(intent):
    try:
        session_attributes = {}
        card_title = "MedBook - Drug Usage"
        reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop."
        should_end_session = False

        name = intent["slots"]["drugName"]["value"]

        name=name.strip(string.punctuation)
        if (" " in name) :
            name=name.replace(" ", "%20")

        
        url='http://www.healthos.co/api/v1/search/medicines/brands/'+name
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
        b = json.load(response)
        _id=b[0]['medicine_id']

        url='http://www.healthos.co/api/v1/medicines/brands/' + _id + '/usages'
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request) 
        b = json.load(response)
        
        usages=[]
        for i in range(len(b[0]['usages'])):
            usages.append(b[0]['usages'][i]['term'])

        name=name.replace("%20"," ")
        speech_output = name.capitalize() + " is generally used for " + (", ".join(usages[:-1])) + " and " + usages[-1] + "."
        speech_output+=". Do you wish to ask any other question?"
    except:
        try:
            name=name.replace("%20"," ")
            speech_output = "Sorry , I cant find the use of "+ name
            speech_output+=" Do you wish to ask any other question?"
        except:
            speech_output = "Sorry , I cant find the use."
            speech_output+=" Do you wish to ask any other question?"
            
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
           
def get_alternate(intent):
    try:
        session_attributes = {}
        card_title = "MedBook - Alternate Medicines"
        reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop."
        should_end_session = False

        name = intent["slots"]["drugNameA"]["value"]

        name=name.strip(string.punctuation)
        if (" " in name) :
            name=name.replace(" ", "%20")
        
        url='http://www.healthos.co/api/v1/search/medicines/brands/'+name
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
        b = json.load(response)
        id=b[0]['medicine_id']

        url='http://www.healthos.co/api/v1/medicines/brands/' + id + '/alternatives?page=1&size=5'
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request) 
        b = json.load(response)

        _len=len(b)
        if _len > 1:
            alternatives=[]
            for i in range(len(b)):
                alternatives.append(b[i]['name'])
            name=name.replace("%20"," ")
            speech_output = "Alternatives of " + name + " are " + (", ".join(alternatives[:-1])) + " and " + alternatives[-1]
            speech_output+=". Do you wish to ask any other question?"
        else:
            name=name.replace("%20"," ")
            speech_output = "Alternatives of " + name + " is " + b[0]['name']
            speech_output+=". Do you wish to ask any other question?"
            
    except:
        try:
            name=name.replace("%20"," ")
            speech_output = "Sorry , I cant find the alternatives of "+name
            speech_output+=". Do you wish to ask any other question?"
        except:
            speech_output = "Sorry , I cant find the alternatives."
            speech_output+=" Do you wish to ask any other question?"
         
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_sideEffect(intent):
    try:
        session_attributes = {}
        card_title = "MedBook - Side Effects"
        reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop."
        should_end_session = False

        name = intent["slots"]["drugNameC"]["value"]

        name=name.strip(string.punctuation)
        if (" " in name) :
            name=name.replace(" ", "%20")
        
        
        url='http://www.healthos.co/api/v1/search/medicines/brands/'+name
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
        b = json.load(response)
        id=b[0]['medicine_id']
            
        url='http://www.healthos.co/api/v1/medicines/brands/' + id + '/side_effects'
        request = urllib2.Request(url)
        request.add_header(token[0],token[1])
        request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request) 
        b = json.load(response)
        
        _len=len(b[0]['side_effects'])
        if _len > 1:
            side_effects=[]
            for i in range(len(b[0]['side_effects'])):
                side_effects.append(b[0]['side_effects'][i]['term'])

            name=name.replace("%20"," ")
            speech_output = "The side effects of " + name + " are " + (", ".join(side_effects[:-1])) + " and " + side_effects[-1]
            speech_output+=". Do you wish to ask any other question?"
        else:
            name=name.replace("%20"," ")
            speech_output = "The side effect of " + name + " is " + b[0]['side_effects'][i]['term']
            speech_output+=". Do you wish to ask any other question?"
            
    except:
        try:
            name=name.replace("%20"," ")
            speech_output = "Sorry , I cant find side-effects of "+name
            speech_output+=". Do you wish to ask any other question?"
        except:
            speech_output = "Sorry , I cant find the side-effects."
            speech_output+=" Do you wish to ask any other question?"
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



def on_session_ended(session_ended_request, session):
    print ("Ending session.")
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "MedBook - Thanks"
    speech_output = "Thank you for using MedBook.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "MedBook"
    speech_output = "Welcome to MedBook. " \
                    "Would you like to ask me about a disease or medicine?" 
    
    reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop."
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_help_response():
    session_attributes = {}
    card_title = "MedBook - Help"
    speech_output = "Welcome to MedBook. " \
                    "I can tell you about a disease, use of a medicine, alternative of a medicine, or side effects of medicines. " \
                    "For example," \
                    " ask me : what is malaria," \
                    " or try : what is the use of paracetamol," \
                    " to get alternatives of a medicine ask : what is the alternative of cetrizien," \
                    " or to know about side-effects of a medicine, you can ask me : what are the side effects of ciplox," \
                    " To exit please tell stop."
    
    reprompt_text = "Please ask me about a disease or a medicine, or to exit please tell stop."
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
    

def lambda_handler(event, context):
    
    if (event["session"]["application"]["applicationId"] != "amzn1.ask.skill........"):             #insert the skill id
        raise ValueError("Invalid Application ID")
    
    try:    
        if event["session"]["new"]:
            on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

        if event["request"]["type"] == "LaunchRequest":
            return on_launch(event["request"], event["session"])
        elif event["request"]["type"] == "IntentRequest":
            return on_intent(event["request"], event["session"])
        elif event["request"]["type"] == "SessionEndedRequest":
            return on_session_ended(event["request"], event["session"])
    except:
        get_error_message()
