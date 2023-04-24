# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.images_image_id_body import ImagesImageIdBody  # noqa: E501
from swagger_server.models.images_upload_body import ImagesUploadBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.inline_response201_zip import InlineResponse201Zip  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_images_image_id_get(self):
        """Test case for images_image_id_get

        Retrieves image data for a specific image ID
        """
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/images/{image_id}'.format(image_id='image_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_image_id_post(self):
        """Test case for images_image_id_post

        Uploads a new image
        """
        body = ImagesImageIdBody()
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/images/{image_id}'.format(image_id='image_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_latest_get(self):
        """Test case for images_latest_get

        Retrieves the latest image in image format
        """
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/images/latest',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_upload_post(self):
        """Test case for images_upload_post

        Uploads multiple images
        """
        body = ImagesUploadBody()
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/images/upload',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zip_get(self):
        """Test case for zip_get

        Retrieves a zip file containing up to 5 of the most recent images.
        """
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/zip',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zip_zip_id_post(self):
        """Test case for zip_zip_id_post

        Uploads a new zip file
        """
        data = dict(file='file_example')
        response = self.client.open(
            '/PREETINANDA/image_api/1.0.0/zip/{zip_id}'.format(zip_id='zip_id_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
