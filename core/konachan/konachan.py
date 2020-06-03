import copy
from collections import defaultdict
from xml.etree import cElementTree as ElementTree

import requests

from .objectClasses import KonachanPost


class Konachan:
    def __init__(self):
        pass

    def ParseXML(self, rawXML):
        """Parses entities as well as attributes following this XML-to-JSON "specification"
            Using https://stackoverflow.com/a/10077069"""

        d = {rawXML.tag: {} if rawXML.attrib else None}
        children = list(rawXML)
        if children:
            dd = defaultdict(list)
            for dc in map(self.ParseXML, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {rawXML.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if rawXML.attrib:
            d[rawXML.tag].update(('@' + k, v) for k, v in rawXML.attrib.items())
        if rawXML.text:
            text = rawXML.text.strip()
            if children or rawXML.attrib:
                if text:
                    d[rawXML.tag]['#text'] = text
            else:
                d[rawXML.tag] = text
        return d

    @staticmethod
    def urlGen(tags=None, limit=None, page=None, **kwargs):
        """Generates a URL to access the api using your input:
        :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
        :param limit: str ||How many posts you want to retrieve
        :param id: int ||The post id.
        :param page: int ||The page number.
        :param deleted: bool||If True, deleted posts will be included in the data
        :param kwargs:
        :return: url string, or None
        All arguments that accept strings *can* accept int, but strings are recommended
        If none of these arguments are passed, None will be returned
        """
        URL = "https://konachan.com/post.xml?"
        if page != None:
            if page > 2000:
                raise Exception("Konachan will reject pages over 2000")
            URL += "&page={}".format(page)
        if limit != None:
            URL += "&limit={}".format(limit)
        if tags != None:
            tags = str(tags).replace(" ", "+")
            URL += "&tags={}".format(tags)
        
        return URL

    def findNew(self, old, new):
        """Returns unique posts by comparing old and new posts
        :param old: list || Old Konachan posts
        :param new: list || New Konachan posts
        """

        self.new = copy.deepcopy(new) # so it won't modify the original value of new list
        
        for post in old:
            count = 0

            for newpost in self.new:
                if post.id == newpost.id:
                    del self.new[count]
                    count = count - 1

                count = count + 1

        return(self.new)

    def getPosts(self, tags=None, limit=None, page=None):
        """Returns posts
        :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
        :param limit: str ||How many posts you want to retrieve
        :param page: int ||The page number."""
        XML = requests.get(self.urlGen(tags=tags, limit=limit, page=page))
        XML = XML.text
        XML = ElementTree.XML(XML)
        XML = self.ParseXML(XML)
        imgList = []
        for post in XML['posts']['post']:
            image = KonachanPost()
            image.parse(post)
            imgList.insert(0, image)
        return imgList
