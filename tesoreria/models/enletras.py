#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Translates numbers in its literal representation in Castilian Spanish
# Convierte números a su representación literal en castellano.
# 

#    Copyright 2012 Diego Schulz <dschulz@gmail.com>
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



#
#     23.334.456.234.456.234
#
#     23 . 334 . 456 . 234 . 456 . 234
#  ____________________________________________________
#  |  Cb |  Ca |  Cb |  Ca |  Cb |  Ca |     Clases
#  |     P2    |     P1    |     P0    |     Periodos
#
#
#
#  9.999.999.999.999.999
#  | ||| ||| ||| ||| |||                                +--- Periodo 0 ---
#  | ||| ||| ||| ||| ||+ Unidades                       |
#  | ||| ||| ||| ||| |+- Decenas                        |  Clase A
#  | ||| ||| ||| ||| +-- Centenas                       |
#  | ||| ||| ||| |||                                    -
#  | ||| ||| ||| ||+---- Miles                          |
#  | ||| ||| ||| |+----- Decenas de miles               |  Clase B
#  | ||| ||| ||| +------ Centenas de miles              |
#  | ||| ||| |||                                        +--- Periodo 1 ---
#  | ||| ||| ||+-------- Unidades de millones           |
#  | ||| ||| |+--------- Decenas de millones            |  Clase A
#  | ||| ||| +---------- Centenas de millones           |
#  | ||| |||                                            -
#  | ||| ||+------------ Miles de millones              |
#  | ||| |+------------- Decenas de miles de millones   |  Clase B
#  | ||| +-------------- Centenas de miles de millones  |
#  | |||                                                +--- Periodo 2 ---
#  | ||+---------------- Unidades de billones           |
#  | |+----------------- Decenas de billones            |  Clase A
#  | +------------------ Centenas de billones           |
#  |                                                    -
#  +-------------------- Miles de billones              |
# ---------------------- Decenas de miles de billones   |  Clase B
# ---------------------- Centenas de miles de billones  |
#                                                       +--- Periodo 3 ---
# ---------------------- Unidades de trillones          |
# ---------------------- Decenas de trillones           |  Clase A 
# ---------------------- Centenas de trillones          |
# ...                                                   -

import re

INVALIDO  = 'Número inválido'
MUYGRANDE = 'Número demasiado grande'
NEGATIVO  = '(negativo)'
UN        = 'un'
VEINTIUN  = 'veintiún'
CERO      = 'cero'
CIEN      = 'cien'
MIL       = 'mil'

UNIDADES  = dict(zip('1 2 3 4 5 6 7 8 9'.split(),
                    'uno dos tres cuatro cinco seis siete ocho nueve'.split()))

DIECIS    = dict(zip('10 11 12 13 14 15 16 17 18 19'.split(),
                    'diez once doce trece catorce quince '
                    'dieciséis diecisiete dieciocho diecinueve'.split()))

VEINTIS   = dict(zip('20 21 22 23 24 25 26 27 28 29'.split(), 
                    'veinte veintiuno veintidós veintitrés veinticuatro veinticinco '
                    'veintiséis veintisiete veintiocho veintinueve'.split()))

DECENAS   = dict(zip('1 2 3 4 5 6 7 8 9'.split(),
                    'diez veinte treinta cuarenta cincuenta '
                    'sesenta setenta ochenta noventa'.split()))

CENTENAS  = dict(zip('1 2 3 4 5 6 7 8 9'.split(),
                    'ciento doscientos trescientos cuatrocientos quinientos '
                    'seiscientos setecientos ochocientos novecientos'.split()))

LLON      = 'llón'
LLONES    = 'llones'

# Periodos numéricos
# 6-pack-numbers groups
#
# 999.999.888.888
# ^^^^^^^ ^^^^^^^
PERIODOS =  dict(zip('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20'.split(),
                    'mi bi tri quatri quinti sexti septi octi noni deci '
                    'undeci duodeci tredeci cuatordeci quindeci ' 
                    'sexdeci septendeci octodeci novendeci viginti'.split()))


# Process the second 3-pack-numbers in a numeric period
#    999.999.999.999
#    ^^^     ^^^
def proc_clase_b(c):
    digitos=c['digitos']
    numero=int(digitos)
    final = []
    centenas = 0
    decenas  = 0
    unidades = 0

    # Special case: 100
    if 100 == numero:
       return '{0} {1}'.format(CIEN, MIL)

    # Find out if there are hundreds
    if numero > 99:
       centenas=int(digitos.rjust(3,'0')[0])
       final.append(CENTENAS[str(centenas)])

    numero = numero - (100*centenas)

    # numero < 100:

    if 1 == numero:
       final.append(UN)   
       return '{0} {1}'.format(' '.join(final), MIL)

    if 21 == numero:
       final.append(VEINTIUN)   
       return '{0} {1}'.format(' '.join(final), MIL)

    if 10 > numero > 1: 
       final.append(UNIDADES[str(numero)])
       return '{0} {1}'.format(' '.join(final), MIL)

    if 20 > numero > 9:
       final.append(DIECIS[str(numero)])
       return '{0} {1}'.format(' '.join(final), MIL)
 
    if 30 > numero > 19:
       final.append(VEINTIS[str(numero)])
       return '{0} {1}'.format(' '.join(final), MIL)
    
    if 100 > numero > 29:
       decenas  = int(digitos.rjust(3,'0')[1])
       unidades = int(digitos.rjust(3,'0')[2])

       if 0 == unidades:
          final.append('{0}'.format(DECENAS[str(decenas)]))
       elif 1 == unidades:
          final.append('{0} y {1}'.format(DECENAS[str(decenas)], UN))
       else:
          final.append('{0} y {1}'.format(DECENAS[str(decenas)], UNIDADES[str(unidades)]))

    return '{0} {1}'.format(' '.join(final), MIL)


# Utility function
# Process the first 3-pack-numbers in a numeric period
#    999.999.999.999
#        ^^^     ^^^
def proc_clase_a(c):
    digitos=c['digitos']
    numero=int(digitos)
    periodo=int(c['periodo'])
    final = []
    centenas = 0
    decenas  = 0
    unidades = 0

    # Special case: 100
    if 100 == numero:
       return CIEN

    # Find out if there are hundreds
    if numero > 99:
       centenas=int(digitos.rjust(3,'0')[0])
       final.append(CENTENAS[str(centenas)])

    numero = numero - (100*centenas)
    
    # numero < 100:


    if 1 == numero:
       if periodo == 0:
          final.append('{0}'.format(UNIDADES[str(numero)]))
       else:
          final.append('{0}'.format(UN))
       return '{0}'.format(' '.join(final))

    if 10 > numero > 0: 
       final.append('{0}'.format(UNIDADES[str(numero)]))
       return '{0}'.format(' '.join(final))


    if 20 > numero > 9:
       final.append('{0}'.format(DIECIS[str(numero)]))
       
       return '{0}'.format(' '.join(final))
 
    if 21 == numero:
       if periodo == 0:
          final.append('{0}'.format(VEINTIS[str(numero)]))
       else:
          final.append('{0}'.format(VEINTIUN))

       return '{0}'.format(' '.join(final))

    if 30 > numero > 21 or numero == 20:
       final.append('{0}'.format(VEINTIS[str(numero)]))
       return '{0}'.format(' '.join(final))

    if 100 > numero > 29:
       decenas  = int(digitos.rjust(3,'0')[1])
       unidades = int(digitos.rjust(3,'0')[2])
       
       if 0 == unidades:
          final.append('{0}'.format(DECENAS[str(decenas)]))
       elif 1 == unidades and periodo > 0:
          final.append('{0} y {1}'.format(DECENAS[str(decenas)], UN))
       elif 2 == decenas and 1 == unidades and periodo > 0:
          final.append('{0} y {1}'.format(DECENAS[str(decenas)], VEINTIUN))
       else:
          final.append('{0} y {1}'.format(DECENAS[str(decenas)], UNIDADES[str(unidades)]))

    return '{0}'.format(' '.join(final))

# Utility function
# Process a 3-pack-numbers group
def proc_clase(c):
    numcls=c['clase']
    digitos=c['digitos']
    numero=int(digitos)

    if 0 == numero:
       return None

    if numcls == 0:
       return proc_clase_a(c)

    return proc_clase_b(c)

# Utility function
# Add the suffix corresponding to each numeric period
# millones, billones, etc
def sufijo_periodo(prd, n):
    if prd == 0: 
         return None
    try:
       if n == 1:
           return '{0} {1}{2}'.format(UN, PERIODOS[str(prd)], LLON)
       if n > 1:
          return '{0}{1}'.format(PERIODOS[str(prd)], LLONES)
         
       return None

    except KeyError:
       return MUYGRANDE

# Utility function
def proc_periodo(p):
    numper=p['periodo']
    digitos=p['digitos']
    numero=int(digitos) 

    # Special case: 'Trescientos diez mil *un* millones.'
    if 1 == numero and numper > 0:
       return '{0}'.format(sufijo_periodo(numper,numero))

    # Split digits into classes
    c1 = digitos[::-1][0:3][::-1]
    c2 = digitos[::-1][3:6][::-1]

    clases = []
    clases.insert(0, { 'digitos': c1, 'clase': 0, 'periodo': numper } )

    if len(digitos) > 3:
       clases.insert(0, { 'digitos': c2, 'clase': 1, 'periodo': numper } )

    # Process class
    final = []
    for clase in map(proc_clase, clases):
       if clase is not None:
          final.append(clase) 

    if 0 == len(final):
       return None
    
    sp = sufijo_periodo(numper, numero)
    if sp is None:  
       return '{0}'.format(' '.join(final))
    else:
       return '{0} {1}'.format(' '.join(final), sufijo_periodo(numper,numero))

def en_letras (numero, sep_decimal=','):
    '''en_letras(string numero,string sep_decimal) -> string
    Convierte un numero en forma de cadena de digitos a su representacion en letras.
    '''
    # Contains strings to be joined at the end 
    final = []

    numero = numero.strip()

    if numero.count(sep_decimal) > 1:
       return INVALIDO

    # Find out if it's a negative number, then strip the - character
    negativo = numero.startswith('-')
    numero = numero.replace('-','')

    # Bailout if there are non-digits 
    if re.search("\D", numero.replace(sep_decimal,'')):
        return INVALIDO
    
    # Split string in integer,decimal
    partes = numero.split(sep_decimal)
  
    # does it have integer and decimal parts?
    npartes = len(partes)
    if npartes < 1 or npartes > 2:
        return INVALIDO

    entero = str(int(partes[0]))
    decimal = ""
    if npartes == 2:
       decimal = str(int(partes[1]))


    # If the integer part is zero
    if entero == "0":
        final.append(CERO)
        if npartes == 2:
           final.append('con {00}/1{1}'.format (int(partes[1]), ''.ljust(len(partes[1]),'0' )))
               
        return ' '.join(final).strip().capitalize()
    
    if negativo:
        final.append(NEGATIVO)

    longitud = len(entero)
    numperiodos = int(longitud / 6)

    if (longitud % 6) > 0:
       numperiodos = numperiodos + 1
 
    periodos = []
    s=0
    for i in range(numperiodos):
       p = entero[::-1][s:s+6][::-1]  
       periodos.insert(0, {'digitos': p, 'periodo': i })
       s = s + 6

    for pp in map(proc_periodo,periodos):
       if pp is not None:
          final.append(pp.strip())

    ## Build final string

    # If theres a decimal part...
    if npartes == 2:
        final.append('con {0}/1{1}'.format (int(partes[1]), ''.ljust(len(partes[1]),'0' )))
    
    fstr = ' '.join(final)
    return fstr.capitalize() 



#### TESTS 
#### TO BE REMOVED
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print ( 'Error: Argumentos insuficientes.\nUso:\n\t{0} número[:separador decimal]\n'.format(sys.argv[0]))
    else:
        # Convert every number in argv
        for arg in sys.argv[1:]:
          if arg.count('#') == 1:
            num,sep = arg.split('#')
            print(en_letras(num,sep_decimal=sep))
          else:
            if arg == 'clstest':
               for n in range(0,1000):
                  s = str(n)
                  print('{0}: {1}'.format( s.rjust(9,' '), en_letras(s)))

               for n in range(220000,222000):
                  s = str(n)
                  print('{0}: {1}'.format( s.rjust(9,' '), en_letras(s)))

               for n in range(999999,1000010):
                  s = str(n)
                  print('{0}: {1}'.format( s.rjust(9,' '), en_letras(s)))

            elif arg == 'stresstest':
               import time
               t1 = time.time()
               errcnt=0
               cnt=0
               for n in range(0,1000000):
                  s = str(n)
                  if len(en_letras(s))<2:
                     errcnt += 1
                  cnt += 1
               t2 = time.time()
               print ('Errores: {0}'.format(errcnt))
               print ('Tomó {0:.2f}ms hacer {1} conversiones (~{2:.6f}ms/conversion)'.format((t2-t1)*1000.0, cnt, 1000.0*float(t2-t1)/float(cnt)  ))
                     
            else:
               print('{0}: {1}'.format( arg.rjust(9,' '), en_letras(arg)))

#~ MONTO = '390.690,00'.replace('.','')
#~ print MONTO

#~ enletras = en_letras (MONTO, sep_decimal=',')

#~ print enletras
