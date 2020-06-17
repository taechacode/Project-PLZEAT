from django.db import models
from .my_crawling import gogogo
from users import models as user_models


class Recipe(models.Model):
    EASY = "쉬움"
    SOSO = "중급"
    HARD = "어려움"
    LEVEL_CHOICES = (
        (EASY, "쉬움"),
        (SOSO, "중급"),
        (HARD, "어려움"),
    )

    name = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to="recipies", default="default.png")

    how_to_create = models.TextField(max_length=10000, null=True)
    recipe_quantity = models.IntegerField(null=True)
    recipe_time = models.IntegerField(null=True)
    recipe_level = models.CharField(
        max_length=30, choices=LEVEL_CHOICES, null=True)
    creator = models.ForeignKey(
        user_models.User, related_name="creators", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if RecipeLink.objects.filter(recipe=self).exists():
            RecipeLink.objects.filter(recipe=self).delete()
        links = gogogo(self.name)
        for link in links:
            new_link_obj = RecipeLink(name=link, recipe=self)
            new_link_obj.save()


class FoodInRecipe(models.Model):
    name = models.CharField(max_length=100, null=True)
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, blank=True, null=True, related_name="foods")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ", "")
        super().save(*args, **kwargs)


class RecipeLink(models.Model):
    name = models.CharField(max_length=50)
    recipe = models.ForeignKey(
        Recipe, related_name="links", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RecipePercent(models.Model):
    user = models.ForeignKey(
        user_models.User, related_name="percents", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name="percents", on_delete=models.CASCADE)
    percent = models.IntegerField()
