import click
import sys
from datetime import datetime

#  \g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\
TAGBLOCK_T_FORMAT='%Y-%m-%d %H.%M.%S'


def format_tagblock_t(dt):
    return dt.strftime(TAGBLOCK_T_FORMAT)

def compute_checksum(sentence):
    """Compute the NMEA checksum for a payload."""
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    checksum_str = '%02x' % checksum
    return checksum_str.upper()


def add_tagblock(nmea, station):
    dt = datetime.utcnow()
    params = dict(
        c=round(dt.timestamp()*1000),
        s=station,
        T=format_tagblock_t(dt)
    )
    param_str = ','.join(["{}:{}".format(k, v) for k,v in params.items()])
    checksum = compute_checksum(param_str)
    return '\\{}*{}\\{}'.format(param_str, checksum, nmea)


@click.command()
@click.argument('input',  type=click.File('r'), default='-')
@click.argument('output', type=click.File('w'), default='-')
@click.option('-s', '--station', default='sdr-experiments')
def tagblock(input, output, station):

    while True:
        nmea = input.readline()
        if not nmea:
            break
        output.write(add_tagblock(nmea, station))


if __name__ == '__main__':
    tagblock()
