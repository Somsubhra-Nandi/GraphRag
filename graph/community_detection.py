class CommunityDetector:

    def __init__(self, graph_client):
        self.client = graph_client

    def detect(self):

        projection_query = """
        CALL gds.graph.project(
            'entityGraph',
            'Entity',
            '*'
        )
        """

        self.client.run_query(projection_query)

        louvain_query = """
        CALL gds.louvain.write(
            'entityGraph',
            {
                writeProperty: 'community_id'
            }
        )
        """

        self.client.run_query(louvain_query)

        drop_query = """
        CALL gds.graph.drop('entityGraph')
        """

        self.client.run_query(drop_query)