# -*- coding: utf-8 -*-
#Exrtaido de....
#https://github.com/sukiweb/CreandoUnChatbotEnPython/blob/master/Creando_un_bot_experto_en_Cruceros.ipynb

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    "Experto_cruceros",

    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/',
    database='chatterbot_cruises',
    
    
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.51,
            'default_response': 'Disculpa, no te he entendido bien, sólo soy experto en viajes. ¿Puedes ser más específico?.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Quiero reservar un crucero',
            'output_text': 'Puedes reservarlo ahora en: https://www.logitravel.com/cruceros/'
        },
    ],
    
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    
    read_only=True,
)
DEFAULT_SESSION_ID = chatbot.default_conversation_id

from chatterbot.trainers import ChatterBotCorpusTrainer
'''
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("./cruises_es.yml")
'''

'''
conversation = [
"Hello",
"Hi there!",
"How are you doing?",
"I'm doing great.",
"That is good to hear",
"Thank you.",
"You're welcome."
]

chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)
'''
#request = raw_input("Escriba su pregunta: ")
'''
response = chatbot.get_response(None)
response = u' '.join((response.text, '')).encode('utf-8').strip()
print 'Bot: '+response
'''
def responder(pregunta):
    print("Pregunta..."+pregunta)
    print("Estamos en chatbot")
    response = chatbot.get_response(pregunta)
    response = u' '.join((response.text, '')).encode('utf-8').strip()
    print response
    return response
