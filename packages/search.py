from .spell_correct import similar

def Result(cursor,query):
    query = query.strip().split(" ")
    result = []
    temp=[]
    similar_word = []
    for word in query:
        similar_word.extend(similar(word))
    similar_word=list(set(similar_word))
    unique_comments=[]
    for w in similar_word:
        query = "select * from comment where comments_text like '%"+str(w)+"%'"
        cursor.execute(query)
        word_result = cursor.fetchall()
        for t in word_result:
            if t[0] not in unique_comments:
                unique_comments.append(t[0])
                temp=list(temp)
                temp.clear()
                temp.append(t)
                result.append(t)

    print(temp)
    return result

