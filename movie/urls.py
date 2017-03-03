
from django.conf.urls import patterns, url
from movie.views import CommentPostView, ReCommentPostView, CommentLikeView, VideoLikeView, UnVideoLikeView
urlpatterns = patterns(".views",

	url('^comment/', CommentPostView.as_view()),
	url('^re_comment/', ReCommentPostView.as_view()),
	url('^like_comment/', CommentLikeView.as_view()),
	url('^like_video/', VideoLikeView.as_view()),
	url('^unlike_video/', UnVideoLikeView.as_view()),
)
