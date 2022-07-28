import uuid
from io import BytesIO

from bs4 import BeautifulSoup as bs
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import ImageField, Model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.defaultfilters import slugify
from PIL import Image

FULL_DOMAIN = settings.FULL_DOMAIN


class ResizeImageMixin:
    def resize(self, imageField: ImageField, size:tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert('RGB')
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format='WebP') # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.WebP'
        imageField.save(random_name, file, save=False)


class BaseToAll(Model):
    class Meta:
        abstract = True

    @property
    def app_label(self):
        return self._meta.app_label
    
    @property
    def object_name(self):
        return self._meta.object_name
    
    @property
    def regularised_description(self):
        if self.object_name == 'Question':
            regularised_description = self.content

        elif self.object_name == 'Company':
            regularised_description = self.description

        else:
            regularised_description = self.resume

        return regularised_description
    
    @property
    def regularised_title(self):
        if self.object_name == 'Company':
            regularised_title = self.name
        else:
            regularised_title = self.title

        return regularised_title
    
    @property
    def dict_for_task(self):
        return {
            'app_label': self.app_label,
            'object_name': self.object_name,
            'id': self.pk,
        }
    
    @property
    def dict_for_email(self):
        dict_task = self.dict_for_task
        dict_task.update(
            {
            'title': self.regularised_title,
            'content': self.regularised_description,
            }
        )
        return dict_task
    
    @property
    def encoded_url(self):
        url = f'{self.id}-{self.app_label}-{self.object_name}'
        return urlsafe_base64_encode(force_bytes(url))
    
    def save_unique_field(self, field, value, extra:int=None):
        max_length = self._meta.get_field(field).max_length
        if extra:
            value = slugify(f"{value}-{extra}")
        if len(value) > max_length:
            value = value[:max_length+1]
        if self.__class__.objects.filter(field=value).exists():
            extra += 1
            return self.save_unique_field(field, value, extra)
        return value


class CommonMixin(BaseToAll):
    class Meta:
        abstract = True
    
    @property
    def related_comments(self):
        return self.comments_related.all()
    
    @property
    def encoded_url_comment(self):
        return self.encoded_url
    
    @property
    def encoded_url_up(self):
        return urlsafe_base64_encode(force_bytes(f'{self.encoded_url}-up'))
    
    @property
    def encoded_url_down(self):
        return urlsafe_base64_encode(force_bytes(f'{self.encoded_url}-down'))

    def vote(self, user, action):
        user_already_upvoted = True if user in self.upvotes.all() else False
        user_already_downvoted = True if user in self.downvotes.all() else False
        vote_result = 0
        update_fields = ['total_votes']
        if action == 'up' and user_already_upvoted == True or action == 'down' and user_already_downvoted == True:
            return vote_result
        if action == 'up':
            if user_already_downvoted == True:
                self.downvotes.remove(user)
                self.upvotes.add(user)
                vote_result = 2
                update_fields += ['downvotes', 'upvotes']
            elif user_already_upvoted == False:
                self.upvotes.add(user)
                vote_result = 1
                update_fields += ['upvotes']

        elif action == 'down':
            if user_already_upvoted == True:
                self.upvotes.remove(user)
                self.downvotes.add(user)
                vote_result = -2
                update_fields += ['downvotes', 'upvotes']
            elif user_already_downvoted == False:
                self.downvotes.add(user)
                vote_result = -1
                update_fields += ['downvotes']
        
        self.author.update_reputation(vote_result)
        self.total_votes += vote_result
        self.save(update_fields=update_fields)
        return vote_result
    
    @property
    def schema_org(self):
        if self.object_name == 'Question':
            schema_org = self.schema_org
        else:
            meta_url = f'{FULL_DOMAIN}/definicion/{self.slug}/'
            if self.object_name == 'PublicBlog':
                meta_url = f'{self.author.custom_url}/p/{self.slug}/'
            schema_org = {
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{meta_url}"
                },
                "headline": f"{self.title}",
                "image": f"{self.non_thumbnail_url}",
                "datePublished": f"{self.published_at}",
                "author": {
                "@type": "Person",
                "name": f"{self.author.full_name}"
                },
                "publisher": {
                "@type": "Organization",
                "name": "Inversiones & Finanzas",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico"
                },
                },
            }
        return schema_org

    @property
    def meta_info(self):
        meta_info = {}
        if self.object_name == 'Question':
            meta_info['modified_time'] = self.updated_at
            meta_info['meta_image'] = self.author.foto
            meta_info['meta_title'] = self.title
            meta_info['meta_desc'] = self.content
            meta_info['meta_url'] = self.get_absolute_url()
            meta_info['meta_tags'] = self.tags.all()
            meta_info['meta_category'] = self.category
            meta_info['meta_author'] = self.author
            meta_info['schema_org'] = self.schema_org
        else:
            try:
                saved_meta = self.meta_information.parameter_settings
            except:
                self.save_secondary_info(str(self._meta).split('.')[1])
            else:
                meta_info['modified_time'] = saved_meta.modified_time
                meta_info['meta_image'] = saved_meta.meta_img
                meta_info['meta_title'] = saved_meta.meta_title
                meta_info['meta_desc'] = saved_meta.meta_description
                meta_info['meta_url'] = saved_meta.meta_url
                meta_info['meta_tags'] = saved_meta.meta_keywords
                meta_info['meta_category'] = 'Inversiones'
                meta_info['meta_author'] = saved_meta.meta_author
                meta_info['schema_org'] = saved_meta.schema_org

        return meta_info

   
class BaseEscritosMixins(Model):
    class Meta:
        abstract = True
    
    def search_image(self, content):
        soup = bs(content, 'html.parser')
        images = [img for img in soup.find_all('img')]
        image = False
        if len(images) !=0:
            image = images[0]
            image = image.get('src')
        return image


    def extra_info(self, image):
        if image == False:
            self.in_text_image = False
        else:
            self.in_text_image = True
            self.non_thumbnail_url = image


    def create_meta_information(self, type_content):
        from apps.seo.models import MetaParameters, MetaParametersHistorial
        
        meta_url = f'{FULL_DOMAIN}/definicion/{self.slug}/'
        if type_content == 'blog':
            meta_url = f'{self.author.custom_url}/p/{self.slug}/'            
            
        meta = MetaParameters.objects.create(
            meta_title = self.title,
            meta_description = self.resume,
            meta_img = self.non_thumbnail_url,
            meta_url = meta_url,
            meta_keywords = ', '.join([tag.name for tag in self.tags.all()]),
            meta_author = self.author,
            published_time = self.published_at,
            modified_time = self.updated_at,
            created_at = self.created_at,
            schema_org = {
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{meta_url}"
                },
                "headline": f"{self.title}",
                "image": f"{self.non_thumbnail_url}",
                "datePublished": f"{self.published_at}",
                "author": {
                "@type": "Person",
                "name": f"{self.author.full_name}"
                },
                "publisher": {
                "@type": "Organization",
                "name": "Inversiones & Finanzas",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico"
                },
                },
            },
        )
        meta_historial = MetaParametersHistorial.objects.create(
            parameter_settings = meta,
            in_use = True,
        )

        self.meta_information = meta_historial
    
    def save_secondary_info(self, content_type):
        if content_type != 'blog':
            for term_part in self.term_parts.all():
                image = self.search_image(term_part.content)
                if image != False:
                    break
        else:
            image = self.search_image(self.content)
        self.extra_info(image)
        self.create_meta_information(content_type)