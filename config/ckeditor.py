# CKEditor
CKEDITOR_BASEPATH   = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS    = {
    'default': {
        'toolbar': 'Default',
        'width': 'auto',
        'height': 275,
        'toolbar_Default': [
            ['Format'],
            ['Bold', 'Italic', 'Underline'],
            ['Table', 'Link'],
            ['NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Source']
        ],
    },
    'basic': {
        'toolbar': 'Basic',
        'width': 'auto',
        'height': 175,
        'toolbar_Basic': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Source']
        ],
    },
    'source': {
        'toolbar': 'Source',
        'width': 'auto',
        'height': 375,
        'toolbar_Source': [
            ['Source']
        ],
    }
}
