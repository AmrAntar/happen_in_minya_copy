from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from embed_video.fields import EmbedVideoField


# Create your models here.


class TagedNewsPost(TaggedItemBase):
    content_object = models.ForeignKey('NewsPost', on_delete=models.CASCADE)

    # def slugify(self, tag, i=None):
    #     slug = arabic_slugify(tag)
    #     if i is not None:
    #         slug += "-%d" % i
    #     return slug
    class Meta:
        verbose_name = 'الفئات'
        verbose_name_plural = 'الفئات'


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)

    class Meta:
        ordering = ('-title',)
        verbose_name = 'التصنيفات'
        verbose_name_plural = 'التصنيفات'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:show_category_tab', args=[self.slug,])


class NewsPost(models.Model):
    category = models.ForeignKey(Category, related_name='cat_post', on_delete=models.CASCADE)
    tags = TaggableManager(through=TagedNewsPost)
    title = models.CharField(max_length=250)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    image = models.ImageField(upload_to='image/', blank=True)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'الاخبار'
        verbose_name_plural = 'الاخبار'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(NewsPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:news_post_detail', args=[self.slug,])


def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='cat_item', on_delete=models.CASCADE, blank=True, null=True)
    caption = models.CharField(max_length=200)
    video = EmbedVideoField()  # same like models.URLField()

    class Meta:
        ordering = ('-caption',)
        verbose_name = 'الفديوهات'
        verbose_name_plural = 'الفديوهات'

    def __str__(self):
        return self.caption
