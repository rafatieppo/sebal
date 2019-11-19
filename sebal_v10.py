# ======================================================================
#                                        Rafael Tieppo
#                                        rafaelt@unemat.br
#                                        https://rafatieppo.github.io/
#                                        30-04-2018
# Sebal algorithm for Eto estimation - running Python 3.x
# ======================================================================

# ------------------------------------------------------------
# libraries
# Order matters
import math
import numpy as np
import os
from grass_session import Session
import grass.script as gscript
from grass.script import core as gcore
from osgeo import ogr

os.system('clear')

# ------------------------------------------------------------
# Finding files and assign local variables

# path = "/home/rafatieppo/Dropbox/PROFISSIONAL/PROJETOS_PESQUISA/1710_SR_EVAPO/SEBAL_ALGORITHM/."
# path = "/media/rafatieppo/SSD_24gb/QGIS_SEBAL/20170904"
# path = "/home/rafatieppo/Documents/QGIS_SEBAL/20170904/"
path = "."
allfiles = os.listdir(path)

mtlfile = []
for ifile in allfiles:
    if ifile.endswith("MTL.txt"):
        print(ifile)
        mtlfile.append(ifile)

tiffile = []
for ifile in allfiles:
    if ifile.endswith((".tif", ".TIF")):
        print(ifile)
        tiffile.append(ifile)

print("------------------------------------------------------------")
print("We found", len(mtlfile), ".mtl file(s) " "and",
      len(tiffile), ".tif  file(s)")
print("------------------------------------------------------------")

print("------------------------------------------------------------")
WS_2m = float(input(
    "Please type the wind speed value in the weather station (height of the 2 m (m/s) : "))
print("------------------------------------------------------------")

print("------------------------------------------------------------")
EToi = float(input(
    "Please type the instantaneous value of reference evapotranspiration (EToi) in the weather station(time of the satellite overpass (mm) : "))
print("------------------------------------------------------------")

print("------------------------------------------------------------")
ETo = float(input(
    "Please type the daily value of reference evapotranspiration (ETo) from the weather station (mm): "))
print("------------------------------------------------------------")
# ------------------------------------------------------------
# create a PERMANENT mapset
# create a Session instance

PERMANENT = Session()
PERMANENT.open(gisdb='/home/rafatieppo/Documents/QGIS_SEBAL/20170904/',
               location='sirgas2000utm21s',
               create_opts='EPSG:31981')

# ------------------------------------------------------------
# Spectral radiance

gcore.parse_command('g.region', flags='p',
                    rast='MDT_Sebal@PERMANENT', quiet=True)

runCC = gcore.parse_command('g.list', type='raster', pattern='CC_432')
runRLo = gcore.parse_command('g.list', type='raster', pattern='RLo')

# Importing Landsat 8 images
# os arquivos tif devem estar na mesma pasta do codigo
print("------------------------------------------------------------")
print("Importing images, it can take a while")
if runCC == {}:
    for i in range(len(tiffile)):
        gcore.parse_command('r.in.gdal', input=tiffile[i],
                            output=os.path.splitext(tiffile[i])[0],
                            overwrite=True)
    print("------------------------------------------------------------")
    print('Top-of-atmosphere reflectance and temperature for Landsat8')
    gcore.parse_command('i.landsat.toar',
                        input=tiffile[0].split('_B')[0] + '_B', output='LS8_corre',
                        metfile=mtlfile, sensor='oli8',
                        overwrite=True)
    # set some common environmental variables, like:
    os.environ.update(dict(GRASS_COMPRESS_NULLS='1',
                           GRASS_COMPRESSOR='ZSTD'))
    gcore.parse_command('g.remove', type='raster',
                        pattern=tiffile[0].split('_B')[0] + '*',
                        flags='f')
    print("------------------------------------------------------------")
    print('Image compositionfor landsat 8: Red=B4 Green=B3 Blue=B2')
    gscript.run_command('i.colors.enhance', red='LS8_corre4',
                        green='LS8_corre3', blue='LS8_corre2',
                        quiet=True)
    gscript.run_command('r.composite', red='LS8_corre4',
                        green='LS8_corre3', blue='LS8_corre2',
                        output='CC_432',
                        quiet=True, overwrite=True)
    print("------------------------------------------------------------")
if runRLo == {}:
    print('NDVI calculation is running')
    NDVI = 'NDVI'
    NDVIEXP = "(LS8_corre5-LS8_corre4)/(LS8_corre5+LS8_corre4)"
    gcore.run_command('r.mapcalc', expression="{NDVI} = {NDVIEXP}".format(
        NDVI=NDVI, NDVIEXP=NDVIEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('SAVI calculation is running')
    SAVI = 'SAVI'
    LSAVI = 0.5
    SAVIEXP = "SAVI= ((LS8_corre5-LS8_corre4)/(LS8_corre5+LS8_corre4+0.5))*(1+0.5)"
    gcore.run_command('r.mapcalc', expression="{SAVI} = {SAVIEXP}".format(
        SAVI=SAVI, SAVIEXP=SAVIEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Leaf area index calculation is running')
    LAI = 'LAI'
    LAIEXP = "LAI=if(SAVI < 0.1, 0.00001,(if(0.1 < SAVI && SAVI < 0.687,-log((0.69-SAVI)/0.59)/0.91,if(SAVI > 0.687,6,0))))"
    gcore.run_command('r.mapcalc', expression="{LAI} = {LAIEXP}".format(
        LAI=LAI, LAIEXP=LAIEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Narrow band surface emissivity NBSE')
    NBSE = 'NBSE'
    NBSEEXP = "NBSE=if(LAI<3 && NDVI>0.,0.97+0.0033*LAI,if(LAI>=3 && NDVI>0.,0.98))"
    gcore.run_command('r.mapcalc', expression="{NBSE} = {NBSEEXP}".format(
        NBSE=NBSE, NBSEEXP=NBSEEXP), overwrite=True, quiet=True)
    NBSEf = 'NBSEf'
    NBSEEXPf = "NBSEf=if(NBSE == 0, 0.99, NBSE)"
    gcore.run_command('r.mapcalc', expression="{NBSEf} = {NBSEEXPf}".format(
        NBSEf=NBSEf, NBSEEXPf=NBSEEXPf), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Broad band surface emissivity BBSE')
    BBSE = 'BBSE'
    BBSEEXP = "BBSE=if(LAI<3 && NDVI>0.,0.95+0.01*LAI,if(LAI>=3 && NDVI>0.,0.98))"
    gcore.run_command('r.mapcalc', expression="{BBSE} = {BBSEEXP}".format(
        BBSE=BBSE, BBSEEXP=BBSEEXP), overwrite=True, quiet=True)
    BBSEf = 'BBSEf'
    BBSEEXPf = "BBSEf=if(BBSE == 0, 0.985, BBSE)"
    gcore.run_command('r.mapcalc', expression="{BBSEf} = {BBSEEXPf}".format(
        BBSEf=BBSEf, BBSEEXPf=BBSEEXPf), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Temperature surface TS')
    TS = 'TS'
    TSEXP = "TS=LS8_corre10/(1+((10.8*LS8_corre10)/14380)*log(NBSEf))"
    gcore.run_command('r.mapcalc', expression="{TS} = {TSEXP}".format(
        TS=TS, TSEXP=TSEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Median temperature surface K')
    TS_MEDIAN = gcore.parse_command(
        'r.univar', flags='ge', map='TS', quiet=True)['median']
    print('It is done:', TS_MEDIAN, 'K')
    print("------------------------------------------------------------")

    for line in open(mtlfile[0]):
        if 'EARTH_SUN_DISTANCE' in line:
            ESD = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_1' in line:
            RADIANCE_MAXIMUM_BAND_1 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_2' in line:
            RADIANCE_MAXIMUM_BAND_2 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_3' in line:
            RADIANCE_MAXIMUM_BAND_3 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_4' in line:
            RADIANCE_MAXIMUM_BAND_4 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_5' in line:
            RADIANCE_MAXIMUM_BAND_5 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_6' in line:
            RADIANCE_MAXIMUM_BAND_6 = float(line.split('=')[-1])
        elif 'RADIANCE_MAXIMUM_BAND_7' in line:
            RADIANCE_MAXIMUM_BAND_7 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_1' in line:
            REFLECTANCE_MAXIMUM_BAND_1 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_2' in line:
            REFLECTANCE_MAXIMUM_BAND_2 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_3' in line:
            REFLECTANCE_MAXIMUM_BAND_3 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_4' in line:
            REFLECTANCE_MAXIMUM_BAND_4 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_5' in line:
            REFLECTANCE_MAXIMUM_BAND_5 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_6' in line:
            REFLECTANCE_MAXIMUM_BAND_6 = float(line.split('=')[-1])
        elif 'REFLECTANCE_MAXIMUM_BAND_7' in line:
            REFLECTANCE_MAXIMUM_BAND_7 = float(line.split('=')[-1])
        elif 'SUN_ELEVATION' in line:
            SUN_ELEVATION = float(line.split('=')[-1])

    # SUNE by BAND
    SUNE_B1 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_1 / REFLECTANCE_MAXIMUM_BAND_1)
    SUNE_B2 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_2 / REFLECTANCE_MAXIMUM_BAND_2)
    SUNE_B3 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_3 / REFLECTANCE_MAXIMUM_BAND_3)
    SUNE_B4 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_4 / REFLECTANCE_MAXIMUM_BAND_4)
    SUNE_B5 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_5 / REFLECTANCE_MAXIMUM_BAND_5)
    SUNE_B6 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_6 / REFLECTANCE_MAXIMUM_BAND_6)
    SUNE_B7 = (math.pi * ESD * ESD) * \
        (RADIANCE_MAXIMUM_BAND_7 / REFLECTANCE_MAXIMUM_BAND_7)
    SUNE = [SUNE_B1, SUNE_B2, SUNE_B3, SUNE_B4, SUNE_B5, SUNE_B6, SUNE_B7]
    print('It is done, sun elevation by band', SUNE)
    print("------------------------------------------------------------")

    W = []
    for i in range(len(SUNE)):
        W.append(SUNE[i] / sum(SUNE))
    W1 = W[0]
    W2 = W[1]
    W3 = W[2]
    W4 = W[3]
    W5 = W[4]
    W6 = W[5]
    W7 = W[6]
    print(W)

    print("------------------------------------------------------------")
    print('Albedo at atmosphere top (AbTA)')
    AbAT = 'AbAT'
    gcore.run_command('r.mapcalc', expression="{AbAT}={LS8_corre1} * {W1} + {LS8_corre2} * {W2} + {LS8_corre3} * {W3} + {LS8_corre4} * {W4} + {LS8_corre5} * {W5} + {LS8_corre6} * {W6} + {LS8_corre7} * {W7}".format(
        AbAT=AbAT,
        LS8_corre1='LS8_corre1',
        LS8_corre2='LS8_corre2',
        LS8_corre3='LS8_corre3',
        LS8_corre4='LS8_corre4',
        LS8_corre5='LS8_corre5',
        LS8_corre6='LS8_corre6',
        LS8_corre7='LS8_corre7',
        W1=W1,
        W2=W2,
        W3=W3,
        W4=W4,
        W5=W5,
        W6=W6,
        W7=W7),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Air Shortwave transmissivity (ASW)')
    ASW = 'ASW'
    ASWEXP = "ASW=0.75+0.00002*MDT_Sebal"
    gcore.run_command('r.mapcalc', expression="{ASW} = {ASWEXP}".format(
        ASW=ASW, ASWEXP=ASWEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Albedo surface (AS)')
    AS = 'AS'
    ASEXP = "AS=(AbAT-0.03)/(ASW^2)"
    gcore.run_command('r.mapcalc', expression="{AS} = {ASEXP}".format(
        AS=AS, ASEXP=ASEXP), overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Incoming shortwave radiation (ISR W/m2)')
    ISR = 'ISR'
    ISRC1 = 1367
    ISRC2 = 90
    ISRC3 = 1
    gcore.run_command('r.mapcalc', expression="{ISR}={ISRC1} * cos({ISRC2} - {SUN_ELEVATION}) * ({ISRC3} / {ESD}^2) * ASW".format(
        ISR=ISR,
        ISRC1=ISRC1,
        ISRC2=ISRC2,
        ISRC3=ISRC3,
        SUN_ELEVATION=SUN_ELEVATION,
        ESD=ESD),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Outgoing longwave radiation (OLR W/m2)')
    OLR = 'OLR'
    OLRC1 = 5.67e-8
    gcore.run_command('r.mapcalc', expression="{OLR}={BBSEf} * {OLRC1} * {TS}^4".format(
        OLR=OLR,
        BBSEf='BBSEf',
        OLRC1=OLRC1,
        TS='TS'),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

print('Working on cold pixel mask')
TS_MEDIAN = gcore.parse_command('r.univar',
                                flags='ge', map='TS', quiet=True)['median']
COLDPIX = 'COLDPIX'
COLDPIXC1 = 0.4
gcore.run_command('r.mapcalc', expression="COLDPIX=if({NDVI}>{COLDPIXC1} && {TS}<{TS_MEDIAN},{TS},null())".format(
    NDVI='NDVI',
    COLDPIX='COLDPIX',
    COLDPIXC1=COLDPIXC1,
    TS='TS',
    TS_MEDIAN=TS_MEDIAN),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Choose the cold pixel coordinates in irrigation areas.')
COLDPIX_XY = str(input('Type the coordinates (East,North): ')).strip('()')
print('Coordinates', COLDPIX_XY)

print('Getting cold pixel value for coordinates')
COLDPIX_TSz = gscript.parse_command('r.what', map='TS', coordinates=COLDPIX_XY)
COLDPIX_TS = list(dict(COLDPIX_TSz).keys())
COLDPIX_TS = float(COLDPIX_TS[0].split('||')[1])
print('Cold pixel value is', COLDPIX_TS, 'K')

# create a file to write the point
a = COLDPIX_XY
tmpf = open('tmp_coldpoint', 'w+')
tmpf.write(a)
tmpf.close()

gscript.write_command('v.in.ascii', input='tmp_coldpoint', output='COLDPOINT',
                      separator=',',
                      stdin='',
                      overwrite='true', quiet='true')

print ('Incoming radiation longwave (IRL - W/m2)')
IRL = 'IRL'
IRLC1 = 0.85
IRLC2 = 0.09
IRLC3 = 5.67e-8
gcore.run_command('r.mapcalc', expression="{IRL}={IRLC1} * ((-log({ASW}))^{IRLC2})*{IRLC3}*{COLDPIX_TS}^4".format(
    IRL=IRL,
    ASW='ASW',
    IRLC1=IRLC1,
    IRLC2=IRLC2,
    IRLC3=IRLC3,
    COLDPIX_TS=COLDPIX_TS),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Net radiation flux (Rn - W/m2')
Rn = 'Rn'
RnC1 = 1
gcore.run_command('r.mapcalc', expression="{Rn}=({RnC1}-{AS})*{ISR}+{IRL}-{OLR}-({RnC1}-{BBSEf})*{IRL}".format(
    Rn=Rn,
    RnC1=RnC1,
    AS='AS',
    ISR='ISR',
    IRL='IRL',
    OLR='OLR',
    BBSEf='BBSEf'),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Soil heat flux (G - W/m2)')
G_Rn = 'G_Rn'
G_RnC1 = 0
G_RnC2 = 0.5
G_RnC3 = 273.15
G_RnC4 = 0.0038
G_RnC5 = 0.0074
G_RnC6 = 1
G_RnC7 = 0.98
gcore.run_command('r.mapcalc', expression="{G_Rn}=if({NDVI}<{G_RnC1},{G_RnC2},(({TS}-{G_RnC3})/{AS})*({G_RnC4}*{AS}+{G_RnC5}*{AS}^2)*({G_RnC6}-{G_RnC7}*{NDVI}^4))".format(
    G_Rn=G_Rn,
    TS='TS',
    AS='AS',
    G_RnC1=G_RnC1,
    G_RnC2=G_RnC2,
    G_RnC3=G_RnC3,
    G_RnC4=G_RnC4,
    G_RnC5=G_RnC5,
    G_RnC6=G_RnC6,
    G_RnC7=G_RnC7,
    NDVI='NDVI'),
    overwrite=True, quiet=True)

G = 'G'
gcore.run_command('r.mapcalc', expression="{G}={G_Rn}*{Rn}".format(
    G=G,
    G_Rn='G_Rn',
    Rn='Rn'),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Working on hot pixel mask')
HOTPIX = 'HOTPIX'
HOTPIXC1 = 0.18
HOTPIXC2 = 0.3
gcore.run_command('r.mapcalc', expression="HOTPIX=if({SAVI}>{HOTPIXC1} && {SAVI}<{HOTPIXC2}, {TS},null())".format(
    SAVI='SAVI',
    TS='TS',
    HOTPIXC1=HOTPIXC1,
    HOTPIXC2=HOTPIXC2),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Choose the hot pixel coordinates in naked areas.')
HOTPIX_XY = str(input('Type the coordinates (East,North): ')).strip('()')
print('Coordinates', HOTPIX_XY)
print('Getting hot pixel value for coordinates')
HOTPIX_TSz = gscript.parse_command('r.what', map='TS', coordinates=HOTPIX_XY)
HOTPIX_TS = list(dict(HOTPIX_TSz).keys())
HOTPIX_TS = float(HOTPIX_TS[0].split('||')[1])
print('Hot pixel value is', HOTPIX_TS, 'K')
# create a file to write the point
b = HOTPIX_XY
tmpf = open('tmp_hotpoint', 'w+')
tmpf.write(b)
tmpf.close()
gscript.write_command('v.in.ascii', input='tmp_hotpoint', output='HOTPOINT',
                      separator=',',
                      stdin='',
                      overwrite='true', quiet='true')

print('Friction velocity (u*) for weather station - (m/s)')
h = 0.15
Zom = 0.123 * h
u_ast = 0.41 * WS_2m / (math.log(2 / Zom))
u_200m = u_ast * (math.log(200 / Zom)) / 0.41
print('It is done')
print("------------------------------------------------------------")

print('Friction velocity', u_ast, '(m/s)')
print("------------------------------------------------------------")

print('Roughness momentum length map (Z0map  (m))')
RMLM0 = 'RMLM0'
RMLM0C1 = -5.809
RMLM0C2 = 5.62
gcore.run_command('r.mapcalc', expression="RMLM0=exp({RMLM0C1}+{RMLM0C2}*SAVI)".format(
    RMLM0='RMLM0',
    SAVI='SAVI',
    RMLM0C1=RMLM0C1,
    RMLM0C2=RMLM0C2),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Friction velocity map (u*map (m/s))')
FVMu = 'FVMu'
FVMuC1 = 0.41
FVMuC2 = 200
gcore.run_command('r.mapcalc', expression="FVMu={FVMuC1}*{u_200m}/log({FVMuC2}/{RMLM0})".format(
    FVMu='FVMu',
    u_200m=u_200m,
    FVMuC1=FVMuC1,
    FVMuC2=FVMuC2,
    RMLM0='RMLM0'),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Heat transport map in terms of neutral stability for Aerodynamic resistance (RAH (s/m))')
RAH = 'RAH'
RAHC1 = 2
RAHC2 = 0.1
RAHC3 = 0.41
gcore.run_command('r.mapcalc', expression="RAH=log({RAHC1}/{RAHC2})/({RMLM0}*{RAHC3})".format(
    RAH='RAH',
    RAHC1=RAHC1,
    RAHC2=RAHC2,
    RAHC3=RAHC3,
    RMLM0='RMLM0'),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

HOTPT_Gz = gscript.parse_command('r.what', map='G', coordinates=HOTPIX_XY)
HOTPT_G = list(dict(HOTPT_Gz).keys())
HOTPT_G = float(HOTPT_G[0].split('||')[1])

HOTPT_RAHz = gscript.parse_command('r.what', map='RAH', coordinates=HOTPIX_XY)
HOTPT_RAH = list(dict(HOTPT_RAHz).keys())
HOTPT_RAH = float(HOTPT_RAH[0].split('||')[1])

HOTPT_Rnz = gscript.parse_command('r.what', map='Rn', coordinates=HOTPIX_XY)
HOTPT_Rn = list(dict(HOTPT_Rnz).keys())
HOTPT_Rn = float(HOTPT_Rn[0].split('||')[1])


print ('Fitting aerodynamic resistance, it can take time')
hotptrah_i = 0
i = 1
while (abs(hotptrah_i - HOTPT_RAH) > 0.00001):
    print('******** Interaction number:', i)
    i = i + 1
    hotptrah_i = HOTPT_RAH
    print('Equation coefficents estimate >> dT = a.Ts + b')
    a = (HOTPT_Rn - HOTPT_G) * hotptrah_i / \
        ((HOTPIX_TS - COLDPIX_TS) * 1.25 * 1004)
    b = -a * COLDPIX_TS
    print('a:', a, 'b:', b)
    print('Working on dT map (K)')
    dT = 'dT'
    gcore.run_command('r.mapcalc', expression="dT={a}*{TS}+{b}".format(
        dT='dT',
        a=a,
        b=b,
        TS='TS'),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Working on sensible heat flux (H (W/m2)')
    H = 'H'
    HC1 = 1.25
    HC2 = 1004
    gcore.run_command('r.mapcalc', expression="H=({dT}/{RAH})*{HC1}*{HC2}".format(
        H='H',
        dT='dT',
        RAH='RAH',
        HC1=HC1,
        HC2=HC2),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Working on Monin-Obukhov length map (L (m))')
    L = 'L'
    LC1 = 1.25
    LC2 = 1004
    LC3 = 0.41
    LC4 = 9.81
    gcore.run_command('r.mapcalc', expression="L=-({LC1}*{LC2}*{TS}*{FVMu}^3)/({LC3}*{LC4}*{H})".format(
        L='L',
        TS='TS',
        RAH='RAH',
        FVMu='FVMu',
        H='H',
        LC1=LC1,
        LC2=LC2,
        LC3=LC3,
        LC4=LC4),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Working on atmospheric stability correction (L200m, L2m, L01m)')
    L200m = 'L200m'
    L200mC1 = 0
    L200mC2 = 2
    L200mC3 = 1
    L200mC4 = 16
    L200mC5 = 200
    L200mC6 = 0.25
    L200mC7 = 0.5
    L200mC8 = 3.14159265
    L200mC9 = -5
    gcore.run_command('r.mapcalc', expression="L200m=if({L}<{L200mC1},{L200mC2}*log(({L200mC3}+({L200mC3}-{L200mC4}*({L200mC5}/{L}))^{L200mC6})/{L200mC2})+log(({L200mC3}+({L200mC3}-{L200mC4}*({L200mC5}/{L}))^{L200mC7})/{L200mC2})-{L200mC2}*atan(({L200mC3}-{L200mC4}*({L200mC5}/{L}))^{L200mC6})+{L200mC7}*{L200mC8},if({L}>{L200mC1},{L200mC9}*({L200mC2}/{L}),{L200mC1}))".format(
        L200m='L200m',
        L='L',
        L200mC1=L200mC1,
        L200mC2=L200mC2,
        L200mC3=L200mC3,
        L200mC4=L200mC4,
        L200mC5=L200mC5,
        L200mC6=L200mC6,
        L200mC7=L200mC7,
        L200mC8=L200mC8,
        L200mC9=L200mC9),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    L2m = 'L2m'
    L2mC1 = 0
    L2mC2 = 2
    L2mC3 = 1
    L2mC4 = 16
    L2mC5 = 0.5
    L2mC6 = -5
    gcore.run_command('r.mapcalc', expression="L2m=if({L}<{L2mC1},{L2mC2}*log(({L2mC3}+({L2mC3}-{L2mC4}*({L2mC2}/{L}))^{L2mC5})/{L2mC2}),if({L}>{L2mC1},{L2mC6}*({L2mC2}/{L}),{L2mC1}))".format(
        L2m='L2m',
        L='L',
        L2mC1=L2mC1,
        L2mC2=L2mC2,
        L2mC3=L2mC3,
        L2mC4=L2mC4,
        L2mC5=L2mC5,
        L2mC6=L2mC6),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    L1m = 'L1m'
    L1mC1 = 0
    L1mC2 = 2
    L1mC3 = 1
    L1mC4 = 16
    L1mC5 = 0.1
    L1mC6 = 0.5
    L1mC7 = -5
    gcore.run_command('r.mapcalc', expression="L1m=if({L}<{L1mC1},{L1mC2}*log(({L1mC3}+({L1mC3}-{L1mC4}*({L1mC5}/{L}))^{L1mC6})/{L1mC2}),if({L}>{L1mC1},{L1mC7}*({L1mC5}/{L}),{L1mC1}))".format(
        L1m='L1m',
        L='L',
        L1mC1=L1mC1,
        L1mC2=L1mC2,
        L1mC3=L1mC3,
        L1mC4=L1mC4,
        L1mC5=L1mC5,
        L1mC6=L1mC6,
        L1mC7=L1mC7),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Working on corrected friction velocity map (u*map (m/s))')
    FVMu = 'FVMu'
    FVMuC1 = 0.41
    FVMuC2 = 200
    gcore.run_command('r.mapcalc', expression="FVMu={FVMuC1}*{u_200m}/(log({FVMuC2}/{RMLM0})-{L200m})".format(
        FVMu='FVMu',
        u_200m=u_200m,
        RMLM0='RMLM0',
        L200m='L200m',
        FVMuC1=FVMuC1,
        FVMuC2=FVMuC2),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    print('Working on corrected aerodynamic resistance to heat transport (RAH (s/m))')
    RAH = 'RAH'
    RAHC1 = 2
    RAHC2 = 0.1
    RAHC3 = 0.41
    gcore.run_command('r.mapcalc', expression="RAH=(log({RAHC1}/{RAHC2})-{L2m}+{L1m})/({FVMu}*{RAHC3})".format(
        RAH='RAH',
        L1m='L1m',
        L2m='L2m',
        FVMu='FVMu',
        RAHC1=RAHC1,
        RAHC2=RAHC2,
        RAHC3=RAHC3),
        overwrite=True, quiet=True)
    print('It is done')
    print("------------------------------------------------------------")

    HOTPT_RAHz = gscript.parse_command(
        'r.what', map='RAH', coordinates=HOTPIX_XY)
    HOTPT_RAH = list(dict(HOTPT_RAHz).keys())
    HOTPT_RAH = float(HOTPT_RAH[0].split('||')[1])

HOTPT_Hz = gscript.parse_command('r.what', map='H', coordinates=HOTPIX_XY)
HOTPT_H = list(dict(HOTPT_Hz).keys())
HOTPT_H = float(HOTPT_H[0].split('||')[1])

HOTPT_dTz = gscript.parse_command('r.what', map='dT', coordinates=HOTPIX_XY)
HOTPT_dT = list(dict(HOTPT_dTz).keys())
HOTPT_dT = float(HOTPT_dT[0].split('||')[1])

print('Hot pixel results, verify if HOTPT_Rn - HOTPT_G = HOTPT_H')
print('Sensible heat flux (HOTPT_H):', HOTPT_H)
print('Heat transport (HOTPT_RAH):', HOTPT_RAH)
print('Soil heat flux (HOTPT_G):', HOTPT_G)
print('Net radiation flux (HOTPT_Rn):', HOTPT_Rn, 'dT:', HOTPT_dT)

print('Working on latent heat flux (LHF (W/m2))')
LHF = 'LHF'
gcore.run_command('r.mapcalc', expression="LHF={Rn}-{G}-{H}".format(
    LHF='LHF',
    Rn='Rn',
    G='G',
    H='H'),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Working on instantaneous evapotranspiration (ETi (mm/h))')
ETi = 'ETi'
ETiC1 = 3600
ETiC2 = 2.45
ETiC3 = 10**6
ETiC4 = 0
gcore.run_command('r.mapcalc', expression="ETi=if({ETiC1}*({LHF}/({ETiC2}*{ETiC3}))<{ETiC4},{ETiC4},{ETiC1}*({LHF}/({ETiC2}*{ETiC3})))".format(
    ETi='ETi',
    LHF='LHF',
    ETiC1=ETiC1,
    ETiC2=ETiC2,
    ETiC3=ETiC3,
    ETiC4=ETiC4),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Working on  reference evapotranspiration fraction (ETof)')
ETof = 'ETof'
gcore.run_command('r.mapcalc', expression="ETof={ETi}/{EToi}".format(
    ETof='ETof',
    ETi='ETi',
    EToi=EToi),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")

print('Working on daily evapotranspiration (ETday (mm/dia)')
ETday = 'ETday'
gcore.run_command('r.mapcalc', expression="{ETday}={ETof}*{ETo}".format(
    ETday='ETday',
    ETof='ETof',
    ETo=ETo),
    overwrite=True, quiet=True)
print('It is done')
print("------------------------------------------------------------")
print("@geoclimamt")
# ------------------------------------------------------------
