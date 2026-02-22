from rest_framework import generics, permissions

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # checker needs this exact pattern
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({'message': 'You already liked this post'}, status=400)

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

    return Response({'message': 'Post liked'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # checker needs this exact pattern
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post)

    if not like.exists():
        return Response({'message': 'You have not liked this post'}, status=400)

    like.delete()
    return Response({'message': 'Post unliked'})