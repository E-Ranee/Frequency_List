import bs4, requests, docx, logging, re, csv, shutil, os
from pprint import pprint
from pyperclip import paste
from ExcelStuff.first import wordMetaData
from Word_Reference import WordReferenceClass, format_definition
import pandas as pd

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
    """Creates a list of words from the text and makes a panda-friendly dictionary"""
    grab_word_regex = re.compile(r"[ \"](\w+'?\w*)[ \.\,\!\?]") # Match entire regex. 
    #                                                           # Extract the bit from within the ()
    mo2 = grab_word_regex.findall(text)                  # makes a list of each string

    data = {"word": [],
        "frequency": [],
            "known": []} #previously known as global_dict
    for word in mo2:
        lowerWord = word.lower()
        data["word"].append(lowerWord)
        data["frequency"].append(1)
        data["known"].append(0)

        # global_dict.setdefault(lowerWord,0)
        # global_dict[lowerWord] += 1

    # output_list = sorted(global_dict.items(), key=lambda x:x[1])
    # output_list.reverse()
    # return(output_list)
    return data

# TODO add words to frequency sheet ###########################################################################
# How many words already on list?

# TODO read csv and grab global data



# TODO Make local frequency list

current_article_data = create_frequency_list_from_text(entire_text) # makes a dictionary for current article (word, frequency, known)
article_data_df = pd.DataFrame(current_article_data) # makes a data frame
article_data_df["frequency"] = article_data_df.groupby(["word"])["frequency"].transform("sum") # add up the frequency for each time word appears
article_data_df.drop_duplicates(inplace=True) # get rid of duplicate entries for each word

# Save the data frame for the article as a csv using a time-stamped name
from datetime import datetime as dt
now = dt.today()
now_str = now.strftime('%Y_%m_%d %H-%M-%S')
article_data_df.sort_values("frequency", axis = 0, ascending = False, inplace = True, ignore_index=True) # sort the data by frequency
article_data_df.reset_index(drop=True, inplace=True)
article_data_df.to_csv(f"csvs/Frequency_{now_str}.csv")

a = os.listdir(".\\csvs") # makes a list of each file in the csv folder
df = pd.concat([pd.read_csv(f".\\csvs/"+filename, index_col=0) for filename in a]) # concatenates each csv to a mega csv in current folder
df["frequency"] = df.groupby(["word"])["frequency"].transform("sum") # add up the frequencies for each word
df = df.drop_duplicates(subset=["word"]) # remove duplicate entries for each word
df.sort_values("frequency", axis = 0, ascending = False, inplace = True, ignore_index=True) # sort the data by frequency
df.reset_index(drop=True, inplace=True)
df.to_csv("combined_csv.csv", index=True, encoding="utf-8-sig") # save it in an accented character-friendly format

d = docx.Document("Imported article.docx")
d.add_page_break()
with open(f"csvs/Frequency_{now_str}.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    rows = [r for r in reader]
    no_of_rows = len(rows)

    for row in rows[no_of_rows-5:]:
        r, p, _def = WordReferenceClass(row[1]).word_info()
        final_text = (f"""
        word: \t\t{r}
        pronunciation: \t{p}
        definition: \t\t{_def}
        """)
        d.add_paragraph(final_text)
    d.save("Imported article.docx")

# TODO Ask if 10 words are known. ##############################################################################
#       if known, tick off
#       if unknown, email
# TODO Make an article highlighter to highlight known words/ unknown by frequency ##############################
print("Done!")