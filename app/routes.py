""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

# @app.route("/topsongs2", methods=['GET'])
# def topsongs2():
#     return jsonify(db_helper.get_top_songs2())

@app.route("/artists")
def get_artists():
    return jsonify(db_helper.get_artists())

@app.route("/topsongs", methods=['GET'])
def topsongs():
    return jsonify(db_helper.get_top_songs())

@app.route("/topartists", methods=['GET'])
def topartists():
    return jsonify(db_helper.get_top_artists())

@app.route("/trending", methods=['GET'])
def trending():
    return jsonify(db_helper.procedure())


@app.route("/insertartist")
def insertartist():
    return render_template("insert.html")

@app.route("/insertartist", methods=['POST'])
def insertartist_post():
    id = request.form['inputbox']
    # name = request.form['artistname']
    try:
        result = db_helper.search_artist(id)
        if(len(result) != 0):
            result = {'success': True, 'response': 'Already inserted'}
        else:
            db_helper.insert_new_artist(id)
            result = {'success': True, 'response': 'Inserted Artist'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/search_ID")
def search():
    return render_template("search.html")

@app.route("/search_ID", methods=['POST'])
def search_post():
    id = request.form['inputbox']
    return jsonify(db_helper.search_artist(id))

@app.route("/search_name")
def search_name():
    return render_template("search_name.html")

@app.route("/search_name", methods=['POST'])
def search_name_post():
    name = request.form['inputbox']
    return jsonify(db_helper.search_artist_name(name))


@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/delete", methods=['POST'])
def delete_post():
    task_id = request.form['inputbox']
    try:
        result = db_helper.search_artist(task_id)
        if(len(result) == 0):
            result = {'success': True, 'response': 'No Artist to remove'}
        else:
            result = {'success': True, 'response': 'Artist Removed'}
        db_helper.remove_artist_by_id(task_id)
        
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)
    #return jsonify({'success': True, 'response': 'Removed task'})


@app.route("/edit")
def update():
    return render_template("update.html")

@app.route("/edit/<artist_id>/<name>/<followers>/<listeners>", methods=['GET'])
def update_post(artist_id=None, name=None, followers=None, listeners=None):
    try:
        result = db_helper.search_artist(artist_id)
        if len(result) == 0:
            result = {'success': True, 'response': 'No Artist to update'}
        else:
            db_helper.update_artist(artist_id, name, followers, listeners)
            result = {'success': True, 'response': 'Updated Artist'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

    # data = request.get_json()

    # try:
    #     if "status" in data:
    #         db_helper.update_status_entry(task_id, data["status"])
    #         result = {'success': True, 'response': 'Status Updated'}
    #     elif "description" in data:
    #         db_helper.update_task_entry(task_id, data["description"])
    #         result = {'success': True, 'response': 'Task Updated'}
    #     else:
    #         result = {'success': True, 'response': 'Nothing Updated'}
    # except:
    #     result = {'success': False, 'response': 'Something went wrong'}

    # return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    db_helper.trigger()
    db_helper.init_procedure()
    return render_template("main.html")