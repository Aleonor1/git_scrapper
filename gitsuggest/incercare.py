from gitsuggest import GitSuggest
githubUser='Aleonor1'
gs = GitSuggest(username=githubUser)
for data in gs.get_suggested_repositories():
        print(data)