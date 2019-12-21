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
        g = Graph(host=self.hostname, port=self.port, user=self.user, password=self.password)
        found = 0

        for i, pair in enumerate(self.pairs):
            query = f'MATCH (n)-[r]-(m) ' + \
                    f'WHERE toLower(n.name) CONTAINS toLower("{pair[0]}") ' + \
                    f'AND toLower(m.name) CONTAINS toLower("{pair[1]}") ' + \
                    f'RETURN m.name, n.name, r.case_count'
            matches = g.run(query).to_table()

            print('( {0:4} / {1:4} ): '.format(i + 1, len(self.pairs)), end='')
            print(pair[0], '\b,', pair[1], '\b:', len(matches), 'matches found', end='')

            if len(matches) > 0:
                found += 1
                print(': ', end='')
            else:
                print('. ', end='')

            print('{0} found so far.'.format(found), flush=True)

            for match in matches:
                print(f'\t{match[0]}\t{match[1]}\t{match[2]}')
