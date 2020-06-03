class Rule34dbPost:
    """To convert fetched db posts into object"""

    id = None

    def parse(self, post):

        self.id = int(post['id'])