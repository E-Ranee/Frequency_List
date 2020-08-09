# Idea: have document with an article
# Have a document with a csv? with each word, the number of times it has appeared, if it is known
# Run through article, extract word
# Add to word freq document
# Ask if 10 words are known
# If not, send in email

# Have function that takes any article, highlight unknown words and their frequency

import pprint
input_data = "Secondo le previsioni del ilmeteo.it, ci troviamo di fronte alla prima vera ondata di caldo proveniente dal Nord Africa, e la colonnina di mercurio è destinata ad aumentare vertiginosamente nei prossimi giorni. Il primo weekend del mese di agosto sarà caratterizzato dal caldo intenso, anche se non vivremo due giornate all'insegna dell'assoluta stabilità atmosferica: tra sabato 1 e domenica 2 agosto l'alta pressione verrà lievemente fiaccata da correnti più instabili di origine atlantica. Sabato 1 agosto il bollente anticiclone africano dominerà incontrastato da Nord a Sud: i termometri voleranno fino a 40 C, in particolare sulla Toscana, con punte anche superiori sulle zone interne delle due isole maggiori. Non andrà meglio sul resto del Paese, con 38 gradi sulle basse pianure del Nord e su parte del Lazio. Domenica 2, dopo un avvio di giornata ancora molto caldo e asciutto, ecco che un fronte instabile in discesa dal Nord Europa darà vita a temporali e piogge sull'arco alpino centro-occidentale (non sono escluse forti grandinate). Entro la serata qualche temporale potrà sconfinare fin verso le pianure di Piemonte, Lombardia e Veneto. Il vortice depressionario riuscirà a sfondare sul nostro Paese con l'inizio della prossima settimana, portando rovesci temporaleschi molto violenti con il pericolo di grandinate e forti colpi di vento."
dictionary = {}

test_list = input_data.lower().split()
for item in test_list:
    dictionary.setdefault(item, 0)
    dictionary[item] += 1

output_list = sorted(dictionary.items(), key=lambda x:x[1])
output_list.reverse()
pprint.pprint(output_list)