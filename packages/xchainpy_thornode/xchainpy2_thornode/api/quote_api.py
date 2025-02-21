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


class QuoteApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def quoteloanclose(self, **kwargs):  # noqa: E501
        """quoteloanclose  # noqa: E501

        Provide a quote estimate for the provided loan close.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteloanclose(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the asset used to repay the loan
        :param int repay_bps: the basis points of the existing position to repay
        :param str to_asset: the collateral asset of the loan
        :param str loan_owner: the owner of the loan collateral
        :param str min_out: the minimum amount of the target asset to accept
        :return: QuoteLoanCloseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.quoteloanclose_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.quoteloanclose_with_http_info(**kwargs)  # noqa: E501
            return data

    def quoteloanclose_with_http_info(self, **kwargs):  # noqa: E501
        """quoteloanclose  # noqa: E501

        Provide a quote estimate for the provided loan close.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteloanclose_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the asset used to repay the loan
        :param int repay_bps: the basis points of the existing position to repay
        :param str to_asset: the collateral asset of the loan
        :param str loan_owner: the owner of the loan collateral
        :param str min_out: the minimum amount of the target asset to accept
        :return: QuoteLoanCloseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'from_asset', 'repay_bps', 'to_asset', 'loan_owner', 'min_out']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quoteloanclose" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501
        if 'from_asset' in params:
            query_params.append(('from_asset', params['from_asset']))  # noqa: E501
        if 'repay_bps' in params:
            query_params.append(('repay_bps', params['repay_bps']))  # noqa: E501
        if 'to_asset' in params:
            query_params.append(('to_asset', params['to_asset']))  # noqa: E501
        if 'loan_owner' in params:
            query_params.append(('loan_owner', params['loan_owner']))  # noqa: E501
        if 'min_out' in params:
            query_params.append(('min_out', params['min_out']))  # noqa: E501

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
            '/thorchain/quote/loan/close', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuoteLoanCloseResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def quoteloanopen(self, **kwargs):  # noqa: E501
        """quoteloanopen  # noqa: E501

        Provide a quote estimate for the provided loan open.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteloanopen(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the collateral asset
        :param int amount: the collateral asset amount in 1e8 decimals
        :param str to_asset: the target asset to receive (loan denominated in TOR regardless)
        :param str destination: the destination address, required to generate memo
        :param str min_out: the minimum amount of the target asset to accept
        :param int affiliate_bps: the affiliate fee in basis points
        :param str affiliate: the affiliate (address or thorname)
        :return: QuoteLoanOpenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.quoteloanopen_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.quoteloanopen_with_http_info(**kwargs)  # noqa: E501
            return data

    def quoteloanopen_with_http_info(self, **kwargs):  # noqa: E501
        """quoteloanopen  # noqa: E501

        Provide a quote estimate for the provided loan open.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteloanopen_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the collateral asset
        :param int amount: the collateral asset amount in 1e8 decimals
        :param str to_asset: the target asset to receive (loan denominated in TOR regardless)
        :param str destination: the destination address, required to generate memo
        :param str min_out: the minimum amount of the target asset to accept
        :param int affiliate_bps: the affiliate fee in basis points
        :param str affiliate: the affiliate (address or thorname)
        :return: QuoteLoanOpenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'from_asset', 'amount', 'to_asset', 'destination', 'min_out', 'affiliate_bps', 'affiliate']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quoteloanopen" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501
        if 'from_asset' in params:
            query_params.append(('from_asset', params['from_asset']))  # noqa: E501
        if 'amount' in params:
            query_params.append(('amount', params['amount']))  # noqa: E501
        if 'to_asset' in params:
            query_params.append(('to_asset', params['to_asset']))  # noqa: E501
        if 'destination' in params:
            query_params.append(('destination', params['destination']))  # noqa: E501
        if 'min_out' in params:
            query_params.append(('min_out', params['min_out']))  # noqa: E501
        if 'affiliate_bps' in params:
            query_params.append(('affiliate_bps', params['affiliate_bps']))  # noqa: E501
        if 'affiliate' in params:
            query_params.append(('affiliate', params['affiliate']))  # noqa: E501

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
            '/thorchain/quote/loan/open', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuoteLoanOpenResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def quotesaverdeposit(self, **kwargs):  # noqa: E501
        """quotesaverdeposit  # noqa: E501

        Provide a quote estimate for the provided saver deposit.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quotesaverdeposit(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str asset: the asset to deposit
        :param int amount: the source asset amount in 1e8 decimals
        :return: QuoteSaverDepositResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.quotesaverdeposit_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.quotesaverdeposit_with_http_info(**kwargs)  # noqa: E501
            return data

    def quotesaverdeposit_with_http_info(self, **kwargs):  # noqa: E501
        """quotesaverdeposit  # noqa: E501

        Provide a quote estimate for the provided saver deposit.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quotesaverdeposit_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str asset: the asset to deposit
        :param int amount: the source asset amount in 1e8 decimals
        :return: QuoteSaverDepositResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'asset', 'amount']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quotesaverdeposit" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501
        if 'asset' in params:
            query_params.append(('asset', params['asset']))  # noqa: E501
        if 'amount' in params:
            query_params.append(('amount', params['amount']))  # noqa: E501

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
            '/thorchain/quote/saver/deposit', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuoteSaverDepositResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def quotesaverwithdraw(self, **kwargs):  # noqa: E501
        """quotesaverwithdraw  # noqa: E501

        Provide a quote estimate for the provided saver withdraw.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quotesaverwithdraw(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str asset: the asset to withdraw
        :param str address: the address for the position
        :param int withdraw_bps: the basis points of the existing position to withdraw
        :return: QuoteSaverWithdrawResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.quotesaverwithdraw_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.quotesaverwithdraw_with_http_info(**kwargs)  # noqa: E501
            return data

    def quotesaverwithdraw_with_http_info(self, **kwargs):  # noqa: E501
        """quotesaverwithdraw  # noqa: E501

        Provide a quote estimate for the provided saver withdraw.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quotesaverwithdraw_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str asset: the asset to withdraw
        :param str address: the address for the position
        :param int withdraw_bps: the basis points of the existing position to withdraw
        :return: QuoteSaverWithdrawResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'asset', 'address', 'withdraw_bps']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quotesaverwithdraw" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501
        if 'asset' in params:
            query_params.append(('asset', params['asset']))  # noqa: E501
        if 'address' in params:
            query_params.append(('address', params['address']))  # noqa: E501
        if 'withdraw_bps' in params:
            query_params.append(('withdraw_bps', params['withdraw_bps']))  # noqa: E501

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
            '/thorchain/quote/saver/withdraw', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuoteSaverWithdrawResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def quoteswap(self, **kwargs):  # noqa: E501
        """quoteswap  # noqa: E501

        Provide a quote estimate for the provided swap.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteswap(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the source asset
        :param str to_asset: the target asset
        :param int amount: the source asset amount in 1e8 decimals
        :param str destination: the destination address, required to generate memo
        :param str refund_address: the refund address, refunds will be sent here if the swap fails
        :param int streaming_interval: the interval in which streaming swaps are swapped
        :param int streaming_quantity: the quantity of swaps within a streaming swap
        :param int tolerance_bps: the maximum basis points from the current feeless swap price to set the limit in the generated memo
        :param int affiliate_bps: the affiliate fee in basis points
        :param str affiliate: the affiliate (address or thorname)
        :return: QuoteSwapResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.quoteswap_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.quoteswap_with_http_info(**kwargs)  # noqa: E501
            return data

    def quoteswap_with_http_info(self, **kwargs):  # noqa: E501
        """quoteswap  # noqa: E501

        Provide a quote estimate for the provided swap.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quoteswap_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int height: optional block height, defaults to current tip
        :param str from_asset: the source asset
        :param str to_asset: the target asset
        :param int amount: the source asset amount in 1e8 decimals
        :param str destination: the destination address, required to generate memo
        :param str refund_address: the refund address, refunds will be sent here if the swap fails
        :param int streaming_interval: the interval in which streaming swaps are swapped
        :param int streaming_quantity: the quantity of swaps within a streaming swap
        :param int tolerance_bps: the maximum basis points from the current feeless swap price to set the limit in the generated memo
        :param int affiliate_bps: the affiliate fee in basis points
        :param str affiliate: the affiliate (address or thorname)
        :return: QuoteSwapResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['height', 'from_asset', 'to_asset', 'amount', 'destination', 'refund_address', 'streaming_interval', 'streaming_quantity', 'tolerance_bps', 'affiliate_bps', 'affiliate']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quoteswap" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'height' in params:
            query_params.append(('height', params['height']))  # noqa: E501
        if 'from_asset' in params:
            query_params.append(('from_asset', params['from_asset']))  # noqa: E501
        if 'to_asset' in params:
            query_params.append(('to_asset', params['to_asset']))  # noqa: E501
        if 'amount' in params:
            query_params.append(('amount', params['amount']))  # noqa: E501
        if 'destination' in params:
            query_params.append(('destination', params['destination']))  # noqa: E501
        if 'refund_address' in params:
            query_params.append(('refund_address', params['refund_address']))  # noqa: E501
        if 'streaming_interval' in params:
            query_params.append(('streaming_interval', params['streaming_interval']))  # noqa: E501
        if 'streaming_quantity' in params:
            query_params.append(('streaming_quantity', params['streaming_quantity']))  # noqa: E501
        if 'tolerance_bps' in params:
            query_params.append(('tolerance_bps', params['tolerance_bps']))  # noqa: E501
        if 'affiliate_bps' in params:
            query_params.append(('affiliate_bps', params['affiliate_bps']))  # noqa: E501
        if 'affiliate' in params:
            query_params.append(('affiliate', params['affiliate']))  # noqa: E501

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
            '/thorchain/quote/swap', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuoteSwapResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
