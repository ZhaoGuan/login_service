import sys

from jinja2 import Environment, select_autoescape, FileSystemLoader
from sanic import html
import settings


class JinJaTemplate(object):
    def __init__(self):
        self.template_paths = [str(settings.BASE_DIR) + "/templates"]
        self.env_sync = Environment(loader=FileSystemLoader(self.template_paths),
                                    autoescape=select_autoescape(['html', 'xml', 'tpl']),
                                    enable_async=False)
        self.env_sync.variable_start_string = '{['  # 修改块开始符号
        self.env_sync.variable_end_string = ']}'
        self.enable_async_flag = sys.version_info >= (3, 6)
        self.env_async = Environment(loader=FileSystemLoader(self.template_paths),
                                     autoescape=select_autoescape(['html', 'xml', 'tpl']),
                                     enable_async=self.enable_async_flag)
        self.env_async.variable_start_string = '{['  # 修改块开始符号
        self.env_async.variable_end_string = ']}'

    def template_render_sync(self, template_file, **kwargs):
        template = self.env_sync.get_template(template_file)
        rendered_template = template.render(kwargs)
        return html(rendered_template)

    async def template_render_async(self, template_file, **kwargs):
        template = self.env_async.get_template(template_file)
        rendered_template = await template.render_async(kwargs)
        return html(rendered_template)
