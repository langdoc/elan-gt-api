from flask import Flask
from flask import request
import re
from collections import OrderedDict
import xml.etree.ElementTree as ET
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3
import itertools

app = Flask(__name__)

@app.route("/", methods=['POST'])
def elan():
    
    # This saves the input so it is easier to examine what is going on
    with open("examples/input_from_elan.xml","wb") as fo:
        fo.write(request.data)
    
    # The language attribute apparently comes from ELAN too somehow
    # This should be picked automatically, and the analyser should
    # be selected based on that. This works very well when each
    # speaker speaks different language (one Komi, another Russian etc.)
    # Q: what should be done if the analyser for one language is not found?
    cg = Cg3("kpv")
    
    tree = ET.fromstring(request.data)

    xmlns = {'corpus': '{http://www.dspin.de/data/textcorpus}'}
    
    # The sentences are somehow tokenized, but this should be done better…
    
    tokens = []
    for token in tree.findall('.//{corpus}token'.format(**xmlns)):
        text = re.sub("(,|\.|\?|!)", '', token.text)
        tokens.append(text)
    
    # This is kind of a fake-approach to just pick one of the readings,
    # since I don't know if it is possible to have that through the pipeline now
    
    disambiguations = cg.disambiguate(tokens)
    
    print(disambiguations)
    
    tags = []
    lemmas = []
    
    for disambiguation in disambiguations:
        possible_words = disambiguation[1]
        temp_list = []
        for possible_word in possible_words:
            possible_word.morphology.pop()
            temp_list.append(possible_word.morphology)
        flat_list = list(itertools.chain(*temp_list))
        unique_list = list(set(flat_list))
        tags.append('|'.join(unique_list))
        
    for disambiguation in disambiguations:
        possible_words = disambiguation[1]
        temp_list = []
        for possible_word in possible_words:
            temp_list.append(possible_word.lemma)
        unique_list = list(set(temp_list))
        lemmas.append('|'.join(unique_list))

    # I collect here everything into distinct lists so that I can later
    # loop over them. There is probably some better data structure in
    # Python -- maybe what comes out from uralicNLP is already something better?
    
    token_ids = []
    for token in tree.findall('.//{corpus}token'.format(**xmlns)):
        token_ids.append(token.attrib['ID'])
    
    tag_ids = []
    for token_id in token_ids:
        tag_ids.append(re.sub('t', 'pt', token_id))
    
    # This constructs the XML, the namespaces were bit tricky, but everything
    # seems to work now. First we create POStags node and then put it to the
    # right place.
    
    pos_tag = ET.Element("ns2:POStags", tagset="stts")
    
    textcorpus = tree.find('.//{corpus}TextCorpus'.format(**xmlns))
    textcorpus.append(pos_tag)
    
    # Printing here was useful to examine what is going on
    
    # for id in token_ids:
    #     print('token ids:' + id)
    # for id in tag_ids:
    #     print('tag ids:' + id)
    # for id in tags:
    #     print('tag:' + id)
    
    # This adds POS tags and morphology into tags under POStags node
    
    for token_id, tag_id, tag in zip(token_ids, tag_ids, tags):
        current_tag = ET.Element("tag", tokenIDs=token_id, ID=tag_id)
        current_tag.text = tag
        textcorpus.append(current_tag)
   
   # This writes the output into file for examination
   
#    with open("output.txt","wb") as fo:
#        fo.write(ET.tostring(tree))
    
    return(ET.tostring(tree))

if __name__ == "__main__":
    app.run()
