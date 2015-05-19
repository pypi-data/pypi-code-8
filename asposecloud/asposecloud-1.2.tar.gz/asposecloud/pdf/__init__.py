__author__ = 'AssadMahmood'
import requests
import json
import os.path

from asposecloud import AsposeApp
from asposecloud import Product
from asposecloud.common import Utils


class Document:
    """
    Wrapper class for Aspose.PDF API Document Resource.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_properties(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperties']['List'] if response['DocumentProperties']['List'] else False

    def delete_properties(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.delete(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return True if response['Status'] == 'OK' else False

    def get_property(self, property_name, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param property_name:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties/' + property_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperty'] if response['Code'] == 200 else False

    def set_property(self, property_name, property_value, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param property_name:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/documentProperties/' + property_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'Value':property_value})

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['DocumentProperty'] if response['Code'] == 200 else False

    def create_empty_pdf(self, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Create a pdf file from any supported format file e.g. html,xml,jpeg,svg,tiff

        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.pdf'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def create_pdf(self, template_file, source_format, data_file=None, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Create a pdf file from any supported format file e.g. html,xml,jpeg,svg,tiff

        :param template_file:
        :param source_format:
        :param data_file: like xml file for xslt format
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not template_file:
            raise ValueError("template_file not specified")

        if not source_format:
            raise ValueError("source_format not specified")

        save_format = 'pdf'

        str_uri = self.base_uri + '?templateFile=' + template_file + '&templateType=' + source_format
        if(data_file):
            str_uri += '&dataFile=' + data_file
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def add_stamp(self, post_data, page_number, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Add Signature to a pdf file

        :param page_number:
        :param post_data:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not post_data:
            raise ValueError("post_data not specified")

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + page_number + '/stamp'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, post_data, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def add_new_page(self, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Add new page to a pdf file

        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        str_uri = self.base_uri + '/pages'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def delete_page(self, page_number, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Add new page to a pdf file

        :param page_number:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.delete(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def move_page(self, page_number, new_location, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Move a page to new location

        :param page_number:
        :param new_location:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        str_uri = self.base_uri + '/pages/' + str(page_number) + '/movePage?newIndex=' + str(new_location)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def add_signature(self, post_data, page_number=None, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Add Signature to a pdf file

        :param page_number:
        :param post_data:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not post_data:
            raise ValueError("post_data not specified")

        str_uri = self.base_uri
        if page_number:
            str_uri += '/pages/' + page_number

        str_uri += '/sign'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, post_data, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def get_form_fields_count(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get Form Feilds Count

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        str_uri = self.base_uri + '/fields'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Fields']['List']) if response['Code'] == 200 else False

    def get_all_form_fields(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get All Form Fields

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        str_uri = self.base_uri + '/fields'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Fields'] if response['Code'] == 200 else False

    def get_form_field(self, field_name, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get a Form Field

        :param field_name:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not field_name:
            raise ValueError("field_name not specified")

        str_uri = self.base_uri + '/fields/' + field_name
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Field'] if response['Code'] == 200 else False

    def update_form_field(self, field_name, field_type, field_value,
                          remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Update Form Field Value

        :param field_name:
        :param field_type:
        :param field_value:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        if not field_name:
            raise ValueError("field_name not specified")

        if not field_type:
            raise ValueError("field_type not specified")

        if not field_value:
            raise ValueError("field_value not specified")

        post_data = {'Name': field_name, 'Type': field_type, 'Values': [field_value]}

        str_uri = self.base_uri + '/fields'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, post_data, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Field'] if response['Code'] == 200 else False

    def get_page_count(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get count of pages in pdf file

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Pages']['List']) if response['Pages']['List'] else 0

    def append_documents(self, append_file, start_page=None, end_page=None,
                         remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Append a pdf file to base pdf

        :param append_file:
        :param start_page:
        :param end_page:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/appendDocument'
        qry = {'appendFile': append_file}
        if start_page:
            qry['startPage'] = start_page
        if end_page:
            qry['endPage'] = end_page
        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if validate_output:
            return validate_output
        else:
            return True

    def split_pdf(self, start_page=None, end_page=None, save_format=None,
                         remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param start_page:
        :param end_page:
        :param save_format:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/split'
        qry = {}
        if start_page:
            qry['from'] = start_page
        if end_page:
            qry['to'] = end_page
        if save_format:
            qry['format'] = save_format
        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if validate_output:
            return validate_output
        else:
            return response

    @staticmethod
    def merge_documents(merged_filename, source_files, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Merge multiple pdf files

        :param merged_filename:
        :param source_files:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        json_data = json.dumps({'List': source_files})

        str_uri = Product.product_uri + 'pdf/' + merged_filename + '/merge'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return True if response['Status'] == 'OK' else False


class TextEditor:
    """
    Wrapper class for Aspose.PDF API for Text Editing features.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_fragment_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count fragments in a pdf file on given page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/fragments'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['TextItems']['List']) if response['TextItems']['List'] else 0

    def get_segment_count(self, page_number, fragment_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count fragments in a pdf file on given page number

        :param page_number:
        :param fragment_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/fragments/' + str(fragment_number) + '/segments'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['TextItems']['List']) if response['TextItems']['List'] else 0

    def get_text(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get text from give page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/textitems'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        output_text = ''
        for item in response['TextItems']['List']:
            output_text += item['Text']
        return output_text

    def get_text_items(self, page_number=None, fragment_number=None, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get text items from given page number

        :param page_number:
        :param fragment_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri
        if(page_number):
            str_uri += '/pages/' + str(page_number)
        if(fragment_number):
            str_uri += '/fragments/' + str(fragment_number)

        str_uri += '/textitems'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['TextItems']['List'] if response['TextItems']['List'] else False

    def get_text_format(self, page_number=None, fragment_number=None, segment_number=None,
                        remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get text format from given page number

        :param page_number:
        :param fragment_number:
        :param segment_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri
        if(page_number):
            str_uri += '/pages/' + str(page_number)
        if(fragment_number):
            str_uri += '/fragments/' + str(fragment_number)
        if(segment_number):
            str_uri += '/segments/' + str(segment_number)

        str_uri += '/textformat'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['TextFormat'] if response['TextFormat'] else False

    def replace_text(self, old_text, new_text, page_number=None, is_reg=False,
                     remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Replace text in pdf file

        :param old_text:
        :param new_text:
        :param page_number:
        :param is_reg:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri
        if(page_number):
            str_uri += '/pages/' + str(page_number)

        str_uri += '/replaceText'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps({'OldValue': old_text, 'NewValue': new_text, 'Regex': is_reg})

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return True
        else:
            return validate_output

    def replace_multiple_text(self, post_data, page_number=None,
                     remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Replace text in pdf file

        :param post_data:
        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri
        if(page_number):
            str_uri += '/pages/' + str(page_number)

        str_uri += '/replaceTextList'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        json_data = json.dumps(post_data)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, json_data, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return True
        else:
            return validate_output

    def replace_image_using_file(self, page_number, image_index, image_file,
                     remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Replace image in pdf file

        :param page_number:
        :param image_index:
        :param image_file:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/image/' + str(image_index)
        str_uri += '?imageFile=' + image_file
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.post(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            return response
        else:
            return validate_output

class Extractor:
    """
    Wrapper class for Aspose.PDF API Extraction features.
    The Aspose.PDF API let's you manipulate PDF files.
    """
    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def get_image(self, page_number, image_index, save_format, width=None, height=None,
                  remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Get image from given page

        :param page_number:
        :param image_index:
        :param save_format:
        :param width:
        :param height:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number) + '/images/' + str(image_index)
        qry = {'format': save_format}
        if width and height:
            qry['width'] = width
            qry['height'] = height
        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_' + str(page_number) \
                + '_' + str(image_index) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def get_image_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count images on a given page

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number) + '/images'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)
        return len(response['Images']['List']) if response['Images']['List'] else 0

    def get_annotations(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count annotations in a pdf file on given page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/annotations'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Annotations']['List'] if response['Annotations']['List'] else 0

    def get_annotations_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count annotations in a pdf file on given page number

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/annotations'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Annotations']['List']) if response['Annotations']['List'] else 0

    def get_annotation(self, page_number, annotation_index, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Count annotations in a pdf file on given page number

        :param page_number:
        :param annotation_index:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/annotation/' + str(annotation_index)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Annotation'] if response['Code'] == 200 else 0

    def get_bookmarks(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/bookmarks'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Bookmarks']['List'] if response['Bookmarks']['List'] else 0

    def get_bookmarks_count(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/bookmarks'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Bookmarks']['List']) if response['Bookmarks']['List'] else 0

    def get_bookmark(self, bookmark_index, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        :param bookmark_index:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/bookmarks/' + str(bookmark_index)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Bookmark'] if response['Code'] == 200 else 0

    def get_links(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/links'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Links']['List'] if response['Links']['List'] else 0

    def get_links_count(self, page_number, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param page_number:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/links'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Links']['List']) if response['Links']['List'] else 0

    def get_link(self, page_number, link_index, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        :param page_number:
        :param link_index:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/pages/' + str(page_number) + '/link/' + str(link_index)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Link'] if response['Code'] == 200 else 0

    def get_attachments(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/attachments'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Attachments']['List'] if response['Attachments']['List'] else 0

    def get_attachments_count(self, remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/attachments'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return len(response['Attachments']['List']) if response['Attachments']['List'] else 0

    def get_attachment(self, attachment_index, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        :param attachment_index:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/attachment/' + str(attachment_index)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        return response['Attachment'] if response['Code'] == 200 else 0

    def download_attachment(self, attachment_index, output_filename, remote_folder='', storage_type='Aspose', storage_name=None):
        """
        :param attachment_index:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """

        str_uri = self.base_uri + '/attachments/' + str(attachment_index) + '/download'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            })
            response.raise_for_status()
            response = response.json()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + output_filename
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output


class Converter:
    """
    Wrapper class for Aspose.PDF API.
    The Aspose.PDF API let's you manipulate PDF files.
    """

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'pdf/' + self.filename

    def convert_to_image(self, page_number, save_format, width=None, height=None, stream_out=False, output_filename=None,
                         remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Convert a page to image

        :param page_number:
        :param save_format:
        :param width:
        :param height:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        if not page_number:
            raise ValueError("page_number not specified")

        str_uri = self.base_uri + '/pages/' + str(page_number)
        qry = {'format': save_format}
        if(width):
            qry['width'] = width
        if(height):
            qry['height'] = height
        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            if not stream_out:
                if output_filename is None:
                    output_filename = self.filename
                output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '_' + str(page_number) + '.' + \
                    save_format
                Utils.save_file(response, output_path)
                return output_path
            else:
                return response.content
        else:
            return validate_output

    @staticmethod
    def convert_by_url(url, save_format, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Convert a pdf file to any supported format

        :param save_format:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not url:
            raise ValueError("url not specified")

        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = Product.product_uri + 'pdf/convert?url=' + url + '&format=' + save_format
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.put(signed_uri, None, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = os.path.basename(url)
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    def convert(self, save_format, stream_out=False, output_filename=None,
                remote_folder='', storage_type='Aspose', storage_name=None):
        """
        Convert a pdf file to any supported format

        :param save_format:
        :param stream_out:
        :param output_filename:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = self.base_uri + '?format=' + save_format
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = self.filename
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content

    @staticmethod
    def convert_local_file(input_file, save_format, stream_out=False, output_filename=None):
        """
        Convert a local pdf file to any supported format

        :param input_file:
        :param save_format:
        :param stream_out:
        :param output_filename:
        :return:
        """
        if not input_file:
            raise ValueError("input_file not specified")

        if not save_format:
            raise ValueError("save_format not specified")

        str_uri = Product.product_uri + 'pdf/convert?format=' + save_format

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = Utils.upload_file_binary(input_file, signed_uri)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        if not stream_out:
            if output_filename is None:
                output_filename = input_file
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return response.content
