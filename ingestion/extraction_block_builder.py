class ExtractionBlockBuilder:

    def __init__(self, block_size=4000):
        self.block_size = block_size

    def build_blocks(self, documents):

        blocks = []

        for doc in documents:
            text = doc["text"]
            source = doc["doc_id"]

            start = 0
            idx = 0

            while start < len(text):
                end = start + self.block_size

                block_text = text[start:end].strip()

                if len(block_text) > 50:
                    blocks.append({
                        "block_id": f"{source}_block_{idx}",
                        "text": block_text,
                        "source": source
                    })
                    idx += 1

                start += self.block_size

        return blocks