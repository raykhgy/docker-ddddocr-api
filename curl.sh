#!/bin/bash

# 定義變數
CAPTCHA_URL="https://lgt.ainja777.com/captcha-handler?get=image&c=backstagecaptcha&t=3eb698d1c191f026f39afb03b4770eaf"
CAPTCHA_FILE="/tmp/captcha.png"
OCR_API="http://localhost:9999/ocr"

# 下載驗證碼圖片
echo "下載驗證碼圖片..."
curl -s -o "$CAPTCHA_FILE" "$CAPTCHA_URL"

# 檢查圖片是否下載成功
if [ ! -f "$CAPTCHA_FILE" ]; then
    echo "錯誤：無法下載驗證碼圖片"
    exit 1
fi

# 確認圖片格式
file "$CAPTCHA_FILE"

# 傳送圖片給 OCR API
echo "傳送圖片給 OCR API..."
curl -X POST -F "image=@$CAPTCHA_FILE" "$OCR_API"

# 清理臨時檔案
rm -f "$CAPTCHA_FILE"
echo "已清理臨時檔案"