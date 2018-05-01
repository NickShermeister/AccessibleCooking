from flask import flash, render_template, jsonify, request
from app.document_models.recipe_documents import Recipe
from app.document_models.tip_documents import Tip
from app.forms import RecipeSearchForm
from app import app
from app.helper_functions.media import video_id_from_url
from app.helper_functions.conversions import request_to_dict, form_to_recipe_dict, form_to_tip_dict

@app.route('/')
@app.route('/index')
def index():
    return jsonify({"Name":"Ariana"})

@app.route('/recipe')
def recipe():
    recipes = Recipe.query.all()
    content = '<h1>Recipes</h1><ol>'
    for recipe in recipes:
        content += '<li>{}</li>'.format(recipe.recipe_name)
    content += '</ol>'
    return content

@app.route('/tip')
def tip():
    tips = Tip.query.all()
    content = '<h1>Tips</h1><ol>'
    for tip in tips:
        content += '<li>{}: {}</li>'.format(tip.tip_name, tip.get_id())
    content += '</ol>'
    return content

@app.route('/search', methods=['GET', 'POST'])
def search_page():
        search = RecipeSearchForm(request.form)
        if request.method == 'POST':
                return search_results(search)

        return render_template('search.html', form=search)

def search_results(search):
        results = []
        search_string = search.data['search']
        s_form = RecipeSearchForm(request.form)

        if search.data['select'] == 'Recipe':
                search_dict = form_to_recipe_dict(search.data)
                results = Recipe.query.recipe_from_dict(search_dict)
                search_type = 'recipe'

        elif search.data['select'] == 'Tip':
            search_dict = form_to_tip_dict(search.data)
            results = Tip.query.tip_from_dict(search_dict)
            search_type = 'tip'

        if not results:
                flash('No results found!')
                return redirect('/')
        else:
                return render_template('search.html', form=s_form, results=results, search_type=search_type)

@app.route('/upload_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        # TODO: separate into smaller functions
        
        # TODO: implement error handling and required fields in form.
        # Currently, the function assumes that all of the field are filled in,
        # and if they are not, an internal server error is thrown.
        new_recipe = Recipe(
                recipe_name=request_dict['recipe_name'],
                description=request_dict['description'],
                servings=request_dict['servings'],
                time=request_dict['time'],
                ingredients=request_dict['ingredients'].split('\n'),
                equipment=request_dict['equipment'].split('\n'),
                instructions=request_dict['instructions'].split('\n'),
                video_id=video_id_from_url(request_dict['media_url']),
                media_url=request_dict['media_url'],
                media_type=request_dict['media_type'],
                difficulty=request_dict['difficulty'],
                tags=request_dict['tag'],
                tips=[])

        new_recipe.save()
        return render_template('upload_recipe_success.html')
    # Render the upload recipe form in the case of GET method.
    return render_template('upload_recipe_form.html')

@app.route('/upload_tip', methods=['GET', 'POST'])
def add_new_tip():
    """Uses form input to add a new recipe to the database.
    """
    if request.method == 'POST':
        request_dict = request_to_dict(request)
        print(request_dict)
        # TODO: implement required fields and error handling.
        new_tip = Tip(
                tip_name=request_dict['tip_name'],
                media_type=request_dict['media_type'],
                media_url=request_dict['media_url'],
                video_id=video_id_from_url(request_dict['media_url']),
                difficulty=request_dict['difficulty'],
                description=request_dict['description'],
                equipment=request_dict['equipment'].split('\n'),
                ingredients=request_dict['ingredients'].split('\n'),
                instructions=request_dict['instructions'].split('\n'),
                tags=request_dict['tag'])

        new_tip.save()
        return render_template('upload_tip_success.html')
    return render_template('upload_tip_form.html')

# @app.route('/<recipe_type>')
# def cookie_page(recipe_type):
#       search_dict = {'recipe_name':recipe_type}
#       recipe = Recipe.query.recipe_from_dict(search_dict).first()
#       return render_template('recipe_page.html', recipe=recipe)

@app.route('/recipe/<recipe_id>')
def specific_recipe(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        return render_template('recipe_template.html', recipe=recipe)

@app.route('/tip/<tip_id>')
def specific_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    return render_template('tip_template.html', tip=tip)

