from typing import Dict
import requests, json
from app.data.classhash import CLASS_HASH

API_ROOT_PATH = "https://www.bungie.net/Platform"

class ApiController:


    __HEADERS: Dict[str, str]

    ###########################################################################
    #
    # Base API
    #
    ###########################################################################    
    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key}
        pass


    def __call_api(self, method: str, apiString: str, params = None, timeout = None):
        import time
        for i in range(0, 3):
            call = requests.request(method=method, url=apiString, headers=self.__HEADERS, params=params, timeout=timeout)

            # break if it has no error
            if call.status_code // 100 == 2:
                return (call.json())['Response']
            
            errorJson = json.loads(call.text)
            if 'ErrorCode' in errorJson:
                errorCode = errorJson['ErrorCode']
                if errorCode == 1665: # privacy settings enabled for user
                    return errorJson
            
            # wait and try again
            DELAY = 5
            print(f"Attemp {i + 1} failed. Error: {call.status_code}. Waiting {DELAY} seconds and trying again.")
            time.sleep(DELAY)
        print(f"API calls failed. Exiting...")
        exit(2)


    ###########################################################################
    #
    # Public functions
    #
    ###########################################################################
    def getProfile(self, membershipType, destinyMembershipId):
        params = {}
        params["components"] = [100]

        call = self.__call_api(
            method='GET', 
            apiString=f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}',
            params=params
        )

        return call


    def getAccountStats(self, membershipType, destinyMembershipId):
        params = {}

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats', headers=self.__HEADERS, params=params)

        return (api_call.json())['Response']


    def getActivities(self, membershipType, destinyMembershipId, characterId, page=0, count=250, mode=None):
        params = {}
        if page is not None: params["page"] = page
        if count is not None: params["count"] = count
        if mode is not None: params["mode"] = mode

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', headers=self.__HEADERS, params=params)
        json_ = (api_call.json())
        if ("Response" not in json_):
            print(json_)
        return json_['Response']


    def getPGCR(self, activityId):
        params = {}

        try:
            api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Stats/PostGameCarnageReport/{activityId}/', headers=self.__HEADERS, params=params, timeout=(10, 10))
        except:
            return None
        return (api_call.json())['Response']


    def getItem(self, itemReferenceId):
        pass
    

    def getCharacterClass(self, membershipType, destinyMembershipId, characterId):
        params = {}
        params['components'] = 200

        try:
            api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}', headers=self.__HEADERS, params=params, timeout=(10, 10))
        except:
            return None
        
        classHash = (api_call.json())['Response']['character']['data']['classHash']

        return CLASS_HASH[classHash]
    