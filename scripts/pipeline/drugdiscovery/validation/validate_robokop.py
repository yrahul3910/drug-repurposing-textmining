from py2neo import Graph


class RobokopValidator:
    """
    Validates pairs from the pipeline using ROBOKOP.
    """
    def __init__(self, pairs: list, user: str = 'neo4j', password: str = 'password'):
        """
        Initializes the validator.
        :param pairs: The list of pairs.
        :param user: Username to connect to the DB
        :param password: Password to connect to the DB
        """
        self.pairs = pairs
        self.hostname = 'robokopdb1.renci.org'
        self.port = 7687
        self.user = user
        self.password = password

    def validate(self):
        g = Graph(host=self.hostname, port=self.port, user=self.user, password='ncatsgamma')

        for pair in self.pairs:
            query = f'MATCH (n)-[r]-(m) WHERE n.name CONTAINS "${pair[0]}" AND m.name CONTAINS "${pair[1]}" ' \
                    f'RETURN m.name, n.name, r.case_count'
            matches = g.run(query)

            print(pair[0], '\b,', pair[1], '\b:', len(matches), 'matches found:')

            for match in matches:
                print(f'\t${match[0]}\t${match[1]}\t${match[2]}')
