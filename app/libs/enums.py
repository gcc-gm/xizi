#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum


class PendingStatus(Enum):
    """
        交易状态
    """
    No_trad = 0
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, status):
        key_map = {
            cls.No_trad:{
                'requester': '等待确认',
                'giver': '等待确认'
            },

            cls.Waiting: {
                'requester': '正在确认',
                'giver': '同意赠送'
            },
            cls.Reject: {
                'requester': '同意拒绝',
                'giver': '已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'giver': '同意撤销'
            },
            cls.Success: {
                'requester': '达成心愿',
                'giver': '送出爱心'
            }
        }
        return key_map[status]

