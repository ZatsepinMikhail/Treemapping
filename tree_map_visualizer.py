import matplotlib.pyplot as plt
import matplotlib.patches as pa
import random
import os

class TreeMapVisualizer:
    def __init__(self, tree_map):
        self.tree_map = tree_map
        self.extension_color_map = {}
        
    def create_plt_rectangle(self, rect, color):
        return pa.Rectangle(rect.get_start_point(), rect.x_size(), rect.y_size(), facecolor=color, edgecolor='black')
        
    def generate_new_color(self, ext):
        self.extension_color_map[ext] = "#"+''.join([random.choice('23456789ABCDEF') for j in range(6)])
        
    def visualize(self, figure):
        for file_path, rect in self.tree_map.rects.items():
            extension = os.path.splitext(file_path)[1]
            if extension not in self.extension_color_map:
                self.generate_new_color(extension)
            figure.gca().add_patch(self.create_plt_rectangle(rect, self.extension_color_map[extension]))
        
        legend_patches = []
        for ext, color in self.extension_color_map.items():
            legend_patches.append(pa.Patch(color=color, label=ext))
        plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=8)
