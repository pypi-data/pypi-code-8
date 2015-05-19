__author__ = 'assadmahmood'

import requests

from asposecloud import AsposeApp
from asposecloud import Product
from asposecloud.common import Utils

# ========================================================================
# DOCUMENT CLASS
# ========================================================================

class Document:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'imaging/' + self.filename

    def update_tiff_properties_local(self, input_file_path, bit_depth, compression, resolution_unit, new_width, new_height,
                               horizontal_resolution, vertical_resolution, output_path,
                               remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param input_file_path:
        :param bit_depth:
        :param compression:
        :param resolution_unit:
        :param new_width:
        :param new_height:
        :param horizontal_resolution:
        :param vertical_resolution:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/tiff'
        qry = {'compression': compression, 'resolutionUnit': resolution_unit, 'newWidth' : new_width,
               'newHeight' : new_height, 'horizontalResolution' : horizontal_resolution,
               'verticalResolution' : vertical_resolution, 'bitDepth' : bit_depth, 'outputPath': output_path}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.tiff'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_tiff_properties(self, bit_depth, compression, resolution_unit, new_width, new_height,
                               horizontal_resolution, vertical_resolution, output_path,
                               remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param bit_depth:
        :param compression:
        :param resolution_unit:
        :param new_width:
        :param new_height:
        :param horizontal_resolution:
        :param vertical_resolution:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'storage/file/' + self.filename
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)
        signed_uri = Utils.sign(str_uri)
        file_content = requests.get(signed_uri, headers={
            'content-type': 'application/json', 'accept': 'application/json'
        }, stream=True)


        str_uri = Product.product_uri + 'imaging/tiff'
        qry = {'compression': compression, 'resolutionUnit': resolution_unit, 'newWidth' : new_width,
               'newHeight' : new_height, 'horizontalResolution' : horizontal_resolution,
               'verticalResolution' : vertical_resolution, 'bitDepth' : bit_depth, 'outputPath': output_path}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.post(signed_uri, file_content, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.tiff'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_psd_properties_local(self, input_file_path, channels_count, compression_method,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param input_file_path:
        :param channels_count:
        :param compression_method:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """


        str_uri = Product.product_uri + 'imaging/psd'
        qry = {'channelsCount': channels_count, 'compressionMethod': compression_method}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.psd'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_psd_properties(self, channels_count, compression_method, output_path,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param channels_count:
        :param compression_method:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """


        str_uri = self.base_uri + '/psd'
        qry = {'channelsCount': channels_count, 'compressionMethod': compression_method,
               'outputPath': output_path}

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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.psd'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_jpg_properties_local(self, input_file_path, quality, compression_type,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param input_file_path:
        :param quality:
        :param compression_type:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """


        str_uri = Product.product_uri + 'imaging/jpg'
        qry = {'quality': quality, 'compressionType': compression_type}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.jpg'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_jpg_properties(self, quality, compression_type, output_path,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param quality:
        :param compression_type:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """


        str_uri = self.base_uri + '/jpg'
        qry = {'quality': quality, 'compressionType': compression_type, 'outputPath': output_path}

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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.jpg'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_gif_properties_local(self, input_file_path, bg_color_index, px_aspect_ratio, interlaced,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param input_file_path:
        :param bg_color_index:
        :param px_aspect_ratio:
        :param interlaced:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/gif'
        qry = {'backgroundColorIndex': bg_color_index, 'pixelAspectRatio': px_aspect_ratio,
               'interlaced': interlaced}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.gif'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_gif_properties(self, bg_color_index, px_aspect_ratio, interlaced, output_path,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param bg_color_index:
        :param px_aspect_ratio:
        :param interlaced:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = self.base_uri + '/gif'
        qry = {'backgroundColorIndex': bg_color_index, 'pixelAspectRatio': px_aspect_ratio,
               'interlaced': interlaced,'outputPath': output_path}

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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.gif'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_bmp_properties_local(self, input_file_path, bits_per_px, h_resolution, v_resolution,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param bits_per_px:
        :param h_resolution:
        :param v_resolution:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/bmp'
        qry = {'bitsPerPixel': bits_per_px, 'horizontalResolution': h_resolution,
               'verticalResolution': v_resolution}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.bmp'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_bmp_properties(self, bits_per_px, h_resolution, v_resolution, output_path,
                              remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param bits_per_px:
        :param h_resolution:
        :param v_resolution:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = self.base_uri + '/bmp'
        qry = {'bitsPerPixel': bits_per_px, 'horizontalResolution': h_resolution,
               'verticalResolution': v_resolution,'outputPath': output_path}

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
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.bmp'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output



    def get_properties(self, remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/properties'
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

        return response

    def get_tiff_frame_properties(self, frame_id, remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/frames/' + str(frame_id) + '/properties'
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

        return response

    def extract_frame(self, frame_id, remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = self.base_uri + '/frames/' + str(frame_id) + '?saveOtherFrames=false'
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)
        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_frame_' + str(frame_id) + '.tiff'
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

        return response

    def append_tiff(self, append_file, remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param remote_folder: storage path to operate
        :param storage_type: type of storage e.g Aspose, S3
        :param storage_name: name of storage e.g. MyAmazonS3
        :return:
        """
        str_uri = Product.product_uri + 'imaging/tiff/' + self.filename + '/appendTiff'

        qry = {'appendFile': append_file}
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

        return response

# ========================================================================
# IMAGE CLASS
# ========================================================================


class Image:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'imaging/' + self.filename

    def rotate_image(self, method, output_path, save_format,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param method:
        :param output_path:
        :param save_format:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/rotateflip'
        qry = {'method': method, 'outputPath': output_path, 'format': save_format}

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
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def crop_image(self, x, y, width, height, output_path, save_format,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param x:
        :param y:
        :param width:
        :param height:
        :param output_path:
        :param save_format:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/crop'
        qry = {'x': x, 'y': y, 'width': width, 'height': height, 'outputPath': output_path, 'format': save_format}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_croped.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_tiff_frame(self, frame_id, params,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param params:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/frames/' + str(frame_id)
        str_uri = Utils.build_uri(str_uri, params)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'tiff'
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated_frame_' + \
                          str(frame_id) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def rotate_tiff_frame(self, frame_id, rotate_method, output_path,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param rotate_method:
        :param new_height:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/frames/' + str(frame_id)
        qry = {'saveOtherFrames': True, 'rotateFlipMethod': rotate_method, 'outputPath': output_path}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'tiff'
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_rotated_frame_' + \
                          str(frame_id) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def resize_tiff_frame(self, frame_id, new_width, new_height, output_path,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param new_width:
        :param new_height:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/frames/' + str(frame_id)
        qry = {'saveOtherFrames': True, 'newWidth': new_width, 'newHeight': new_height, 'outputPath': output_path}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'tiff'
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_resized_frame_' + \
                          str(frame_id) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def crop_tiff_frame(self, frame_id, x, y, new_width, new_height, output_path,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param frame_id:
        :param x:
        :param y:
        :param new_width:
        :param new_height:
        :param output_path:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/frames/' + str(frame_id)
        qry = {'saveOtherFrames': True, 'x':x, 'y':y, 'newWidth': new_width, 'newHeight': new_height,
               'outputPath': output_path}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'tiff'
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_croped_frame_' + \
                          str(frame_id) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def resize_image(self, input_file_path, new_width, new_height, output_filename, save_format,
                           remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param input_file_path:
        :param new_width:
        :param new_height:
        :param output_filename:
        :param save_format:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/resize'
        qry = {'newWidth': new_width, 'newHeight': new_height, 'format': save_format}

        str_uri = Utils.build_uri(str_uri, qry)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.post(signed_uri, data=payload, headers={
                    'content-type': 'application/json', 'accept': 'application/json', 'x-aspose-client' : 'PYTHONSDK/v1.0'
                }, stream=True)
                response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)

        if not validate_output:
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(input_file_path) + '.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output

    def update_image(self, params, save_format, remote_folder='', storage_type='Aspose', storage_name=None):

        """

        :param params:
        :param save_format:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = self.base_uri + '/updateImage'
        params['format'] = save_format
        str_uri = Utils.build_uri(str_uri, params)
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            response = requests.get(signed_uri, headers={
                'content-type': 'application/json', 'accept': 'application/json'
            }, stream=True)
            response.raise_for_status()
        except requests.HTTPError as e:
            print e
            print response.content
            exit(1)

        validate_output = Utils.validate_result(response)
        if not validate_output:
            save_format = 'zip' if save_format == 'html' else save_format
            output_path = AsposeApp.output_path + Utils.get_filename(self.filename) + '_updated.' + save_format
            Utils.save_file(response, output_path)
            return output_path
        else:
            return validate_output


# ========================================================================
# CONVERTER CLASS
# ========================================================================

class Converter:

    def __init__(self, filename):
        self.filename = filename

        if not filename:
            raise ValueError("filename not specified")

        self.base_uri = Product.product_uri + 'imaging/' + self.filename

    def convert_local_file(self, input_file_path, save_format, stream_out=False, output_filename=None,
                           remote_folder='', storage_type='Aspose', storage_name=None):
        """

        :param input_file_path:
        :param save_format:
        :param stream_out:
        :param output_filename:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/' + self.filename + '/saveAs?format=' + save_format
        str_uri = Utils.append_storage(str_uri, remote_folder, storage_type, storage_name)

        signed_uri = Utils.sign(str_uri)

        response = None
        try:
            with open(input_file_path, 'rb') as payload:
                response = requests.get(signed_uri, data=payload, headers={
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
                    output_filename = input_file_path
                save_format = 'zip' if save_format == 'html' else save_format
                output_path = AsposeApp.output_path + Utils.get_filename(output_filename) + '.' + save_format
                Utils.save_file(response, output_path)
                return output_path
            else:
                return response.content
        else:
            return validate_output

    def convert_tiff_to_fax(self, stream_out=False, output_filename=None, remote_folder='', storage_type='Aspose', storage_name=None):

        """
        :param stream_out:
        :param output_filename:
        :param remote_folder:
        :param storage_type:
        :param storage_name:
        :return:
        """

        str_uri = Product.product_uri + 'imaging/tiff/' + self.filename + '/toFax'
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
                output_path = AsposeApp.output_path + output_filename
                Utils.save_file(response, output_path)
                return output_path
            else:
                return response.content
        else:
            return validate_output
