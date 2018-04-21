#encoding: utf-8
#https://github.com/sukiweb/CreandoUnChatbotEnPython/blob/master/Creando_un_bot_experto_en_Cruceros.ipynb

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    "Experto_cruceros",

    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/',
    database='chat_1',
    
    
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.51,
            'default_response': 'Disculpa, no he entendido lo que ha querido decir. Puede replantearlo.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Quiero guardar una cita',
            'output_text': 'Puede guardar una cita en http://google.com'
        },
    ],
    
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    
    read_only=True,
)
DEFAULT_SESSION_ID = chatbot.default_conversation_id

from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("./cruises_es.yml")


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
    #print("Estamos en chatbot")
    #pregunta = pregunta.replace('á','&atilde;').replace('é','&etilde;').replace('í','&itilde;').replace('ó','&otilde;').replace('ú','&utilde;').replace('ñ','&ntilde;')
    pregunta= u' '.join((pregunta, '')).encode('utf-8').strip()
    
    response = chatbot.get_response(pregunta)
    response = response.text.replace('&atilde;','á').replace('&etilde;','é').replace('&itilde;','í').replace('&otilde;','ó').replace('&utilde;','ú').replace('&ntilde;','ñ')
    #response = response.encode("utf-8",'replace')
    response = u' '.join((response, '')).decode('utf-8').strip()
    print response
    return response
#drop database....
#mongo chat_1 --eval "db.dropDatabase()"
