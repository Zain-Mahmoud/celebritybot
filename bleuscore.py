"Calculating sample BLEU Score"
from sacrebleu.metrics import BLEU

# Sample sentences from the corpus
REFERENCES = [['President Obama has weakened our military by weakening our economy.',
               'He’s crippled us with wasteful spending, massive debt, low growth, a huge trade deficit and open \
               borders.',
               'Our manufacturing trade deficit with the world is now approaching $1 trillion a year.']]

# Sample output from our chatbot
HYPOTHESIS = ("president and all want, i ’ m very honored that he did come up frankly. "
              "well , we ’ re going to win everything.").split('.')


if __name__ == '__main__':

    BLEU_SCORE = BLEU()
    print(BLEU_SCORE.corpus_score(HYPOTHESIS, REFERENCES))

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sacrebleu.metrics.BLEU'],
        'max-line-length': 120
    })
