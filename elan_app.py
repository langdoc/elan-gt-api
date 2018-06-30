from flask import Flask
from flask import request
import re
from collections import OrderedDict
import xml.etree.ElementTree as ET
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3

app = Flask(__name__)

@app.route("/", methods=['POST'])
def elan():
    
    # This saves the input so it is easier to examine what is going on
    with open("examples/input_from_elan.xml","wb") as fo:
        fo.write(request.data)
    
    # The language attribute apparently comes from ELAN too somehow
    cg = Cg3("kpv")
    
    tree = ET.fromstring(request.data)

    xmlns = {'corpus': '{http://www.dspin.de/data/textcorpus}'}
    
    tokens = []
    for token in tree.findall('.//{corpus}token'.format(**xmlns)):
        tokens.append(token.text)
    
    # This is kind of a fake-approach to just pick one of the readings,
    # since I don't know if it is possible to have that through the pipeline now
    
    disambiguations = cg.disambiguate(tokens)
    
    forms = []
    lemmas = []
    tags_all = []
    
    for disambiguation in disambiguations:
        forms.append(disambiguation[0])
        
        possible_words = disambiguation[1]
        
        one_analysis = possible_words[0]
        lemmas.append(one_analysis.lemma)
        tags_all.append(one_analysis.morphology)
    
    clean_tags = [[re.sub('(@.+@|(?<=<W).+>)', '', tag) for tag in m] for m in tags_all]
    [tag_list.remove('<W') for tag_list in clean_tags]
    uniq_tags = [list(OrderedDict.fromkeys(tag_list)) for tag_list in clean_tags]
    tags = [' | '.join(tag_list) for tag_list in uniq_tags]
    
    token_ids = []
    for token in tree.findall('.//{corpus}token'.format(**xmlns)):
        token_ids.append(token.attrib['ID'])
    
    tag_ids = []
    for token_id in token_ids:
        re.sub('t', 'pt', token_id)
    
    # This constructs the XML, I'm not sure if this works at all
    # I think I wanted to have there just some random content
    # to get something through 
    
    pos_tag = ET.Element("POStags", tagset="stts")
    
    textcorpus = tree.find('{corpus}TextCorpus'.format(**xmlns))
    textcorpus.append(pos_tag)
    
    print(tags)
    for token_id, tag_id, tag in zip(token_ids, tag_ids, tags):
        current_tag = ET.Element("tag", tokenIDs=token_id, ID=tag_id)
        current_tag.text = tag
        print(tag)
        textcorpus = tree.find('POStags')
        textcorpus.append(current_tag)

    postags = tree.find('POStags')
    tag = ET.Element("tag", tokenIDs="t_0", ID="pt_0")
    tag.text = "ok"
    postags.append(tag)
   
   # This writes the output into file for examination
   
    with open("output.txt","wb") as fo:
        fo.write(ET.tostring(tree))
    
    return(ET.tostring(tree))

if __name__ == "__main__":
    app.run()
