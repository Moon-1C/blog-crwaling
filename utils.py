from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenizer(text):
    okt = Okt()
     # 품사 태깅
    tagged_words = okt.nouns(text)
    
    # 조사, 어미 등을 제외한 단어만 추출
    #filtered_words = [word for word, tag in tagged_words if tag not in ['Josa', 'Eomi', 'Punctuation', 'Suffix']]
    return list(filter(lambda x: len(x) >= 2 and x not in ["제주","제주도","제주시"] , tagged_words))    #2글자 이상인것만 추출

def extract_important_words(texts):
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, max_features=150)
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer.get_feature_names_out()

