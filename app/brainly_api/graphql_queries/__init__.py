USER_DATA_FRAGMENT = """
fragment UserData on User {
    id
    nick
    avatar {url}
    specialRanks {name}
    rank {name}
    created
    answerCountBySubject {
        count
        subject {name}
    }
}
"""

USER_WITH_ANSWERS_COUNT_FRAGMENT = """
fragment UserWithAnswersCount on User {
    answerCountBySubject { count subject {name} }
    nick
    avatar {url}
    rank {name}
    created
    id
}
"""
