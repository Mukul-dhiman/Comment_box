from .spell_correct import similar


def Result(cursor,query):
    query = query.strip().split(" ")
    result = ()
    temp=()
    similar_word = []
    for word in query:
        similar_word.extend(similar(word))
    similar_word=list(set(similar_word))
    unique_comments=[]
    for w in similar_word:
        cursor.execute("select * from comment where comments_text regexp '(^|[[:space:]])"+str(w)+"([[:space:]]|$)'")
        word_result = cursor.fetchall()
        print(word_result)
        for t in word_result:
            if t['comment_id'] not in unique_comments:
                unique_comments.append(t['comment_id'])
                temp=list(temp)
                temp.clear()
                temp.append(t)
                result = result + tuple(temp)
    return result

