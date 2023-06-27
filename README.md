# 无字幕视频自动生成字幕
## 引言
该项目通过使用腾讯云AI录音文件识别让无字幕视频自动生成字幕
## 依赖

### 1.需下载安装ffmpeg，并设置环境变量

ffmpeg官网链接：https://ffmpeg.org/download.html#build-mac

### 2.借助腾讯云COS获取音频URL

COS SDK链接：https://cloud.tencent.com/document/product/436/12269

COSCMD工具链接：https://cloud.tencent.com/document/product/436/10976

### 3.使用腾讯云ASR录音文件识别服务

(1)在[控制台](https://console.cloud.tencent.com/asr/demonstrate )开通ASR服务

(2)在[API密钥管理页面](https://console.cloud.tencent.com/cam/capi )新建或查询SecertId与SecretKey

(3)调用[录音文件识别](https://cloud.tencent.com/document/product/1093/37823 )服务
  
### 4.运行

当前使用python版本为python3

(1)配置文件输出目录
在commom目录下进行配置
```
OUTPUT_PATH = '/XXX/video-srt/audio/'
```
(2)配置COS相关信息
```
SECRET_ID = '******' # 用户的 SecretId
SECRET_KEY = '******' # 用户的 SecretKeys
BUCKET = 'examplebucket-1250000000' # 已创建的cos桶
REGION = 'ap-shanghai' # 已创建桶归属的 region
SCHEME = 'https' # 指定使用 http/https 协议来访问 COS，默认为 https
TOKEN = None # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
```
(3)配置腾讯云ASR服务相关信息
```
APP_ID = '******' # 用户的 AppId
SECRET_ID = '******' # 用户的 SecretId
SECRET_KEY = '******' # 用户的 SecretKey
ENGINE_TYPE = '16k_zh' # ASR引擎模型类型
```
(4)运行脚本
```
python main 视频文件路径
python main.py audio/test.mov
```
