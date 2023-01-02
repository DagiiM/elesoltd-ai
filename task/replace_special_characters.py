from html import escape

def replace_special_characters(input_text):
    replacements = {
        '\n': '<br>',
        '\t': '&emsp;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&apos;',
        '<': '&lt;',
        '>': '&gt;',
        '\b': '&#8;',
        '\f': '&#12;',
        '\0': '&#0;',
        '&#xA0;': '&nbsp;',
        '&#xA1;': '&iexcl;',
        '&#xA2;': '&cent;',
        '&#xA3;': '&pound;',
        '&#xA4;': '&curren;',
        '&#xA5;': '&yen;',
        '&#xA6;': '&brvbar;',
        '&#xA7;': '&sect;',
        '&#xA8;': '&uml;',
        '&#xA9;': '&copy;',
        '&#xAA;': '&ordf;',
        '&#xAB;': '&laquo;',
        '&#xAC;': '&not;',
        '&#xAD;': '&shy;',
        '&#xAE;': '&reg;',
        '&#xAF;': '&macr;',
        '&#xB0;': '&deg;',
        '&#xB1;': '&plusmn;',
        '&#xB2;': '&sup2;',
        '&#xB3;': '&sup3;',
        '&#xB4;': '&acute;',
        '&#xB5;': '&micro;',
        '&#xB6;': '&para;',
        '&#xCC;': '&Igrave;',
        '&#xCD;': '&Iacute;',
        '&#xCE;': '&Icirc;',
        '&#xCF;': '&Iuml;',
        '&#xD0;': '&ETH;',
        '&#xD1;': '&Ntilde;',
        '&#xD2;': '&Ograve;',
        '&#xD3;': '&Oacute;',
        '&#xD4;': '&Ocirc;',
        '&#xD5;': '&Otilde;',
        '&#xD6;': '&Ouml;',
        '&#xD7;': '&times;',
        '&#xD8;': '&Oslash;',
        '&#xD9;': '&Ugrave;',
        '&#xDA;': '&Uacute;',
        '&#xDB;': '&Ucirc;',
        '&#xDC;': '&Uuml;',
        '&#xDD;': '&Yacute;',
        '&#xDE;': '&THORN;',
        '&#xDF;': '&szlig;',
        '&#xE0;': '&agrave;',
        '&#xE1;': '&aacute;',
        '&#xE2;': '&acirc;',
        '&#xE3;': '&atilde;',
        '&#xE4;': '&auml;',
        '&#xE5;': '&aring;',
        '&#xE6;': '&aelig;',
        '&#xE7;': '&ccedil;',
        '&#xE8;': '&egrave;',
        '&#xE9;': '&eacute;',
        '&#xEA;': '&ecirc;',
        '&#xEB;': '&euml;',
        '&#xEC;': '&igrave;',
        '&#xED;': '&iacute;',
        '&#xEE;': '&icirc;',
        '&#xEF;': '&iuml;',
        '&#xF0;': '&eth;',
        '&#xF1;': '&ntilde;',
        '&#xF2;': '&ograve;',
        '&#xF3;': '&oacute;',
        '&#xF4;': '&ocirc;',
        '&#xF5;': '&otilde;',
        '&#xF6;': '&ouml;',
        '&#xF7;': '&divide;',
        '&#xF8;': '&oslash;',
        '&#xF9;': '&ugrave;',
        }
    for old, new in replacements.items():
        if old in input_text:
            input_text = input_text.replace(old, new)
            
    return escape(input_text)

    return input_text