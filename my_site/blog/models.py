"""
包含所有的資料庫創建
"""
from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email_address=models.EmailField(unique=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()

class Tag(models.Model):
    caption=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.caption
    

class Post(models.Model):
    title=models.CharField(max_length=200,help_text="The title of the post.")
    excerpt=models.CharField(max_length=150)
    image=models.ImageField(upload_to="posts",null=True,blank=True) #null=True 允許無圖片

    date=models.DateField(auto_now_add=True) #文章創建時自動設置日期
    slug=models.SlugField(unique=True,db_index=True)
    content=models.TextField(validators=[MinLengthValidator(10)])
    author=models.ForeignKey(Author, on_delete=models.SET_NULL,null=True,related_name="posts") # 作者刪除後設為 null

    tags=models.ManyToManyField(Tag) # 多對多關係 文章可以有多個標籤

    class Meta:  #默認按日期排序
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title}"



class Comment(models.Model):
    user_name = models.CharField(max_length=50, )  
    user_email = models.EmailField() 
    text = models.TextField(max_length=500)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # 關聯文章，文章刪除後留言也會刪除



class Cash(models.Model):
    ntd=models.IntegerField()
    usd=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    note = models.CharField(max_length=50, help_text="簡短說明或備註")
    date=models.DateField(editable=True)

    def __str__(self) -> str:
        return f"第{self.id} 筆資料,新台幣:{self.ntd} 美金:{self.usd}"
    
class Stock(models.Model):
    stock_symbol=models.CharField(max_length=50)
    stock_count=models.IntegerField()#成交股數
    stock_price=models.DecimalField(max_digits=10,decimal_places=2)#成交單價
    processing_fee=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    date=models.DateField(editable=True)
    def __str__(self):
        return f"第{self.id} 筆資料 股票代號:{self.stock_symbol} 成交股數:{self.stock_count}成交單價:{self.stock_price}"