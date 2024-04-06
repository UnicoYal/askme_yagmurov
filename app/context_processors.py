from app.models import Tag
from app.models import Profile

def tag_processor(request):
  return {'TAGS': Tag.objects.get_popular_tags() }

def user_processor(request):
  return {'BEST_MEMBERS': Profile.objects.get_popular_profiles() }
