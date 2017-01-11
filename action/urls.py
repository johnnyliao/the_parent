
from django.conf.urls import patterns, url
from action.views import comment, CommentPostView, ReCommentPostView
urlpatterns = patterns(".views",

	url('^comment/', comment),
	url('^comment_post/', CommentPostView.as_view()),
	url('^re_comment_post/', ReCommentPostView.as_view()),
)
