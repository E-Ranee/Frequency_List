import requests, bs4

def format_definition(word):
    r, p, _def = WordReferenceClass(word).word_info()

    print(f"""
             word: \t{r}
    pronunciation: \t{p}
       definition: \t{_def}
    """)

class WordReferenceClass():

    soup = None

    def __init__(self, word):
        URL = "https://www.wordreference.com/iten/" + word
        res = requests.get(URL)
        res.raise_for_status()
        self.soup = bs4.BeautifulSoup(res.text, "html.parser") # get rid of the error


    def word_info(self):
        "Searches for the EN translation of the word"

        p = ""
        r = ""
        _def = ""

        try:
            r = self.root_word()
        except IndexError:
            r = "Unknown word"

        try:
            p = self.pronunciation()
        except IndexError:
            p = "No pronunciation available"
        # print(definition(word))

        try:
            _def = self.IT_def()
        except:
            _def = "No additional information available"

        return r, p, _def


    def root_word(self):

        root_CSS = "div#articleHead > h3"
    
        root = self.soup.select(root_CSS)
        root_text = root[0].text.strip()
        return root_text

    def pronunciation(self):

        pronunciation_CSS = "span#pronWR"
    
        pronunciation = self.soup.select(pronunciation_CSS)
        pronunciation_text = pronunciation[0].text.strip()
        return pronunciation_text

    def IT_def(self):

        IT_def_CSS = ".WRD tr td:nth-child(2):not(.FrEx):not(.ToEx)"
    
        IT_def = self.soup.select(IT_def_CSS)
        IT_def_text = IT_def[1].text.strip()
        return IT_def_text

# def definition(word, htmlRes):

#     definition_CSS = ".WRD tr td:nth-child(3):not(.FrEx):not(.ToEx)"
   
#     definition = soup.select(definition_CSS)
#     definition_text = definition[1].text.strip()
#     definition_text2 = definition[2].text.strip()
#     definition_text3 = definition[3].text.strip()

    # extras = ["nnoun: Refers to person, place, thing, quality, etc.", 
    #     "vtrtransitive verb: Verb taking a direct object--for example, \"Say something.\" \"She found the cat.\"",
    #     "in vtr phrasal insepphrasal verb, transitive, inseparable: Verb with adverb(s) or preposition(s), having special meaning, not divisible--for example,\"go with\" [=combine nicely]: \"Those red shoes don\'t go with my dress.\" NOT [S]\"Those red shoes don\'t go my dress with.\"[/S]",
    #     "adjadjective: Describes a noun or pronoun--for example, \"a tall girl,\" \"an interesting book,\" \"a big house.\""
        
    #     ]


    # return definition_text, definition_text2, definition_text3

if __name__ == "__main__":
    format_definition("bandire")