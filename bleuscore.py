from sacrebleu.metrics import BLEU

# Sample sentences from the corpus
references = [['President Obama has weakened our military by weakening our economy.',
               'He’s crippled us with wasteful spending, massive debt, low growth, a huge trade deficit and open borders.',
               'Our manufacturing trade deficit with the world is now approaching $1 trillion a year.']]

# Sample output from our chatbot
hypothesis = ("president and all want, i ’ m very honored that he did come up frankly. "
              "well , we ’ re going to win everything.").split('.')

# BLEU score
bleu = BLEU()
print(bleu.corpus_score(hypothesis, references))
