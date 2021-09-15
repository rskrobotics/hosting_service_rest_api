from rest_framework import renderers


class JPEGRenderer(renderers.BaseRenderer):
    '''Custom renderer for retrieving an image content in jpeg'''
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class PNGRenderer(renderers.BaseRenderer):
    '''Custom renderer for retrieving an image content in png'''
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data
