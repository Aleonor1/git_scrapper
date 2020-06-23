import itertools
from collections import defaultdict
from operator import attrgetter
from os import path

import github
from gensim import corpora, models
from nltk.corpus import words, stopwords
from nltk.tokenize import RegexpTokenizer


class GitSuggest(object):
    MAX_DESC_LEN = 300

    def __init__(
        self, username=None, password=None, token=None, deep_dive=False
    ):
        if token:
            self.github = github.Github(token)
            username = self.github.get_user().login
            assert username is not None, "Invalid token"
        else:
            assert username is not None, "Suggest cannot work without username"
            # Github handle.
            if password is not None and password != "":
                self.github = github.Github(username, password)
            else:
                self.github = github.Github()

        self.deep_dive = deep_dive

        # Populate repositories to be used for generating suggestions.
        self.user_starred_repositories = list()
        self.user_following_starred_repositories = list()
        self.__populate_repositories_of_interest(username)

        # Construct LDA model.
        self.lda_model = None
        self.__construct_lda_model()

        # Suggested repository set.
        self.suggested_repositories = None

    # Search for repositories is the costliest operation so defer it as
    # much as possible.

    @staticmethod
    def get_unique_repositories(repo_list):
        unique_list = list()
        included = defaultdict(lambda: False)
        for repo in repo_list:
            if not included[repo.full_name]:
                unique_list.append(repo)
                included[repo.full_name] = True
        return unique_list

    @staticmethod
    def minus(repo_list_a, repo_list_b):
        included = defaultdict(lambda: False)

        for repo in repo_list_b:
            included[repo.full_name] = True

        a_minus_b = list()
        for repo in repo_list_a:
            if not included[repo.full_name]:
                included[repo.full_name] = True
                a_minus_b.append(repo)

        return a_minus_b

    def __populate_repositories_of_interest(self, username):
        # Handle to the user to whom repositories need to be suggested.
        user = self.github.get_user(username)

        # Procure repositories starred by the user.
        self.user_starred_repositories.extend(user.get_starred())

        # Repositories starred by users followed by the user.
        if self.deep_dive:
            for following_user in user.get_following():
                self.user_following_starred_repositories.extend(
                    following_user.get_starred()
                )

    def __get_interests(self):
        # All repositories of interest.
        repos_of_interest = itertools.chain(
            self.user_starred_repositories,
            self.user_following_starred_repositories,
        )

        # Extract descriptions out of repositories of interest.
        repo_descriptions = [repo.description for repo in repos_of_interest]
        return list(set(repo_descriptions))

    def __get_words_to_ignore(self):
        # Stop words in English.
        english_stopwords = stopwords.words("english")

        here = path.abspath(path.dirname(__file__))

        # Languages in git repositories.
        git_languages = []
        with open(path.join(here, "gitlang/languages.txt"), "r") as langauges:
            git_languages = [line.strip() for line in langauges]

        # Other words to avoid in git repositories.
        words_to_avoid = []
        with open(path.join(here, "gitlang/others.txt"), "r") as languages:
            words_to_avoid = [line.strip() for line in languages]

        return set(
            itertools.chain(english_stopwords, git_languages, words_to_avoid)
        )

    def __get_words_to_consider(self):
        return set(words.words())

    def __clean_and_tokenize(self, doc_list):
        # Some repositories fill entire documentation in description. We ignore
        # such repositories for cleaner tokens.
        doc_list = filter(
            lambda x: x is not None and len(x) <= GitSuggest.MAX_DESC_LEN,
            doc_list,
        )

        cleaned_doc_list = list()

        # Regular expression to remove out all punctuations, numbers and other
        # un-necessary text substrings like emojis etc.
        tokenizer = RegexpTokenizer(r"[a-zA-Z]+")

        # Get stop words.
        stopwords = self.__get_words_to_ignore()

        # Get english words.
        dict_words = self.__get_words_to_consider()

        for doc in doc_list:
            # Lowercase doc.
            lower = doc.lower()

            # Tokenize removing numbers and punctuation.
            tokens = tokenizer.tokenize(lower)

            # Include meaningful words.
            tokens = [tok for tok in tokens if tok in dict_words]

            # Remove stopwords.
            tokens = [tok for tok in tokens if tok not in stopwords]

            # Filter Nones if any are introduced.
            tokens = [tok for tok in tokens if tok is not None]

            cleaned_doc_list.append(tokens)

        return cleaned_doc_list

    def __construct_lda_model(self):
        if not cleaned_tokens:
            cleaned_tokens = [["zkfgzkfgzkfgzkfgzkfgzkfg"]]

        # Setup LDA requisites.
        dictionary = corpora.Dictionary(cleaned_tokens)
        corpus = [dictionary.doc2bow(text) for text in cleaned_tokens]

        # Generate LDA model
        self.lda_model = models.ldamodel.LdaModel(
            corpus, num_topics=1, id2word=dictionary, passes=10
        )

    def __get_query_for_repos(self, term_count=5):
        repo_query_terms = list()
        for term in self.lda_model.get_topic_terms(0, topn=term_count):
            repo_query_terms.append(self.lda_model.id2word[term[0]])
        return " ".join(repo_query_terms)

    def __get_repos_for_query(self, query):
        return self.github.search_repositories(
            query, "stars", "desc"
        ).get_page(
            0
        )

    def get_suggested_repositories(self):
        if self.suggested_repositories is None:
            # Procure repositories to suggest to user.
            repository_set = list()
            for term_count in range(5, 2, -1):
                query = self.__get_query_for_repos(term_count=term_count)
                repository_set.extend(self.__get_repos_for_query(query))

            # Remove repositories authenticated user is already interested in.
            catchy_repos = GitSuggest.minus(
                repository_set, self.user_starred_repositories
            )

            # Filter out repositories with too long descriptions. This is a
            # measure to weed out spammy repositories.
            filtered_repos = []

            if len(catchy_repos) > 0:
                for repo in catchy_repos:
                    if (
                        repo is not None
                        and repo.description is not None
                        and len(repo.description) <= GitSuggest.MAX_DESC_LEN
                    ):
                        filtered_repos.append(repo)

            # Present the repositories, highly starred to not starred.
            filtered_repos = sorted(
                filtered_repos,
                key=attrgetter("stargazers_count"),
                reverse=True,
            )

            self.suggested_repositories = GitSuggest.get_unique_repositories(
                filtered_repos
            )

        # Return an iterator to help user fetch the repository listing.
        for repository in self.suggested_repositories:
            yield repository
