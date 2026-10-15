#导入数据
from astropy.io import fits
from astropy.stats import SigmaClip
from photutils.background import Background2D
from photutils.segmentation import detect_sources
import numpy as np
import matplotlib.pyplot as plt

#导入文件
fits_path=r"frame-r-005867-5-0107.fits.bz2"
#打开文件
hdul=fits.open(fits_path)
image_data=hdul[0].data   # ✅ 修改！图像在HDU0
header=hdul[0].header



#背景扣除
sigma_clip=SigmaClip(sigma=3)
bkg=Background2D(image_data,box_size=(64,64),sigma_clip=sigma_clip,filter_size=(3,3))
image_sub=image_data-bkg.background

#绘图：左右对比图
plt.figure(figsize=(12,6))
#左图：原始图像
plt.subplot(1,2,1)
plt.imshow(np.log10(image_data.clip(min=1)),cmap='gray',origin='lower',vmin=1,vmax=3)
plt.title("原始SDSS R波段图像")
plt.colorbar()
#右图：扣除天光背景后的图像
plt.subplot(1,2,2)
plt.imshow(np.log10(image_sub.clip(min=0)),cmap='gray',origin='lower',vmin=0,vmax=2)
plt.title("扣除天光背景后图像")
plt.colorbar()

plt.tight_layout()
plt.show()

# ========== 天体源检测，生成分割图 ==========
threshold = 3 * bkg.background_rms
seg_map = detect_sources(image_sub, threshold, npixels=5)

#绘制天体分割标记图
plt.figure(figsize=(8,8))
plt.imshow(seg_map, origin="lower", cmap="nipy_spectral")
plt.title("天体源检测分割图")
plt.colorbar(label="天体源编号")
plt.show()

hdul.close()