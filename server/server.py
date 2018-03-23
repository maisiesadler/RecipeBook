import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.serving import run_simple
from jinja2 import Environment, FileSystemLoader
import persist
import recent
import custom

class RecipeServer():
    links = []
    
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)

        self.url_map = Map([
            Rule('/', endpoint='homepage'),
            Rule('/recent', endpoint='view_recent'),
            Rule('/clear', endpoint='clear_recent'),
            Rule('/custom', endpoint='custom')
        ])
        
        self.links.append({'url': '/', 'name': 'Home'})
        self.links.append({'url': '/recent', 'name': 'Recent'})
        self.links.append({'url': '/custom', 'name': 'Custom'})
        
    def on_homepage(self, request):
        recipes=persist.getSaved()
        print(recipes)
        return self.render_template('sld.html',
            links = self.links,
            recipes=recipes
        )
        
    def on_view_recent(self, request):
        recentRecipes=recent.getRecent()
        print(recentRecipes)
        return self.render_template('recent.html',
            links = self.links,
            recentRecipes=reversed(recentRecipes)
        )
        
    def on_clear_recent(self, request):
        recent.clear()
        return Response('done')
        
    def on_custom(self, request):
        c = custom.getSaved()
        print(c)
        recipes = []
        [recipes.append({'name': s, 'val': c[s]}) for s in c.keys()]
        return self.render_template('custom.html',
            links = self.links,
            recipes=recipes
        )

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound, e:
            return self.error_404()
        except HTTPException, e:
            return e

    def error_404(self):
        response = self.render_template('404.html')
        response.status_code = 404
        return response

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
    app = RecipeServer()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


app = create_app()
run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
