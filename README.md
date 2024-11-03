# Tg-Bot-Topic-Analyze
This telegram bot allows you to analyze the results of surveys or any other text set. The result is displayed in a simple and understandable form

# Project structure
- **_app_**: Telegram bot + database (PostgreSQL)
- **how_to_use**: Deployment guide, test runs and usage
- **topic_funcs**: Text preprocessing and analysis
- **main**: Launching the main functionality

The purpose of the project
- Facilitate the analysis of the results of surveys, reviews, questionnaires and other text sets
- User-friendly and flexible user interface in telegram bot
- Accessibility for everyone, many aspects of the type of survey are difficult to find in a similar implementation

<h1 align=center>Briefly about the implementation</h1>

<p align=center>First of all, we process the text by normalizing and lemmatizing it. The processed version is analyzed using the LDA model (its advantages will also be discussed) and then the result is visualized and displayed in the form of 2 diagrams.
<br> <br>
In addition, the interface of the telegram bot is used with the passage of a questionnaire and a request to an analogue of the GPT chat, which you can read in more detail in the article on the <a href="https://habr.com/p/855786/">hubr</a>
</p>
<br>
<p align=center>
 
</p>
<br>

## How to build on your device
It is written about this in the section **how_to_use**, but to summarize briefly, it is necessary to copy the directory, install dependencies and enter private data

## What tools did we use
Libraries such as **mystem** and **nltk** are used for reading, processing, clearing stop words and normalization. Their functionality covers all needs and works great compared to other options that we also wanted to implement

To analyze the text and highlight semantic groups, **gensim** and its **lda model** are used, which differs from other models in better process quality and good processing speed

For visualization (looking at diagrams), we use **matplotlib**, for which there are simply no analogues of the same level

Instead of the API for **GPT Chat**, we use a third-party project **g4f**, which is already used by hundreds of projects, and the author himself regularly updates and supplements the library, which stands out more and more every day

For ease of use, we use a telegram bot implemented using the most up-to-date **aiogram**. Its functionality is discussed in detail in the article. We also decided to include the questionnaire and record information in the database, not using NoSQL and Alchemy for this, but using standard queries and **Psycopg**. This choice is associated with a small number of requests

## Autors
- Kolpakov Makar
- Folomkin Ivan
