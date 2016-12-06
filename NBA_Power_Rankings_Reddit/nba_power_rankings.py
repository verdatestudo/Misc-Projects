'''
NBA power rankings from Reddit

Users on Reddit post regular power rankings for NBA teams.
Using this data we can calculate some basic statistics and graphs.

Example: https://www.reddit.com/r/nba/comments/5goop7/official_rnba_power_rankings_3_12052016/

Last Updated: 2016-Dec-06
First Created: 2016-Nov-05
Python 3.5
Chris

Todo:
# scatter plot
# github
# line by line optimise
# add assertions, try/except, comments, pylint, tidy comments
'''

import matplotlib.pyplot as plt
import csv
import collections

class Week(object):
    '''
    '''
    def __init__(self, week_no, csv_file):
        '''
        Create Week object. Takes an int for week_no, filename for csv_file.
        '''
        self.week_no = week_no
        self.csv_file = csv_file

        self.pr_data = self.convert_csv_to_list()
        self.power_rankings = self.get_power_rankings()

    def convert_csv_to_list(self):
        '''
        Takes a csv of data and converts it into a dict.
        Returns a dict in the form {team1: [ranking1, ranking2], team2: [ranking1, ranking2]} etc.
        '''
        # so that when appending row no, if it's the first append for this team
        # it first creates a list before appending the value. Could also use try... except.
        pr_data = collections.defaultdict(list)

        for row_idx, row in enumerate(csv.reader(open(self.csv_file))):
            if row_idx > 0: # skip header
                for col_team in row[1:31]:
                    pr_data[col_team].append(row_idx)

        pr_data.pop('--', None) # get rid of missing rankers

        # check there are 30 nba teams
        assert len(pr_data) == 30
        return pr_data

    def get_power_rankings(self):
        '''
        '''
        # using sum at the moment which is ok as all have same number of rankings
        return [item[0] for item in sorted(self.pr_data.items(), key=lambda x:sum(x[1]))]

    def create_boxplot(self):
        '''
        Create boxplot.
        '''
        team_labels = list(reversed(self.power_rankings)) # reversed to get 1. team at top, 32. team at bottom.
        team_rankings = [self.pr_data[team] for team in team_labels]
        team_labels = [TEAM_NICKNAMES[team] for team in team_labels]

        team_colors = [TEAM_COLORS[team] if team in TEAM_COLORS else ('red', 'black', 'yellow') for team in team_labels]

        # Create a figure instance
        fig = plt.figure(figsize=(15, 8))

        # Create an axes instance
        ax = fig.add_subplot(111)

        ax.set_title('NBA Reddit Power Rankings - #%d' %(self.week_no))
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
        ax.set_yticklabels([str(30 - x) + '. ' + team_labels[x] for x in range(len(team_labels))])

        ## Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # set x limit rank to 1-31
        ax.set_xlim(0, 31)

        # add faint grid on x axis to make it easier to see rank
        ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.7)

        plt.show()

        # Save the figure
        fig.savefig('boxplots/nba_power_rankings_boxplot_week%s.png' %(str(3).rjust(2, '0')), bbox_inches='tight')

### END OF WEEK OBJECT

def get_team_names_from_file(filename):
    '''
    dict {'Houston': 'Rockets', 'Golden State': 'Warriors'}
    '''
    team_names_dict = {}
    with open(filename, 'r') as open_file:
        for line in open_file:
            line_data = line.split()
            if len(line_data) == 2 and line_data[0] != 'LA':
                team_names_dict[line_data[0]] = line_data[-1]
            elif len(line_data) == 3 or line_data[0] == 'LA':
                team_names_dict[line_data[0] + ' ' + line_data[1]] = line_data[-1]
            else:
                print('error!')
    return team_names_dict

def get_team_colors(colors_filename):
    '''
    Takes a txt filename and returns a dict of tuples of team colors
    in the format {Team1: (Main Color, Secondary Color, Third Color)}.
    If a color is missing then a complimentary color is appended.

    # http://teamcolorcodes.com/nba-team-color-codes/
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
            except:
                raise ValueError('Problem with color', team, colors)

    return team_colors

def get_weeks_data(weeks):
    '''
    Takes a list of weeks and returns a list of Week objects.
    '''
    return [Week(week_no, CSV_FILE_LIST[week_no - 1]) for week_no in weeks]

def produce_current_week_graphs(weeks_data):
    '''
    Produce all graphs for the current week.
    '''
    #create_scatter(weeks_data)
    weeks_data[-1].create_boxplot()

#####
# Required information.
CUR_WEEK = 3

TEAM_COLORS_FILE = 'team_color_codes.txt'
TEAM_COLORS = get_team_colors(TEAM_COLORS_FILE)
TEAM_NICKNAMES = get_team_names_from_file('team_list.txt')
CSV_FILE_LIST = ['csv_data/2016_R%s.csv' %(str(week_num).rjust(2, '0')) for week_num in range(1, CUR_WEEK + 1)]
#####

weeks_data = get_weeks_data(list(range(1, CUR_WEEK + 1)))
produce_current_week_graphs(weeks_data)
