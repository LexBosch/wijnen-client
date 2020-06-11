""" wijnen client-application.
    Package allows the user to connect to a wijnen web-api and retrieve data stored within

    Author: Lex
    Date: 11-06-2020
"""
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor
from requests import post
from json import dumps
from hashlib import sha224


class wijnen:
    def __init__(self, host: str, server_port: str, api_key: str = None):
        """ Creates connection object, containing host, port and api-key. Allows the user to connect to chosen
        web-server and retireve certain features

        :param host: Hostname/Ip-adress of the wijnen web-api
        :param server_port: server port of the wijnen web-api
        :param api_key: api key assigned to the wijnen web-api
        """
        self.__server_adress = host
        self.__server_port = server_port
        self.__api_key_hash = self.__get_api_hash(api_key)

    def get_attributes(self) -> dict:
        """ Gives database attributes to the user.

        :return: Dictionary containing {Database attribute name: attribute description}
        """
        data_dictionary = {"api_key": self.__api_key_hash}
        data_json = dumps(data_dictionary)
        response = post("http://{0}:{1}/attribute_summary".format(self.__server_adress, self.__server_port),
                        data=data_json)
        return response.json()

    def get_variations(self, variations: list, parameters: list = []) -> dict:
        """ Calls multi-request builder to send asynchronous api calls to the wijnen web-api

        :param variations: Variations as given by the user. will be compared at the web-api
        :param parameters: Optional attributes to return to the user
        :return: Dictionary containg list with variations suspected of potentially being cancerous and a list of not
         found variations
        """
        return_value = self.__mutli_call(variations, parameters)
        return return_value

    @staticmethod
    def __get_api_hash(api_key):
        """ Hashes given string

        :param api_key: String to hash
        :return: hashed string or None
        """
        if api_key is not None:
            return sha224(str.encode(api_key)).hexdigest()
        else:
            return None

    @staticmethod
    def __chunks(cutting_list: list, chunk_size: int) -> list:
        """ Creates chunks of data of given size from list

        :param cutting_list: List to be split
        :param chunk_size: Size to create the parts from
        :return: Yields chunks of the given size
        """
        for i in range(0, len(cutting_list), chunk_size):
            yield cutting_list[i:i + chunk_size]

    def __single_multi_call(self, variations: list, parameters: list):
        """ Creates a single call to the wijnen web-api

        :param variations: List of variations to be processed in the web-api
        :param parameters: Additional attributes to be returned
        :return: Json return from the api-call
        """
        data_dictionary = {"api_key": self.__api_key_hash,
                           "variations": variations,
                           "additional_parameters": parameters}
        data_json = dumps(data_dictionary)
        response = post("http://{0}:{1}/process_variations".format(self.__server_adress, self.__server_port),
                        data=data_json)
        processed_response = response.json()
        return processed_response

    def __mutli_call(self, variations: list, parameters: list) -> dict:
        """ Calls multiple instances of __single_multi_call and combines their futures

        :param variations: List of variations to be processed in the web-api
        :param parameters: Additional attributes to be returned
        :return: Dictionary containing all the api's returns
        """
        variation_chunk = self.__chunks(variations, 100)
        futures = []
        for single_element in variation_chunk:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future = executor.submit(self.__single_multi_call, single_element, parameters)
                futures.append(future)
        wait(futures)
        result_dictionary = self.__merge_futures(futures)
        return result_dictionary

    @staticmethod
    def __merge_futures(futures: list) -> dict:
        """ Combines all future objects into a dictionary

        :param futures: List of the api's future objects
        :return: Dictionary containing all the api's returns
        """
        results = {}
        for fut in futures:
            for return_key in fut.result().keys():
                if return_key in results:
                    results[return_key] += (fut.result()[return_key])
                else:
                    results[return_key] = fut.result()[return_key]
        return results
