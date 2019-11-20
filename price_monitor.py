#!/usr/bin/env python
# coding: utf-8
# @Author : JackLee
# @contact: jackleeforce@gmail.com
# @Time : 2019-06-10 16:18
# @File : price_monitor.py
# @desc:
import getopt
import logging
import sys
import func


class PriceMonitor:
    __monitor_type = ''
    __operation = ''
    __target = ''
    __keyword = ''
    __ideal_price = ''

    def __init__(self, monitor_type, operation, target, keyword, ideal_price):
        self.__monitor_type = monitor_type
        self.__operation = operation
        self.__target = target
        self.__keyword = keyword
        self.__ideal_price = ideal_price

        print(
            'monitor_type:{0},operation:{1},target:{2},keyword:{3},ideal_price:{4}'.format(self.__monitor_type,
                                                                                           self.__operation,
                                                                                           self.__target,
                                                                                           self.__keyword,
                                                                                           self.__ideal_price))

    def handle_operation(self):

        if self.__operation == 'add':
            return self.__add()
        elif self.__operation == 'delete':
            return self.__delete()
        elif self.__operation == 'modify':
            return self.__delete()
        elif self.__operation == 'query':
            return self.__query()
        else:
            logging.error('Unsupport operation type:' + self.__operation)
            print_help()
        return

    def __add(self):
        if self.__target == 'amazon_china':
            pass
        else:
            logging.error('Unsupport target:' + self.__target)
            print_help()

    def __delete(self):
        pass

    def __modify(self):
        pass

    def __query(self):
        pass


def print_help():
    help_command = 'price_monitor.py --monitor_type --op <operation> --target <target_website> --keyword <search_keyword> --ideal_price <ideal_price>'

    print(help_command)


def main(argv):
    monitor_type = ''
    operation = ''
    target = ''
    keyword = ''
    ideal_price = ''

    try:
        opts, args = getopt.getopt(argv, "h",
                                   ["help", "monitor_type=", "op=", "target=", "keyword=", "ideal_price=", "id="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print_help()
            sys.exit()
        elif opt in '--monitor_type':
            monitor_type = arg
        elif opt in '--op':
            operation = arg
        elif opt in '--target':
            target = arg
        elif opt in '--keyword':
            keyword = arg
        elif opt in '--ideal_price':
            ideal_price = arg

    price_monitor = PriceMonitor(monitor_type, operation, target, keyword, ideal_price)

    price_monitor.handle_operation()

    return


if __name__ == '__main__':
    func.init_log('price_monitor.log')

    main(sys.argv[1:])

    exit(0)
