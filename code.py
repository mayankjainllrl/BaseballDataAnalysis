"""My First Data Analysis Project"""

import csv

MINIMUM_AB = 500


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0


def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0


def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    result = []
    for row in statistics:
        if int(row[yearid]) == year:
            result.append(row)
    return result


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    result = []
    for i, row in enumerate(statistics):
        result.append((row[info["playerid"]], formula(info, statistics[i])))
    result.sort(key=lambda pair: pair[1], reverse=True)
    return result[:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    stat = read_csv_as_nested_dict(info["masterfile"], info["playerid"],
                                   info["separator"], info["quote"])
    result = []
    for index, row in enumerate(top_ids_and_stats):
        result.append("{:.3f} --- {} {}".format(top_ids_and_stats[index][1],
                                                stat[row[0]][info["firstname"]],
                                                stat[row[0]][info["lastname"]]))
    return result


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    statistics = read_csv_as_list_dict(info["battingfile"],
                                       info["separator"],
                                       info["quote"])
    year_stats = filter_by_year(statistics, year, info["yearid"])
    ids = top_player_ids(info, year_stats, formula, numplayers)
    return lookup_player_names(info, ids)


def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    result = {}
    listy = fields + [playerid]
    for row in statistics:
        if row[playerid] in result:
            for field in fields:
                result[row[playerid]][field] = int(result[row[playerid]][field]) + int(row[field])
        else:
            result[row[playerid]] = {field: row[field] for field in listy}
    for val in result.values():
        for keto in val:
            if keto != playerid:
                val[keto] = int(val[keto])
    return result


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    statistics = read_csv_as_list_dict(info["battingfile"], info["separator"], info["quote"])
    batting_stats = aggregate_by_player_id(statistics,
                                           info["playerid"],
                                           info["battingfields"])
    player = top_player_ids(info, list(batting_stats.values()), formula, numplayers)
    return lookup_player_names(info, player)


def test_baseball_statistics():
    """
    Simple testing code.
    """
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    baseballdatainfo = {
        "masterfile": "Master_2016.csv",  # Name of Master CSV file
        "battingfile": "Batting_2016.csv",  # Name of Batting CSV file
        "separator": ",",  # Separator character in CSV files
        "quote": '"',  # Quote character in CSV files
        "playerid": "playerID",  # Player ID field name
        "firstname": "nameFirst",  # First name field name
        "lastname": "nameLast",  # Last name field name
        "yearid": "yearID",  # Year field name
        "atbats": "AB",  # At bats field name
        "hits": "H",  # Hits field name
        "doubles": "2B",  # Doubles field name
        "triples": "3B",  # Triples field name
        "homeruns": "HR",  # Home runs field name
        "walks": "BB",  # Walks field name
        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]
    }

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


test_baseball_statistics()
