#!/bin/python

import difflib, typing, logging, sys
from requests   import post, get, session as sessions
from .crypto    import Encryption

Client = 'RubikaClient'

class Rubino(object):

    def __init__(self, base_logger: str = __name__, session: str = None) -> (None):
        
        '''
        from rb import RubinoClient

        with RubinoClient(...) as client:
            client.create_page(...)
        '''
        
        if isinstance(base_logger, str):
            base_logger: str = logging.getLogger(base_logger)
        
        elif not isinstance(base_logger, logging.Logger):
            
            try:
                from . import __name__ as base_log
                base_logger: str = base_log
            except Exception: ...

        self.session, self.auth, self.url, self.logger = sessions(), session, 'https://rubino12.iranlms.ir', self.base_logger

    def __call__(self):
        pass
    
    def __dir__(self):
        pass
    
    def __enter__(self) -> (object):
        return self

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> (None):
        pass

    def __post(self, json: dict) -> (dict):
        
        for i in range(5):
            
            try:
                with self.session.post(
                    url=self.url,
                    json=json
                    ) as (res):
                    
                    if (res.status_code != 200):
                        continue

                    else:
                        return res.json()
                        break

            except Exception as e:
                print(e)

    def makeJson(
        self,
        method  :   str,
        data    :   dict
        ) -> (dict):

        return (
            {
                'api_version'   :   '0',
                'auth'          :   self.auth,
                'client'        :   clients.android,
                'data'          :   data,
                'method'        :   method
                }
        )

    def get_profile_list(
        self,
        limit   :   typing.Union[int, str]      =   10,
        sort    :   str                         =   'FromMax',
        equal   :   bool                        =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getProfileList',
            {
                'equal': equal,
                'limit': limit,
                'sort' : sort,
                }
        )
        return self.__post(json=json)

    def request_follow(
        self,
        followee_id :   str,
        profile_id  :   str,
        f_type      :   str  =  'Follow'
        ) -> (dict):
        
        '''
        `f_type` is a action for follow type; and actions: `Follow` and `Unfollow`
        '''
        
        json = self.makeJson(
            'requestFollow',
            {
                'f_type'        :   'Follow',
                'followee_id'   :   followee_id,
                'profile_id'    :   profile_id
                }
            )

        return self.__post(json=json)

    def create_page(
        self, **kwargs
        ) -> (dict):
        
        '''
        `self.create_page(bio='', name='', username='', email='')`
        '''
        
        json = self.makeJson(
            'createPage',
            {**kwargs}
            )
        return self.__post(json=json)

    def update_profile(
        self,
        **kwargs
        ) -> (dict):
        
        '''
        `self.update_profile(bio='', name='', username='', email='')`
        '''
        json = self.makeJson(
            'updateProfile',
            {**kwargs}
            )
        
        return self.__post(json=json)

    def is_exist_username(
        self,
        username: str
        ) -> (dict):
        
        json = self.makeJson(
            'isExistUsername',
            {
                'username': username.replace('@','')
                }
            )
        return self.__post(json=json)

    def get_post_by_shareLink(
        self,
        share_string:   str,
        profile_id  :   str
        ) -> (dict):
        
        json = self.makeJson(
            'getPostByShareLink',
            {
                'share_string'  :   share_string,
                'profile_id'    :   profile_id
                }
            )
        return self.__post(json=json)

    def add_comment(
        self,
        text            :   str,
        post_id         :   str,
        post_profile_id :   str,
        profile_id      :   str
        ) -> (dict):
        
        json = self.makeJson(
            'addComment',
            {
                'content'           :   text,
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id,
                'rnd'               :   randint(1111111111, 9999999999),
                'profile_id'        :   profile_id
                }
            )

        return self.__post(json=json)

    def like_post_action(
        self,
        post_id         :   str,
        post_profile_id :   str,
        profile_id      :   str,
        action_type     :   str =   'Like' or 'Unlike'
        ) -> (dict):
        
        
        '''
        `action_type` is a action for post; and, actions: `Like` or `Unlike`
        '''

        json = self.makeJson(
            'likePostAction',
            {
                'action_type'       :   action_type,
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id,
                'profile_id'        :   profile_id
                }
            )

        return self.__post(json=json)

    def add_post_view_count(
        self,
        post_id         :   str,
        post_profile_id :   str
        ) -> (dict):
        
        json = self.makeJson(
            'addPostViewCount',
            {
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id
                }
            )
        return self.__post(json=json)

    def get_comments(self,
        post_id         :   str,
        profile_id      :   str,
        post_profile_id :   str,
        limit           :   int     =   50,
        sort            :   str     =   'FromMax',
        equal           :   bool    =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getComments',
            {
                'equal'             :   equal,
                'limit'             :   limit,
                'sort'              :   sort,
                'post_id'           :   post_id,
                'profile_id'        :   profile_id,
                'post_profile_id'   :   post_profile_id
                }
            )
        return self.__post(json=json)

    def get_recent_following_posts(
        self        :   'RubinoClient',
        profile_id  :   'str',
        limit       :   'int'   =   30,
        sort        :   'str'   =   'FromMax',
        equal       :   'bool'  =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
            'equal'         :   equal,
            'limit'         :   limit,
            'sort'          :   sort,
            'profile_id'    :   profile_id
            }
            )
        return self.__post(json=json)

    def get_profile_posts(self,
        target_profile_id   :   str,
        profile_id          :   str,
        limit               :   int     =   50,
        sort                :   str     =   'FromMax',
        equal               :   bool    =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
                'equal'             :   equal,
                'limit'             :   limit,
                'sort'              :   sort,
                'profile_id'        :   profile_id,
                'target_profile_id' :   target_profile_id
                }
            )
        return self.__post(json=json)

    def get_profile_stories(
        self,
        target_profile_id   :   str,
        limit               :   int =   100
        ) -> (dict):
        
        json = self.makeJson(
            'getProfileStories',
            {
                'limit'         :   limit,
                'profile_id'    :   target_profile_id
                }
            )
        return self.__post(json=json)

class RubinoClient(Rubino):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        try:
            sys.modules[self.base_logger] = RubinoClient
        except Exception: ...

    def __getattr__(self, name, *args, **kwargs) -> typing.Union[object, None]:
        
        method = 'MethodNameNotFound'
        
        attr = difflib.get_close_matches(name, dir(Rubino), n=1)

        if attr:
            method = getattr(__base[0], attr[0])
        
        try:
            return method(*args, **kwargs)
        except Exception:
            return method