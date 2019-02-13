#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def is_number_or_key(word):
    number_or_key = 'key'
    if word.isdigit():
        number_or_key = 'number'
    return number_or_key


def email_bind():
    verification_code = random.randrange(1000,9999)
    return verification_code

