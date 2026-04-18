# docker-ddddocr-api

基於 [ddddocr](https://github.com/sml2h3/ddddocr) 的驗證碼識別 REST API，使用 Docker 部署。

## 功能

- 支援上傳圖片檔案進行 OCR 識別
- 支援傳入 Base64 字串進行 OCR 識別（含或不含 `data:image/...;base64,` 前綴）
- 支援限制識別字符集（純數字、純英文等）
- 使用 ddddocr beta 模型，適合各類驗證碼

## 快速啟動

```bash
docker compose up -d --build
```

服務啟動後監聽 `http://localhost:9999`。

## API

### POST `/ocr_image`

上傳圖片檔案進行識別。

**請求：** `multipart/form-data`

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| image | file | 是 | 驗證碼圖片 |
| ranges | string | 否 | 限制識別字符集，見下方說明 |

**範例：**

```bash
# 基本識別
curl -X POST -F "image=@/tmp/captcha.png" http://localhost:9999/ocr_image

# 限制只識別數字
curl -X POST -F "image=@/tmp/captcha.png" -F "ranges=0" http://localhost:9999/ocr_image
```

**回應：**

```json
{ "result": "a1b2" }
```

---

### POST `/ocr_image_str`

傳入 Base64 字串進行識別。

**請求：** `application/json`

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| image | string | 是 | Base64 編碼的圖片（支援含 `data:image/...;base64,` 前綴） |
| ranges | string / number | 否 | 限制識別字符集，見下方說明 |

**範例：**

```bash
# 基本識別
curl -X POST -H "Content-Type: application/json" \
  -d '{"image":"iVBORw0KGgo..."}' \
  http://localhost:9999/ocr_image_str

# 限制只識別數字
curl -X POST -H "Content-Type: application/json" \
  -d '{"image":"iVBORw0KGgo...", "ranges": 0}' \
  http://localhost:9999/ocr_image_str
```

**回應：**

```json
{ "result": "a1b2" }
```

---

## 參數說明

### `ranges` — 字符集限制

| 值 | 字符集 |
|----|--------|
| `0` | 純數字 `0-9` |
| `1` | 純小寫 `a-z` |
| `2` | 純大寫 `A-Z` |
| `3` | 大小寫混合 `a-z A-Z` |
| `4` | 小寫 + 數字 `a-z 0-9` |
| `5` | 大寫 + 數字 `A-Z 0-9` |
| `6` | 全英數 `a-z A-Z 0-9` |
| `7` | 預設字符集（含特殊字元） |
| 自訂字串 | 例如 `"0123456789+-x/="` |

---

## 更新代碼

修改 `app.py` 後，只需重啟 container（無需重新 build）：

```bash
docker compose restart
```

## 升級 ddddocr 版本

### 注意事項

- `set_ranges` 方法從 **1.5.x** 開始支援，**1.4.x 以下無此方法**，帶 `ranges` 參數會返回 500 錯誤
- ddddocr **1.6.x 需要 Python ≥ 3.10**，目前 image 使用 Python 3.9，最高只能裝到 **1.5.6**
- 若要升級至 1.6.x，須同步將 `Dockerfile` 的 base image 改為 `python:3.10-slim` 以上

### 升級步驟

**步驟 1：確認目標版本支援 Python 3.9**

```bash
pip index versions ddddocr
```

**步驟 2：修改 `requirements.txt`**

```
ddddocr==1.5.6   # 改為目標版本號
```

**步驟 3：重新建置並啟動**

```bash
docker compose down
docker rmi docker-ddddocr-api-ocr-api
docker compose up -d --build
```

**步驟 4：驗證版本與功能**

```bash
# 確認版本
docker exec docker-ddddocr-api-ocr-api-1 python -c "import ddddocr; print(ddddocr.__version__)"

# 確認 set_ranges 存在
docker exec docker-ddddocr-api-ocr-api-1 python -c "import ddddocr; ocr = ddddocr.DdddOcr(show_ad=False); print('set_ranges:', 'set_ranges' in dir(ocr))"

# 測試帶 ranges 請求
curl -X POST -F "image=@/tmp/captcha.png" -F "ranges=0" http://localhost:9999/ocr_image
```

## 重新建置

修改 `requirements.txt` 或 `Dockerfile` 後才需要重新 build：

```bash
docker compose down
docker rmi docker-ddddocr-api-ocr-api
docker compose up -d --build
```

## 技術棧

| 項目 | 版本 |
|------|------|
| Python | 3.9-slim |
| Flask | 2.0.1 |
| ddddocr | 1.5.6 |
| Pillow | 9.5.0 |
| Port | 9999 |
