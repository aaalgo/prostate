#!/usr/bin/env python3 
import cv2 
import numpy as np 
import os
from skimage import measure,color,morphology 
import scipy
from glob import glob
import sys
import traceback

max_ob = {1:3,    #1: Red
          2:1,    #2: Green
          3:2,    #3: Blue
         }

def find_mask(img): 
    color_map = {}
    id_map = {}
    for i in range(1,4):
        mask = (img == i) 
        #remove small object
        mask = morphology.remove_small_objects(mask, min_size=256, connectivity=1, in_place=False)
        color_map[i] = mask
    for key in color_map:
        image = color_map[key]
        min_id = key
        labels = measure.label(image,connectivity = 1)
        if min_id == 2:  ##green part
            assert labels.max() == max_ob[min_id]
            mask = (labels == 1) 
            ttt = mask
            mask = scipy.ndimage.morphology.binary_fill_holes(mask).astype(np.uint8)
            id_map[1]=mask

        elif min_id == 3:  ## blue part 
            assert labels.max() == max_ob[min_id]
            tmp = []
            min_pos = [] 
            for i in range(1,max_ob[min_id]+1): 
                mask = (labels == i)
                mask = scipy.ndimage.morphology.binary_fill_holes(mask).astype(np.uint8)
                tmp.append(mask)
            for j in tmp:
                a = np.where(j == 1)
                min_pos.append(min(a[1]))
            if min_pos[0] > min_pos[1]:
                id_map[2]=tmp[1]
                id_map[3]=tmp[0]
            else:
                id_map[2]=tmp[0]
                id_map[3]=tmp[1]

        else:  # red part 
            remove_min = 0
            if labels.max() > max_ob[min_id]:
                print ("ERROR!!,Red region > 3! Remove smallest one")
                remove_min = 1
            tmp = []  ##masks 
            min_pos = []  ## x axis 
            region = [] ##mask area
            #for i in range(1,max_ob[min_id]+1):
            for i in range(1,labels.max()+1):
                mask = (labels == i)
                mask = scipy.ndimage.morphology.binary_fill_holes(mask).astype(np.uint8)
                region.append((measure.regionprops(mask))[0].area)
                tmp.append(mask)
                a = np.where(mask == 1)
                min_pos.append(min(a[1]))

            ##remove small regions if regions > 3    
            if remove_min == 1:
                region_tmp = region
                for t in range(1,len(region_tmp)-2):
                    min_index = region.index(min(region)) 
                    del tmp[min_index] 
                    del min_pos[min_index]
                    del region[min_index] 
            num = 4 # red region starts from 4
            for i in sorted(min_pos):
                id_map[num]=tmp[min_pos.index(i)]
                num += 1 
    return color_map,id_map

def main():
    # mask in one image
    #MASK_PATH = '/shared/s2/users/lcai/prostate/masks/'
    MASK_PATH = './paperworks/masks/'
    os.system('mkdir -p maskrcnn; rm -rf maskrcnn/*')
    #masks for mask-rcnn
    os.system('mkdir -p masks; rm -rf masks/*')
    for img_file in os.listdir(MASK_PATH):
        #print(img_file)
        suff = img_file.split(".png")[0]
        #print (suff)
        cnn = "./maskrcnn/"+suff +'/'
        os.system('mkdir -p ' + cnn)
        img = cv2.imread(MASK_PATH+img_file,0)
        H,W = img.shape
        try:
            color_map,id_map = find_mask(img)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ("*** ERROR:")
            print(img_file)
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            continue
        mask_all = np.zeros((H,W),dtype=int)

        for key in id_map:
            mask = id_map[key] * key
            mask_all += mask 
            mask = cv2.normalize(mask,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
            cv2.imwrite(str(cnn)+str(key)+".png",mask)
            pass
        cv2.imwrite("./masks/"+str(img_file),mask_all) 

    '''
    img = cv2.imread("/shared/s2/users/lcai/prostate/masks/ProstateX-03383-t2tsesag-59385.png",0)
    color_map,id_map = find_mask(img)

    for key in id_map:

        print(key)
        mask = cv2.normalize(id_map[key],None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
        cv2.imwrite("mask"+str(key)+".png",mask)
    '''
if __name__ == '__main__':
    main()
