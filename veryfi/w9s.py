import os
import base64
from typing import *

from veryfi.client_base import Client


class W9s:
    def __init__(self, client: Client):
        self.client = client

    def process_w9_document_url(
        self, file_url: str, file_name: Optional[str] = None, **kwargs: Dict
    ) -> Dict:
        """
        Process W9 Document from url and extract all the fields from it.

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional request parameters

        :return: Data extracted from the document.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/w9s/"
        request_arguments = {
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client.request("POST", endpoint_name, request_arguments)

    def process_w9_document(self, file_path: str, file_name: Optional[str] = None, **kwargs):
        """
        Process W9 Document from url and extract all the fields from it.

        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional request parameters

        :return: Data extracted from the document.
        """
        endpoint_name = "/w9s/"
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        document = self.client.request("POST", endpoint_name, request_arguments)
        return document
