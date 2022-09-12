# logicore-django-react

A little Python module helping to use Django and React on a single port during development and production

Serves as a foundation for [logicore-forms-django](https://github.com/Logicore-project/logicore-forms-django) project, but can be used without it

### Running Django and React on a single port during development

TODO: Motivation

### Usage from scratch: starting a Django + React project for development

1. Install Django and start the project
```bash
mkvirtualenv django_react_project1 # Or venv etc

python3 -m pip install Django
django-admin.py startproject django_react_project1
cd django_react_project1

# Configure database, etc and commit
```
Now you have fresh Django! Check it works:
```commandline
python manage.py runserver
```
and stop the development server.

2. Make a React for-development installation (inside a Django folder), called `frontend`.
Then, commit the changes and eject (we need it all): 
```commandline
create-react-app frontend
git add --all :/ && git commit -m "added frontend"
cd frontend
yarn eject
git add --all :/ && git commit -m "ejected frontend"
```

3. Install `logicore_django_react` and make use of it from your Django project:
```commandline
pip install -U logicore_django_react
```
(`-U` is required to ensure to get latest version)

Add to `urls.py`:
```python

from logicore_django_react.urls import top, bottom

urlpatterns = [
    # ...
]

urlpatterns = top + urlpatterns + bottom
```
Which will add necessary views for React to work via Django:

* `top` — serves hot-reload hooks and static files
* `bottom` — global (aka _match-all_, `.*`) view, that just serves HTML template that includes React

The latter (HTML template) might be overridden by changing
the `LOGICORE_DJANGO_REACT_TEMPLATE` setting, which is by default set to
`logicore_django_react/home.html` filename.

Please see source of a corresponding template file as an example.

4. Either:

* create your main app in Django (e.g. called `main`)
* or add non-app templates and static folders

 to prepare for React build bundles (templates and static files) to be saved into and remember it for the next step:

```bash
python manage.py startapp main # and add to INSTALLED_APPS
mkdir main/templates/ # here, "react" folder will automatically be added later
mkdir main/static/ # here, "react" folder will automatically be added later
```
or
```bash
# add "my_global_templates" to TEMPLATE_DIRS
mkdir my_global_templates/ # here, "react" folder will automatically be added later
# add "my_global_static" to STATICFILES_DIRS
mkdir my_global_static/ # here, "react" folder will automatically be added later
```

_Hint:_ gitkeep the templates/static folders created

5. Make modifications to `frontend` sub-project:

* in frontend/config/env.js — replace:
```javascript
    WDS_SOCKET_PORT: process.env.WDS_SOCKET_PORT,
```
by
```javascript
    WDS_SOCKET_PORT: 3000,
```
This will make React project's built-in websocket to the right port — where the React's server
is and not e.g. 8000.

* In `frontend/scripts/start.js` comment out `openBrowser` command. Before:
```javascript
      openBrowser(urls.localUrlForBrowser);
```
after:
```javascript
      //openBrowser(urls.localUrlForBrowser);
```
which doesn't open a browser at port `3000`, 'cause we don't want direct output
of React's dev server (it will be got by Django instead).

* make the following modifications to `frontend/scripts/build.js` file
(to make build process also integrate with Django):
  * Add to the beginning:
```javascript
const rimraf = require('rimraf');
const mkdirp = require('mkdirp');
```
  * and also, install that modules (inside your `frontend` folder):
```commandline
yarn add -D rimraf mkdirp
```

* before the first `.catch(...)` statement in the file, prepend the following extra step:
```javascript
.then(function () {
    const filename = __dirname + '/../build/asset-manifest.json';
    const chunks = {};
    JSON.parse(fs.readFileSync(filename)).entrypoints.map(e => {
      let ext = e.split('.');
      ext = ext[ext.length - 1];
      if (!chunks[ext]) chunks[ext] = [];
      chunks[ext].push(e.replace('static/', '/static/react/'));
    });
    const appBase = __dirname + '/../../main/';
    const templates = {
      css: url => `<link rel="stylesheet" type="text/css" href="${url}" />`,
      js: url => `<script type="text/javascript" src="${url}"></script>`,
    }
    for (let [k, v] of Object.entries(templates)) {
      const html = chunks[k]?.map(v).join('');
      const fileDir = `${appBase}templates/react/`;
      mkdirp.sync(fileDir);
      fs.writeFileSync(`${fileDir}bundle_${k}.html`, html);
    }
    const srcDir = __dirname + '/../build/static/';
    const destDir = appBase + 'static/react/';

    console.log(`will remove dir ${destDir}`);
    rimraf.sync(destDir);
    fs.copySync(srcDir, destDir, { overwrite: true }, function (err) {
      if (err) {
        console.error(err);
      } else {
        console.log(chalk.green("copy assets to build: success!"));
      }
    });
  })
```
and check that the path `__dirname + '/../../main/` (the `appBase`) points exactly to where your
location for auto-generated (during the build) templates and static files is.
This example is given for storing the files inside the folders of an app called `main` .

6. _gitignore_ the auto-generated folders of yours:
```gitignore
main/templates/react/**
main/static/react/**
```

7. Add files and commit — now you should have ready-to-go setup for
developing and deploying Django + React project on a single port!
