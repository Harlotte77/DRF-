from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from rest_framework import serializers
from rest_framework.response import Response
from CBVpractice.models import Book, Publish, Author


# Create your views here.
# CBV(class based view)


# -------------------------序列化器--------------------------------
# 针对模型设计序列化器
class BookSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=32)
    # required=False表示该字段是可选的，可以为空，反序列化的时候可以不传入price的值
    price = serializers.IntegerField(required=False)
    # 修改字段名
    # 浏览器中显示的是date, 但实际上序列化的还是pub_date
    date = serializers.DateField(source="pub_date")

    # 重写serializers.Serializer的父类BaseSerializer中的方法create
    def create(self, validated_data):
        new_book = Book.objects.create(**self.validated_data)
        return new_book

    def update(self, instance, validated_data):
        # 校验通过，进行更新
        # 合格的数据存放在serializer.validated_data中
        Book.objects.filter(pk=instance.pk).update(**validated_data)
        updated_book = Book.objects.get(pk=id)  # 更新之后的新数据
        return updated_book  # 返回更新后的数据


# 模型序列化器(ModelSerializer)
class BookSerializers(serializers.ModelSerializer):
    # 灵活配置
    date = serializers.DateField(source="pub_date")

    class Meta:
        model = Book
        # 针对所有字段
        # fields = "__all__"  # 包括id

        # 针对某些字段
        # fields = ["title", "price"]

        # 排除某个字段
        exclude = ["pub_date"]


class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


# ----------------------------------------------------------------


# -------------------基于View、APIView的接口实现-------------------
# 对所有数据进行操作的接口
# APIView提供了免除csrf认证
class BookView(APIView):
    def get(self, request):
        '''
        查看所有书籍
        :param request:
        :return:
        '''

        book_list = Book.objects.all()

        # 构建序列化器对象
        # instance: 用来做序列化传参
        # data: 用来做反序列化传参
        # many: True表示序列化或者反序列化对象中有多个模型类对象，False表示只有一个模型类对象
        serializer = BookSerializers(instance=book_list, many=True)
        '''
        temp = []
        for obj in book_list:
            d = {}
            d["title"] = obj.title
            d["print"] = obj.print
            d["pub_date"] = obj.pub_date

            temp.append(d)
        '''
        # 序列化的结果
        res = serializer.data
        # print(res)
        return Response(res)

    def post(self, request):
        # 获取请求数据
        print("data", request.data)

        # 构建序列化器对象
        # 反序列化用data传参
        serializer = BookSerializers(data=request.data)
        # 校验数据
        # 所有字段都通过校验的时候返回True，否则返回False
        # 合法的数据都会放到serializer.validated_data中
        # 不合法的放到serializer.errors中
        if serializer.is_valid():
            # 数据校验通过
            # 将数据插入到数据库中
            serializer.save()
            # 返回反序列化的数据给前端
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)


# 对某个或者某些数据进行操作的接口
class BookDetailView(APIView):

    def get(self, request, id):
        # 根据id找到对象
        # 这两句代码实际上是等价的，都是通过主键（Primary Key）来获取数据库中的一条记录。
        # 在 Django 中，pk 是指主键字段，而默认情况下主键字段名为 id，因此 pk 和 id 在这里是等价的。
        # book = Book.objects.get(id=id)
        book = Book.objects.get(pk=id)
        # 序列化从数据库拿到的对象数据
        serializer = BookSerializers(instance=book, many=False)
        # 序列化的结果: serializer.data
        return Response(serializer.data)

    def put(self, request, id):
        # 获取用户提交的数据：request.data
        # print("data", request.data)

        """
        更新和查找不同，需要传入instance和data两个参数
        要更新的数据，传给instance，新的数据(用户提交的)传给data
        """
        update_book = Book.objects.get(pk=id)  # 要更新的数据(更新之前的数据)
        # 构建序列化器对象
        serializer = BookSerializers(instance=update_book, data=request.data)
        # 校验
        if serializer.is_valid():
            # 数据校验通过
            serializer.save()
            return Response(serializer.data)
        else:
            # 校验不通过，返回错误信息
            return Response(serializer.errors)

    def delete(self, request, id):
        Book.objects.get(pk=id).delete()
        return Response()


# ----------------------------------------------------------------


# -------------------基于GenericAPIView的接口实现-------------------
class BookGenericApiView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BookDetailGenericApiView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


class PublishGenericApiView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublishDetailGenericApiView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


class AuthorGenericApiView(GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AuthorDetailGenericApiView(GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


# ----------------------------------------------------------------


# -------------------基于Mixin的接口实现-------------------
class AuthorMixinView(ListModelMixin, GenericAPIView, CreateModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class AuthorDetailMixinView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class BookMixinView(ListModelMixin, GenericAPIView, CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookDetailMixinView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class PublishMixinView(ListModelMixin, GenericAPIView, CreateModelMixin):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class PublishDetailMixinView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# -------------------基于Minxin的接口实现(简洁版)-------------------
class AuthorMixinSimpleView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class AuthorDetailMixinSimpleView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class BookMixinSimpleView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class BookDetailMixinSimpleView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class PublishMixinSimpleView(ListCreateAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


class PublishDetailMixinSimpleView(RetrieveUpdateDestroyAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


# -------------------基于ViewSet的接口实现-------------------
# ViewSet重新构建了分发机制
# 一个类可以实现增删改查查五个接口的开发，可以自定义相应方法的名称
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class PublishViewSet(ModelViewSet):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
