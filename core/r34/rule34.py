import copy
from collections import defaultdict
from xml.etree import cElementTree as ElementTree

import requests

from .objectClasses import Rule34Post


class Rule34:
    def __init__(self):
        pass

    def ParseXML(self, rawXML):
        """Parses entities as well as attributes following this XML-to-JSON "specification"
            Using https://stackoverflow.com/a/10077069"""
        """if "Search error: API limited due to abuse" in str(rawXML.items()):
            raise Rule34_Error('Rule34 rejected your request due to "API abuse"')"""

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
    def urlGen(tags=None, limit=None, id=None, PID=None, deleted=None, **kwargs):
        """Generates a URL to access the api using your input:
        :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
        :param limit: str ||How many posts you want to retrieve
        :param id: int ||The post id.
        :param PID: int ||The page number.
        :param deleted: bool||If True, deleted posts will be included in the data
        :param kwargs:
        :return: url string, or None
        All arguments that accept strings *can* accept int, but strings are recommended
        If none of these arguments are passed, None will be returned
        """
        # I have no intentions of adding "&last_id=" simply because its response can easily be massive, and all it returns is ``<post deleted="[ID]" md5="[String]"/>`` which has no use as far as im aware
        URL = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"
        if PID != None:
            if PID > 2000:
                raise Exception("Rule34 will reject PIDs over 2000")
            URL += "&pid={}".format(PID)
        if limit != None:
            URL += "&limit={}".format(limit)
        if id != None:
            URL += "&id={}".format(id)
        if tags != None:
            tags = str(tags).replace(" ", "+")
            URL += "&tags={}".format(tags)
        if deleted == True:
            URL += "&deleted=show"
        if PID != None or limit != None or id != None or tags != None:
            return URL
        else:
            return URL

    def findNew(self, old, new):
        """Returns unique posts by comparing old and new posts
        :param old: list || Old rule34 posts
        :param new: list || New rule34 posts
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

    def getPosts(self, tags=None, limit=None, PID=None, deleted=None):
        """Returns posts
        :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
        :param limit: str ||How many posts you want to retrieve
        :param PID: int ||The page number.
        :param deleted: bool||If True, deleted posts will be included in the data"""
        XML = requests.get(self.urlGen(tags=tags, limit=limit, PID=PID, deleted=deleted))
        XML = XML.text
        XML = ElementTree.XML(XML)
        XML = self.ParseXML(XML)
        imgList = []
        for post in XML['posts']['post']:
            image = Rule34Post()
            image.parse(post)
            imgList.insert(0, image)
        return imgList
