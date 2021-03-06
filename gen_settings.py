import os
import sys

settings = os.path.abspath(sys.argv[1])

# this goes into a mapnik_settings.js file beside the C++ _mapnik.node
settings_template = """
module.exports.paths = {
    'fonts': %s,
    'input_plugins': %s
};
"""

def wrap_quotes(v):
    # Conditionally wrap an environment variable in quotes
    for i in ["'",'"']:
        if v[0] == v[-1] == i:
            return v
    return '\'%s\'' % v

def write_mapnik_settings(fonts='undefined',input_plugins='undefined'):
    global settings_template
    if '__dirname' in fonts or '__dirname' in input_plugins:
        settings_template = "var path = require('path');\n" + settings_template
    open(settings,'w').write(settings_template % (fonts,input_plugins))
    
if __name__ == '__main__':
    settings_dict = {}
    
    # settings for fonts and input plugins
    # environment settings are for windows tilemill packaging:
    # https://github.com/mapbox/tilemill/blob/master/platforms/windows/package.bat#L37
    ip = os.environ.get('MAPNIK_INPUT_PLUGINS')
    if ip:
        settings_dict['input_plugins'] = wrap_quotes(ip)
    else:
        settings_dict['input_plugins'] = '\'%s\'' % os.popen("./mason_packages/.link/bin/mapnik-config --input-plugins").readline().strip()
    
    mf = os.environ.get('MAPNIK_FONTS')
    if mf:
        settings_dict['fonts'] = wrap_quotes(mf)
    else:
        settings_dict['fonts'] = '\'%s\'' % os.popen("./mason_packages/.link/bin/mapnik-config --fonts").readline().strip()

    write_mapnik_settings(**settings_dict)
