def comments_sorted_by_score(comments: list) -> bool:
    comments_sorted = all(comments[i]['score'] >= comments[i + 1]['score'] for i in range(len(comments) - 1))
    replies_sorted = all(comments_sorted_by_score(comment['replies']) for comment in comments)

    return comments_sorted and replies_sorted
