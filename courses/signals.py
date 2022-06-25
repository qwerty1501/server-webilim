from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from courses.models import CourseComment, CommentReply


@receiver(m2m_changed, sender=CourseComment.likes.through)
def comments_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()

@receiver(m2m_changed, sender=CommentReply.likes.through)
def comment_replies_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()
