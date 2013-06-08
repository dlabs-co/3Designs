#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    text2QrStl - Convert your QR codes to stl
"""

import qrcode
import sys
import argparse


class QRGen(object):
    """
        Main class, generates qr code and scad
    """
    def __init__(self, scale=4):
        self.scale = scale
        self.data = ""
        self.qr_base = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def make_qr(self):
        self.qr_base.add_data(sys.argv[1])
        self.qr_base.make(fit=True)

    def make_scad(self):
        result = "qr_size=" + str(self.qr_base.modules_count) + ";"
        result += 'module qrcode() {\n'
        for row in range(self.qr_base.modules_count):
            for column in range(self.qr_base.modules_count):
                if self.qr_base.modules[row][column]:
                    result += '    translate([%(x)s, %(y)s, 0])' % {
                        'x': 1 * column - self.qr_base.modules_count / 2,
                        'y': - 1 * row + self.qr_base.modules_count / 2
                    }
                    result += 'cube([%(side)s, %(side)s, 1]);\n' % {
                        'side': 1
                    }
        result += '}\n'
        result += "scale([%s,%s,%s]){ union(){ qrcode(); " \
                %( self.scale, self.scale, self.scale ) + \
            "translate([-10, -10, -1]) cube([qr_size,qr_size,1]); }}"
        return result

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', dest="filename", help='File to save it')
    parser.add_argument('data', metavar='N', type=str, nargs='+', help='Qr data')
    parser.add_argument('--scale', dest="scale", help='Scale the qr code', default=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = argument_parser()
    qr = QRGen(args.scale)
    qr.make_qr()
    if args.filename:
        with open(args.filename, "w") as file_:
            file_.write(qr.make_scad())
    else:
        print qr.make_scad()
