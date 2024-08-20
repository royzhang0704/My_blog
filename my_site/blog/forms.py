"""
這個模塊包含了表單類別，用於處理使用者留言、現金記錄和股票交易記錄的數據。
"""
from django import forms
from .models import Comment,Cash,Stock

class CommentForm(forms.ModelForm):
    """
    用於處理使用者留言的表單，基於 Comment 模型。

    此表單排除了與post的關聯欄位 因為該欄位在表單提交後會由視圖手動設定。
    """
    class Meta:
        """
        設置表單註釋
        """
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "用戶名稱",
            "user_email": "電子郵件",
            "text": "內容"
        }


class CashForm(forms.ModelForm):
    """
    用於處理現金記錄的表單，基於 Cash 模型。

    表單字段包括台幣、美金、備註和日期。
    """
    class Meta:
        """
        設置表單註釋
        """
        model = Cash
        fields = ["ntd", "usd", "note", "date"]
        labels = {
            "ntd": "台幣",
            "usd": "美金",
            "note": "備註",
            "date": "日期"
        }


class StockForm(forms.ModelForm):
    """
    用於處理股票交易記錄的表單，基於 Stock 模型。

    表單字段包括股票代號、成交股數、成交單價、手續費、交易稅和日期。
    """
    class Meta:
        """
        設置表單註釋
        """
        model = Stock
        fields = ["stock_symbol", "stock_count", "stock_price", "processing_fee", "tax", "date"]
        labels = {
            "stock_symbol": "股票代號",
            "stock_count": "成交股數",
            "stock_price": "成交單價",
            "processing_fee": "手續費",
            "tax": "交易稅",
            "date": "日期"
        }
