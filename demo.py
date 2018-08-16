from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=['POST'])
def demo():
        
    return '''<?xml version="1.0" encoding="UTF-8"?>
     <D-Spin xmlns="http://www.dspin.de/data" version="0.4">
        <MetaData xmlns="http://www.dspin.de/data/metadata">
            <source></source>
            <Services>
                <CMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.clarin.eu/cmd/" CMDVersion="1.1" 
                    xsi:schemaLocation="http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1320657629623/xsd">
                    <Components>
                        <WebServiceToolChain>
                            <Toolchain>
                                <ToolInChain>
                                    <PID>11858/00-1778-0000-0004-BA56-7</PID>
                                    <Parameter name="version" value="0.4"></Parameter>
                                </ToolInChain>
                                </Toolchain>
                        </WebServiceToolChain>
                    </Components>
                </CMD>
            </Services>
        </MetaData>
        <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="de">
            <text>This text doesn't seem to matter?.</text>
            <tokens>
                <token ID="t_0">Тайӧ</token>
                <token ID="t_1">ӧтик</token>
                <token ID="t_2">сёрникузя</token>
                <token ID="t_3">тайӧ</token>
                <token ID="t_4">мӧд</token>
                <token ID="t_5">тайӧ</token>
                <token ID="t_6">куймӧд</token>
            </tokens>
            <sentences>
                <sentence ID="s_0" tokenIDs="t_0 t_1 t_2"></sentence>
                <sentence ID="s_1" tokenIDs="t_3 t_4"></sentence>
                <sentence ID="s_3" tokenIDs="t_5 t_6"></sentence>
            </sentences>
            <POStags tagset="stts">
                <tag ID="pt_0" tokenIDs="t_0">sometag1</tag>
                <tag ID="pt_1" tokenIDs="t_1">sometag2</tag>
                <tag ID="pt_2" tokenIDs="t_2">sometag3</tag>
                <tag ID="pt_3" tokenIDs="t_3">sometag4</tag>
                <tag ID="pt_4" tokenIDs="t_4">sometag5</tag>
                <tag ID="pt_5" tokenIDs="t_5">sometag6</tag>
                <tag ID="pt_6" tokenIDs="t_6">sometag7</tag>
            </POStags>
        </TextCorpus>
     </D-Spin>'''

if __name__ == "__main__":
    app.run()