from django.contrib import admin
from .models import PetPost, AnimalCategory, RecommendPost, ShowoffPost, NewsScrap
from pet.models import SGIHotel, KoreaHotel, HotelCategory, SaveAnimalCategory, Animals, PostCategory
# Register your models here.

admin.site.register(PetPost)
admin.site.register(RecommendPost)
admin.site.register(ShowoffPost)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    
class AnimalsAdmin(admin.ModelAdmin):
    model = Animals
    
class AnimalCateAdmin(admin.ModelAdmin):
    model = AnimalCategory
    prepopulated_fields = {'slug' :   ('name', )}



# 반려동물 동반 호텔 
class HotelCateAdmin(admin.ModelAdmin):
    model = HotelCategory
    prepopulated_fields = {'slug' :   ('name', )}

# 전국  
class KRHotelAdmin(admin.ModelAdmin):
    model = KoreaHotel
# 서경인 
class SGIHotelAdmin(admin.ModelAdmin):
    model = SGIHotel

admin.site.register(AnimalCategory, AnimalCateAdmin)
# - 보호중동물
admin.site.register(Animals, AnimalsAdmin)
admin.site.register(SaveAnimalCategory, CategoryAdmin)
# - 호텔
admin.site.register(SGIHotel, SGIHotelAdmin)
admin.site.register(KoreaHotel, KRHotelAdmin)
admin.site.register(HotelCategory, HotelCateAdmin)
admin.site.register(NewsScrap)
admin.site.register(PostCategory)
