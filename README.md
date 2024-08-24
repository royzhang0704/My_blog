# 我的BLOG專案

這是一個基於 Django 的博客專案，用戶可以創建和管理博客文章、對文章留言，並追蹤自己的現金和股票投資組合。

## 功能

- **博客文章**：用戶可以創建、查看和管理博客文章。
- **留言功能**：用戶可以在博客文章下方留言。
- **財務投資組合**：用戶可以追蹤現金和股票投資。
- **稍後閱讀**：用戶可以將文章保存至稍後閱讀清單。

## 安裝

### 先決條件

- Python 3.9 或更高版本
- pip
- Virtualenv（可選，但推薦使用）

### 設置

1. **Clone 此倉庫**：
    ```bash
    git clone https://github.com/royzhang0704/My_blog.git
    cd My_blog
    ```

2. **創建並啟用虛擬環境**（可選但推薦）：
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows 系統使用 `.venv\Scripts\activate`
    ```

3. **安裝所需依賴**：
    ```bash
    pip install -r requirements.txt
    ```

4. **創建本地 MySQL 資料庫**：
    ```bash
    CREATE DATABASE my_blog_db;
    ```

5. **複製 .env.example 文件並重命名為 .env**：
    ```bash
    cp .env.example .env
    ```
    在 `.env` 文件中填寫：
    - SECRET_KEY: 你的密鑰。
    - DATABASE_NAME: 你的資料庫名稱（例如 `my_blog_db`）
    - DATABASE_USER: 你的資料庫用戶名
    - DATABASE_PASSWORD: 你的資料庫密碼

6. **生成 SECRET_KEY**（如果需要生成新的 SECRET_KEY）：
    - 進入 Django Shell：
        ```bash
        python manage.py shell
        ```
    - 在 Django Shell 中運行以下 Python 代碼來生成一個新的 SECRET_KEY：
        ```python
        from django.core.management.utils import get_random_secret_key
        print(get_random_secret_key())
        ```
    - 複製生成的 SECRET_KEY 並把它貼到 `.env` 文件中的 SECRET_KEY 欄位。

7. **應用數據遷移**：
    ```bash
    python3 manage.py migrate
    ```

8. **加載初始 JSON 數據到資料庫**：
    ```bash
    python manage.py loaddata initial_data.json
    ```

9. **運行開發伺服器**：
    ```bash
    python3 manage.py runserver
    ```

## 技術說明

- 利用 Django 框架使用 FBV 與 CBV 處理不同的操作邏輯讓代碼有更多的擴充性與良好架構性。
- 選擇 MySQL 當作我的資料庫，在理財管理系統利用到了 CRUD 功能，展示了我對資料庫的基本操作，並且使用了 ORM 進行資料庫的操作，且有（one to one）、（one to many）與（many to many）的設計架構。
- 利用 Django 的 Session 機制去實現稍後觀看清單的功能，因為它簡單且與 Django 框架深度整合。
- 使用 DTL (Django Template Language) 去呈現動態網頁，讓使用者體驗更加良好。
- 使用 Django 內建 Form 表單功能去實現部落格留言與現金股票庫存表單，在設計上有更好的結構性。
- 在美金匯率與股票價格使用了第三方 API 做串接，以達成即時更新的功能。

## 使用方法

- **首頁**：顯示最新的三篇博客文章。
- **所有文章**：查看所有博客文章。
- **文章詳情**：查看單篇文章的詳細內容，可留言和保存稍後閱讀。
- **財務投資組合**：管理和查看現金及股票投資記錄。

## 貢獻

歡迎貢獻此項目！請 fork 此倉庫並提交 pull request。

## 授權

此專案採用 MIT 授權許可。詳情請參閱 LICENSE 文件。

## 聯繫方式

如有任何問題或反饋，請隨時聯繫我! [royzhang0704@gmail.com](mailto:royzhang0704@gmail.com)。
