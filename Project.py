import bs4, requests, docx, logging, openpyxl, re, csv, shutil, os
from pprint import pprint
from pyperclip import paste
from ExcelStuff.first import wordMetaData
from Word_Reference import WordReferenceClass, format_definition

# LOGGING ####################################################################################################
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.CRITICAL)
logging.debug("Start of program")

def clipboard_to_doc(clipboard):
    """Takes text from the clipboard and turns it into a doc"""
    d = docx.Document()
    d.add_paragraph(clipboard)
    d.save("Imported article.docx")

def repubblica_it(URL):
    "Takes a URL from repubblica.it and creates a formatted .docx"
    res = requests.get(URL)
    res.raise_for_status()
    # Check that it was able to request okay

    title_CSS = "div#container article > header > h1"
    summary_CSS = "body#detail header > p"
    body_CSS = "span#article-body"

    soup = bs4.BeautifulSoup(res.text, "html.parser") # get rid of the error
    # Where to find each piece of text
    title = soup.select(title_CSS)
    summary = soup.select(summary_CSS)
    body = soup.select(body_CSS)

    # Get the text
    try:
        title_text = title[0].text.strip()
    except IndexError: 
        title_text = ""
    try:
        summary_text = summary[0].text.strip()
    except IndexError:
        summary_text = ""
    body_text = body[0].text.strip()

    # Put the text into the document
    d = docx.Document()
    d.add_paragraph(title_text)
    d.add_paragraph(summary_text)
    d.add_paragraph(body_text)

    # Label each section
    p1 = d.paragraphs[0]
    p2 = d.paragraphs[1]
    p3 = d.paragraphs[2]

    # Format each section
    p1.style = "Title"
    p2.style = "Subtitle"
    p2.italic = True
    p3.style = "Normal"

    # Save the document
    d.save("Imported article.docx")

def URL_or_content(clipboard):
    """Takes whatever is on the clipboard and turns it into a docx

    \nIf it's a URL from repubblica.it uses the repubblica_it function
    
    \nOtherwise adds clipboard directly to document
    """
    URL_Regex = re.compile(r"repubblica")
    mo = URL_Regex.search(clipboard)

    if mo == None:
        clipboard_to_doc(clipboard)
    else:
        repubblica_it(clipboard)

def getText(filename):
    "Turns .docx into a single string"
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)

clipboard = paste()
URL_or_content(clipboard) 
entire_text = getText("Imported article.docx")

def create_frequency_list_from_text(text):
    grab_word_regex = re.compile(r"[ \"](\w+'?\w*)[ \.\,\!\?]") # Match entire regex. 
    #                                                           # Extract the bit from within the ()
    mo2 = grab_word_regex.findall(text)                  # makes a list of each string

    global_dict = {}
    for word in mo2:
        lowerWord = word.lower()
        global_dict.setdefault(lowerWord,0)
        global_dict[lowerWord] += 1

    output_list = sorted(global_dict.items(), key=lambda x:x[1])
    output_list.reverse()
    return(output_list)

# TODO add words to frequency sheet ###########################################################################
# How many words already on list?

# TODO read csv and grab global data



# TODO Make local frequency list

output_list = create_frequency_list_from_text(entire_text)
# pprint(output_list)

from datetime import datetime as dt
now = dt.today()
now_str = now.strftime('%Y_%m_%d %H-%M-%S')

with open(f"csvs/Frequency_{now_str}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output_list)

with open(f"csvs/Frequency_{now_str}.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# d = docx.Document("Imported article.docx")
# d.add_page_break()
# for word in output_list[len(output_list)-5:]:
#     r, p, _def = WordReferenceClass(word[0]).word_info()

#     final_text = (f"""
#     word: \t\t{r}
#     pronunciation: \t{p}
#     definition: \t\t{_def}
#     """)
#     d.add_paragraph(final_text)
# d.save("Imported article.docx")

# TODO Ask if 10 words are known. ##############################################################################
#       if known, tick off
#       if unknown, email
# TODO Make an article highlighter to highlight known words/ unknown by frequency ##############################
print("Done!")