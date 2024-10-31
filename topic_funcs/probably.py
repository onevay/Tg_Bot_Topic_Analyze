import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def probably_topics(lda_model, dictionary, num_topics):
    matplotlib.use('TkAgg')
    topic_probs = np.zeros(num_topics)

    for word_id in range(len(dictionary)):
        word_probabilities = lda_model.get_term_topics(word_id)

        for topic_id, probability in word_probabilities:
            topic_probs[topic_id] += probability

    topic_probs /= np.sum(topic_probs)

    labels = [f'Топик {i}' for i in range(num_topics)]
    sizes = topic_probs * 100

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Значимость каждой подтемы в общем массиве ответов')
    plt.axis('equal')

    plt.savefig('../res2.png')