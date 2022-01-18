from django.views.generic import View


class BaseView(View):

    section_title = ''
    section_name  = ''
    section_helper_top = None
    section_helper_bottom = None
    section_action_button_left = None
    section_action_button_right = None
    list_display = []
    fluid_width = False

    def get_section_title(self):
        return self.section_title

    def get_section_name(self):
        return self.section_name

    def get_section_helper_top(self):
        return self.section_helper_top

    def get_section_helper_bottom(self):
        return self.section_helper_bottom

    def get_section_action_button_left(self):
        return self.section_action_button_left

    def get_section_action_button_right(self):
        return self.section_action_button_right

    def get_list_display(self):
        return self.list_display

    def get_fluid_width(self):
        return self.fluid_width

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['section_title'] = self.get_section_title()
        context_data['section_name'] = self.get_section_name()
        context_data['section_helper_top'] = self.get_section_helper_top()
        context_data['section_helper_bottom'] = self.get_section_helper_bottom()
        context_data['section_action_button_left'] = self.get_section_action_button_left()
        context_data['section_action_button_right'] = self.get_section_action_button_right()
        context_data['list_display'] = self.get_list_display()
        context_data['fluid_width'] = self.get_fluid_width()
        return context_data

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class coreView(BaseView):
    pass
