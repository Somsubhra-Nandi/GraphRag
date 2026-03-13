from configs.settings import settings


class DocumentChunker:

    def chunk(self, doc):

        text = doc["text"]

        chunks = []

        start = 0

        while start < len(text):

            end = start + settings.CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append({
                "chunk_id": f"{doc['doc_id']}_{len(chunks)}",
                "text": chunk_text,
                "source": doc["doc_id"]
            })

            start += settings.CHUNK_SIZE - settings.CHUNK_OVERLAP

        return chunks