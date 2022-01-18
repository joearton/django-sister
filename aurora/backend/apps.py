import os
import time
from django.apps import AppConfig
from django.utils.autoreload import autoreload_started, StatReloader
from django.conf import settings
from aurora import boot
from aurora.backend.library.bootstrap import browser
from django.utils.translation import gettext_lazy as _



class backendConfig(AppConfig):
    name = 'aurora.backend'
    verbose_name = _('Backend')

    
    def watch_folder(self, sender, *args, **kwargs):
        # only get scss dirs for watching needs
        scss_dirs = boot.generate_scss_to_css(execute_scss = False)
        for scss_dir in scss_dirs:
            sender.watch_dir(scss_dir, '*.scss')
        # js_dirs = boot.generate_js_admin(execute_js = False)
        # for js_dir in js_dirs:
            # sender.watch_dir(js_dir, 'admin.js')


    def get_execution_stat(self):
        execute_function = False
        current_time = time.time()
        ls_filepath = os.path.join(settings.CACHE_DIR, '.last_sync')
        if os.path.isfile(ls_filepath):
            with open(ls_filepath, 'r') as agent:
                last_changed = float(agent.read())
                if (current_time - last_changed ) > 2:
                    execute_function = True
        with open(ls_filepath, 'w') as agent:
            agent.write("{0}".format(current_time))
        return execute_function


    def ready(self):
        if settings.DEBUG and settings.DESIGN_MODE:
            # avoid call function twice when starting project
            execute_function = self.get_execution_stat()
            if execute_function:                
                # watch scss folder
                autoreload_started.connect(self.watch_folder)
                 
                # generate scss to css when file changed
                boot.generate_scss_to_css()

                # generate admin js when file changed
                # boot.generate_js_admin()

                # browser will automatically reload when file changed
                browser.create_reload_signer()
