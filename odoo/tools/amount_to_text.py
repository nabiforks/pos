# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#-------------------------------------------------------------
# French
#-------------------------------------------------------------


to_19_fr = ( u'zéro',  'un',   'deux',  'trois', 'quatre',   'cinq',   'six',
          'sept', 'huit', 'neuf', 'dix',   'onze', 'douze', 'treize',
          'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf' )
tens_fr  = ( 'vingt', 'trente', 'quarante', 'Cinquante', 'Soixante', 'Soixante-dix', 'Quatre-vingts', 'Quatre-vingt Dix')
denom_fr = ( '',
          'Mille',     'Millions',         'Milliards',       'Billions',       'Quadrillions',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Décillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Icosillion', 'Vigintillion' )

def _convert_nn_fr(val):
    """ convert a value < 100 to French
    """
    if val < 20:
        return to_19_fr[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_fr)):
        base = 10
        if dval in [60, 80]:
            base = 20
        if dval + base > val:
            if val % base:
                bond = (val % base in [1, 11] and dval != 80) and '-et-' or '-'
                return dcap + bond + to_19_fr[val % base]
            return dcap

def _convert_nnn_fr(val):
    """ convert a value < 1000 to french
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        word = (rem > 1 and to_19_fr[rem] + ' cents') or 'Cent'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_fr(mod)
    return word

def french_number(val):
    if val < 100:
        return _convert_nn_fr(val)
    if val < 1000:
         return _convert_nnn_fr(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_fr))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn_fr(l) + ' ' + denom_fr[didx]
            if r > 0:
                ret = ret + ', ' + french_number(r)
            return ret

def amount_to_text_fr(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = french_number(abs(int(list[0])))
    end_word = french_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and ' Cents' or ' Cent'
    final_result = start_word +' '+units_name+' '+ end_word +' '+cents_name
    return final_result

#-------------------------------------------------------------
# Dutch
#-------------------------------------------------------------

to_19_nl = ( 'Nul',  'Een',   'Twee',  'Drie', 'Vier',   'Vijf',   'Zes',
          'Zeven', 'Acht', 'Negen', 'Tien',   'Elf', 'Twaalf', 'Dertien',
          'Veertien', 'Vijftien', 'Zestien', 'Zeventien', 'Achttien', 'Negentien' )
tens_nl  = ( 'Twintig', 'Dertig', 'Veertig', 'Vijftig', 'Zestig', 'Zeventig', 'Tachtig', 'Negentig')
denom_nl = ( '',
          'Duizend', 'Miljoen', 'Miljard', 'Triljoen', 'Quadriljoen',
           'Quintillion', 'Sextiljoen', 'Septillion', 'Octillion', 'Nonillion',
           'Decillion', 'Undecillion', 'Duodecillion', 'Tredecillion', 'Quattuordecillion',
           'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

def _convert_nn_nl(val):
    """ convert a value < 100 to Dutch
    """
    if val < 20:
        return to_19_nl[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_nl)):
        if dval + 10 > val:
            if val % 10:
                return to_19_nl[val % 10] + '-en-' +  dcap
            return dcap

def _convert_nnn_nl(val):
    """ convert a value < 1000 to Dutch
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        word = (rem > 1 and to_19_nl[rem] + 'honderd') or 'Honderd'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_nl(mod)
    return word

def dutch_number(val):
    if val < 100:
        return _convert_nn_nl(val)
    if val < 1000:
         return _convert_nnn_nl(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_nl))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn_nl(l) + ' ' + denom_nl[didx]
            if r > 0:
                ret = ret + ', ' + dutch_number(r)
            return ret

def amount_to_text_nl(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = dutch_number(int(list[0]))
    end_word = dutch_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and 'cent' or 'cent'
    final_result = start_word +' '+units_name+' '+ end_word +' '+cents_name
    return final_result

#-------------------------------------------------------------
# Generic functions
#-------------------------------------------------------------

_translate_funcs = {'fr' : amount_to_text_fr, 'nl' : amount_to_text_nl}

def add_amount_to_text_function(lang, func):
    _translate_funcs[lang] = func
    
#TODO: we should use the country AND language (ex: septante VS soixante dix)
#TODO: we should use en by default, but the translation func is yet to be implemented
def amount_to_text(nbr, lang='fr', currency='euro'):
    """ Converts an integer to its textual representation, using the language set in the context if any.

        Example::
        
            1654: mille six cent cinquante-quatre.
    """
#    if nbr > 1000000:
##TODO: use logger   
#        print "WARNING: number too large '%d', can't translate it!" % (nbr,)
#        return str(nbr)
    
    if not _translate_funcs.has_key(lang):
#TODO: use logger   
        print "WARNING: no translation function found for lang: '%s'" % (lang,)
#TODO: (default should be en) same as above
        lang = 'fr'
    return _translate_funcs[lang](abs(nbr), currency)

if __name__=='__main__':
    from sys import argv
    
    lang = 'nl'
    if len(argv) < 2:
        for i in range(1,200):
            print i, ">>", amount_to_text(i, lang)
        for i in range(200,999999,139):
            print i, ">>", amount_to_text(i, lang)
    else:
        print amount_to_text(int(argv[1]), lang)

#################### New functions added in Indian format currency  ####################
ones = {
   0: '', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine',
   10:'ten', 11:'eleven', 12:'twelve', 13:'thirteen', 14:'fourteen', 15:'fifteen', 16:'sixteen',
   17:'seventeen', 18:'eighteen', 19:'nineteen', 20:'twenty',
}

tens = {
   1: 'ten', 2:'twenty', 3:'thirty',4:'forty', 5:'fifty', 6:'sixty', 7:'seventy', 8:'eighty', 9:'ninety'
}

#START
def _100_to_text_in(chiffre):
   if chiffre in ones:
      return ones[chiffre]
   else:
      if chiffre%10>0:
         return tens[chiffre / 10]+'-'+ones[chiffre % 10]
      else:
         return tens[chiffre / 10]
def _1000_to_text_in(chiffre):
   d = _100_to_text_in(chiffre % 100)
   d2 = chiffre/100
   if d2>0:
      return ones[d2]+' hundred '+d
   else:
      return d

def _10000_to_text_in(chiffre):
   if chiffre==0:
      return 'zero'
   part1 = _1000_to_text_in(chiffre % 1000)
   part2 = (int(str(chiffre/1000)[-2:])>0 and _1000_to_text_in(int(str(chiffre/1000)[-2:]))+' thousand') or ''
   part3 = ((int(str(chiffre/100000)[-2:]))>1 and _1000_to_text_in(int(str(chiffre/100000)[-2:]))+' lakhs') or ((int(str(chiffre/100000)[-2:]))>0 and _1000_to_text_in(int(str(chiffre/100000)[-2:]))+' lakh') or ''
   part4 = ((int(str(chiffre/10000000)[-2:]))>1 and _1000_to_text_in(int(str(chiffre/10000000)[-2:]))+' crores') or ((int(str(chiffre/10000000)[-2:]))>0 and _1000_to_text_in(int(str(chiffre/10000000)[-2:]))+' crore') or ''
   if (part2 or part3 or part4) and part1:
      part1 = ' '+part1
   if (part3 or part4) and part2:
      part2 = ' '+part2
   if part4 and part3:
      part3 = ' '+part3
   return part4+part3+part2+part1

def amount_to_text_in(number, currency):
   units_number = int(number)
   units_name = currency
   if units_number > 1:
      units_name += 's'
   units = _10000_to_text_in(units_number)
   units = units_number and '%s %s' % (units_name, units) or ''
   
   cents_number = int(number * 100) % 100
   cents_name = (cents_number > 1) and '& Paise' or '& Paisa'
   cents = _100_to_text_in(cents_number)
   cents = cents_number and '%s %s' % (cents_name, cents) or ''
   
   if units and cents:
      cents = ' '+cents
     
   return units + cents+' only.'
#END
