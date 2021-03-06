from . import web
from flask import (render_template,
                   abort, request, redirect,
                   url_for, flash, session)
from aslo.persistence.activity import Activity
from aslo.service import activity as activity_service
from flask_babel import gettext


@web.route('/', defaults={'page': 1})
@web.route('/page/<int:page>')
def index(page=1, items_per_page=9):
    # If Ignore_lang in the parameters, show all other non-translated apps
    lang_code = session['lang_code']
    ignore_lang = request.args.get('ignore_lang', False, type=bool)
    if ignore_lang:
        activities = activity_service.get_all(page=page)
    else:
        activities = activity_service.filter_by_lang_code(lang_code, page=page)

    return render_template('index.html', activities=activities,
                           lang_code=lang_code, ignore_lang=ignore_lang)


@web.route('/<bundle_id>/<activity_version>', strict_slashes=False)
def activity_detail(bundle_id, activity_version):
    lang_code = session['lang_code']
    activity_version = float(activity_version)
    activity = Activity.get_by_bundle_id(bundle_id)
    if activity is None:
        abort(404)

    release = activity_service.find_release(activity, activity_version)
    if release is None:
        abort(404)
    else:
        return render_template('detail.html', activity=activity,
                               current_release=release, lang_code=lang_code)


@web.route('/search', methods=['GET', 'POST'])
@web.route('/search/page/<int:page>', methods=['GET', 'POST'])
def search(page=1, items_per_page=10):
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')

    if not name:
        return redirect(url_for('web.index'))

    lang_code = session['lang_code']
    activities = activity_service.search_by_activity_name(
        lang_code=lang_code, activity_name=name, page=page
    )
    flash(gettext("Search Results for {}").format(name), 'success')
    return render_template('index.html', activities=activities,
                           search_query=name, lang_code=lang_code)
