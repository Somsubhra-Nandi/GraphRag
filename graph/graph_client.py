from neo4j import GraphDatabase
from configs.settings import settings


class GraphClient:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):

        self.driver.close()

    def run_query(self, query, params=None):

        with self.driver.session() as session:

            result = session.run(query, params or {})

            return result.data()