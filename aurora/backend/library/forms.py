from django import forms
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout
from crispy_forms.bootstrap import StrictButton, TabHolder, Tab, Accordion, AccordionGroup
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.shortcuts import render
from django.template.loader import render_to_string



class AbstractForm:
    horizontal_form = True
    custom_layout   = []
    btn_css_class   = 'btn-primary'
    submit_label    = _('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.upper_label = True
        if self.horizontal_form:
            self.helper.form_class  = 'form-horizontal'
            self.helper.label_class = 'col-sm-3'
            self.helper.field_class = 'col-sm-9'
        grid = []
        if self.custom_layout:
            grid = self.custom_layout
        else:
            for field_name, field_model in self.fields.items():
                self.fields[field_name].label = self.fields[field_name].label.title()
                grid.append(field_name)
        submit_btn = Submit(self.submit_label, self.submit_label, css_class = self.btn_css_class)
        submit_btn_phd = Div(submit_btn, css_class = "text-center my-4")
        if not isinstance(grid, list):
            self.helper.layout = Layout(grid, submit_btn_phd)
        else:
            self.helper.layout = Layout(*grid, submit_btn_phd)


class BaseForm(AbstractForm, forms.Form):
    pass

class BaseModelForm(AbstractForm, forms.ModelForm):
    pass


class Formset(LayoutObject):
    template = "backend/elements/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})

