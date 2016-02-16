# -*- coding: utf-8 -*-s

import datetime
import hashlib
import random
import string
import traceback

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Min, Sum, Max
from django.http.response import HttpResponse, HttpResponseServerError
from oscar.core.loading import get_model


Product = get_model('catalogue', 'product')
StockProductConfig = get_model('commission', 'StockProductConfig')
        

            
            
        