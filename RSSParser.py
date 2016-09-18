import feedparser
import re

from config import settings as s

class Movies(object):
    def __init__(self, movie):
        self.movie = movie

    def getTitle(self):
        t = self.movie['title'].split("[")  # remove the [1080] part in title
        self.title = t[0]
        return self.title

    def getIMDBscore(self):
        text_score = self._scrapeScore()
        split_a = text_score.split(": ")  # splits the IMDB part from the score
        split_b = split_a[1].split("/")  # removes the /10 part
        score = split_b[0]
        return float(score)


    def _getSummary(self):
        self.summary = self.movie['summary']
        return self.summary

    def _scrapeScore(self):
        '''
        Scrapes the score part from the summary
        :return:
        '''
        summary = self._getSummary()
        lookup = re.search(s.IMDBRGX, summary)
        return summary[lookup.start():lookup.end()]

class YIFYXML(object):
    def __init__(self, rss_url):
        self.xml = feedparser.parse(rss_url)


    def get1080p(self):
        for x in self.xml.entries:
            if '[1080p]' in x['title']:
                y = Movies(x)
                print y.getTitle(), y.getIMDBscore()
                # if y.getIMDBscore() > 7:
                #     print y.getTitle(), y.getIMDBscore()





def getLatestMovies():
    parsed_xml = feedparser.parse(s.RSSURL)
    for x in parsed_xml.entries:
        if '[1080p]' in x['title']:
            print x['title']


if __name__ == '__main__':
    x = YIFYXML(s.RSSURL)
    x.get1080p()


    # rss = "https://yts.ag/rss"
    # parsed_rss = feedparser.parse(rss)
    #
    # print parsed_rss.feed
    # print parsed_rss.entries[0]['summary_detail']['value']
    #
    # text = 'the quick brown IMDB Rating: 4.9/10 <br> asd jumps over asd : <> the lazy dog'
    # # text = 'the quick brown IMDB Rating:<br> asd jumps over asd : <> the lazy dog'
    # pattern = 'IMDB Rating:[ ]\d*\.?\d[/][1][0]'
    # m = re.search(pattern, text)
    #
    # # if m:
    # #     print "yay"
    # # else:
    # #     print "nay"
    # p = re.compile(s.IMDBRGX)
    # p.search(text)
    # print p.match(s).group