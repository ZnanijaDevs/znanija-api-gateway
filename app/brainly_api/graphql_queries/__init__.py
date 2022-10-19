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

GET_FEED_QUERY = """fragment AuthorData on User {
  nick
  id
  specialRanks {name}
  created
  rank {name}
  avatar {url}
}

query {
  feed(first: 50, status: ALL) {
    pageInfo {endCursor}
    edges {
      node {
        ... on Question {
          moderationItem {id}
          subject {id name}
          id
          content
          created
          author {...AuthorData}
          attachments {url}
          answers {
            nodes {
                id
              content
              created
              isConfirmed
              isBest
              author {...AuthorData}
              moderationItem {id}
              attachments {url}
            }
          }
        }
      }
    }
  }
}"""
