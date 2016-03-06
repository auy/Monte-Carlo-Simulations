"""
Assume a uniform random process governs the deployment of WSN. Perform
Monte Carlo simulations to find out the necessary number of 99% sensing
coverage as a function of sensing radius. Assume disk sensing model. Assume
that the deployment is done on 100m by 100m square 2D region. Take into
consideration statistical significance. (Answers based on single experiments
will not be graded). State all your extra assumptions. Give table(s)
summarizing the data for all your experiment results and also draw figure(s)
for visual assesment. You must submit your simulation code in a form that
allows the instructor to repeat the experiments if necessary.
"""

import random
from PIL import Image, ImageDraw

# Note that 1m is simulated with 5px in this script
EXPERIMENT_COUNT = 10  # Change this value when necessary
STARTING_SENSING_RADIUS = 50  # Experiments start from radius of 10m
ENDING_SENSING_RADIUS = 250  # Limit value of sensing radius for experiments
RADIUS_INCREMENT_VALUE = 25  # Repeat experiments by increment radius with this value
DESIRED_COVERAGE = 99  # Desired coverage percentage
AREA_WIDTH = 500  # Width of area in pixels
AREA_HEIGHT = 500  # Height of area in pixels
# Milestone points for coverage. Used in node coverage graphic in report
COVERAGE_MILESTONES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 100, 150, 200]


class Node(object):
    """Class for represent sensor nodes
    Sensing range can be changed by
    changing SENSING_RADIUS value
    """

    sensing_radius = 20  # Sensing radius for any node
    x = 0  # x coordinate of node
    y = 0  # y coordinate of node

    def __init__(self, x, y, sensing_radius=None):
        """Creates new node object with given coordinates
        and sensing radius value. If no radius is given
        default value is applied
        """

        self.x = x
        self.y = y
        if sensing_radius:
            self.sensing_radius = sensing_radius


class Area(object):
    """Class for representing target area
    Size of are can be modified with
    WIDTH and HEIGHT parameters
    """

    width = 0  # Width of area
    height = 0  # Height of area
    nodes = []  # List of deployed nodes
    coverage = {}  # Total coverage percentages for every step
    image = None  # Image object for checking total coverage
    draw = None  # ImageDraw object for drawing nodes

    def __init__(self, width, height):
        """Creates new Area object with give size.
        An image is created for coverage calculations.
        Predefined coverage milestones are created inside.
        """

        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), 0xffffff)
        self.draw = ImageDraw.Draw(self.image)
        self.nodes = []
        self.coverage = {
            1: 100,
            2: 100,
            3: 100,
            4: 100,
            5: 100,
            6: 100,
            7: 100,
            8: 100,
            9: 100,
            10: 100,
            15: 100,
            20: 100,
            30: 100,
            50: 100,
            100: 100,
            150: 100,
            200: 100,
        }

    def start_deployment(self, radius):
        """Starts random deployment within this area.
        In every step (deployment of a single node) total coverage
        checked from image file and saved in coverage variable.

        In every step this method controls whether total coverage
        reached 99% or not. If desired coverage reached, this method returns
        number of nodes.

        Args:
            radius (int): radius of the area

        Returns:
            Number of nodes
        """

        while True:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            node = Node(x, y)
            self.nodes.append(node)
            self.draw.ellipse(
                (
                    node.x - radius,
                    node.y - radius,
                    node.x + radius,
                    node.y + radius
                ), 128)

            if self.check_coverage(len(self.nodes)) is True:
                return len(self.nodes)

    def check_coverage(self, node_count):
        """checks total coverage of nodes for this area
        if coverage > 99% returns True, false otherwise

        Args:
            node_count (int): Number of nodes

        Returns:
            True if deployment reached default coverage False otherwise
        """

        empty_pixel_size = len([i for i in list(self.image.getdata()) if i == (255, 255, 255)])
        coverage_percentage = (float(empty_pixel_size) / float(self.width * self.height)) * 100
        if node_count in COVERAGE_MILESTONES:
            self.coverage[node_count] = (100 - coverage_percentage)

        return True if coverage_percentage <= 100 - DESIRED_COVERAGE else False


class Experiment(object):
    """Class for representing single experiment"""

    area = None  # Deployment area
    sensing_radius = 0  # Node sensing radius for this experiment

    def __init__(self, area, sensing_radius):
        """Creates new experiment for given
        area and node sensing range
        """

        self.area = area
        self.sensing_radius = sensing_radius

    def start(self):
        """Starts the experimen"""

        self.area.start_deployment(self.sensing_radius)

    def get_coverage(self):
        """Returns total coverage result for
        this experiment
        """

        return sorted(self.area.coverage.iteritems(), key=lambda (x, y): float(x))

    def get_node_count(self):
        """Returns total number of nodes
        when 99% of total coverage reached
        """

        return len(self.area.nodes)


def main():
    """Entry point of this script"""

    for i in range(STARTING_SENSING_RADIUS, ENDING_SENSING_RADIUS + 1, RADIUS_INCREMENT_VALUE):
        mean_coverage_values = {}
        mean_node_count = 0
        print "sensing radius: " + str(i / 5) + "m"

        for j in range(EXPERIMENT_COUNT):
            print "experiment " + str(j + 1) + " is in progress"
            experiment = Experiment(Area(AREA_WIDTH, AREA_HEIGHT), i)
            experiment.start()

            for coverage in experiment.get_coverage():
                if coverage[0] in mean_coverage_values:
                    mean_coverage_values[coverage[0]] += coverage[1]
                else:
                    mean_coverage_values[coverage[0]] = coverage[1]

            print "node count: " + str(experiment.get_node_count())
            mean_node_count += experiment.get_node_count()

        for k in mean_coverage_values.keys():
            mean_coverage_values[k] /= EXPERIMENT_COUNT

        print sorted(mean_coverage_values.iteritems(), key=lambda (x, y): float(x))
        print mean_node_count / EXPERIMENT_COUNT
        print "--------------------------------------------------"


if __name__ == '__main__':
    main()
