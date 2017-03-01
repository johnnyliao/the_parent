
from django.conf.urls import patterns, url
from action.views import comment, CommentPostView, ReCommentPostView, get_winning, WinningDataView
urlpatterns = patterns(".views",

	url('^comment/', comment),
	url('^get_winning/', get_winning),
	url('^comment_post/', CommentPostView.as_view()),
	url('^winngin_data/', WinningDataView.as_view()),
	url('^re_comment_post/', ReCommentPostView.as_view()),
)
