from configs.settings import settings

class DocumentChunker:
    def chunk(self, doc):
        text = doc["text"]
        doc_source = doc.get("source", doc.get("doc_id", "unknown_doc"))
        
        chunks = []
        start = 0

        while start < len(text):
            end = start + settings.CHUNK_SIZE
            chunk_text = text[start:end].strip() 
            
            if len(chunk_text) > 10 and (not chunks or chunk_text != chunks[-1]["text"]):
                chunks.append({
                    "chunk_id": f"{doc_source}_chunk{len(chunks)}",
                    "text": chunk_text,
                    "source": doc_source
                })

            start += settings.CHUNK_SIZE - settings.CHUNK_OVERLAP

        return chunks