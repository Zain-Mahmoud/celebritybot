from graph import Graph
from sacrebleu.metrics import BLEU

references = [['President Obama has weakened our military by weakening our economy.',
               'He’s crippled us with wasteful spending, massive debt, low growth, a huge trade deficit and open borders.',
               'Our manufacturing trade deficit with the world is now approaching $1 trillion a year.']]
hypothesis = ("president and all want, i ’ m very honored that he did come up frankly. "
              "well , we ’ re going to win everything.").split('.')
bleu = BLEU()

print(bleu.corpus_score(hypothesis, references))
