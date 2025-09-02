from __future__ import annotations
import json
import re
import time
from dataclasses import dataclass
from typing import List ,Optional ,Dict ,Any
import requests

@dataclass
class LLMConfig :
    base_url :str ='http://localhost:11434'
    model :str ='qwen2.5:7b-instruct'
    temperature :float =0.2
    max_tokens :int =64
    timeout :float =8.0
    decision_interval :int =3

class OllamaLLM :

    def __init__ (self ,cfg :LLMConfig ):
        self .cfg =cfg
        self ._cache :Dict [str ,str ]={}

    def _key (self ,prompt :str )->str :
        return f'{self .cfg .model }::{self .cfg .temperature }::{self .cfg .max_tokens }::{hash (prompt )}'

    def _post_generate (self ,prompt :str )->str :
        url =f'{self .cfg .base_url }/api/generate'
        payload ={'model':self .cfg .model ,'prompt':prompt ,'options':{'temperature':self .cfg .temperature },'stream':True }
        try :
            with requests .post (url ,json =payload ,timeout =self .cfg .timeout ,stream =True )as r :
                r .raise_for_status ()
                chunks =[]
                for line in r .iter_lines ():
                    if not line :
                        continue
                    try :
                        obj =json .loads (line .decode ('utf-8'))
                        if 'response'in obj :
                            chunks .append (obj ['response'])
                        if obj .get ('done'):
                            break
                    except Exception :
                        continue
                return ''.join (chunks ).strip ()
        except Exception :
            return ''

    def complete (self ,prompt :str )->str :
        key =self ._key (prompt )
        if key in self ._cache :
            return self ._cache [key ]
        url =f'{self .cfg .base_url }/api/generate'
        payload ={'model':self .cfg .model ,'prompt':prompt ,'options':{'temperature':self .cfg .temperature ,'num_predict':self .cfg .max_tokens },'stream':False }
        try :
            r =requests .post (url ,json =payload ,timeout =self .cfg .timeout )
            r .raise_for_status ()
            obj =r .json ()
            text =obj .get ('response','')or ''
        except Exception :
            text =''
        text =re .sub ('[^\\S\\r\\n]+',' ',text ).strip ()
        self ._cache [key ]=text
        return text

    def choose (self ,context :str ,options :List [str ])->int :
        options_str ='\n'.join ((f'- {i }: {opt }'for i ,opt in enumerate (options )))
        prompt =f'You are an economic agent. Read the context and pick exactly ONE option index.\n\nContext:\n{context }\n\nOptions (reply ONLY the number):\n{options_str }\n\nAnswer format: just the NUMBER (e.g., 0)\n'
        text =self .complete (prompt )
        m =re .search ('\\b(\\d+)\\b',text )
        if not m :
            return 0
        idx =int (m .group (1 ))
        if 0 <=idx <len (options ):
            return idx
        return 0

    def is_available (self )->bool :
        try :
            url =f'{self .cfg .base_url }/api/tags'
            r =requests .get (url ,timeout =1.5 )
            return bool (r .ok )
        except Exception :
            return False