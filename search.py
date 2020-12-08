


def Result(cursor,query):
    query = query.strip().split(" ")
    result = ()
    for word in query:
        cursor.execute("select comment_id from comment where comments_text regexp '(^|[[:space:]])"+str(word)+"([[:space:]]|$)'")
        word_result = cursor.fetchall()
        result = result + word_result
    return result