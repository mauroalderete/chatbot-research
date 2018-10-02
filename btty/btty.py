from chatterbot import ChatBot


btty = ChatBot(
    'Btty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.VariableInputTypeAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    database='./btty0.sqlite3',
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    read_only=True,
    response_selection_method='chatterbot.response_selection.get_random_response'
)

print("Btty Running")

btty.get_response('')
while True:
    try:
        human = input(">>")
        btty.get_response(human)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

print("Btty terminated")
