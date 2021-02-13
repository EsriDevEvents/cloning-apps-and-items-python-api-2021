def clean_data(target):
    ## Clean up previous .epk if exists
    for i in target.content.search("DEVtoTEST Migration Package"):
        assert i.delete()

    ## Remove the group
    for grp in target.groups.search("Target group - DevSummit 2021"):
        assert grp.delete()

    return 0