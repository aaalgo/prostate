#!/usr/bin/env python3
import sys
import logging
import cv2
from gallery import Gallery
from PX import *

image_ID = 0

# dump image from a row of the image csv
# into html table cel
def dump_image (html, row, root):

    i, j, k = [int(x) for x in row['ijk'].split(' ')]
    print("TL", row['TopLevel'])
    print("ijk", i,j,k)
    sys.stdout.flush()

    try:
        ProxID = row['ProxID']
        SerDescr = row['DCMSerDescr']
        SerNum = row['DCMSerNum']
        dcm_dir = dcm_list[ProxID][SerDescr][SerNum]
    except:
        logging.exception('%s %s %d not found' % (ProxID, SerDescr, SerNum))
        return
    try:
        volume = DicomVolume(dcm_dir)
    except:
        logging.exception(dcm_dir)
        return

    print("shape", volume.images.shape)
    L, H, W = volume.images.shape
    try:
        assert i >= 0 and i < W
        assert j >= 0 and j < H
        print("SLICE", k)
        #print("I", i)
        #i = slices[sli]
        assert k >= 0 and k < L
        dcm = volume.dcms[k].dcm
        sanity_check_coord_dicom(row, dcm)
        
        image = dcm.pixel_array.astype(np.float32)
        #print(np.max(image))
        #image = cv2.normalize(image, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        image *= 255/(np.max(image) * 0.8)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        print('MA', np.max(image))
        #image[row, col, 1] = 255
        #image[col, row, 2] = 255
        cv2.circle(image, (i, j), 15, (0, 255, 0))
    except:
        logging.exception('xxx')
        return
    # now we have the image
    global image_ID
    image_fname = '%d.jpg' % image_ID
    image_ID += 1
    html.write('<table><tr><td><img src="%s"></img></td></tr><tr><td>%s</td></tr></table>' %
                    (image_fname, SerDescr))
    cv2.imwrite(os.path.join(root, image_fname), image)
    pass

def dump_images (html, images, root):
    html.write('<td>')
    for row in images:
        dump_image(html, row, root) 
    html.write('</td>')

def dump_findings (path, findings):
    try:
        os.mkdir(path)
    except:
        pass
    with open(os.path.join(path, 'index.html'), 'w') as html:
        html.write('<html><body><table border="1"><tr><th>ProxID</th><th>fid</th><th>zone</th><th>T2_cor</th><th>T2_sag</th><th>T2_tra</th><th>PD</th><th>DW</th><th>Others</th></tr>\n')
        for patient in findings:
            for finding in patient:
                html.write('<tr><td>%s</td><td>%d</td><td>%s</td>' % (finding.ProxID, finding.fid, finding.zone))
                dump_images(html, finding.views['T2_cor'], path)
                dump_images(html, finding.views['T2_sag'], path)
                dump_images(html, finding.views['T2_tra'], path)
                dump_images(html, finding.views['PD'], path)
                dump_images(html, finding.views['DW'], path)
                dump_images(html, finding.views['others'], path)
                html.write('</tr>\n')
                pass
            pass
        html.write('</table></body></html>\n')
        pass
    pass

findings = load_train_csv()
dump_findings('pos', [x for x in findings if x[0].ClinSig])
dump_findings('neg', [x for x in findings if not x[0].ClinSig])

