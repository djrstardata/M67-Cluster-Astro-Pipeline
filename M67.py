# ========= 导入运行所需要的数据库 =========
from astropy.io import fits
from astropy.stats import SigmaClip
from photutils.background import Background2D
from photutils.segmentation import detect_sources
from photutils.segmentation import SourceCatalog
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
plt.imshow(image_data,cmap="gray",origin="lower")                                                          #灰白色，坐标原点设置在左下角
plt.title("Linear Stretch Image")                                                                          #标题写作“线性拉伸图像”
plt.colorbar(label="Flux")                                                                                 

#第二张，扣除天光背景的图像进行Astropy对数拉伸后的图像
plt.subplot(1,3,2)
interval=ZScaleInterval()
norm_log=ImageNormalize(image_sub,interval=interval,stretch=LogStretch())                                
plt.imshow(image_sub,cmap="gray",origin="lower",norm=norm_log)                                             #灰白色，坐标原点设置在左下角
plt.title("Astropy Stretch Image")                                                                         #标题写作“Astropy 对数拉伸图像”
plt.colorbar(label="Normalized Value")                                                                   

#第三张，扣除天光背景的图像进行Astropy反双曲正弦拉伸后的图像
plt.subplot(1,3,3)
norm_asinh=ImageNormalize(image_sub,interval=interval,stretch=AsinhStretch(a=0.1))
plt.imshow(image_sub,cmap="gray",origin="lower",norm=norm_asinh)                                           #灰白色，坐标原点设置在左下角
plt.title("Astropy AsinhStretch Image")                                                                    #标题写作“Astropy 反双曲正弦拉伸图像”
plt.colorbar(label="Normalized Value")

#绘制图像
plt.tight_layout()                                                                                          #将三幅图排版整齐

plt.show()

# ========= 天体源检测 =========
print("正在进行天体源检测，请稍后...")

#计算噪声的均方根
threshold=3.0*bkg.background_rms                                                                           #把阈值的三倍作为标准，背景噪声超过阈值3倍以上的判定为天体

#调用detect_sources
seg_map=detect_sources(image_sub,threshold,npixels=5)                                                      #如果连在一起的亮像素少于5个，判定为坏像素或宇宙射线，过滤去除

#统计找到的天体源数量
num_sources=seg_map.max()
print(f"图中共有{num_sources}个天体源")

#检测结果的图样
plt.figure(figsize=(10,8))
plt.imshow(seg_map,origin="lower",cmap="nipy_spectral")                                                    #用不同颜色显示不同的源
plt.title(f"Find {num_sources}")
plt.colorbar(label="源编号(0为背景)")

plt.show()

# ========= 获得源的中心坐标 =========
catalog=SourceCatalog(image_sub,seg_map)
#提取探测到的源的中心坐标
x_centers=catalog.xcentroid
y_centers+catalog.ycentroid

print(f"提取到了{len(x_centers)}个源的中心坐标”）
print(f"最亮源的中心坐标是:X={x_centers[0]:2f},Y={y_centers[0]:2f}")

# ========= 将坐标存为文件 =========
#把坐标存入DataFrame
data={
     "X_Center":catalog.xcentroid,
     "Y_Center":catalog.ycentroid,
     "Area":catalog.area                                                                                  #存下面积，代表形体大小
     }  
df=pd.DataFrame(data)
#导出为CSV文件
csv_name="M67_Source_Catalog.csv"
df.to_csv(csv_name,index=False)

print(f"已将{len(df)}个天体源保存至{csv_name}")










      


































