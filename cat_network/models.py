from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

list_of_breeds = [
    ("Abyssinian", "Abyssinian"),
    ("American Bobtail", "American Bobtail"),
    ("American Curl", "American Curl"),
    ("American Wirehair", "American Wirehair"),
    ("Aphrodite Giant", "Aphrodite Giant"),
    ("Arabian Mau", "Arabian Mau"),
    ("Asian Semi-longhair", "Asian Semi-longhair"),
    ("Australian Mist", "Australian Mist"),
    ("Balinese", "Balinese"),
    ("Bambino", "Bambino"),
    ("Bengal", "Bengal"),
    ("Birman", "Birman"),
    ("Bombay", "Bombay"),
    ("British Shorthair", "British Shorthair"),
    ("Burmese", "Burmese"),
    ("Chantilly-Tiffany", "Chantilly-Tiffany"),
    ("Colorpoint Longhair", "Colorpoint Longhair"),
    ("Colorpoint Persian", "Colorpoint Persian"),
    ("Colorpoint Shorthair", "Colorpoint Shorthair"),
    ("Devon Rex", "Devon Rex"),
    ("Don Sphynx", "Don Sphynx"),
    ("Egyptian Mau", "Egyptian Mau"),
    ("Foldex", "Foldex"),
    ("German Rex", "German Rex"),
    ("Havana Brown", "Havana Brown"),
    ("Khao Manee", "Khao Manee"),
    ("Korat", "Korat"),
    ("Maine Coon", "Maine Coon"),
    ("Minskin", "Minskin"),
    ("Munchkin", "Munchkin"),
    ("Oriental", "Oriental"),
    ("Persian", "Persian"),
    ("Siamese", "Siamese"),
    ("Sphynx", "Sphynx"),
    ("Other", "Other"),
]


class CatUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    breed = models.CharField(max_length=50,
                             choices=list_of_breeds,
                             default="Other")
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="catusers", blank=True
    )
    profile_picture = CloudinaryField("image", null=True, blank=True,
                                      resource_type="image", folder="profile_pictures")

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField("image", null=True, blank=True,
                            resource_type="image", folder="posts")

    def __str__(self):
        return f"{self.title} - {self.author}"


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.text}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.post} - Like"
