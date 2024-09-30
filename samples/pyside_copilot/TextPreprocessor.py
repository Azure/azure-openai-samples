import re
import xx_ent_wiki_sm
import en_core_web_md

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class TextPreprocessor:

    def __init__(self):
        self.re_pre_despace = re.compile(r'\s+')
        self.re_pre_dehtml = re.compile(r'<[^>]+>')
        self.re_pre_depunc = re.compile(r'[^\w\s]')
        
        self.nlp = xx_ent_wiki_sm.load()
        self.nlp_en = en_core_web_md.load()
        return
    

    def __re_text(self, text: str) -> str:
        text = text.lower()
        text = self.re_pre_dehtml.sub(' ', text)
        text = self.re_pre_despace.sub(' ', text)
        text = self.re_pre_depunc.sub('', text)
        return text
    
    
    def process_text_pre(self, text: str) -> str:
        text = self.__re_text(text)

        doc = self.nlp(text)
        text = ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])
        return text
    

    def process_text_en(self, text: str) -> str:
        doc = self.nlp_en(text)
        list_text = []
        for token in doc:
            if not token.is_stop and not token.is_punct:
                if token.lemma_ != '':
                    list_text.append(token.lemma_)
                else:
                    list_text.append(token.text)
        text = ' '.join(list_text)
        return text
