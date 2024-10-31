import matplotlib.pyplot as plt
import matplotlib

def plot_topic_distribution(lda_model, num_words=10):
    num_topics = lda_model.num_topics

    topics = []
    words = []
    weights = []

    for topic_id in range(num_topics):
        topic_terms = lda_model.show_topic(topic_id, topn=num_words)
        for term, weight in topic_terms:
            topics.append(f'Topic {topic_id + 1}')
            words.append(term)
            weights.append(weight)

    import pandas as pd
    df = pd.DataFrame({
        'Topic': topics,
        'Word': words,
        'Weight': weights
    })

    plt.figure(figsize=(12, 6))
    for topic in range(num_topics):
        topic_data = df[df['Topic'] == f'Topic {topic + 1}']
        plt.bar(topic_data['Word'], topic_data['Weight'], label=f'Topic {topic + 1}')

    plt.title('Весомые слова в каждой из подтем')
    plt.xlabel('Слова')
    plt.ylabel('Вес слова')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../res1.png')


