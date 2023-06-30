# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.114.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from xchainpy2_thornode.api_client import ApiClient


class TSSApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def keysign(self, height, **kwargs):  # noqa: E501
        """keysign  # noqa: E501

        Returns keysign information for the provided height - the height being the first block a tx out item appears in the signed-but-unobserved outbound queue.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.keysign(height, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: (required)
        :return: KeysignResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.keysign_with_http_info(height, **kwargs)  # noqa: E501
        else:
            (data) = self.keysign_with_http_info(height, **kwargs)  # noqa: E501
            return data

    def keysign_with_http_info(self, height, **kwargs):  # noqa: E501
        """keysign  # noqa: E501

        Returns keysign information for the provided height - the height being the first block a tx out item appears in the signed-but-unobserved outbound queue.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.keysign_with_http_info(height, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: (required)
        :return: KeysignResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method keysign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'height' is set
        if ('height' not in params or
                params['height'] is None):
            raise ValueError("Missing the required parameter `height` when calling `keysign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'height' in params:
            path_params['height'] = params['height']  # noqa: E501

        query_params = []

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
            '/thorchain/keysign/{height}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='KeysignResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def keysign_pubkey(self, height, pubkey, **kwargs):  # noqa: E501
        """keysign_pubkey  # noqa: E501

        Returns keysign information for the provided height and pubkey - the height being the block at which a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound queue.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.keysign_pubkey(height, pubkey, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: (required)
        :param str pubkey: (required)
        :return: KeysignResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.keysign_pubkey_with_http_info(height, pubkey, **kwargs)  # noqa: E501
        else:
            (data) = self.keysign_pubkey_with_http_info(height, pubkey, **kwargs)  # noqa: E501
            return data

    def keysign_pubkey_with_http_info(self, height, pubkey, **kwargs):  # noqa: E501
        """keysign_pubkey  # noqa: E501

        Returns keysign information for the provided height and pubkey - the height being the block at which a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound queue.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.keysign_pubkey_with_http_info(height, pubkey, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: (required)
        :param str pubkey: (required)
        :return: KeysignResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'pubkey']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method keysign_pubkey" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'height' is set
        if ('height' not in params or
                params['height'] is None):
            raise ValueError("Missing the required parameter `height` when calling `keysign_pubkey`")  # noqa: E501
        # verify the required parameter 'pubkey' is set
        if ('pubkey' not in params or
                params['pubkey'] is None):
            raise ValueError("Missing the required parameter `pubkey` when calling `keysign_pubkey`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'height' in params:
            path_params['height'] = params['height']  # noqa: E501
        if 'pubkey' in params:
            path_params['pubkey'] = params['pubkey']  # noqa: E501

        query_params = []

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
            '/thorchain/keysign/{height}/{pubkey}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='KeysignResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def metrics(self, **kwargs):  # noqa: E501
        """metrics  # noqa: E501

        Returns keygen and keysign metrics for current vaults.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :return: MetricsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.metrics_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.metrics_with_http_info(**kwargs)  # noqa: E501
            return data

    def metrics_with_http_info(self, **kwargs):  # noqa: E501
        """metrics  # noqa: E501

        Returns keygen and keysign metrics for current vaults.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :return: MetricsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method metrics" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

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
            '/thorchain/metrics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MetricsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def metrics_keygen(self, pubkey, **kwargs):  # noqa: E501
        """metrics_keygen  # noqa: E501

        Returns keygen metrics for the provided vault pubkey.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics_keygen(pubkey, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pubkey: (required)
        :param int height: optional block height, defaults to current tip
        :return: list[KeygenMetric]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.metrics_keygen_with_http_info(pubkey, **kwargs)  # noqa: E501
        else:
            (data) = self.metrics_keygen_with_http_info(pubkey, **kwargs)  # noqa: E501
            return data

    def metrics_keygen_with_http_info(self, pubkey, **kwargs):  # noqa: E501
        """metrics_keygen  # noqa: E501

        Returns keygen metrics for the provided vault pubkey.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.metrics_keygen_with_http_info(pubkey, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pubkey: (required)
        :param int height: optional block height, defaults to current tip
        :return: list[KeygenMetric]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['pubkey', 'height']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method metrics_keygen" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'pubkey' is set
        if ('pubkey' not in params or
                params['pubkey'] is None):
            raise ValueError("Missing the required parameter `pubkey` when calling `metrics_keygen`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'pubkey' in params:
            path_params['pubkey'] = params['pubkey']  # noqa: E501

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
            '/thorchain/metric/keygen/{pubkey}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[KeygenMetric]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
