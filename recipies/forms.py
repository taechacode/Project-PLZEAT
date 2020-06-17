from django import forms
from . import models


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = (
            "photo",
            "name",
            "how_to_create",
            "recipe_quantity",
            "recipe_time",
            "recipe_level",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "레시피명"}),
            "subname": forms.TextInput(attrs={"placeholder": "부제목"}),
            "how_to_create": forms.Textarea(attrs={"placeholder": "조리방법을 작성 해 주세요!", "class": "how_to_create"}),
            "recipe_time": forms.NumberInput(attrs={"placeholder": "조리시간(분)", "style": "-webkit-appearance:none;"}),
            "recipe_level": forms.Select()
        }
    need_food = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "식자재"}),
    )
