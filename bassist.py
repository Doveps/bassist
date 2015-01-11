#!/usr/bin/env python
# This script parses output from the Doveps scanner. For documentation,
# see README.md
import argparse
import logging
import logging.config
import os

import lib.parser.host
import lib.flavor.directory
import lib.diff.flavor

logging.config.fileConfig('log.conf')
logger = logging.getLogger('bassist')

try:
    from log_override import LOG_OVERRIDES
    logging.config.dictConfig(LOG_OVERRIDES)
except:
    logger.debug('unable to load log_override; ignoring')

arg_parser = argparse.ArgumentParser(
        description='Generate either a new flavor, or compare to an existing \
                flavor by parsing scanner results.')
arg_parser.add_argument(
        '-l', '--parse-logs',
        nargs='*', metavar='LOG',
        help='Only parse the given logs, for example "debs_stdout"')
arg_parser.add_argument(
        '-r', '--record',
        action='store_true',
        help='When set, record to the given flavor name; otherwise compare to \
                the given flavor name')

required_args = arg_parser.add_argument_group('required arguments')
required_args.add_argument(
        '-f', '--flavor-directory',
        required=True,
        help='The path to the directory containing bassist flavors')
required_args.add_argument(
        '-n', '--flavor-name',
        required=True,
        help='Compare with or record to the given flavor name')
required_args.add_argument(
        '-s', '--scanner-directory',
        required=True,
        help='The path to the directory containing scanner results')

args = arg_parser.parse_args()

logger.debug('reading flavors')
flavors = lib.flavor.directory.Directory(args.flavor_directory).db
requested_flavor = flavors.get_obj_from_name(args.flavor_name)
logger.debug('retrieved requested flavor %s', requested_flavor)

compared_flavor = None
if not args.record:
    compared_flavor = lib.flavor.obj.Obj()

logger.debug('importing parsers')
parsed_host = lib.parser.host.Host(args.scanner_directory)
logger.debug('finished importing parsers')

parse_all = not args.parse_logs

for parser in parsed_host.parsers:

    logger.debug('parser log: %s', parser.log)
    if not parse_all:
        if not parser.log in args.parse_logs:
            logger.info(
                    'skipping parse of %s since you requested only %s',
                    parser.path, args.parse_logs)
            continue

    logger.info('parsing: %s', parser.path)
    parser.parse()
    if args.record:
        parser.record(requested_flavor)
    else:
        if parse_all:
            parser.record(compared_flavor)
        else:
            parser.diff(requested_flavor)

if parse_all and not args.record:
    diff = lib.diff.flavor.Flavor(requested_flavor, compared_flavor)

flavors.close()
