"""Defines all the functions related to the database"""
from app import db

# def get_top_songs2() -> dict:
#     song_list = []
#     for i in range(0,8):
#         item = {
#             "name": "song" + str(i)
#         }
#         song_list.append(item)

#     return song_list

def get_artists() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Artists").fetchall()
    conn.close()
    artist_list = []
    for result in query_results:
        item = {
            'artist_id': result[0],
            'name': result[1],
            'followers': result[2],
            'listeners': result[3]
        }
        artist_list.append(item)
    return artist_list

def get_top_songs() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT s.name, s.song_id FROM Songs s WHERE (s.album_id IN " + 
"(SELECT alb.album_id FROM (Artists art JOIN Albums alb ON(art.artist_id =alb.artist_id) JOIN Reviews r ON(art.artist_id=r.artists_review))" +
" WHERE r.rating >= 4)) ORDER BY s.total_plays DESC LIMIT 15;").fetchall()
    conn.close()
    song_list = []
    for result in query_results:
        item = {
            "name": result[0],
            "song id": result[1]
        }
        song_list.append(item)

    return song_list

def get_top_artists() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT art.name, COUNT(alb.album_id) as alb_count, art.artist_id" +
" FROM Artists art JOIN Albums alb ON(art.artist_id=alb.artist_id)" + 
" GROUP BY art.artist_id ORDER BY alb_count DESC LIMIT 15;").fetchall()
    conn.close()
    artists = []
    for result in query_results:
       item = {
           "name": result[0],
           "num_albums": result[1],
           "artist id": result[2]
       }
       artists.append(item)
    # artists = []
    # for i in range(0, 5):
    #     item = {
    #         "name": "artist" + str(i),
    #         "num_albums": str(20-i)
    #     }
    #     artists.append(item)
    return artists

def insert_new_artist(id: int) ->  None:
    """Insert new artist to Artists table.
    Args:
        text (str): Task description
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into Artists (artist_id, name, total_listeners, total_followers) VALUES ("{}", "{}", "{}", "{}");'.format(
        id, "change in update", 0, 0)
    conn.execute(query)
    conn.close()

def update_artist(task_id: int, name, followers, listeners) -> None:
    conn = db.connect()
    query = 'Update Artists SET name = "{}", total_followers = {}, total_listeners = {} WHERE artist_id = {};'.format(name, followers, listeners, task_id)
    conn.execute(query)
    conn.close()


def search_artist(task_id: int) -> dict:
    conn = db.connect()
    query = 'SELECT * FROM Artists WHERE artist_id={}'.format(task_id)
    query_results = conn.execute(query).fetchall()
    conn.close()

    artists = []
    for result in query_results:
        item = {
            "artist_id": result[0],
            "artist name": result[1],
            "total listeners": result[2],
            "total followers": result[3]
        }
        artists.append(item)

    return artists

def search_artist_name(name: str) -> dict:
    conn = db.connect()
    query = 'SELECT * FROM Artists WHERE name LIKE %s'
    args = ['%' + name + '%']
    query_results = conn.execute(query, args).fetchall()
    conn.close()

    artists = []
    for result in query_results:
        item = {
            "artist_id": result[0],
            "artist name": result[1],
            "total listeners": result[2],
            "total followers": result[3]
        }
        artists.append(item)

    return artists

def remove_artist_by_id(task_id: int) -> None:
    conn = db.connect()
    query = 'Delete From Artists where artist_id={};'.format(task_id)
    conn.execute(query)
    conn.close()

# def fetch_todo() -> dict:
#     """Reads all tasks listed in the todo table
#     Returns:
#         A list of dictionaries
#     """

#     conn = db.connect()
#     query_results = conn.execute("Select * from Artists LIMIT 15;").fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "song_id": result[0],
#             "name": result[1],
#             "status": result[2]
#         }
#         todo_list.append(item)

#     return todo_list

def trigger() -> None:
    conn = db.connect()
    conn.execute("DROP TRIGGER IF EXISTS trendset;")
    query = "CREATE TRIGGER trendset BEFORE UPDATE ON Artists FOR EACH ROW BEGIN SET @previouschange = 0; IF NEW.total_listeners - OLD.changed_listeners > 100 THEN SET @previouschange = OLD.changed_listeners / 2; END IF; IF OLD.changed_listeners < -100 THEN SET @previouschange = OLD.changed_listeners / 2; END IF; SET NEW.changed_listeners = NEW.total_listeners - OLD.total_listeners + @previouschange; END;"
    conn.execute(query)
    conn.close()

def init_procedure() -> None:
    conn = db.connect()
    conn.execute("DROP PROCEDURE IF EXISTS Trending")
    query = "CREATE PROCEDURE Trending() BEGIN DECLARE exit_loop BOOLEAN DEFAULT FALSE; DECLARE varart_id INT; DECLARE varart_cl INT; DECLARE varart_tl INT; DECLARE varart_name VARCHAR(30); DECLARE cur CURSOR FOR (SELECT DISTINCT art.artist_id, art.changed_listeners, art.total_listeners, art.name FROM Artists art JOIN (SELECT * FROM Albums a WHERE a.year_released > 2005) as alb ON(art.artist_id=alb.artist_id) LIMIT 50); DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE; DROP TABLE IF EXISTS NewTable; CREATE TABLE NewTable ( art_id INT PRIMARY KEY, art_name VARCHAR(30), art_listeners INT, art_cl INT); OPEN cur; cloop: LOOP FETCH cur INTO varart_id, varart_cl, varart_tl, varart_name; IF (exit_loop) THEN LEAVE cloop; END IF; INSERT INTO NewTable VALUES (varart_id, varart_name, varart_tl, varart_cl); END LOOP cloop; CLOSE cur; SELECT tbl.art_id, tbl.art_name, tbl.art_listeners FROM (SELECT n.art_id, n.art_name, n.art_listeners / n.art_cl as metric, n.art_listeners FROM NewTable n) as tbl ORDER BY tbl.metric DESC; END;"
    
    conn.execute(query)
    conn.close()

def procedure() -> dict:
    conn = db.connect()
    query_results = conn.execute("CALL Trending;").fetchall()
    conn.close()

    artists = []
    for result in query_results:
        item = {
            "artist_id": result[0],
            "artist name": result[1],
            "total listeners": result[2]
        }
        artists.append(item)

    return artists

'''
CREATE PROCEDURE Trending()
BEGIN

DECLARE exit_loop BOOLEAN DEFAULT FALSE;
DECLARE varart_id INT;
DECLARE varart_cl INT;
DECLARE varart_tl INT;
DECLARE varart_name VARCHAR(30);

DECLARE cur CURSOR FOR (SELECT DISTINCT art.artist_id, art.changed_listeners, art.total_listeners, art.name
                        FROM Artists art JOIN (SELECT * FROM Albums a WHERE a.year_released > 2005) as alb 
                        ON(art.artist_id=alb.artist_id) LIMIT 50);
                        
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

DROP TABLE IF EXISTS NewTable;
CREATE TABLE NewTable (
    art_id INT PRIMARY KEY, 
    art_name VARCHAR(30),
    art_listeners INT,
    art_cl INT
);

OPEN cur;
cloop: LOOP
    FETCH cur INTO varart_id, varart_cl, varart_tl, varart_name;
    IF (exit_loop) THEN
        LEAVE cloop;
    END IF;

    IF (varart_cl > 100) THEN
        INSERT INTO NewTable VALUES (varart_id, varart_name, varart_tl, varart_cl);
    END IF;

END LOOP cloop;
CLOSE cur;


SELECT tbl.art_id, tbl.art_name, tbl.art_listeners
FROM (SELECT n.art_id, n.art_name, n.art_listeners / n.art_cl as metric, n.art_listeners
        FROM NewTable n) as tbl
ORDER BY tbl.metric DESC;

END;
'''