BASIC_DATA_FRAGMENT = """fragment UserBasicData on User {
    id
    nick
    avatar {url}
    specialRanks {name}
    rank {name}
    created
    gender
} """

GET_MODERATION_RANKING_QUERY = BASIC_DATA_FRAGMENT + """
query GetModerationRanking($type: UserRankingTypes!) {
  userRankings(rankingType: $type) {
    place
    points
    user {...UserBasicData}
  }
}"""

USER_DATA_FRAGMENT = """
fragment UserData on User {
    id
    nick
    avatar {url}
    specialRanks {name}
    rank {name}
    gender
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
    specialRanks {name}
    created
    id
    gender
}
"""

GET_FEED_QUERY = BASIC_DATA_FRAGMENT + """
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
          author {...UserBasicData}
          attachments {url}
          answers {
            nodes {
                id
              content
              created
              isConfirmed
              isBest
              author {...UserBasicData}
              moderationItem {id}
              attachments {url}
            }
          }
        }
      }
    }
  }
}"""
