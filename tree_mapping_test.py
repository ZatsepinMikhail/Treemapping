import argparse
import matplotlib.pyplot as plt
import os

from tree_map import TreeMap
from tree_map_squarified import TreeMapSquarified
from tree_map_visualizer import TreeMapVisualizer

parser = argparse.ArgumentParser(description='Treemapping test')
parser.add_argument('--directory', help='directory for tree mapping')
args = parser.parse_args()

if __name__ == '__main__':
    assert(os.path.exists(args.directory))
    assert(os.path.isdir(args.directory))

    print('tree map build start')
    tree_map = TreeMap(args.directory)
    visualizer = TreeMapVisualizer(tree_map)
    print('tree map visualization start')
    visualizer.visualize(plt.figure(figsize=(20, 20)))

    plt.savefig('result/tree_mapping.png')

    print('tree map squarified build start')
    tree_map_squarified = TreeMapSquarified(args.directory)
    visualizer_squarified = TreeMapVisualizer(tree_map_squarified)
    visualizer_squarified.extension_color_map = visualizer.extension_color_map
    print('tree map squarified visualization start')
    visualizer_squarified.visualize(plt.figure(figsize=(20, 20)))

    plt.savefig('result/tree_mapping_squarified.png')
