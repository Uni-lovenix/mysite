from haystack import indexes
# 修改此处，为你自己的model
from blog.models import ContentItems


# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class ContentItemsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    uid = indexes.CharField(model_attr='uid')
    posttime = indexes.DateTimeField(model_attr='posttime')
    content = indexes.CharField(model_attr='content')
    cai = indexes.IntegerField(model_attr='cai')

    def get_model(self):
        # 修改此处，为你自己的model
        return ContentItems

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
