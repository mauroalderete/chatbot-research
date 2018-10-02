# -*- coding: utf-8 -*-

from chatterbot import ChatBot

btty = ChatBot(
    'Btty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    database='./btty0.sqlite3',
    trainer="chatterbot.trainers.ChatterBotCorpusTrainer"
)

btty.train(
    "chatterbot.corpus.spanish"
)

print("Btty training corpus spanish default finish")
