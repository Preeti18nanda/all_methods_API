# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse201(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, status: str=None, message: str=None, image_id: str=None):  # noqa: E501
        """InlineResponse201 - a model defined in Swagger

        :param status: The status of this InlineResponse201.  # noqa: E501
        :type status: str
        :param message: The message of this InlineResponse201.  # noqa: E501
        :type message: str
        :param image_id: The image_id of this InlineResponse201.  # noqa: E501
        :type image_id: str
        """
        self.swagger_types = {
            'status': str,
            'message': str,
            'image_id': str
        }

        self.attribute_map = {
            'status': 'status',
            'message': 'message',
            'image_id': 'image_id'
        }
        self._status = status
        self._message = message
        self._image_id = image_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse201':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_201 of this InlineResponse201.  # noqa: E501
        :rtype: InlineResponse201
        """
        return util.deserialize_model(dikt, cls)

    @property
    def status(self) -> str:
        """Gets the status of this InlineResponse201.


        :return: The status of this InlineResponse201.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this InlineResponse201.


        :param status: The status of this InlineResponse201.
        :type status: str
        """

        self._status = status

    @property
    def message(self) -> str:
        """Gets the message of this InlineResponse201.


        :return: The message of this InlineResponse201.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this InlineResponse201.


        :param message: The message of this InlineResponse201.
        :type message: str
        """

        self._message = message

    @property
    def image_id(self) -> str:
        """Gets the image_id of this InlineResponse201.


        :return: The image_id of this InlineResponse201.
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id: str):
        """Sets the image_id of this InlineResponse201.


        :param image_id: The image_id of this InlineResponse201.
        :type image_id: str
        """

        self._image_id = image_id
