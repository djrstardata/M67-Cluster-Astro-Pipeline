# ========= 导入运行所需要的数据库 =========
from astropy.io import fits
from astropy.stats import SigmaClip
from photutils.background import Background2D
from photutils.segmentation import detect_sources
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import ImageNormalize,LogStretch,AsinhStretch,ZScaleInterval

# ========= 打开文件，并获取文件信息 =========
#导入FITS文件
fits_path=r"frame-r-005867-5-0107.fits.bz2"
#打开文件，并读取图像的位置
hdul=fits.open(fits_path)
image_data=hdul[0].data
header=hdul[0].header


# ========= 背景扣除 =========
#借助Background2D进行背景扣除，盒子尺寸为64*64，并由filter进行平滑处理
sigma_clip=SigmaClip(sigma=3)                                                                              #算值大于3倍的均值则认定为天体而剔除
bkg=Background2D(image_data,box_size=(64,64),sigma_clip=sigma_clip,filter_size=(3,3))                      #进行背景扣除，盒子尺寸为64*64，并由filter进行平滑处理
image_sub=image_data-bkg.background                                                                        #获得背景扣除后的干净图像

# ========= 绘制图像 =========
plt.figure(figsize=(18,6))                                                                                 #产生18*6的画布

#第一张，未扣除天光背景的图像进行线性拉伸后的图像
plt.subplot(1,3,1)
plt.imshow(image_data,cmap="gray",origin="lower")                                                           #灰白色，坐标设置在左下角
plt.title("Linear Stretch Image")
plt.colorbar(label="Flux")

#第二张，扣除天光背景的图像进行Astropy对数拉伸后的图像
plt.subplot(1,3,2)
interval=ZScaleInterval()
norm_log=ImageNormalize(image_sub,interval=interval,stretch=LogStretch())
plt.imshow(image_sub,cmap="gray",origin="lower",norm=norm_log)
plt.title("Astropy Stretch Image")
plt.colorbar(label="Normalized Value")

#第三张，扣除天光背景的图像进行Astropy反双曲正弦拉伸后的图像
plt.subplot(1,3,3)
norm=asinh=ImageNormalize(image_sub,interval=interval,stetch=AsinhStretch(a=0.1))
plt.imshow(image_sub,cmap="gray",origin("lower"),norm=norm_asinh)
plt.title("Astropy AsinhStretch Image")
plt.colorbar(label="Normalized Value")

#绘制图像
plt.tight_layout()                                                                                          #将三幅图排版整齐

plt.show()


