from database.database import init_db
from modules.documents import list_documents


def test_document_listing_is_callable():
    init_db()
    docs = list_documents()
    assert isinstance(docs, list)
