
import qrcode
qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
)
qr.add_data('Some data')
qr.make(fit=True)
print qr.modules

result = ""
result += 'module qrcode() {\n'
for row in range(qr.modules_count):
    for column in range(qr.modules_count):
        if qr.modules[column][row] != False:
            result += '    translate([%(x)s, %(y)s, 0])' % {
                'x': 1 * column - qr.modules_count / 2,
                'y': - 1 * row + qr.modules_count / 2
            }
            result += ' cube([%(block_side)s, %(block_side)s, 1]);\n' % {
                'block_side': 1
            }
result += '}\n'
result += "scale([%s,%s,%s]){union(){qrcode(); translate([-10, -10, -1]) cube([qr_size,qr_size,1]); }}";

print result
