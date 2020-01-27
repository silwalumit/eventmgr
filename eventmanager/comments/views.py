from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse


@login_required 
def comment_delete(request, id):
    try:
        comment = Comment.objects.get(id = id) 
    except:
        raise Http404

    if comment.user != request.user:
        response = HttpResponse("You do not have permission to delete this")
        response.status_code = 403
        return response

    if request.method == 'POST':
        if comment.is_parent:
            url = comment.content_object.get_absolute_url()
        else:
            temp_comment = comment.parent
            url = temp_comment.get_absolute_url()
        comment.delete()
        return HttpResponseRedirect(url)

    context = {'comment':comment}
    return render(request, 'comments/delete.html', context = context)

def comment_thread(request, id):
    try:
        comment = Comment.objects.get(id = id) # get_object_or_404(Comment, id = id, parent = None)
    except:
        raise Http404

    if not comment.is_parent:
        comment = comment.parent

    initial_data = {
        'content_type': comment.content_type,
        'object_id': comment.object_id,
    }
    
    form = CommentForm(request.POST or None, initial = initial_data)
    
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model = c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get('content')    
              
        # parent_id = None
        # parse parent_id from form
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        
        # if parent id exists get the parent
        if parent_id:
            parent_qs = Comment.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
   
        new_comment, created = Comment.objects.create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(comment.get_absolute_url())

    context = {
        'comment':comment,
        'form':form,
    }
    return render(request, 'comments/comment_thread.html', context = context)