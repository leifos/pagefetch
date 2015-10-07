#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   04/07/2013
Last revision: 27/10/2013

Requires:
---------
"""
from django.core.management import setup_environ
from pagefetch_project import settings
setup_environ(settings)

from pagefetch import game_model_functions
import argparse
import os
from pagefetch import deployment_model_functions


#fetch data for population from file
def get_trending_queries(filename):
    """Extract population data from a file.
       Returns a list of tuples created from comma separated values in file
    """
    f = open(filename, 'r')
    trend_tuples_list = []
    for line in f:
        trend_tuples_list.append(tuple((line.strip()).split(',')))
    f.close()
    return trend_tuples_list

def main():

    parser = argparse.ArgumentParser(
        description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=int,default=True,
                        help="if set to false deletes category from database\
                        if already present.")
    #TODO(mtbvc):won't need this
    parser.add_argument("-cn", "--category_name", type=str,
                        help="Name of category.")
    parser.add_argument("-f", "--filename",
                        default= os.getcwd() + '/data/trends/game_data.txt', type=str,
                        help="relative path to population data file")
    parser.add_argument("-l", "-local", type=str, default=False,
                        help="If populating images from disk use this flag")

    args = parser.parse_args()
    if args.filename:
        data_list = get_trending_queries(args.filename)
        for data_tuple in data_list:
            cat = game_model_functions.get_category(data_tuple[0],'icon','',append=args.append)
            #data_tuple[1] is url
            #game_model_functions.populate_pages([data_tuple[1]],cat)
            deployment_model_functions.populate_pages([data_tuple[1]],cat,halved_screen_shot=True)
        return 0
    else:
        print parser.print_help()
        return 2
        #import doctest
        #test_results = doctest.testmod()
        #print test_results
        #if not test_results.failed:
        #    populate(args.file_name, args.category_name, args.append)
        #    print "Category and pages have been populated"
        #return 0


if __name__ == '__main__':
    main()
