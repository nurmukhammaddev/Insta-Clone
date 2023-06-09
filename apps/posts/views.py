import magic
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from apps.posts.models import Post, PostMedia, Comment, PostLike
from apps.posts.choices import MediaTypes
from apps.posts.forms import PostForm, CommentForm
from apps.posts.utils import extract_tags


# Create your views here.
class PostDetailView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()

        media_files = post.post_medias.all()
        print(post.is_liked(request.user.id))

        return render(
            request,
            'posts/post_detail.html',
            {
                'post': post, 'comments': comments, 'comment_form': CommentForm(),
                'media_files': media_files, 'media_range': range(media_files.count()),
                'is_liked': post.is_liked(request.user.id)
            }
        )

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # if form is valid
            Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_form.cleaned_data['text']
            )
            messages.info(request, "Comment added successfully!", extra_tags='success')

            return redirect('posts:post-detail', post_id=post.id)

        # if values in form is NOT valid
        comments = post.comments.all()
        media_files = post.post_medias.all()
        return render(
            request,
            'posts/post_detail.html',
            {
                'post': post, 'comments': comments, 'comment_form': CommentForm(), 'media_files': media_files,
                'is_liked': PostLike.objects.filter(post=post, user=request.user).exists()
            }
        )


class PostCreateView(LoginRequiredMixin, View):

    def get(self, request):

        post_form = PostForm()

        return render(
            request, 'posts/new_post.html', {'post_form': post_form}
        )

    def post(self, request):
        post_form = PostForm(data=request.POST, files=request.FILES)

        if post_form.is_valid():
            post = Post.objects.create(user=request.user, allow_commentary=post_form.cleaned_data['allow_commentary'])

            # extract tags from post text
            text = extract_tags(post.id, post_form.cleaned_data['text'])
            post.text = text
            post.save()

            media_files = request.FILES.getlist('media_files')

            for media in media_files:
                # check file type
                mime_type = magic.from_buffer(media.read(), mime=True)
                if mime_type.startswith('video/'):
                    media_type = MediaTypes.VIDEO
                elif mime_type.startswith('image/'):
                    media_type = MediaTypes.IMAGE
                else:
                    messages.error(request, "Incorrect media type!", extra_tags='danger')
                    return render(
                        request, 'posts/new_post.html', {'post_form': post_form}
                    )

                PostMedia.objects.create(post=post, file=media, media_type=media_type)

            return redirect('posts:post-detail', post_id=post.id)

        # if Form is not valid
        return render(
            request, 'posts/new_post.html', {'post_form': post_form}
        )


class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        like = PostLike.objects.filter(user=user, post=post)

        if like.exists():
            # if post is already liked by this user
            like.delete()
            # messages.info(request, "You unliked this post!", extra_tags='warning')
        else:
            # if post is not liked yet by this user
            PostLike.objects.create(user=user, post=post)
            # messages.info(request, "You liked this post!", extra_tags='success')

        return redirect(request.META.get('HTTP_REFERER'))
