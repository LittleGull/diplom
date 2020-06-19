# Landsat Util
# License: CC0 1.0 Universal

#from __future__ import print_function, division, absolute_import

import os
import sys
import time
import re
from os.path import join
import logging


try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO
import datetime
import geocoder
import logging


class Capturing(list):
    """
    Captures a subprocess stdout.

    :Usage:
        >>> with Capturing():
        ...     subprocess(args)
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


class timer(object):
    """
    A timer class.

    :Usage:
        >>> with timer():
        ...     your code
    """
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print('Time spent : {0:.2f} seconds'.format((self.end - self.start)))


def exit(message, code=0):
    """ output a message to stdout and terminates the process.

    :param message:
        Message to be outputed.
    :type message:
        String
    :param code:
        The termination code. Default is 0
    :type code:
        int

    :returns:
        void
    """
    logger = logging.getLogger('log')
    #v = VerbosityMixin()
    if code == 0:
        logger.info('===> ' + message)
        #v.output(message, normal=True, arrow=True)
        #v.output('Done!', normal=True, arrow=True)
    else:
        logger.error(message)
        #v.output(message, normal=True, error=True)
    sys.exit(code)


def create_paired_list(value):
    """ Create a list of paired items from a string.

    :param value:
        the format must be 003,003,004,004 (commas with no space)
    :type value:
        String

    :returns:
        List

    :example:
        >>> create_paired_list('003,003,004,004')
        [['003','003'], ['004', '004']]

    """
    if isinstance(value, list):
        value = ",".join(value)

    array = re.split('\D+', value)

    # Make sure the elements in the list are even and pairable
    if len(array) % 2 == 0:
        new_array = [list(array[i:i + 2]) for i in range(0, len(array), 2)]
        return new_array
    else:
        raise ValueError('The string should include pairs and be formatted. '
                         'The format must be 003,003,004,004 (commas with '
                         'no space)')


def check_positive_int(s):
    msg = "Not a valid positive int value: '{0}'.".format(s)
    try:
        ivalue = int(s)
        if ivalue <= 0:
            raise ValueError(msg)
        return ivalue
    except ValueError:
        raise ValueError(msg)


def check_create_folder(folder_path):
    """ Check whether a folder exists, if not the folder is created.

    :param folder_path:
        Path to the folder
    :type folder_path:
        String

    :returns:
        (String) the path to the folder
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def get_file(path):
    """ Separate the name of the file or folder from the path and return it.

    :param path:
        Path to the folder
    :type path:
        String

    :returns:
        (String) the filename

    :example:
        >>> get_file('/path/to/file.jpg')
        'file.jpg'
    """
    return os.path.basename(path)


def get_filename(path):
    """ Return the filename without extension.

    :param path:
        Path to the folder
    :type path:
        String

    :returns:
        (String) the filename without extension

    :example:
        >>> get_filename('/path/to/file.jpg')
        'file'
    """
    #return os.path.splitext(get_file(path))[0]
    return (get_file(path)).split('.')[0]


def three_digit(number):
    """ Add 0s to inputs that their length is less than 3.

    :param number:
        The number to convert
    :type number:
        int

    :returns:
        String

    :example:
        >>> three_digit(1)
        '001'
    """
    number = str(number)
    if len(number) == 1:
        return u'00%s' % number
    elif len(number) == 2:
        return u'0%s' % number
    else:
        return number


def georgian_day(date):
    """ Returns the number of days passed since the start of the year.

    :param date:
        The string date with this format %m/%d/%Y
    :type date:
        String

    :returns:
        int

    :example:
        >>> georgian_day('05/1/2015')
        121
    """
    try:
        fmt = '%m/%d/%Y'
        return datetime.datetime.strptime(date, fmt).timetuple().tm_yday
    except (ValueError, TypeError):
        return 0


def year(date):
    """ Returns the year.

    :param date:
        The string date with this format %m/%d/%Y
    :type date:
        String

    :returns:
        int

    :example:
        >>> year('05/1/2015')
        2015
    """
    try:
        fmt = '%m/%d/%Y'
        return datetime.datetime.strptime(date, fmt).timetuple().tm_year
    except ValueError:
        return 0


def reformat_date(date, new_fmt='%Y-%m-%d'):
    """ Returns reformated date.

    :param date:
        The string date with this format %m/%d/%Y
    :type date:
        String
    :param new_fmt:
        date format string. Default is '%Y-%m-%d'
    :type date:
        String

    :returns:
        int

    :example:
        >>> reformat_date('05/1/2015', '%d/%m/%Y')
        '1/05/2015'
    """
    try:
        if isinstance(date, datetime.datetime):
            return date.strftime(new_fmt)
        else:
            fmt = '%m/%d/%Y'
            return datetime.datetime.strptime(date, fmt).strftime(new_fmt)
    except ValueError:
        return date


def convert_to_integer_list(value):
    """ Converts a comma separate string to a list

    :param value:
        the format must be 003,003,004,004 (commas with no space)
    :type value:
        String

    :returns:
        List

    :example:
        >>> convert_to_integer_list('003,003,004,004')
        ['003', '003', '004', '004']

    """
    if isinstance(value, list) or value is None:
        return value
    else:
        s = re.findall('(10|11|QA|[0-9])', value)
        for k, v in enumerate(s):
            try:
                s[k] = int(v)
            except ValueError:
                pass
        return s


# Geocoding confidence scores, from https://github.com/DenisCarriere/geocoder/blob/master/docs/features/Confidence%20Score.md
geocode_confidences = {
    10: 0.25,
    9: 0.5,
    8: 1.,
    7: 5.,
    6: 7.5,
    5: 10.,
    4: 15.,
    3: 20.,
    2: 25.,
    1: 99999.,
    # 0: unable to locate at all
}


def geocode(address, required_precision_km=1.):
    """ Identifies the coordinates of an address

    :param address:
        the address to be geocoded
    :type value:
        String
    :param required_precision_km:
        the maximum permissible geographic uncertainty for the geocoding
    :type required_precision_km:
        float

    :returns:
        dict

    :example:
        >>> geocode('1600 Pennsylvania Ave NW, Washington, DC 20500')
        {'lat': 38.89767579999999, 'lon': -77.0364827}

    """
    geocoded = geocoder.google(address)
    precision_km = geocode_confidences[geocoded.confidence]

    if precision_km <= required_precision_km:
        (lon, lat) = geocoded.geometry['coordinates']
        return {'lat': lat, 'lon': lon}
    else:        
        raise ValueError("Address could not be precisely located")


def convert_to_float_list(value):
    """ Converts a comma separate string to a list

    :param value:
        the format must be 1.2,-3.5 (commas with no space)
    :type value:
        String

    :returns:
        List

    :example:
        >>> convert_to_float_list('1.2,-3.5')
        [1.2, -3.5]

    """
    if isinstance(value, list) or value is None:
        return value
    else:
        s = re.findall('([-+]?\d*\.\d+|\d+|[-+]?\d+)', value)
        for k, v in enumerate(s):
            try:
                s[k] = float(v)
            except ValueError:
                pass
        return s


def check_tile(value):
    """ Check if tile name is correct.

    :param value:
        tile name ('38ULA')
    :type value:
        String

    :returns:
        value

    """
    if re.match(r"\d{1,2}[A-Z]{3}", value):
        return value
    else:
        raise ValueError("Wrong tile name: '{}'".format(value))


def adjust_bounding_box(bounds1, bounds2):
    """ If the bounds 2 corners are outside of bounds1, they will be adjusted to bounds1 corners

    @params
    bounds1 - The source bounding box
    bounds2 - The target bounding box that has to be within bounds1

    @return
    A bounding box tuple in (y1, x1, y2, x2) format
    """

    # out of bound check
    # If it is completely outside of target bounds, return target bounds
    if ((bounds2[0] > bounds1[0] and bounds2[2] > bounds1[0]) or
            (bounds2[2] < bounds1[2] and bounds2[2] < bounds1[0])):
        return bounds1

    if ((bounds2[1] < bounds1[1] and bounds2[3] < bounds1[1]) or
            (bounds2[3] > bounds1[3] and bounds2[1] > bounds1[3])):
        return bounds1

    new_bounds = list(bounds2)

    # Adjust Y axis (Longitude)
    if (bounds2[0] > bounds1[0] or bounds2[0] < bounds1[3]):
        new_bounds[0] = bounds1[0]
    if (bounds2[2] < bounds1[2] or bounds2[2] > bounds1[0]):
        new_bounds[2] = bounds1[2]

    # Adjust X axis (Latitude)
    if (bounds2[1] < bounds1[1] or bounds2[1] > bounds1[3]):
        new_bounds[1] = bounds1[1]
    if (bounds2[3] > bounds1[3] or bounds2[3] < bounds1[1]):
        new_bounds[3] = bounds1[3]

    return tuple(new_bounds)


def remove_slash(value):

    assert(isinstance(value, str))
    return re.sub('(^\/|\/$)', '', value)


def url_builder(segments):

    # Only accept list or tuple
    assert((isinstance(segments, list) or isinstance(segments, tuple)))
    return "/".join([remove_slash(s) for s in segments])


def convert_date(ordinal_date, format='%Y-%m-%d'):
    """ Convert date from 'YYYYDDD' to date string with format.
    """
    date = datetime.datetime(int(ordinal_date[:4]), 1, 1) + datetime.timedelta(int(ordinal_date[4:]) - 1)
    return date.strftime(format)


def convert_to_datetime(date):
    """ Convert date from string 'YYYY-MM-DD' to datetime.
    """
    if isinstance(date, datetime.date):
        return date
    date = date.split('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))


def form_file_name(format='{prefix}_{date}_{dstype}_{resolution}_{field_group}.tif', prefix='', date='', dstype='', resolution='', field_group='', field_id=''):
    """ Form file name string.
    """            
    return format.format(prefix=prefix, date=date, dstype=dstype, resolution=resolution, field_group=field_group, field_id=field_id)


def split_file_name(layer_name):

    name = layer_name.split('_')
    field_id = None
    if len(name) < 7:
        return None
    elif len(name) > 7:
        field_id = name[7]

    date = '{}-{}-{}'.format(name[1], name[2], name[3])
    image_set = name[4]
    resolution = name[5]
    field_group_id = name[6] if name[6] != 'None' else None

    return date, image_set, resolution, field_group_id, field_id, layer_name

def merge_two_dicts(dict1, dict2):
    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3


def start_logging(logger, logs_dir, debug=False):
    if debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    # Logger settings
    logger.setLevel(logging_level)
    logger.propagate = False

    handler_stdout = logging.StreamHandler()
    handler_stdout.setLevel(logging_level)

    # Check if logs folder is created
    check_create_folder(logs_dir)

    handler_file = logging.FileHandler(join(logs_dir, 'landsat.log'))
    handler_file.setLevel(logging_level)

    # Create log's formatters
    formatter_file = logging.Formatter('%(asctime)s [%(module)s] [%(levelname)s]  %(message)s')
    formatter_stdout = logging.Formatter('%(message)s')

    handler_stdout.setFormatter(formatter_stdout)
    handler_file.setFormatter(formatter_file)

    if not logger.handlers:
        logger.addHandler(handler_file)
        logger.addHandler(handler_stdout)
    logger.info('\n\n\nStart processing.\n')

if __name__ == "__main__":
     # print(create_paired_list('003,003,004,004'))

    print(convert_to_tiles_list('38ULA,38ULB'))

