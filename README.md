# LSB隐写工具（带界面 + 密码版）

一个基于Python开发的图片隐写工具，支持将文本信息隐藏到图片中，并通过密码保护进行安全存储。

## ✨ 功能特点

* 支持中文/英文/符号隐藏
* 自动将图片转换为PNG格式（防止数据丢失）
* 基于LSB算法的隐形水印
* 密码加密保护（输入错误密码无法正确解密）
* 图形化界面（简单易用）
* 支持批量图片处理

## 🛠 使用方法

1. 选择图片（支持JPG/PNG等）
2. 输入隐藏内容
3. 输入密码
4. 点击加密生成新图片

解密时输入正确密码即可恢复内容。

## ⚠ 注意

* 建议使用较大尺寸图片以保证容量
* JPG格式会自动转换为PNG
* 密码丢失无法恢复数据

## 📌 应用场景

* 图片版权保护
* 隐私信息传输
* 数字水印标记
* 数据隐藏与验证
# LSB Steganography Tool (GUI + Password Protected)

A Python-based image steganography tool that allows you to hide text inside images with password protection.

## ✨ Features

* Supports Unicode (Chinese, English, symbols)
* Automatically converts images to PNG (to avoid data loss)
* Uses LSB (Least Significant Bit) steganography
* Password-protected encryption (wrong password = invalid output)
* Simple GUI interface
* Batch image processing support

## 🛠 Usage

1. Select an image (JPG/PNG supported)
2. Enter the hidden message
3. Enter a password
4. Click encode to generate a new image

Use the correct password to decode the hidden message.

## ⚠ Notes

* Use larger images for more capacity
* JPG images are automatically converted to PNG
* Lost passwords cannot recover data

## 📌 Use Cases

* Image copyright protection
* Secure message transmission
* Digital watermarking
* Data hiding and verification
