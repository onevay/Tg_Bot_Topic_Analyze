import gensim
from topic_funcs.clean import cleaning_and_normalize, mstem, punctions_del
from gensim import corpora
from gensim.utils import simple_preprocess
from topic_funcs.thems import thems_count

def start(answers):

    answers = punctions_del(answers)
    list_of_answers = mstem(answers)
    list_of_answers = cleaning_and_normalize(list_of_answers)

    mydict = corpora.Dictionary([simple_preprocess(line) for line in list_of_answers])
    corpus = [mydict.doc2bow(simple_preprocess(line)) for line in list_of_answers]
    them_count = thems_count(mydict)
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=mydict,
                                            num_topics=them_count,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=30000,
                                            passes=15,
                                            alpha='auto',
                                            per_word_topics=True)
    stl = lda_model.print_topics()
    st = ''
    for i in range(1, them_count):
        st = st + "Группа номер: " + str(i) + "\n\n"
        st += stl[i][1] + '\n\n'
    lda_topics = lda_model.show_topics(num_words=5)
    for topic in lda_topics:
        print(topic)
    return f'В ходе одработки ответов было выделено {them_count} тем\nДалее вы можете ознакомиться с результатами', lda_model, them_count, mydict, corpus, st