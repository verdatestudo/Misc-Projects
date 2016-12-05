'''
NFL power rankings from Reddit

Users on Reddit post weekly power rankings for NFL teams.
Using this data we can calculate some basic statistics and graphs.

Example: https://www.reddit.com/r/nfl/comments/5ecn32/official_rnfl_week_11_power_rankings/
Example box plot from thread: http://i.imgur.com/fHSRwKz.png

Last Updated: 2016-Dec-05
First Created: 2016-Nov-23
Python 3.5
Chris

Todo:
# fix scatter plot strange bug
# add assertions, try/except, comments, pylint, tidy comments
# tidy so that it auto imports from default sheet without any editing
'''

import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import collections
import statistics # can also use numpy or manually calculate mean and std, see:
# http://stackoverflow.com/questions/15389768/standard-deviation-of-a-list

class Week(object):
    '''
    Week object.
    Takes a week_no (int), csv_file (str) and team_colors (dict of tuples).
    '''
    def __init__(self, week_no, csv_file, team_colors):
        '''
        Create Week object. Takes an int for week_no, filename for csv_file.
        '''
        self.week_no = week_no
        self.csv_file = csv_file

        self.team_colors = team_colors

        self.pr_data = self.convert_csv_to_list()

        self.mean_std_dict = self.calc_mean_std()
        self.power_rankings = self.get_power_rankings()

    def convert_csv_to_list(self):
        '''
        Takes a csv of data and converts it into a dict.
        Returns a dict in the form {team1: [ranking1, ranking2], team2: [ranking1, ranking2]} etc.
        '''
        # so that when appending row no, if it's the first append for this team
        # it first creates a list before appending the value. Could also use try... except.
        pr_data = collections.defaultdict(list)

        row_no = 0
        for row in csv.reader(open(self.csv_file)):
            row_no += 1
            for team in row:
                # ensure no whitespace. using group to get the actual string.
                try:
                    team = re.match('(\w+)', team).group(0)
                    pr_data[team].append(row_no)
                except:
                    raise ValueError('Error importing %s on line %d!' %(team, row))

        # check there are 32 teams
        assert len(pr_data) == 32

        return pr_data

    def calc_mean_std(self):
        '''
        Using power rankings data, calculates the mean and std for each team.
        Returns a dict of tuples in the form {Team1: (mean, std)}
        '''
        mean_std_dict = {team: (statistics.mean(self.pr_data[team]), statistics.pstdev(self.pr_data[team])) for team in self.pr_data}
        return mean_std_dict

    def get_power_rankings(self):
        '''
        Using mean_std_dict, return a list of teams in ascending order of mean.
        '''
        # item[0] = team, x[1] = (mean, std), so x[1][0] = sort by mean
        return [item[0] for item in sorted(self.mean_std_dict.items(), key=lambda x: x[1][0])]

    def print_power_rankings(self):
        '''
        Print power rankings in the format 1 Cowboys \n 2 Patriots
        '''
        for rank, team in enumerate(self.power_rankings, 1):
            print(rank, team)

    def create_boxplot(self):
        '''
        Create boxplot.
        '''
        team_labels = list(reversed(self.power_rankings)) # reversed to get 1. team at top, 32. team at bottom.
        team_rankings = [self.pr_data[team] for team in team_labels]

        team_colors = [self.team_colors[team] if team in self.team_colors else ('red', 'black', 'yellow') for team in team_labels]

        # Create a figure instance
        fig = plt.figure(figsize=(15, 8))

        # Create an axes instance
        ax = fig.add_subplot(111)

        ax.set_title('Avg. Rank Team vs Rank - Week %d' %(self.week_no))
        ax.set_xlabel('Rank')
        ax.set_ylabel('Team Avg. Rank')

        # Create the boxplot
        bp = ax.boxplot(team_rankings, patch_artist=True, vert=False)

        ## change outline color, fill color and linewidth of the boxes
        assert len(bp['boxes']) == len(bp['medians']), 'Boxes and medians differ.'

        for idx in range(len(bp['boxes'])):
            box = bp['boxes'][idx]
            median = bp['medians'][idx]
            box.set(color='black', linewidth=2) # change outline color of box to team color 1
            box.set(facecolor=team_colors[idx][0], alpha=0.7) # change fill color of box to team color 1
            median.set(color=team_colors[idx][1], linewidth=2, marker='o') # change median color to team color 3

        ## change color and linewidth of the whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='grey', linewidth=2, alpha=0.5)

        ## change color and linewidth of the caps
        for cap in bp['caps']:
            cap.set(color='grey', linewidth=2)

        ## change the style of fliers and their fill
        for flier in bp['fliers']:
            flier.set(marker='o', color='#e7298a', alpha=0.2)

        ## Custom y-axis labels
        ax.set_yticklabels([str(32 - x) + '. ' + team_labels[x] for x in range(len(team_labels))])

        ## Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # set x limit rank to 1-33
        ax.set_xlim(0, 33)

        # add faint grid on x axis to make it easier to see rank
        ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.7)

        #plt.show()

        # Save the figure
        fig.savefig('boxplots/nfl_power_rankings_boxplot_week%s.png' %(str(self.week_no).rjust(2, '0')), bbox_inches='tight')

        #####


def get_team_colors(colors_filename):
    '''
    Takes a txt filename and returns a dict of tuples of team colors
    in the format {Team1: (Main Color, Secondary Color, Third Color)}.
    If a color is missing then a complimentary color is appended.

    # http://teamcolorcodes.com/nfl-team-color-codes/
    '''
    team_colors = {}
    with open(colors_filename) as file_name:
        team_colors = {item[0]: item[1:] for item in [line.split() for line in file_name]}

    for team, colors in team_colors.items():
        while len(colors) < 3:
            try:
            # http://stackoverflow.com/questions/1664140/js-function-to-calculate-complementary-colour
            # if missing a color, then add a roughly complimentary color to the main team color.
            # format by adding # and removing 0x from the start of the hex string.
                complimentary_color = (int(hex(0xffffff), 16) ^ int('0x'+colors[0][1:], 16))
                colors.append('#'+hex(complimentary_color)[2:])
                # some complimentary_colors were coming out wrong, this was temp code to avoid problems.
                # seems to be fixed.
                # if len(str(complimentary_color)) == 7 or len(str(complimentary_color)) == 8:
                #     colors.append('#'+hex(complimentary_color)[2:])
                # else:
                #     print(team, colors, complimentary_color, 'not working,, fix sometime')
                #     colors.append('red')
            except:
                raise ValueError('Problem with color', team, colors)

    return team_colors

def create_scatter(weeks_data):
    '''
    Create a scatter plot of progress of teams over the specified weeks (default = full season).
    X-axis = rank, Y-axis = team, Alpha value of dot = week no. (earlier weeks more transparent).

    Takes a list of weeks, the last item should be the current week.
    '''
    cur_week = weeks_data[-1]

    team_labels = list(reversed(cur_week.power_rankings)) # reversed to get 1. team at top, 32. team at bottom.
    # team_colors is a list ordered to match team_labels.
    team_colors = [cur_week.team_colors[team] if team in cur_week.team_colors else ('red', 'black', 'yellow') for team in team_labels]
    # alpha should go from 0.2 (near transparent) until 0.95 (near opaque) the more recent the data is.
    alphas = [0.2 + (x * 0.75 / (len(weeks_data) - 1)) for x in range(len(weeks_data))]

    # Create a figure instance
    fig = plt.figure(figsize=(15, 8))

    # Create an axes instance
    ax = fig.add_subplot(111)

    ax.set_title('Average (mean) Reddit Power Rankings of NFL teams during the 2016 season '\
    '- weeks %d to %d.' % (weeks_data[0].week_no, weeks_data[-1].week_no))
    ax.set_xlabel('Rank')
    ax.set_ylabel('Team')

    for idx, week_data in enumerate(weeks_data):
        team_rankings = [week_data.pr_data[team] for team in team_labels]
        team_means = [sum(data) / len(data) for data in team_rankings] # float

        for team_idx in range(len(team_labels)):
            # s = magic number, may need editing depending on graph size.
            plt.scatter(team_means[team_idx], team_idx, c=team_colors[team_idx], alpha=alphas[idx], s=50)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # set x limit rank to 1-33
    ax.set_xlim(0, 33)
    ax.set_ylim(-1, 32)

    # fix this strange bug
    y_labels = [str(32 - x) + '. ' + team_labels[x] for x in range(len(team_labels))]
    y_labels.insert(0, '')
    y_labels.insert(1, '')
    ax.set_yticklabels(y_labels)

    # add faint grid on x axis to make it easier to see rank
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.7)

    #plt.show()

    # Save the figure
    fig.savefig('scatterplots/nfl_power_rankings_boxplot_week%s.png' %(str(cur_week.week_no).rjust(2, '0')), bbox_inches='tight')

    return None

def get_weeks_data(weeks):
    '''
    Takes a list of weeks and returns a list of Week objects.
    '''
    return [Week(week_no, CSV_FILE_LIST[week_no - 1], TEAM_COLORS) for week_no in weeks]

def produce_all_graphs(weeks_data):
    '''
    Produce all graphs for all weeks.
    '''
    for idx, week_data in enumerate(weeks_data):
        if idx > 0:
            create_scatter(weeks_data[:idx+1])
        week_data.create_boxplot()

def produce_current_week_graphs(weeks_data):
    '''
    Produce all graphs for the current week.
    '''
    create_scatter(weeks_data)
    weeks_data[-1].create_boxplot()

###
# Required information.
CUR_WEEK = 12

TEAM_COLORS_FILE = 'nfl_team_color_codes.txt'
TEAM_COLORS = get_team_colors(TEAM_COLORS_FILE)
CSV_FILE_LIST = ['csv_data/nfl_power_rankings_week%s.csv' %(str(week_num).rjust(2, '0')) for week_num in range(1, 18)]
###

weeks_data = get_weeks_data(list(range(1, CUR_WEEK + 1)))



### END ###
