#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Akshat Singhal <akshat.singhal014@gmail.com>
# Junior Research Fellow
# Distributed under terms of the IUCAA, Pune
# Revised version with minor correction
# Aug 2016


"""
This program coadds CRTS images with same field name 
from the IUCAA repository. Due to restrictions on ssh
from repository server to the perseus server, hence
some alternative methods and some precautions are used
in the code to copy images fom IUCAA repository server 
to the perseus server. In the essence
1) Given a Filed-id (e.g N29041) 
from scp to rename and swarp.
It requires swarp_conf_varun.swarp in $HOME directory
and Mask_S.fits in this directory.
2) Since it is possible that images corresponding to a field-ID
has images which are scattered at different positions on the sky
the code discards any image which is more than 1.5 deg apart from
the median image.
3) This new feature was added as the final co-add for some images
were huge and occupied a lot of disk space.

run on perseus as:

for i in {1..10}; do bsub -e err$i -o out$i
python -W ignore bsub_CRTS.py $(expr $i \* 10); done

"""

import numpy as np
import os
import sys
import glob
import time
from astropy.io import fits
from astropy.wcs import WCS
import datetime
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u


try:
    index = int(sys.argv[1])
except:
    index = 0

print index
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print st
count = index - 1

ran = np.random.random()*2
time.sleep(ran)  # so that multiple ssh does not clash


def clean(add):
    """Makes a new directory if it does not exist
    or removes its all contents

    :add: Name of directory
    :returns: Empty directory

    """

    for iter in [1, 2]:
        x = -1
        try:
            if os.path.exists(str(add)):
                x = os.system('rm -rf '+str(add)+'/*')
            else:
                x = os.system('mkdir '+str(add))
            if x == 0:
                break
        except:
            pass

    return


server = "project@14.139.108.116"  # passwordless ssh 
disk_dump = "emgw@192.168.11.83:/disk2/crts/"  # passwordless ssh


def comm(command, itern=2, rand=10):
    """It is an iterative loop which
    avoids crash exception and breaks only
    when executed correctly

    :command: string of command for shell
    :itern: Number iterantion
    :returns: value of os.system(command)
:
    """
    count_itr = 0
    ran = np.random.random()*rand
    time.sleep(ran)
    for itrn in np.arange(itern):
        count_itr += 1
        try:
            check = os.system(command)
        except:
            check = 1
        if check == 0:
            break

    return check, count_itr


def get_Images(name0, num0):
    """TODO: Gets images of required ID from CRTS import server
    to local directory with the same name.
    1) It first copies all the files i CRTS project Home directory,
    2) SCP them to local directory
    3) Remove the same in CRTS home directory.
    4) Saves LOG files

    It would have been easier and better to directly SCP it from list,
    but we can not scp from CRTS to perseus.

    :name0: Name of ID
    #:num0: Actual number of images
    ##  :ind: index; keeps track of iteration
    :num0: Expected number of files based on list of all CRTS images
    :returns: All .H files in local directory

    """

    # SSH sends a command to CRTS server to copy all required files
    # to its home directory
    ts00 = time.time()
    command01 = "ssh {0} 'cat CRTS_list.txt |".format(server)
    command01 += "grep _{0}_ |xargs -I % cp -r % ~'".format(name0)
    check01, itr = comm(command01, 5, 10)
    ts01 = time.time()
    tt = np.around((ts01-ts00), decimals=2)
    # check01 == 0 if all goes well
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    if check01 == 0:

        H01 = open('Sc_SSH_log.txt', 'a')
        H01.write("SSH {0} TTT= {1} s i= {2} {3}\n".format(name0, tt, itr, st))
        H01.close()
    else:
        E01 = open("Sc_SSH_error.txt", 'a')
        E01.write("ConnectionError {0} TTT= {1} s {2}\n".format(name0, tt, st))
        E01.close()

    # SCP the same files to a local directory with same name
    command02 = "scp {1}:~/*{0}*.H ./{0}/".format(name0, server)
    ts10 = time.time()
    check02, itr = comm(command02, 5, 10)
    ts11 = time.time()
    tt = np.around((ts11-ts10), decimals=2)
    im_file = glob.glob("{0}/*.H".format(name0))
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    # Check of how many files were copied compare to how many were expected
    if len(im_file) == num0:
        H02 = open('Sc_SCP_log.txt', 'a')
        H02.write("SCP {0} TTT= {1} s i= {2} {3}\n".format(name0, tt, itr, st))
        H02.close()
    else:
        E02 = open("Sc_SCP_less.txt", 'a')
        app_text = "Received files {0}/{1} ".format((num0-len(im_file)), num0)
        app_text += "image(s) less for {0} {1}\n".format(name0, st)
        E02.write(app_text)
        E02.close()

    # SSH delete command to server, to remove all copied file from ~/
    ts20 = time.time()
    command025 = "ssh {1} 'rm -rf *{0}*H'".format(name0, server)
    check025, itr = comm(command025, 10, 15)
    ts21 = time.time()
    tt = np.around((ts21-ts20), decimals=2)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    if check025 == 0:
        H025 = open('Sc_RM_log.txt', 'a')
        H025.write("RM {0} TTT= {1} s i= {2} {3}\n".format(name0, tt, itr, st))
        H025.close()
    else:
        E025 = open('Sc_RM_error.txt', 'a')
        E025.write("RM error {0} TTT = {1} s {2}\n".format(name0, tt, st))
        E025.close()

    return


def hdecomp(name0, num0):
    """TODO: H-decompress all the .H files in given dir.

    :name0: Name of directory
    :num
    :returns: decompresses and removes the original

    """

    # Run hdecompress in local directory for all *.H files
    ts30 = time.time()
    command03 = "hdecompress -r {0}/*H".format(name0)
    check03, iter = comm(command03, 2)
    ts31 = time.time()
    tt = np.around((ts31-ts30), decimals=2)
    im_file = glob.glob("{0}/*.H".format(name0))
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    # check == 0 if every thing goes well
    if len(im_file) == 0:
            H03 = open('Sc_HD_log.txt', 'a')
            H03.write("HD {0} T= {1} i= {2} {3}\n".format(name0, tt, iter, st))
    else:
        count = num0 - len(im_file)
        E03 = open("Sc_Hdecompr_error.txt", 'a')
        E03.write("Herr {0} for {2} T {1} {3}\n".format(name0, tt, count, st))

    return


def a2c(img, hduid=0):
    """TODO: Computes Corners of a FITS image.

    :img: Name/Address of Image
    :returns: Coordinates of corner

    """

    # hdu, w are astropy objects of image
    hdu = fits.open(img)
    w = WCS(hdu[hduid].header)
    # r,c are number of rows, cloumns of image
    # where  Row == Dec == Y == NAXIS2,
    # and column == RA  == X == NAXIS1
    r, c = np.shape(hdu[hduid].data)
    # radec = w.wcs_pix2world(x, y)
    [[r0, d0], [r1, d1], [r2, d2], [r3, d3], [r4, d4]] = [
                                                w.wcs_pix2world(0, 0, 1),
                                                w.wcs_pix2world(0, r, 1),
                                                w.wcs_pix2world(c, r, 1),
                                                w.wcs_pix2world(c, 0, 1),
                                                [hdu[0].header['CENTRA'],
                                                    hdu[0].header['CENTDEC']]]
    Co = [[r0, d0], [r1, d1], [r2, d2], [r3, d3], [r4, d4]]
    Co = np.around(np.array(Co), decimals=4)
    # Above step is not required, but just in case we need to print them
    # it will look clean:w

    return Co.tolist()


def Extras(name0):
    """TODO:
    1) Renames all the files from *arch to *fits from given directory.
    2) Makes default.swarp (parameter file)

    :name0: Name of directory
    :returns: TODO

    """

    command04 = "for file in {0}/*arch; ".format(name0)
    command04 += "do mv ${file} ${file/arch/fits}; done"
    comm(command04, 2)

    command05 = "cp /data1/visitor/cakshat/swarp_conf_varun.swarp "
    command05 += " {0}/".format(name0)
    comm(command05, 2)


def Input_file(dir, num0):
    """Makes Input.txt file for the SWarp
    of a given directory.
    That means, only those images which have valid WCS
    goes into Input.txt

    :dir: Name of directory
    :returns: Input.txt and Failed_wcs.txt in the directory

    """
    I = open("{0}/Input.txt".format(dir), 'w')
    i_list = []
    wcs = []
    # J = open("{0}/Failed_wcs.txt".format(dir), 'w')
    i_c = 0  # Input_count
    m_f = 0  # Mask_Fail
    p_w = 0  # Poor WCS
    f_w = 0  # Failed WCS --- different than Poor WCS

    files = glob.glob("{0}/*fits".format(dir))
    for fi in files:

        try:
            im = fits.open(fi)
            da = im[0].data
            x1, x2 = np.shape(da)
            Cord = a2c(fi)
            if (float(Cord[2][0]) <= 360 and float(Cord[2][1]) <= 90 and
                    x1 == 4096 and x2 == 4110):
                fi_in = os.path.basename(fi)
                i_c += 1
                i_list += [fi_in]
                wcs += [Cord[-1]]
            elif(x1 != 4096 or x2 != 4110):
                fi_in = os.path.basename(fi)
                m_f += 1
                L = open("{0}/Failed_Mask.txt".format(dir), 'a')
                L.write(fi_in+'\n')
                L.close()
            else:
                fi_in = os.path.basename(fi)
                p_w += 1
                J = open("{0}/Failed_wcs.txt".format(dir), 'a')
                J.write(fi_in+'\n')
                J.close()

        except:
            fi_in = os.path.basename(fi)
            f_w += 1
            J = open("{0}/Failed_wcs.txt".format(dir), 'a')
            J.write(fi_in+'\n')
            J.close()

    wcs = np.array(wcs)
    i_list = np.array(i_list)
    m_rd = wcs[np.argsort(wcs[:, 0])][(len(wcs)/2)]
    scd = Table()
    scd['name'] = i_list
    scd['ra'] = wcs[:, 0]
    scd['dec'] = wcs[:, 1]
    c1 = SkyCoord(m_rd[0], m_rd[1], unit=u.deg)
    c2 = SkyCoord(wcs[:, 0], wcs[:, 1], unit=u.deg)
    scd['sep'] = c1.separation(c2)
    print 'Full Table'
    print scd
    scd.write('{0}/Scatter_Table.tbl'.format(dir), format='ipac')
    tab = scd[scd['sep'] <= 1.5]
    print 'Truncated Table'
    print tab
    tab.write('{0}/Scatless_Table.tbl'.format(dir), format='ipac')
    for nl in tab['name']:
        I = open("{0}/Input.txt".format(dir), 'a')
        I.write(nl+'\n')
        I.close()

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    JJ = open("scat_data.txt", 'a')
    app_text = "{0} has {1} , {2} , {3} , ".format(dir, len(tab), i_c, m_f)
    app_text += "{0} , {1} OutOf {2} TotalImages ".format(p_w, f_w, num0)
    app_text += "are LessScat GoodWCS FailMask PoorWCS FailWCS "
    app_text += "{0}\n".format(st)
    JJ.write(app_text)

    JJ.close

    if (num0 - i_c > 0):
        w_e = num0 - i_c
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        WCS_E = open("Sc_WCS_error.txt", 'a')
        app_text = "{0} has {1} images out of ".format(dir, w_e)
        app_text += "{0} were not Coaddable {1} \n".format(len(files), st)
        WCS_E.write(app_text)
        WCS_E.close()

    return i_c, tab


clip_amp = 0.3 #Default value in config file
clip_sig = 4.0 #Default value in config file
sc = np.loadtxt('Sc_list.txt', dtype=np.str)
cr = np.loadtxt('/data1/visitor/cakshat/CRTS_id_num.txt', dtype=np.str)
da = np.array([[i, cr[np.where(cr == i)[0]][0][1]] for i in sc])
n_n = da

count = 0

end = np.min((index + 60, len(n_n)))

#Each job in a cluster co-adds ~60 fields one by one
for name, num in n_n[index:end]:

    num = int(num)
    i_time = time.time()
    count += 1

    clean(name)

    print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    print count, name, num
    print 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'

    get_Images(name, num)  # Get Images from CRTS import server
    hdecomp(name, num)  # Hdecompress them
    Extras(name)  # Rename file extension and make default.swarp

    # Make Input.txt
    count06 = Input_file(name, num)

    # Finally the COADD
    command07 = "cd {0}/; swarp @Input.txt ".format(name)
    command07 += "-c swarp_conf_varun.swarp "
    command07 += "-COMBINE_TYPE CLIPPED "
    # -COMBINE_TYPE can have following values
    # MEDIAN, AVERAGE, MIN, MAX, WEIGHTED, CLIPPED,
    # CHI-OLD, CHI-MODE, CHI-MEAN, SUM,
    # WEIGHTED_WEIGHT, MEDIAN_WEIGHT,
    # AND, NAND, OR or NOR

    # command07+= "-CLIP_AMPFRAC {0} -CLIP_SIGMA {1}".format(clip_amp,clip_sig)
    command07 += " -SUBTRACT_BACK Y "
    command07 += "-DELETE_TMPFILES Y -IMAGEOUT_NAME "

    filename = "{0}_clip_mask_SBG_Y".format(name)

    command07 += "{0}.fits -WEIGHTOUT_NAME {0}.weight.fits ".format(filename)
    command07 += "-WEIGHT_IMAGE ../Mask_S.fits -WEIGHT_TYPE MAP_WEIGHT "
    command07 += "-VERBOSE_TYPE NORMAL  -WEIGHT_SUFFIX .weight.fits"
    # -VERBOSE_TYPE can have following values
    # QUIET, LOG, NORMAL, or FULL

    ci_time = time.time()
    check07 = os.system(command07)
    cf_time = time.time()

    command08 = "rm -rf {0}/*_{0}_*fits".format(name)
    check08 = os.system(command08)

    f_time = time.time()
    coadd = np.around((cf_time - ci_time), decimals=2)
    taken = np.around((f_time - i_time), decimals=2)

    if check07 == 0:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        G07 = open("Sc_Coadd_LOG.txt", 'a')
        app_text = "{0} coadded CT {1} TTT {2} for ".format(name, coadd, taken)
        app_text += "{0}/ {1} images {2}\n".format(count06[0], num, st)
        G07.write(app_text)
        G07.close()
    else:
        E07 = open("Sc_Coadd_FAIL.txt", 'a')
        E07.write("{0} FAIL CT {1} T {2} {3}\n".format(name, coadd, taken, st))
        E07.close()

    im = glob.glob("{0}/*fits".format(name))
    try:
        size = os.path.getsize(im[0])/1e9  # size in GB
    except:
        size = 0
    if size > 3:
        ts90 = time.time()
        command09 = "rm -rvf {0}/*fits".format(name)
        # command09 = "ls {0}/*fits".format(name)
        check09, itr = comm(command09, 3)
        ts91 = time.time()
        tt = np.around((ts91-ts90), decimals=2)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        if check09 == 0:
            E09 = open("Sc_Scatter.txt", 'a')
            app_text = "Sc {0} TTT= {1} s Size= {2} ".format(name, tt, size)
            app_text += "{0}\n".format(st)
            E09.write(app_text)
            E09.close()
            fname = "{0}/Scatter.txt".format(name)
            E99 = open(fname, 'a+')
            app_text = "Sc {0} TTT= {1} s Size= {2} G ".format(name, tt, size)
            app_text += "{0}\n".format(st)
            E99.write(app_text)
            E99.close()
        else:
            E09 = open("Sc_Scatter_del_err.txt", 'a')
            E09.write("Scatter Error {0} TTT= {1} {2}\n".format(name, tt, st))
            E09.close()
            fname = "{0}/Scatter_del_err.txt".format(name)
            E95 = open(fname, 'a+')
            E95.write("Scatter Error {0} TTT= {1} {2}\n".format(name, tt, st))
            E95.close()
    else:
        pass

    ts100 = time.time()
    command10 = "scp -r {0} *txt {1}".format(name, disk_dump)
    check10, itr = comm(command10, 3)
    ts101 = time.time()
    tt = np.around((ts101-ts100), decimals=2)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    if check10 == 0:
        H10 = open('Sc_DD_log.txt', 'a')
        H10.write("DISK {0} TTT= {1} s i= {2} {3}\n".format(name, tt, itr, st))
        H10.close()
    else:
        E10 = open("Sc_DD_error.txt", 'a')
        E10.write("DiskDump error for {0} TTT= {1} {2}\n".format(name, tt, st))
        E10.close()

    ts110 = time.time()
    command11 = "rm -rvf {0}".format(name)
    check11, itr = comm(command11, 3)
    ts111 = time.time()
    tt = np.around((ts111-ts110), decimals=2)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st

    if check11 == 0:
        H10 = open('Sc_PRM_log.txt', 'a')
        H10.write("Del {0} TTT= {1} s i= {2} {3}\n".format(name, tt, itr, st))
        H10.close()
    else:
        E10 = open("Sc_PRM_error.txt", 'a')
        E10.write("Delete error for {0} TTT = {1} {2}\n".format(name, tt, st))
        E10.close()
