import os
import base64
from typing import *

from veryfi.model import AddLineItem, UpdateLineItem
from veryfi.client_base import Client


class Documents:
    def __init__(self, client: Client):
        self.client = client

    CATEGORIES = [
        "Advertising & Marketing",
        "Automotive",
        "Bank Charges & Fees",
        "Legal & Professional Services",
        "Insurance",
        "Meals & Entertainment",
        "Office Supplies & Software",
        "Taxes & Licenses",
        "Travel",
        "Rent & Lease",
        "Repairs & Maintenance",
        "Payroll",
        "Utilities",
        "Job Supplies",
        "Grocery",
    ]

    def get_documents(
        self,
        q: Optional[str] = None,
        external_id: Optional[str] = None,
        tag: Optional[str] = None,
        created_gt: Optional[str] = None,
        created_gte: Optional[str] = None,
        created_lt: Optional[str] = None,
        created_lte: Optional[str] = None,
        **kwargs: Dict,
    ):
        """
        Get list of documents
        :param query: Search term to search for a specific document by its content. These fields will be searched: external_id, category, vendor.name, notes, invoice_number, total and ocr_text.
        :param external_id:	Search for documents that match your custom identifier
        :param tag:	Search for documents with the specified tag
        :param created__gt:	Search for documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__gt and created__gte in a single request.
        :param created__gte: Search for documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__gt and created__gte in a single request.
        :param created__lt:	Search for documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__lt and created__lte in a single request.
        :param created__lte: Search for documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__lt and created__lte in a single request.
        :param kwargs: Additional request parameters
        :return: List of previously processed documents
        """
        endpoint_name = "/documents/"

        request_params = {}
        if q:
            request_params["q"] = q
        if external_id:
            request_params["external_id"] = external_id
        if tag:
            request_params["tag"] = tag
        if created_gt:
            request_params["created__gt"] = created_gt
        if created_gte:
            request_params["created__gte"] = created_gte
        if created_lt:
            request_params["created__lt"] = created_lt
        if created_lte:
            request_params["created__lte"] = created_lte
        request_params.update(kwargs)
        if request_params:
            endpoint_name += "?" + "&".join(f"{k}={v}" for k, v in request_params.items())

        documents = self.client.request("GET", endpoint_name, {})

        if "documents" in documents:
            return documents["documents"]
        return documents

    def get_document(self, document_id):
        """
        Retrieve document by ID
        :param document_id: ID of the document you'd like to retrieve
        :return: Data extracted from the Document
        """
        endpoint_name = "/documents/{}/".format(document_id)
        request_arguments = {"id": document_id}
        document = self.client.request("GET", endpoint_name, request_arguments)
        return document

    def process_document(
        self,
        file_path: str,
        categories: Optional[List] = None,
        delete_after_processing: bool = False,
        **kwargs: Dict,
    ):
        """
        Process a document and extract all the fields from it
        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param kwargs: Additional request parameters

        :return: Data extracted from the document
        """
        endpoint_name = "/documents/"
        if not categories:
            categories = self.CATEGORIES
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
            "categories": categories,
            "auto_delete": delete_after_processing,
        }
        request_arguments.update(kwargs)
        document = self.client.request("POST", endpoint_name, request_arguments)
        return document

    def process_document_url(
        self,
        file_url: Optional[str] = None,
        categories: Optional[List[str]] = None,
        delete_after_processing=False,
        boost_mode: int = 0,
        external_id: Optional[str] = None,
        max_pages_to_process: Optional[int] = None,
        file_urls: Optional[List[str]] = None,
        **kwargs: Dict,
    ) -> Dict:
        """Process Document from url and extract all the fields from it.

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param categories: List of categories to use when categorizing the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param max_pages_to_process: When sending a long document to Veryfi for processing, this parameter controls how many pages of the document will be read and processed, starting from page 1.
        :param boost_mode: Flag that tells Veryfi whether boost mode should be enabled. When set to 1, Veryfi will skip data enrichment steps, but will process the document faster. Default value for this flag is 0
        :param external_id: Optional custom document identifier. Use this if you would like to assign your own ID to documents
        :param kwargs: Additional request parameters

        :return: Data extracted from the document.
        """
        endpoint_name = "/documents/"
        request_arguments = {
            "auto_delete": delete_after_processing,
            "boost_mode": boost_mode,
            "categories": categories,
            "external_id": external_id,
            "file_url": file_url,
            "file_urls": file_urls,
            "max_pages_to_process": max_pages_to_process,
        }
        request_arguments.update(kwargs)
        return self.client.request("POST", endpoint_name, request_arguments)

    def delete_document(self, document_id):
        """
        Delete Document from Veryfi
        :param document_id: ID of the document you'd like to delete
        """
        endpoint_name = f"/documents/{document_id}/"
        request_arguments = {"id": document_id}
        self.client.request("DELETE", endpoint_name, request_arguments)

    def update_document(self, document_id: int, **kwargs) -> Dict:
        """
        Update data for a previously processed document, including almost any field like `vendor`, `date`, `notes` and etc.

        ```veryfi_client.update_document(id, date="2021-01-01", notes="look what I did")```

        :param document_id: ID of the document you'd like to update
        :param kwargs: fields to update

        :return: A document json with updated fields, if fields are writable. Otherwise a document with unchanged fields.
        """
        endpoint_name = f"/documents/{document_id}/"

        return self.client.request("PUT", endpoint_name, kwargs)

    def get_line_items(self, document_id):
        """
        Retrieve all line items for a document.
        :param document_id: ID of the document you'd like to retrieve
        :return: List of line items extracted from the document
        """
        endpoint_name = f"/documents/{document_id}/line-items/"
        request_arguments = {}
        line_items = self.client.request("GET", endpoint_name, request_arguments)
        return line_items

    def get_line_item(self, document_id, line_item_id):
        """
        Retrieve a line item for existing document by ID.
        :param document_id: ID of the document you'd like to retrieve
        :param line_item_id: ID of the line item you'd like to retrieve
        :return: Line item extracted from the document
        """
        endpoint_name = f"/documents/{document_id}/line-items/{line_item_id}"
        request_arguments = {}
        line_items = self.client.request("GET", endpoint_name, request_arguments)
        return line_items

    def add_line_item(self, document_id: int, payload: Dict) -> Dict:
        """
        Add a new line item on an existing document.
        :param document_id: ID of the document you'd like to update
        :param payload: line item object to add
        :return: Added line item data
        """
        endpoint_name = f"/documents/{document_id}/line-items/"
        request_arguments = AddLineItem(**payload).dict(exclude_none=True)
        return self.client.request("POST", endpoint_name, request_arguments)

    def update_line_item(self, document_id: int, line_item_id: int, payload: Dict) -> Dict:
        """
        Update an existing line item on an existing document.
        :param document_id: ID of the document you'd like to update
        :param line_item_id: ID of the line item you'd like to update
        :param payload: line item object to update

        :return: Line item data with updated fields, if fields are writable. Otherwise line item data with unchanged fields.
        """
        endpoint_name = f"/documents/{document_id}/line-items/{line_item_id}"
        request_arguments = UpdateLineItem(**payload).dict(exclude_none=True)
        return self.client.request("PUT", endpoint_name, request_arguments)

    def delete_line_items(self, document_id):
        """
        Delete all line items on an existing document.
        :param document_id: ID of the document you'd like to delete
        """
        endpoint_name = f"/documents/{document_id}/line-items/"
        request_arguments = {}
        self.client.request("DELETE", endpoint_name, request_arguments)

    def delete_line_item(self, document_id, line_item_id):
        """
        Delete an existing line item on an existing document.
        :param document_id: ID of the document you'd like to delete
        :param line_item_id: ID of the line item you'd like to delete
        """
        endpoint_name = f"/documents/{document_id}/line-items/{line_item_id}"
        request_arguments = {}
        self.client.request("DELETE", endpoint_name, request_arguments)

    def add_tag(self, document_id, tag_name):
        """
        Add a new tag on an existing document.
        :param document_id: ID of the document you'd like to update
        :param tag_name: name of the new tag
        :return: Added tag data
        """
        endpoint_name = f"/documents/{document_id}/tags/"
        request_arguments = {"name": tag_name}
        return self.client.request("PUT", endpoint_name, request_arguments)

    def replace_tags(self, document_id, tags):
        """
        Replace multiple tags on an existing document.
        :param document_id: ID of the document you'd like to update
        :param tags: array of strings
        :return: Added tags data
        """
        endpoint_name = f"/documents/{document_id}/"
        request_arguments = {"tags": tags}
        return self.client.request("PUT", endpoint_name, request_arguments)

    def add_tags(self, document_id, tags):
        """
        Add multiple tags on an existing document.
        :param document_id: ID of the document you'd like to update
        :param tags: array of strings
        :return: Added tags data
        """
        endpoint_name = f"/documents/{document_id}/tags/"
        request_arguments = {"tags": tags}
        return self.client.request("POST", endpoint_name, request_arguments)
