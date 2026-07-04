import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.management import call_command
import datetime

@staff_member_required
def media_manager_view(request):
    media_root = settings.MEDIA_ROOT
    files_list = []
    
    if os.path.exists(media_root):
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, media_root)
                size = os.path.getsize(file_path)
                files_list.append({
                    'name': file,
                    'path': rel_path,
                    'size': size,
                    'url': f"{settings.MEDIA_URL}{rel_path}".replace('\\', '/')
                })
                
    if request.method == 'POST':
        file_to_delete = request.POST.get('delete_file')
        if file_to_delete:
            full_path = os.path.join(media_root, file_to_delete)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                os.remove(full_path)
                messages.success(request, f"Deleted {file_to_delete}")
            return redirect('media_manager')
            
    return render(request, 'admin/media_manager.html', {'files': files_list, 'title': 'Media Manager'})

@staff_member_required
def backup_manager_view(request):
    backups_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backups_dir, exist_ok=True)
    
    if request.method == 'POST':
        filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(backups_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                call_command('dumpdata', stdout=f, exclude=['contenttypes', 'auth.permission'])
            messages.success(request, f"Backup created successfully: {filename}")
        except Exception as e:
            messages.error(request, f"Backup failed: {str(e)}")
            
        return redirect('backup_manager')
        
    backups = []
    for f in os.listdir(backups_dir):
        if f.endswith('.json'):
            backups.append({
                'name': f,
                'size': os.path.getsize(os.path.join(backups_dir, f)),
                'date': datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(backups_dir, f)))
            })
            
    backups.sort(key=lambda x: x['date'], reverse=True)
    return render(request, 'admin/backup_manager.html', {'backups': backups, 'title': 'Backup Manager'})
