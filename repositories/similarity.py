import tensorflow_hub as hub
import tensorflow_text as text
from sklearn.metrics.pairwise import cosine_similarity
import time

preprocess_path = "a.i.models/bert_en_uncased_preprocess_3"
bert_12_path = "a.i.models/bert_en_uncased_L-12_H-768_A-12_4"
bert_24_path = "a.i.models/bert_en_uncased_L-24_H-1024_A-16_4"

bert_preprocess = hub.KerasLayer(hub.load(preprocess_path))
bert_encoder_12 = hub.KerasLayer(hub.load(bert_12_path))
# bert_encoder_24 = hub.KerasLayer(hub.load(bert_24_path))

print ("hello")

def get_sentence_embeding_12(sentences):
    preprocessed_text = bert_preprocess(sentences)
    return bert_encoder_12(preprocessed_text)['pooled_output']

# def get_sentence_embeding_24(sentences):
#     preprocessed_text = bert_preprocess(sentences)
#     return bert_encoder_24(preprocessed_text)['pooled_output']




def get_similarity(ph1, ph2):
    start = time.time()
    e12 = get_sentence_embeding_12([ph1, ph2])
    end = time.time()
    print ("inside ", end - start)
   # e24 = get_sentence_embeding_24([ph1, ph2])
   # e24 = [0, 0]
    return (cosine_similarity([e12[0]],[e12[1]])[0][0])# + cosine_similarity([e24[0]],[e24[1]])[0][0])/2


