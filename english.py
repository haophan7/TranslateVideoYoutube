from youtube_transcript_api import YouTubeTranscriptApi

outls = []

tx = YouTubeTranscriptApi.get_transcript('gzRXsXQJXmw', languages=['de', 'en'])
for i in tx:
    outtxt = (i['text'])
    outls.append(outtxt)

    with open("op.txt", "a") as opf:
        opf.write(outtxt + "\n")

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

vectorizer.fit(outls)

print("Vocabulary: ", vectorizer.vocabulary_)
