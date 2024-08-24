"""
這個模塊包含了部落格應用的視圖。

包含以下視圖：
- StartingPage: 顯示前三則貼文。
- AllPost: 顯示所有貼文。
- PostDetail: 處理文章詳細內容。
- ReadLater: 管理文章read later列表。
- cash_form_page: 處理現金表單紀錄。
- stock_form_page: 處理股票表單紀錄。
- stock_index: 理財網頁首頁。
"""

from decimal import Decimal
import requests

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import ListView, View
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .models import Post, Cash, Stock
from .forms import CommentForm, StockForm, CashForm


class StartingPage(ListView):
    """
    文章首頁，抓取最新前三則貼文並顯示。
    """
    template_name = "blog/post_index.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        """
        獲取最新的三篇文章。

        回傳:
            QuerySet: 包含最新三篇文章的查詢集。
        """
        queryset = super().get_queryset()
        return queryset[:3]


class AllPost(ListView):
    """
    顯示所有文章的視圖，按照日期排序。
    """
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        """
        獲取上下文數據，並添加一條自訂訊息。

        參數:
            kwargs: 其他上下文參數。

        回傳:
            dict: 包含上下文數據的字典。
        """
        context = super().get_context_data(**kwargs)
        context['message'] = "嘿，你好！準備好來閱讀一些有趣的內容嗎？"
        return context


class PostDetail(View):
    """
    顯示單篇文章的詳細內容，並處理留言和稍後閱讀功能。
    """

    def get(self, request, slug):
        """
        處理 GET 請求並顯示文章詳情頁面。

        參數:
            request: HTTP 請求對象。
            slug: 文章的唯一標識符。

        回傳:
            HttpResponse: 包含文章詳情頁面的回應。
        """
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        """
        處理 POST 請求，根據請求處理留言或稍後閱讀功能。

        參數:
            request: HTTP 請求對象。
            slug: 文章的唯一標識符。

        回傳:
            HttpResponseRedirect: 重定向到文章詳情頁面。
        """
        if "comment_form" in request.POST:
            return self.handle_comment_form(request, slug)
        return self.handle_read_later(request, slug)

    def handle_comment_form(self, request, slug):
        """
        處理留言表單提交。

        參數:
            request: HTTP 請求對象。
            slug: 文章的唯一標識符。

        回傳:
            HttpResponseRedirect: 重定向到文章詳情頁面。
        """
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def handle_read_later(self, request, slug):
        """
        處理將文章添加到稍後閱讀列表或從列表中移除的功能。

        參數:
            request: HTTP 請求對象。
            slug: 文章的唯一標識符。

        回傳:
            HttpResponseRedirect: 重定向到文章詳情頁面。
        """
        post = get_object_or_404(Post, slug=slug)
        stored_posts = request.session.get("stored_posts", [])

        if post.id not in stored_posts:
            stored_posts.append(post.id)
        else:
            stored_posts.remove(post.id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

    def is_stored_post(self, request, post_id):
        """
        檢查某個貼文是否已經儲存在使用者的 session 中以供稍後閱讀。

        參數:
            request: 包含 session 資料的 HTTP 請求對象。
            post_id: 要檢查的貼文 ID。

        回傳:
            bool: 如果貼文已經被儲存，回傳 True 否則回傳 False。
        """
        stored_posts = request.session.get("stored_posts", [])
        return post_id in stored_posts


class ReadLater(View):
    """
    管理使用者的稍後閱讀列表，提供添加和刪除功能。
    """

    def post(self, request):
        """
        處理 POST 請求，將文章添加到稍後閱讀列表或從列表中移除。

        參數:
            request: HTTP 請求對象。

        回傳:
            HttpResponseRedirect: 重定向到起始頁面。
        """
        stored_posts = request.session.get("stored_posts", [])
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect(reverse("starting-page"))

    def get(self, request):
        """
        處理 GET 請求，顯示使用者的稍後閱讀列表。

        參數:
            request: HTTP 請求對象。

        回傳:
            HttpResponse: 包含稍後閱讀列表頁面的回應。
        """
        stored_posts = request.session.get("stored_posts")
        context = {}
        if not stored_posts:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/read_later.html", context)



def cash_form_page(request, cash_id=None):
    """
    顯示或處理現金表單的頁面。

    參數:
        request: HTTP 請求對象。
        cash_id: 現金紀錄的 ID。

    回傳:
        HttpResponse: 包含現金表單頁面的回應。
    """
    cash = get_object_or_404(Cash, pk=cash_id) if cash_id else None
    if request.method == "POST":
        form = CashForm(request.POST, instance=cash)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("stock-index"))
    else:
        form = CashForm(instance=cash)
    
    return render(request, "blog/cash_form_page.html", {
        "form": form,
        "cash": cash
    })



def stock_form_page(request, symbol=None):
    """
    顯示或處理股票表單的頁面。

    參數:
        request: HTTP 請求對象。
        symbol: 股票代號。

    回傳:
        HttpResponse: 包含股票表單頁面的回應。
    """
    stock = get_object_or_404(Stock, stock_symbol=symbol) if symbol else None
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock_symbol = form.cleaned_data['stock_symbol']
            stock = Stock.objects.filter(stock_symbol=stock_symbol).first()
            if stock:
                stock.stock_count += form.cleaned_data['stock_count']
                stock.stock_price = form.cleaned_data['stock_price']
                stock.processing_fee += form.cleaned_data['processing_fee']
                stock.tax += form.cleaned_data['tax']
                stock.date = form.cleaned_data['date']
                stock.save()
            else:
                form.save()
            return HttpResponseRedirect(reverse("stock-index"))
    else:
        form = StockForm(instance=stock)

    return render(request, "blog/stock_form_page.html", {
        "form": form,
        "stock": stock
    })

def stock_index(request):
    """
    顯示和處理理財首頁，包含現金和股票的數據。

    根據用戶的 POST 請求處理刪除或編輯現金與股票的操作，
    並計算和顯示當前的現金、股票數據和其報酬率。
    
    參數:
        request: HTTP 請求對象。

    回傳:
        HttpResponse: 包含理財首頁的回應。
    """
    if request.method == "POST":
        if "delete_cash" in request.POST:
            cash_id = request.POST.get("id")
            Cash.objects.filter(id=cash_id).delete()
            return redirect("stock-index")
        elif "edit_cash" in request.POST:
            cash_id = request.POST.get("id")
            return redirect("edit-cash", cash_id=cash_id)
        else: #delete_stock
            stock_stock_symbol = request.POST.get("stock_id")
            Stock.objects.filter(stock_symbol=stock_stock_symbol).delete()

    context = {}
    stock_data = []
    total_stock_value = Decimal(0)

    cash_total = Cash.objects.aggregate(
        ntd_total=Sum("ntd"), usd_total=Sum("usd"))
    ntd_total = cash_total.get("ntd_total", 0) or 0
    usd_total = cash_total.get("usd_total", Decimal(0)) or Decimal(0)

    stocks = Stock.objects.all().order_by("-date")
    for stock in stocks:
        current_stock_value = stock.stock_price * stock.stock_count
        total_cost = (stock.stock_price * stock.stock_count) + \
            stock.processing_fee + stock.tax
        average_cost = total_cost / \
            stock.stock_count if stock.stock_count > 0 else Decimal(0)
        rate_of_return = ((current_stock_value - total_cost) /
                          total_cost) * 100 if total_cost > 0 else Decimal(0)
        price = current_price(stock.stock_symbol)
        stock_info = {
            'stock_symbol': stock.stock_symbol,
            'stock_count': stock.stock_count,
            'current_price': price,
            'current_value': price * stock.stock_count,
            'total_cost': total_cost,
            'average_cost': round(average_cost, 2),
            'rate_of_return': round(rate_of_return, 2)
        }
        stock_data.append(stock_info)
        total_stock_value += price * stock.stock_count

    for stock in stock_data:
        stock['stock_percentage'] = round(
            (stock['current_value'] / total_stock_value) * 100, 2) \
        if total_stock_value > 0 else Decimal(0)
    context["cash_data"] = Cash.objects.all().order_by("-date")
    context['usd_to_twd_rate'] = usd_to_twd_rate()
    context["stock_data"] = stock_data
    context['ntd_total'] = ntd_total
    context['usd_total'] = usd_total
    context['total_cash'] = round(
        (usd_to_twd_rate() * usd_total) + ntd_total, 3)

    return render(request, "blog/stock_index.html", context)


def usd_to_twd_rate():
    """
    抓取並返回即時的美元對台幣匯率。

    回傳:
        Decimal: 美元對台幣的匯率，若抓取失敗則返回 0。
    """
    try:
        data = requests.get('https://tw.rter.info/capi.php', timeout=5)
        data.raise_for_status()
        result = data.json()
        return round(Decimal(result['USDTWD']['Exrate']), 3)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching USD to TWD rate: {e}")
        return Decimal(0)


def current_price(stock_symbol):
    """
    抓取並返回指定股票代號的當前價格。

    參數:
        stock_symbol: 股票的代號。

    回傳:
        Decimal: 股票的當前價格，若抓取失敗則返回 0。
    """
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock_symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        price_array = data.get('data', [])
        if price_array:
            latest_price = price_array[-1][6]
            return Decimal(latest_price)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current price for {stock_symbol}: {e}")
    return Decimal(0)
