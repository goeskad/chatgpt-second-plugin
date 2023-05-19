from models.api import QueryRequest, QueryResponse
from models.models import QueryResult, DocumentChunkWithScore, DocumentMetadata
from kbs import kbsHelper

d1 = DocumentChunkWithScore(text="abc", score=0.8, metadata=DocumentMetadata())
d2 = DocumentChunkWithScore(text="133", score=0.9, metadata=DocumentMetadata())
q1 = QueryResult(query="q1", results=[d1, d2])
kbsHelper.process_ds_response([q1])
