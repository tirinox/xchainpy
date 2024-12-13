# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from xchainpy2_thornode.api_client import ApiClient


class CloutApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def swapper_clout(self, address, **kwargs):  # noqa: E501
        """swapper_clout  # noqa: E501

        Returns the clout score of an address  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.swapper_clout(address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str address: (required)
        :param int height: optional block height, defaults to current tip
        :return: SwapperCloutResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.swapper_clout_with_http_info(address, **kwargs)  # noqa: E501
        else:
            (data) = self.swapper_clout_with_http_info(address, **kwargs)  # noqa: E501
            return data

    def swapper_clout_with_http_info(self, address, **kwargs):  # noqa: E501
        """swapper_clout  # noqa: E501

        Returns the clout score of an address  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.swapper_clout_with_http_info(address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str address: (required)
        :param int height: optional block height, defaults to current tip
        :return: SwapperCloutResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['address', 'height']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method swapper_clout" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'address' is set
        if ('address' not in params or
                params['address'] is None):
            raise ValueError("Missing the required parameter `address` when calling `swapper_clout`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'address' in params:
            path_params['address'] = params['address']  # noqa: E501

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/thorchain/clout/swap/{address}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SwapperCloutResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
