
from django.conf.urls import patterns, url
from action.views import comment, CommentPostView, ReCommentPostView, get_winning, WinningDataView, send_mail
urlpatterns = patterns(".views",

	url('^comment/', comment),
	url('^get_winning/', get_winning),
	url('^send_mail/', send_mail),
	url('^comment_post/', CommentPostView.as_view()),
	#url('^winngin_data/', WinningDataView.as_view()),
	url('^re_comment_post/', ReCommentPostView.as_view()),
)
